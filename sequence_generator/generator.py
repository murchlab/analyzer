import os
import sys
import clr
import time
import numpy as np
import matplotlib.pyplot as plt
from System import Array, Byte
#import threading
#from numba import jit
#import tewx

controller_path = r"C:\Users\Crow108\Documents\Python\controller"
if controller_path  not in sys.path:
    sys.path.append(controller_path)
import instFunction
#from instFunction import SendScpi
import proteusapi

SAMPLE_RATE = 1E9 # Gig samples/sec
#SAMPLE_RATE = 1.25E9 # Gig samples/sec

    # Select appropriate slot
sys.path.append(os.getcwd())


winpath = os.environ['WINDIR'] + "\\System32\\"
#winpath = R'D:/Projects/ProteusAwg.trunk/x64\Debug/'

files_dir = os.getcwd()
#files_dir = R'D:\\Documents\\fromJoni\\WashU\\'

clr.AddReference(winpath + R'TEPAdmin.dll')
from TaborElec.Proteus.CLI.Admin import CProteusAdmin
from TaborElec.Proteus.CLI.Admin import IProteusInstrument
from TaborElec.Proteus.CLI.Admin import TaskInfo
from TaborElec.Proteus.CLI import TaskStateType, IdleWaveform
from TaborElec.Proteus.CLI import EnableSignalType, AbortSignalType
from TaborElec.Proteus.CLI import ReactMode, TaskCondJump

admin = None

def proteus_init(slotId):
    global admin
    admin = None
    try:
        admin = CProteusAdmin()
        if not admin:
            raise RuntimeError("CProteusAdmin() failed")
    
        if not admin.IsOpen():
            rc = admin.Open()
            if 0 != rc:
                raise RuntimeError("admin.Open() = {0}".format(rc))
        
        inst = admin.OpenInstrument(slotId)
        print(f"initializing slotId = {slotId}")
        if not inst:
            errStr = "admin.OpenInstrument(slotId={0}) failed".format(slotId)
            print(errStr)
            raise RuntimeError(errStr)
        else:
            return inst
    except:
        pass
    
def proteus_close(slotId):
    try:
        rc = admin.CloseInstrument(slotId)
        if 0 != rc:
            errStr = "admin.CloseInstrument(slotId={0})={1}".format(slotId, rc)
            raise RuntimeError(errStr)
    finally:
        if admin is not None:
            admin.Close()
            
def proteus_start_seq():
    query_syst_err = True
    global insts

    inst = insts[np.uint32(3)]
    for ch_index in range(4):
        instFunction.SendScpi(inst, ":INST:CHAN {}".format(ch_index+1), query_syst_err)
        instFunction.SendScpi(inst, ":TASK:SEL 1", query_syst_err)
        instFunction.SendScpi(inst, ":TASK:DEF:NEXT1 2", query_syst_err)
        
#        ## commands from end of load_seq_new:
#        verbose=0
#        # Setting up amplitudes and offsets
#        instFunction.SendScpi(inst, f":INST:CHAN {ch_index+1}", query_syst_err, verbose=verbose) ##@ REMOVED +1 from ch_index
##        instFunction.SendScpi(inst, f":VOLT {amp[ch_index]}", query_syst_err, verbose=verbose)
##        instFunction.SendScpi(inst, f":VOLT:OFFS {offset[ch_index]}", query_syst_err, verbose=verbose)
#        instFunction.SendScpi(inst, ":SOUR:FUNC:MODE TASK", query_syst_err, verbose=verbose)
#        
#        # connect ouput
#        instFunction.SendScpi(inst, ":OUTP ON", query_syst_err, verbose=verbose)
#        
#        # enble markers
#        instFunction.SendScpi(inst, ":MARK:MASK 65535", query_syst_err, verbose=verbose)
#        instFunction.SendScpi(inst, ":MARK:SEL 1", query_syst_err, verbose=verbose)
#        instFunction.SendScpi(inst, ":MARK:STAT ON", query_syst_err, verbose=verbose)
#        # 
#        instFunction.SendScpi(inst, ":MARK:SEL 2", query_syst_err, verbose=verbose)
#        instFunction.SendScpi(inst, ":MARK:STAT ON", query_syst_err, verbose=verbose)
            
            
            
def loadMarkData(inst, markData, query_err=False):
    inDatLength = len(markData)
    inDatOffset = 0
    res = inst.WriteBinaryData(":MARK:DATA 0,#", markData, inDatLength, inDatOffset)
    
    if (res.ErrCode != 0):
        print("Error {0} ".format(res.ErrCode))

    if len(res.RespStr) > 0:
        print("{0}".format(res.RespStr))

    if query_err:
        err = inst.SendScpi(':SYST:ERR?')
        if not err.RespStr.startswith('0'):
            print(err.RespStr)
            err = inst.SendScpi('*CLS')
            
            
def loadTaskTable(inst, num_steps, dummy_header=True, query_err=False, verbose=True):
    segNum_offset = 256
    
    dummy_offset = 0
    if dummy_header:
        dummy_offset = 1
    
    for ch_index in range(4):
        instFunction.SendScpi(inst, f":INST:CHAN {ch_index+1}", query_err, verbose=verbose)
        
        taskTableLen = num_steps + dummy_offset
        taskTableRow = TaskInfo()
        rowBinarySize = taskTableRow.SerializedSize
        #tableBinDat = np.zeros(taskTableLen * rowBinarySize, dtype=np.uint8)
        tableBinDat = bytearray(taskTableLen * rowBinarySize)
        tableBinDat = Array[Byte](tableBinDat)
        
        if(ch_index % 2 == 0):
            step_index_start = 1 + segNum_offset
        else:
            step_index_start = num_steps + 1 + segNum_offset
        
        if dummy_header:
            taskTableRow.SegNb = 1
            taskTableRow.TaskState = TaskStateType.Single
            taskTableRow.TaskLoopCount = 1
            taskTableRow.SeqLoopCount = 1
            taskTableRow.TaskIdleWaveform = IdleWaveform.DC
            taskTableRow.TaskDcVal = 32768
            taskTableRow.TaskEnableSignal = 0
            taskTableRow.TaskAbortSignal = 0
            taskTableRow.TaskAbortJump = ReactMode.Eventually
            taskTableRow.TaskCondJumpDest = TaskCondJump.Next1Task
            taskTableRow.NextTask1 = 1
            taskTableRow.NextTask2 = 0
            taskTableRow.NextTaskDelay = 0
            taskTableRow.TaskLoopTrigEnable = False
            taskTableRow.Serialize(tableBinDat, 0)
        
        for step_index in range(num_steps):
            taskTableRow.SegNb = step_index + step_index_start + dummy_offset
            #
            #% TaskState is either
            #%  TaskStateType.Single, 
            #%  TaskStateType.StartSequence,
            #%  TaskStateType.EndSequence or
            #%  TaskStateType.InsideSequence
            taskTableRow.TaskState = TaskStateType.Single
            #
            taskTableRow.TaskLoopCount = 1
            taskTableRow.SeqLoopCount = 1
            #
            #% TaskIdleWaveform is either
            #%  IdleWaveform.DC,
            #%  IdleWaveform.FirstPoint or
            #%  IdleWaveform.CurrentSeg
            taskTableRow.TaskIdleWaveform = IdleWaveform.DC
            #
            taskTableRow.TaskDcVal = 32768 # Mid-DAC (16 bits)
            #
            #% TaskEnableSignal is (currently) either
            #%   EnableSignalType.None,
            #%   EnableSignalType.ExternTrig1,
            #%   EnableSignalType.ExternTrig2,
            #%   EnableSignalType.InternTrig,
            #%   EnableSignalType.CPU,
            #%   EnableSignalType.FeedbackTrig or
            #%   EnableSignalType.HwControl
            taskTableRow.TaskEnableSignal = EnableSignalType.ExternTrig1
            #
            #% TaskAbortSignal is (currently) either
            #%   AbortSignalType.None,
            #%   AbortSignalType.ExternTrig1,
            #%   AbortSignalType.ExternTrig2,
            #%   AbortSignalType.InternTrig,
            #%   AbortSignalType.CPU,
            #%   AbortSignalType.FeedbackTrig or
            #%   AbortSignalType.AnyExternTrig
            taskTableRow.TaskAbortSignal = 0
            #
            #% TaskAbortJump is either
            #%   ReactMode.Eventually or
            #%   ReactMode.Immediately
            taskTableRow.TaskAbortJump = ReactMode.Eventually
            #
            #% TaskCondJumpDest is either
            #%   TaskCondJump.Next1Task
            #%   TaskCondJump.FeedbackTrigValue
            #%   TaskCondJump.SwitchNext1Next2
            #%   TaskCondJump.NextTaskSel
            #%   TaskCondJump.NextScenario
            taskTableRow.TaskCondJumpDest = TaskCondJump.Next1Task
            #
            taskTableRow.NextTask1 = (step_index+1)%num_steps + 1 + dummy_offset
#                taskTableRow.NextTask1 = (step_index)%num_steps + 1
            taskTableRow.NextTask2 = 0
            #
            # These two lines seem to be extra.
            taskTableRow.NextTaskDelay = 0
            taskTableRow.TaskLoopTrigEnable = False #(this does not matter for single loop tasks)
            #
            ##% The offset of the n-th row is: (n-1)*rowBinarySize
            taskTableRow.Serialize(tableBinDat, (step_index + dummy_offset) * rowBinarySize)
        res = inst.WriteBinaryData(':TASK:DATA 0,#', tableBinDat)
    
    if (res.ErrCode != 0):
        print("Error {0} ".format(res.ErrCode))

    if len(res.RespStr) > 0:
        print("{0}".format(res.RespStr))

    if query_err:
        err = inst.SendScpi(':SYST:ERR?')
        if not err.RespStr.startswith('0'):
            print(err.RespStr)
            err = inst.SendScpi('*CLS')


class Pulse:
    '''
    DESCRIPTION: an object to contain all pulse parameters. 
            If using SSM, self.ssm_bool= True
    PARAMETERS:
        (base): duration, start (time), amplitude, 
        (if ssm_bool): ssm_freq (GHz), phase
    FUNCTIONS:
        make(): create short copy of pulse 
        show(): graph output
        copy(): deep copy, I hope...
        NOTES:
                This does not include difference b/t cos/sin because they can be included in phase
    '''
    def __init__(self,duration, start, amplitude, ssm_freq=None, phase=0,gaussian_bool=False):
        self.duration = int(duration)
        self.start = int(start)
        self.amplitude = amplitude
        if ssm_freq is not None:
            self.ssm_bool = True  
            self.ssm_freq = ssm_freq
            self.phase = phase
        else:
            self.ssm_bool = False
        #self.waveform = self.make() ## make is currently not working.

        # FUTURE FEATURES:
        self.gaussian_bool = gaussian_bool  

    
    def make(self):
        new_array = np.zeros(self.duration)
        if self.ssm_bool:
            gen_pulse( dest_wave = new_array, pulse=self)
        else:
            gen_pulse(new_array, pulse=self)

        return new_array

    def show(self):
        plt.plot(np.arange(self.start,self.duration), self.waveform)
        plt.show()

    def copy(self):
        # there must be a better/ more general way to do this.
        if self.ssm_bool:
            return Pulse(self.duration, self.start, self.amplitude, self.ssm_freq, self.phase, self.gaussian_bool)
        else:
            return Pulse(self.duration, self.start, self.amplitude, gaussian_bool=self.gaussian_bool)

    def toString(self):
        outString = "Pulse of {0} [amp] from {1}+{2}".format(self.amplitude, self.start, self.duration)
        if self.ssm_bool:
            outString += " SSM @ {0} MHz with phase={1}".format(self.ssm_freq*1000, self.phase)
        return outString
#END pulse class
        
    
class Sequence:
    '''
    DESCRIPTION: an object to contain all sequence parameters. 
    PARAMETERS:
        (base): duration, start (time), amplitude, 
        (if ssm_bool): ssm_freq (GHz), phase
    FUNCTIONS:
        
        NOTES:
                This does not include difference b/t cos/sin because they can be included in phase
    '''
    def __init__(self,sequence_length, num_steps,mixer_orthogonality=90):
        
        self.sequence_length = int(sequence_length)
        self.num_steps = int(num_steps)
        self.mixer_orthogonality = mixer_orthogonality
        
        self.channel_list = self._initialize_channels()
        # all_data is list of [ch1, ch2, ch3, ch4]
        #   e.g. ch1 =  [waveform, m1, m2]
        #       e.g. waveform contains sweep: m1.shape = [num_steps, samples_per_step]
        
    def insert_waveform(self, channel_num, pulse, step_index):
        full_seq_waveform = self.channel_list[channel_num-1][0] # 0 for waveform
        current_step = full_seq_waveform[step_index]
        gen_pulse(current_step, pulse) ##in-place insertion
        #self.all_data[channel_num-1][0] += current_step
        
    def insert_marker(self,channel_num, marker_num, pulse):
        full_seq_marker = self.channel_list[channel_num-1][marker_num-1]
        current_step = full_seq_marker[step_index]
        gen_pulse(current_step, pulse)
        self.channel_list[channel_num-1][marker_num-1] += current_step

    def insert_bothChannels(self,primary_channel_num, pulse,step_index):
        ## adds pulse to both channels, offset by mixer_ortho.
        ch_num = primary_channel_num
        self.insert_waveform(ch_num,pulse,step_index)
        copy = pulse.copy()
        copy.phase += self.mixer_orthogonality
        self.insert_waveform(ch_num,copy,step_index)
        
    def convert_to_tabor_format(self, channel_num):
        # each of the following is a [num_steps x samples_per_step] matrix
        waveform = self.channel_list[channel_num][0]
        mark1 = self.channel_list[channel_num][1]
        mark2 = self.channel_list[channel_num][2]
        binarized = int(2**12*waveform) + int(2**14 *mark1) + int(2**15 *mark2)       
        return binarized
    
    
    def add_gate(self, source_1, source_2=None,destination_tuple=(1,1)): #input channel numbers #channel1 marker1 is default use dest_tuple=(3,2) for ch3/4 mkr2
        # each of the following is a [num_steps x samples_per_step] matrix
        channel1_channel = self.channel_list[source_1-1][0] # dim 0: channel 1; dim 1: [ch,m1,m2]
        both_ch1_ch2 = channel1_channel**2
        if source_2:
            channel2_channel = self.channel_list[source_2-1][0] # dim 0: channel 1; dim 1: [ch,m1,m2]
            both_ch1_ch2 += channel2_channel**2
        qubit_gate = create_gate(both_ch1_ch2)
        self.channel_list[destination_tuple[0]-1][destination_tuple[1]] = qubit_gate     

    def add_sweep(self, channel, marker=0, sweep_name='none', start=0, stop=0, initial_pulse=Pulse(amplitude=0, duration=0,start=0)):
        '''
        DESCRIPTION:  A thin wrapper to add pulses to the correct channel 
        INPUT: channel = {1-4} (converts to indices); marker=0(channel),1,2; arguments for gen_sweep 
        OUTPUT:
        '''

        ## error checking
        if start==stop and sweep_name != 'none':
            raise Warning("Start and sweep are the same; did you mean that?")
        if channel not in [1,2,3,4]:
            raise IOError("Invalid channel number: "+str(channel))
        if marker not in [0,1,2]:
            raise IOError("Invalid marker number: "+str(marker))
       
        ## send the input to _gen_sweep 
        dest_wave = self.channel_list[channel-1][marker]
        self._gen_sweep(sweep_name, start=start, stop=stop, dest_wave=dest_wave, initial_pulse=initial_pulse )
    #END add_sweep


    def _initialize_sequence_matrix(self):
        '''
        DESCRIPTION: prepare an empty matrix of size [time_steps, sequence_steps] for each channel
        INPUT:
        OUTPUT:
        '''
        num_steps = self.num_steps
        file_length = self.sequence_length
        channel= np.zeros((num_steps,file_length))
        mark1  = np.zeros((num_steps,file_length))
        mark2  = np.zeros((num_steps,file_length))
        
        return channel, mark1, mark2
    ##END _intiialize_sequence_matrix

    
    def _initialize_channels(self):
        '''
        DESCRIPTION: prepare the channels and markers
        INPUT:
        OUTPUT:
        '''
        num_channels = 4
        
        channel_array = [ [None,None,None] for i in range(num_channels) ] 
        for ch_index in range(len(channel_array)):
            wave, mark1, mark2 = self._initialize_sequence_matrix()
            channel_array[ch_index] = [wave, mark1, mark2]
        
        # The WX2184C channel (ch) 1 and 2 share markers; likewise ch 3 and 4
        #   so we will copy ch 1 to 2 and 3 to 4
        mark1_index, mark2_index = 1,2
        ## set ch2 markers equal to ch1 markers
        channel_array[1][mark1_index] = channel_array[0][mark1_index] # ch1/2 m1
        channel_array[1][mark2_index] = channel_array[0][mark2_index] # ch1/2 m2
        ## set ch4 markers equal to ch3 markers
        channel_array[3][mark1_index] = channel_array[2][mark1_index] # ch3/4 mmark1_index
        channel_array[3][mark2_index] = channel_array[2][mark2_index] # ch3/4 mmark2_index
        return channel_array
    ##END _intitialize_channels

    
    def _gen_sweep(self, sweep_name, start, stop, dest_wave, initial_pulse=Pulse(amplitude=0, duration=0,start=0)):
        '''
        DESCRIPTION:  sweeps 'none', 'amplitude', 'width', 'start' or 'phase' 
                'none' sets same pulse for all steps in sequence
        INPUT:       sets range for initial + [start,stop)
                updates parameters to initial_pulse
        OUTPUT:     writes to dest_wave 
        '''
        
        ## Check input
        if len(dest_wave) < self.num_steps:
            raise IOError("dest_wave is too short ({0})".format(len(dest_wave)))
        
        updated_pulse = initial_pulse.copy()
        if sweep_name == 'none':
            for step_index in range(self.num_steps):
                gen_pulse( dest_wave = dest_wave[step_index], pulse=updated_pulse)

        elif sweep_name == 'start':
            for step_index, param_val in enumerate(np.linspace(start,stop,self.num_steps)):
                updated_pulse.start = initial_pulse.start + int(param_val)
                gen_pulse( dest_wave = dest_wave[step_index], pulse=updated_pulse)

        elif sweep_name == 'amplitude':
            for step_index, param_val in enumerate(np.linspace(start,stop,self.num_steps)):
                updated_pulse.amplitude= initial_pulse.amplitude+ param_val
                gen_pulse( dest_wave = dest_wave[step_index], pulse=updated_pulse)

        elif sweep_name == 'width':
            for step_index, param_val in enumerate(np.linspace(start,stop,self.num_steps)):
                updated_pulse.duration= initial_pulse.duration + int(param_val)
                gen_pulse( dest_wave = dest_wave[step_index], pulse=updated_pulse)

        elif sweep_name == 'phase':
            if not initial_pulse.ssm_bool: raise ValueError("Sweeping phase w/o SSM")
            for step_index, param_val in enumerate(np.linspace(start,stop,self.num_steps)):
                updated_pulse.phase= initial_pulse.phase+ param_val
                gen_pulse( dest_wave = dest_wave[step_index], pulse=updated_pulse)
         
        elif sweep_name == 'ssm':
            for step_index, param_val in enumerate(np.linspace(start,stop,self.num_steps)):
                updated_pulse.ssm_freq = initial_pulse.ssm_freq + param_val
                gen_pulse( dest_wave = dest_wave[step_index], pulse=updated_pulse)

        else:
            raise ValueError("Bad sweep parameter: "+sweep_name)
    #END gen_sweep 


    def write_sequence(self, base_name='foo', file_path=os.getcwd(), use_range_01=False,num_offset=0, write_binary=False): 
        ''' 
        DESCRIPTION: writes a single channel INPUT:
            (optional) mark1/2: numpy arrays with marker data (0,1)
        OUTPUT:
        TODO:
        '''
        t = time.time()
        if not file_path.endswith("\\"): file_path+= "\\"
        print("writing to {}".format(file_path))

        for ch_index, (channel, mark1, mark2) in enumerate(self.channel_list):
            ch_name = "ch" + str(ch_index+1)
            print("writing "+ch_name)

            for step_index in range(self.num_steps):
                if write_binary:
                    file_name = file_path+base_name+"_"+ch_name+"_{:04d}.bin".format(step_index+num_offset)
                    mark_file_name = file_path+base_name+"_"+ch_name+"_{:04d}.mrk".format(step_index+num_offset)
                else:
                    file_name = file_path+base_name+"_"+ch_name+"_{:04d}.csv".format(step_index+num_offset)

                if use_range_01: # write floats between 0 and 1
                    with_index = zip(range(len(channel[step_index])), channel[step_index] )
                    np.savetxt(file_name, with_index, fmt='%d, %f')
                    continue

                # convert to binary
                # 15 bits = 12 bits of information, 2**13=sign bit, 2**14=mark1, 2**15=mark2
                else:
                    new_mark1 = [ int(i*2**14) for i in mark1[step_index] ]
                    new_mark2 = [ int(i*2**15) for i in mark2[step_index] ]
                    if write_binary:
                        binary_file = np.array([ round(2**15 *val + 2**15) for val in channel[step_index] ])
                        binary_file = binary_file.clip(0, 2**16-1)
                    else:
                        binary_file = np.array([ int(2**12 *val) for val in channel[step_index] ])
                        binary_file += new_mark1
                        binary_file += new_mark2
                    
                    #pd.DataFrame(binary_file).to_csv(file_name,float_format='%d', header=False)
                    #These codes contains hard coded 200ns padding
                    if write_binary:
                        binary_file = binary_file.astype('uint16')
                        binary_file = np.hstack((np.ones(12, dtype=np.uint16)*2**15, binary_file))
                        binary_file = np.hstack((binary_file, np.ones(500, dtype=np.uint16)*2**15))
                        binary_file.astype('uint16').tofile(file_name)
                        new0_mark = mark1[step_index][::2]
                        new0_mark = np.logical_or(new0_mark, mark1[step_index][1::2])
                        new1_mark = np.zeros(int(len(new0_mark) / 2), dtype=np.uint8)
                        new1_mark[new0_mark[::2]] += 2**0
                        new1_mark[new0_mark[1::2]] += 2**4
                        new0_mark = mark2[step_index][::2]
                        new0_mark = np.logical_or(new0_mark, mark2[step_index][1::2])
                        new1_mark[new0_mark[::2]] += 2**1
                        new1_mark[new0_mark[1::2]] += 2**5
                        new1_mark = np.hstack((np.zeros(128, dtype=np.uint8),new1_mark))
                        new1_mark.astype('uint8').tofile(mark_file_name)
                    else:
                        with_index = zip(range(len(binary_file)), binary_file)
                        np.savetxt(file_name, list(with_index), fmt='%d, %d')
            ##end for loop through channels
        print(f"Finished in {time.time() - t} seconds.")
    #END write_sequence


    def load_sequence_new(self, num_offset=0, amp=[1, 1, 1, 1], offset=[0, 0, 0, 0],\
                      dummy_header=True, slotId = 3, verbose=False):
        t = time.time()
        
        global admin
        global insts
        sclk = SAMPLE_RATE #1.25e9 
        num_steps = self.num_steps
        segNum_offset = 256
        query_syst_err = True
        
        dummy_offset = 0
        if dummy_header:
            dummy_offset = 1
            
        try:
            bin_queue = []
            
            def generate_bin():
                for ch_index, (channel, mark1, mark2) in enumerate(self.channel_list):
                    for step_index in range(self.num_steps):
                        seg_data = np.asarray(channel[step_index], dtype=np.float64)
                        seg_data = (seg_data + 1) * 2**15
#                        seg_data = np.array([ round(2**15 *val + 2**15) for val in channel[step_index]])
#                        seg_data = seg_data.clip(0, 2**16-1)
                        seg_data[seg_data<0] = 0
                        seg_data[seg_data>2**16-1] = 2**16-1
                        seg_data = np.uint16(seg_data)
                        # padding
        #                binary_data = np.hstack((np.ones(12, dtype=np.uint16)*2**15, binary_data))
        #                binary_data = np.hstack((binary_data, np.ones(500, dtype=np.uint16)*2**15))
                        
                        mark_mask = mark1[step_index][::2]
                        mark_mask = np.logical_or(mark_mask, mark1[step_index][1::2])
                        mark_data = np.zeros(int(len(mark_mask) / 2), dtype=np.uint8)
                        mark_data[mark_mask[::2]] += 2**0
                        mark_data[mark_mask[1::2]] += 2**4
                        
                        # the 2nd marker (not for our devices)
        #                mark_mask = mark2[step_index][::2]
        #                mark_mask = np.logical_or(mark_mask, mark2[step_index][1::2])
        #                mark_data[mark_mask[::2]] += 2**1
        #                mark_data[mark_mask[1::2]] += 2**5
                        
                        mark_data = mark_data.astype('uint8')
#                        bin_queue.insert(0, (seg_data,mark_data))
                        bin_queue.append((seg_data,mark_data))
            
#            thread = threading.Thread(target=generate_bin)
#            thread.start()
            generate_bin()
            
            slotId = np.uint32(slotId)
            inst = proteus_init(slotId)
            
            print("Resetting Proteus")
            
            instFunction.SendScpi(inst, "*CLS", query_syst_err, verbose=verbose)
            instFunction.SendScpi(inst, "*RST", query_syst_err, verbose=verbose)
            
            for ch_index, _ in enumerate(self.channel_list):
                instFunction.SendScpi(inst, f":INST:CHAN {ch_index+1}", query_syst_err, verbose=verbose)
                # set sampling DAC freq.
                instFunction.SendScpi(inst, f":FREQ:RAST {sclk}", query_syst_err, verbose=verbose)
                # delete all segments in RAM
                instFunction.SendScpi(inst, ":TRAC:DEL:ALL", query_syst_err, verbose=verbose)
                # enable task mode
                instFunction.SendScpi(inst, ":SOUR:FUNC:MODE ARB", query_syst_err, verbose=verbose)
    #                # common segment defs
    #            instFunction.SendScpi(inst, ":TRAC:DEF:TYPE NORM", query_syst_err)
                instFunction.SendScpi(inst, ":TRIG:STAT OFF", query_syst_err, verbose=verbose)
            
            for ch_index, (channel, mark1, mark2) in enumerate(self.channel_list):
                
                ch_name = "ch" + str(ch_index+1)
                print("Loading "+ch_name)
                
                if(ch_index % 2 == 0):
                    step_index_start = 1 + segNum_offset
                    instFunction.SendScpi(inst, f":INST:CHAN {ch_index+1}", query_syst_err, verbose=verbose)
                    if dummy_header:
                        instFunction.loadSegmentData(inst, 1, np.full(64, 32768, dtype=np.uint16).view(np.uint8), query_syst_err, verbose=verbose)
                else:
                    step_index_start = num_steps + 1 + segNum_offset

                for step_index in range(self.num_steps):
#                    seg_data = np.array([ round(2**15 *val + 2**15) for val in channel[step_index] ])
#                    seg_data = seg_data.clip(0, 2**16-1)
#                    seg_data = seg_data.astype('uint16')
#                    # padding
#    #                binary_data = np.hstack((np.ones(12, dtype=np.uint16)*2**15, binary_data))
#    #                binary_data = np.hstack((binary_data, np.ones(500, dtype=np.uint16)*2**15))
#                    
#                    mark_mask = mark1[step_index][::2]
#                    mark_mask = np.logical_or(mark_mask, mark1[step_index][1::2])
#                    mark_data = np.zeros(int(len(mark_mask) / 2), dtype=np.uint8)
#                    mark_data[mark_mask[::2]] += 2**0
#                    mark_data[mark_mask[1::2]] += 2**4
#                    
#                    # the 2nd marker (not for our devices)
#    #                mark_mask = mark2[step_index][::2]
#    #                mark_mask = np.logical_or(mark_mask, mark2[step_index][1::2])
#    #                mark_data[mark_mask[::2]] += 2**1
#    #                mark_data[mark_mask[1::2]] += 2**5
#                    
#                    mark_data = mark_data.astype('uint8')
                    # padding
    #                mark_data = np.hstack((np.zeros(128, dtype=np.uint8),mark_data))
                    
                    # load segments & markers
    #                thread = threading.Thread(target=instFunction.loadSegmentData, args=(inst, step_index_start + step_index + dummy_offset, seg_data.view(np.uint8), query_syst_err))
    #                thread.start()
#                    thread = threading.Thread(target=loadMarkData, args=(inst, mark_data, query_syst_err))
#                    thread.start()
                    while not bin_queue:
                        time.sleep(0.5)
                    seg_data, mark_data = bin_queue.pop(0)
#                    seg_data, mark_data = bin_queue.pop()
                    instFunction.loadSegmentData(inst, step_index_start + step_index + dummy_offset, seg_data.view(np.uint8), query_syst_err, verbose=verbose)
                    loadMarkData(inst, mark_data, query_syst_err)
                
            
            loadTaskTable(inst, num_steps, dummy_header, query_syst_err, verbose=verbose)
                
                    
            for ch_index, _ in enumerate(self.channel_list):
                instFunction.SendScpi(inst, f":INST:CHAN {ch_index+1}", query_syst_err, verbose=verbose) ##@ REMOVED +1 from ch_index
                
                instFunction.SendScpi(inst, ":TRIG:SOUR:ENAB TRG1", query_syst_err, verbose=verbose) # Set tigger enable signal to TRIG1 (CH specific)
#                instFunction.SendScpi(inst, ":TRIG:SEL EXT1", query_syst_err, verbose=verbose) # Select trigger for programming (CH specific)
                instFunction.SendScpi(inst, ":TRIG:LEV 0", query_syst_err, verbose=verbose) # Set trigger level
                instFunction.SendScpi(inst, ":TRIG:COUN 1", query_syst_err, verbose=verbose) # Set number of waveform cycles (1) to generate (CH specific)
    #                SendScpi(inst, ":TRIG:TIM 200e-9")
                instFunction.SendScpi(inst, ":TRIG:IDLE DC", query_syst_err, verbose=verbose) # Set output idle level to DC (CH specific)
                instFunction.SendScpi(inst, ":TRIG:IDLE:LEV 0", query_syst_err, verbose=verbose) # Set DC level in DAC value (CH specific)
                instFunction.SendScpi(inst, ":TRIG:STAT ON", query_syst_err, verbose=verbose) # Enable trigger state (CH specific)
                instFunction.SendScpi(inst, ":INIT:CONT OFF", query_syst_err, verbose=verbose) # Enable trigger mode (CH specific)
    #                SendScpi(inst, ":INIT:CONT ON") # Enable trigger mode (CH specific)
                
    #                SendScpi(inst, ":TRIG:SOUR:ENAB INT") # Set tigger enable signal to TRIG1 (CH specific)
    #                SendScpi(inst, ":TRIG:SEL NT1") # Select trigger for programming (CH specific)
    ##                SendScpi(inst, ":TRIG:LEV 0") # Set trigger level 
    #                SendScpi(inst, ":TRIG:COUN 1") # Set number of waveform cycles (1) to generate (CH specific)
    #                SendScpi(inst, ":TRIG:TIM 200e-9")
    #                SendScpi(inst, ":TRIG:IDLE DC") # Set output idle level to DC (CH specific)
    #                SendScpi(inst, ":TRIG:IDLE:LEV {0}".format(0)) # Set DC level in DAC value (CH specific)
    #                SendScpi(inst, ":TRIG:STAT ON") # Enable trigger state (CH specific)
    #                SendScpi(inst, ":INIT:CONT OFF") # Enable trigger mode (CH specific)
            
            
            for ch_index, _ in enumerate(self.channel_list):
                # Setting up amplitudes and offsets
                instFunction.SendScpi(inst, f":INST:CHAN {ch_index+1}", query_syst_err, verbose=verbose) 
                instFunction.SendScpi(inst, f":VOLT {amp[ch_index]}", query_syst_err, verbose=verbose)
                instFunction.SendScpi(inst, f":VOLT:OFFS {offset[ch_index]}", query_syst_err, verbose=verbose)
                instFunction.SendScpi(inst, ":SOUR:FUNC:MODE TASK", query_syst_err, verbose=verbose)
    #                instFunction.SendScpi(inst, (":SOUR:FUNC:MODE ARB")
                
                # connect ouput
                instFunction.SendScpi(inst, ":OUTP ON", query_syst_err, verbose=verbose)
                
                # enble markers
#                instFunction.SendScpi(inst, ":MARK:MASK 65535", query_syst_err, verbose=verbose)
                instFunction.SendScpi(inst, ":MARK:SEL 1", query_syst_err, verbose=verbose)
                instFunction.SendScpi(inst, ":MARK:STAT ON", query_syst_err, verbose=verbose)
                # 
                instFunction.SendScpi(inst, ":MARK:SEL 2", query_syst_err, verbose=verbose)
                instFunction.SendScpi(inst, ":MARK:STAT ON", query_syst_err, verbose=verbose)
            
            
            ## JTM ADDED 20/09/08 to circumvent failure of start_from() and to 
            ##   fix channel timing bugs
            task_start_index = 0
            for ch_index, _ in enumerate(self.channel_list):
                instFunction.SendScpi(inst, f":INST:CHAN {ch_index+1}", query_syst_err, verbose=verbose)
                instFunction.SendScpi(inst, f":FREQ:RAST {sclk}", query_syst_err, verbose=verbose)
                instFunction.SendScpi(inst, f":TASK:SEL 1", query_syst_err, verbose=verbose)
                instFunction.SendScpi(inst, f":TASK:DEF:NEXT1 {2 + task_start_index}", query_syst_err, verbose=verbose)
        
        finally:
            proteus_close(slotId)
        print(f"Finished in {time.time() - t} seconds.")
        
        #proteusapi.start_from(0, inst_index=inst_index)
    ##END load_sequence_new
    
    
    def load_sequence(self, num_offset=0, amp=[1, 1, 1, 1], offset=[0, 0, 0, 0],\
                      dummy_header=True, inst_index=0, verbose=True):        
        sclk = SAMPLE_RATE #1.25e9 
#        sclk = 1e8
        num_steps = self.num_steps
        segNum_offset = 256
        global insts
        slotId = np.uint32(3)
        
        dummy_offset = 0
        if dummy_header:
            dummy_offset = 1
        
        if verbose: print("Resetting Proteus")
        
        proteusapi.SendScpi("*RST", inst_index=inst_index)
        
        for ch_index, _ in enumerate(self.channel_list):
            proteusapi.SendScpi(":INST:CHAN {}".format(ch_index+1), inst_index=inst_index)
            # set sampling DAC freq.
            proteusapi.SendScpi(":FREQ:RAST {0}".format(sclk), inst_index=inst_index)
            # delete all segments in RAM
            proteusapi.SendScpi(":TRAC:DEL:ALL", inst_index=inst_index)
            # enable task mode
            proteusapi.SendScpi(":SOUR:FUNC:MODE ARB", inst_index=inst_index)
#                # common segment defs
            proteusapi.SendScpi(":TRAC:DEF:TYPE NORM", inst_index=inst_index)
            proteusapi.SendScpi(":TRIG:STAT OFF", inst_index=inst_index)
            
#        seg_data_save = []
#            
#        channel_list2 = [self.channel_list[1], self.channel_list[0], self.channel_list[2], self.channel_list[3]]
        for ch_index, (channel, mark1, mark2) in enumerate(self.channel_list):
#            if ch_index == 0:
#                ch_index = 1
#            elif ch_index == 1:
#                ch_index = 0
            
            ch_name = "ch" + str(ch_index+1)
            if verbose: print("Loading "+ch_name)
            
            if(ch_index % 2 == 0):
                step_index_start = 1 + segNum_offset
#                step_index_start = num_steps + 1 + segNum_offset
                proteusapi.SendScpi(":INST:CHAN {}".format(ch_index+1), inst_index=inst_index) ##@ REMOVED +1 from ch_index
                if dummy_header:
                    proteusapi.loadSegData(1, np.full(64, 32768, dtype=np.uint16), inst_index=inst_index)
            else:
                step_index_start = num_steps + 1 + segNum_offset
#                step_index_start = 1 + segNum_offset
                
            for step_index in range(self.num_steps):
                
                seg_data = np.array([ round(2**15 *val + 2**15) for val in channel[step_index] ])
                seg_data = seg_data.clip(0, 2**16-1)
                seg_data = seg_data.astype('uint16')
#                if ch_index == 0:
#                    seg_data = np.bitwise_and(seg_data, np.uint16(0x8000))
#                if ch_index == 1:
#                    seg_data = np.bitwise_and(seg_data, np.uint16(0x8000))
#                if ch_index == 1:
#                    seg_data = np.array([ round(2**15 *val + 2**15) for val in self.channel_list[0][0][step_index] ])
#                    seg_data = seg_data.clip(0, 2**16-1)
#                    seg_data = seg_data.astype('uint16')
                # padding
#                binary_data = np.hstack((np.ones(12, dtype=np.uint16)*2**15, binary_data))
#                binary_data = np.hstack((binary_data, np.ones(500, dtype=np.uint16)*2**15))
                
                mark_mask = mark1[step_index][::2]
                mark_mask = np.logical_or(mark_mask, mark1[step_index][1::2])
                mark_data = np.zeros(int(len(mark_mask) / 2), dtype=np.uint8)
                mark_data[mark_mask[::2]] += 2**0
                mark_data[mark_mask[1::2]] += 2**4
                
                # the 2nd marker (not for our devices)
#                mark_mask = mark2[step_index][::2]
#                mark_mask = np.logical_or(mark_mask, mark2[step_index][1::2])
#                mark_data[mark_mask[::2]] += 2**1
#                mark_data[mark_mask[1::2]] += 2**5
                
                mark_data = mark_data.astype('uint8')
                # padding
#                mark_data = np.hstack((np.zeros(128, dtype=np.uint8),mark_data))
                
                # load segments & markers
                proteusapi.loadSegData(step_index_start + step_index + dummy_offset, seg_data, inst_index=inst_index)
                #loadMarkData(mark_data)
                # update with new, faster loading method
                proteusapi.loadMarkData(mark_data, inst_index=inst_index)
#                inst = insts[slotId]
#                loadMarkData(inst, mark_data, 1)
            
        
        proteusapi.loadTaskTable(num_steps, dummy_header=dummy_header)
            
                
        for ch_index, _ in enumerate(self.channel_list):
            proteusapi.SendScpi(":INST:CHAN {}".format(ch_index+1), inst_index=inst_index) ##@ REMOVED +1 from ch_index
            
            proteusapi.SendScpi(":TRIG:SOUR:ENAB TRG1", inst_index=inst_index) # Set tigger enable signal to TRIG1 (CH specific)
            proteusapi.SendScpi(":TRIG:SEL EXT1", inst_index=inst_index) # Select trigger for programming (CH specific)
            proteusapi.SendScpi(":TRIG:LEV 0", inst_index=inst_index) # Set trigger level 
            proteusapi.SendScpi(":TRIG:COUN 1", inst_index=inst_index) # Set number of waveform cycles (1) to generate (CH specific)
#                SendScpi(inst, ":TRIG:TIM 200e-9")
            proteusapi.SendScpi(":TRIG:IDLE DC", inst_index=inst_index) # Set output idle level to DC (CH specific)
            proteusapi.SendScpi(":TRIG:IDLE:LEV {0}".format(0), inst_index=inst_index) # Set DC level in DAC value (CH specific)
            proteusapi.SendScpi(":TRIG:STAT ON", inst_index=inst_index) # Enable trigger state (CH specific)
            proteusapi.SendScpi(":INIT:CONT OFF", inst_index=inst_index) # Enable trigger mode (CH specific)
#                SendScpi(inst, ":INIT:CONT ON") # Enable trigger mode (CH specific)
            
#                SendScpi(inst, ":TRIG:SOUR:ENAB INT") # Set tigger enable signal to TRIG1 (CH specific)
#                SendScpi(inst, ":TRIG:SEL NT1") # Select trigger for programming (CH specific)
##                SendScpi(inst, ":TRIG:LEV 0") # Set trigger level 
#                SendScpi(inst, ":TRIG:COUN 1") # Set number of waveform cycles (1) to generate (CH specific)
#                SendScpi(inst, ":TRIG:TIM 200e-9")
#                SendScpi(inst, ":TRIG:IDLE DC") # Set output idle level to DC (CH specific)
#                SendScpi(inst, ":TRIG:IDLE:LEV {0}".format(0)) # Set DC level in DAC value (CH specific)
#                SendScpi(inst, ":TRIG:STAT ON") # Enable trigger state (CH specific)
#                SendScpi(inst, ":INIT:CONT OFF") # Enable trigger mode (CH specific)
        
        
        for ch_index, _ in enumerate(self.channel_list):
            # Setting up amplitudes and offsets
            proteusapi.SendScpi(":INST:CHAN {}".format(ch_index+1), inst_index=inst_index) ##@ REMOVED +1 from ch_index
            proteusapi.SendScpi(":VOLT {}".format(amp[ch_index]), inst_index=inst_index)
            proteusapi.SendScpi(":VOLT:OFFS {}".format(offset[ch_index]), inst_index=inst_index)
            proteusapi.SendScpi(":SOUR:FUNC:MODE TASK", inst_index=inst_index)
#                proteusapi.SendScpi(":SOUR:FUNC:MODE ARB")
            
            # connect ouput
            proteusapi.SendScpi(":OUTP ON", inst_index=inst_index)
            
            # enble markers
            proteusapi.SendScpi(":MARK:MASK 65535", inst_index=inst_index)
            proteusapi.SendScpi(":MARK:SEL 1", inst_index=inst_index)
            proteusapi.SendScpi(":MARK:STAT ON", inst_index=inst_index)
            # 
            proteusapi.SendScpi(":MARK:SEL 2", inst_index=inst_index)
            proteusapi.SendScpi(":MARK:STAT ON", inst_index=inst_index)
        
        
        ## JTM ADDED 20/09/08 to circumvent failure of start_from() and to 
        ##   fix channel timing bugs
        task_start_index = 0
        for ch_index, _ in enumerate(self.channel_list):
            proteusapi.SendScpi(":INST:CHAN {}".format(ch_index+1), inst_index=inst_index)
            proteusapi.SendScpi(":FREQ:RAST {0}".format(sclk), inst_index=inst_index)
            proteusapi.SendScpi(":TASK:SEL {}".format(1), inst_index=0)
            proteusapi.SendScpi(":TASK:DEF:NEXT1 {}".format(2 + task_start_index), inst_index=0)
        
        #proteusapi.start_from(0, inst_index=inst_index)
    ##END load_sequence

    
    def load_sequence_proteusapi(self, instr_addr, base_name='foo', file_path=os.getcwd(), num_offset=0):
        ''' 
        DESCRIPTION: loads multi channel INPUT:
        OUTPUT:
        TODO:
        '''
        sclk = 1e9
        num_steps = self.num_steps
        if not file_path.endswith("\\"): file_path+= "\\"
        print("loading {}".format(file_path))        
        
        # get hw option
        proteusapi.SendScpi("*OPT?")
        # reset - must!
        proteusapi.SendScpi("*RST")
        for ch_index, _ in enumerate(self.channel_list):
            proteusapi.SendScpi(":INST:CHAN {}".format(ch_index+1))
            # set sampling DAC freq.
            proteusapi.SendScpi(":FREQ:RAST {0}".format(sclk))
            # delete all segments in RAM
            proteusapi.SendScpi(":TRAC:DEL:ALL")
            # enable task mode
            proteusapi.SendScpi(":SOUR:FUNC:MODE ARB")
#                # common segment defs
            proteusapi.SendScpi(":TRAC:DEF:TYPE NORM")
            proteusapi.SendScpi(":TRIG:STAT OFF")
            
            
        for ch_index, _ in enumerate(self.channel_list):
            ch_name = "ch" + str(ch_index+1)
            print("loading "+ch_name)
            # select channel
            proteusapi.SendScpi(":INST:CHAN {}".format(ch_index+1))
            
            if(ch_index % 2 == 0):
                step_index_start = 1
            else:
                step_index_start = num_steps + 1
                
            # load segments & markers
            for step_index in range(num_steps):
                proteusapi.SendScpi(":INST:CHAN {}".format(ch_index+1))
                file_name = file_path+base_name+"_"+ch_name+"_{:04d}.bin".format(step_index+num_offset)
#                    file_name = r"C:\Users\crow108\Documents\Python\segments16bitCSV\TwentyCyclesSine_16Bit2048pts.csv"
                proteusapi.loadSegment(step_index_start + step_index, file_name)
                mark_file_name = file_path+base_name+"_"+ch_name+"_{:04d}.mrk".format(step_index+num_offset)
#                    mark_file_name = r"C:\Users\crow108\Documents\Python\markers\marker_test.mrk"
                proteusapi.SendBinScpi(":MARK:DATA:FNAM 0 , #", mark_file_name)
            
        
        proteusapi.loadTaskTable(num_steps)
            
                
        for ch_index, _ in enumerate(self.channel_list):
            proteusapi.SendScpi(":INST:CHAN {}".format(ch_index+1))
            
            proteusapi.SendScpi(":TRIG:SOUR:ENAB TRG1") # Set tigger enable signal to TRIG1 (CH specific)
            proteusapi.SendScpi(":TRIG:SEL EXT1") # Select trigger for programming (CH specific)
            proteusapi.SendScpi(":TRIG:LEV 0") # Set trigger level 
            proteusapi.SendScpi(":TRIG:COUN 1") # Set number of waveform cycles (1) to generate (CH specific)
#                SendScpi(inst, ":TRIG:TIM 200e-9")
            proteusapi.SendScpi(":TRIG:IDLE DC") # Set output idle level to DC (CH specific)
            proteusapi.SendScpi(":TRIG:IDLE:LEV {0}".format(0)) # Set DC level in DAC value (CH specific)
            proteusapi.SendScpi(":TRIG:STAT ON") # Enable trigger state (CH specific)
            proteusapi.SendScpi(":INIT:CONT OFF") # Enable trigger mode (CH specific)
#                SendScpi(inst, ":INIT:CONT ON") # Enable trigger mode (CH specific)
            
#                SendScpi(inst, ":TRIG:SOUR:ENAB INT") # Set tigger enable signal to TRIG1 (CH specific)
#                SendScpi(inst, ":TRIG:SEL NT1") # Select trigger for programming (CH specific)
##                SendScpi(inst, ":TRIG:LEV 0") # Set trigger level 
#                SendScpi(inst, ":TRIG:COUN 1") # Set number of waveform cycles (1) to generate (CH specific)
#                SendScpi(inst, ":TRIG:TIM 200e-9")
#                SendScpi(inst, ":TRIG:IDLE DC") # Set output idle level to DC (CH specific)
#                SendScpi(inst, ":TRIG:IDLE:LEV {0}".format(0)) # Set DC level in DAC value (CH specific)
#                SendScpi(inst, ":TRIG:STAT ON") # Enable trigger state (CH specific)
#                SendScpi(inst, ":INIT:CONT OFF") # Enable trigger mode (CH specific)
            
        for ch_index, _ in enumerate(self.channel_list):
            proteusapi.SendScpi(":TASK:SEL 1")
        for ch_index, _ in enumerate(self.channel_list):
            proteusapi.SendScpi(":TRIG:STAT ON") # Enable trigger state (CH specific)
            
            
        amp = [1, 1, 1, 1]
        offset = [0, 0, 0, 0]
        for ch_index, _ in enumerate(self.channel_list):
            # Setting up amplitudes and offsets
            proteusapi.SendScpi(":INST:CHAN {}".format(ch_index+1))
            proteusapi.SendScpi(":VOLT {}".format(amp[ch_index]))
            proteusapi.SendScpi(":VOLT:OFFS {}".format(offset[ch_index]))
            proteusapi.SendScpi(":SOUR:FUNC:MODE TASK")
#                proteusapi.SendScpi(":SOUR:FUNC:MODE ARB")
            
            # connect ouput
            proteusapi.SendScpi(":OUTP ON")
            
            # enble markers
            proteusapi.SendScpi(":MARK:MASK 65535")
            proteusapi.SendScpi(":MARK:SEL 1")
            proteusapi.SendScpi(":MARK:STAT ON")
            proteusapi.SendScpi(":MARK:SEL 2")
            proteusapi.SendScpi(":MARK:STAT ON")
    
    def load_sequence_proteusapi_old(self, instr_addr, base_name='foo', file_path=os.getcwd(), num_offset=0):
        ''' 
        DESCRIPTION: loads multi channel INPUT:
        OUTPUT:
        TODO:
        '''
        sclk = 1e9
        num_steps = self.num_steps
        if not file_path.endswith("\\"): file_path+= "\\"
        print("loading {}".format(file_path))        
        
        # get hw option
        proteusapi.SendScpi("*OPT?")
        # reset - must!
        proteusapi.SendScpi("*RST")
        for ch_index, _ in enumerate(self.channel_list):
            proteusapi.SendScpi(":INST:CHAN {}".format(ch_index+1))
            # set sampling DAC freq.
            proteusapi.SendScpi(":FREQ:RAST {0}".format(sclk))
            # delete all segments in RAM
            proteusapi.SendScpi(":TRAC:DEL:ALL")
            # enable task mode
            proteusapi.SendScpi(":SOUR:FUNC:MODE ARB")
#                # common segment defs
            proteusapi.SendScpi(":TRAC:DEF:TYPE NORM")
            proteusapi.SendScpi(":TRIG:STAT OFF")
            
            
        for ch_index, _ in enumerate(self.channel_list):
            ch_name = "ch" + str(ch_index+1)
            print("loading "+ch_name)
            # select channel
            proteusapi.SendScpi(":INST:CHAN {}".format(ch_index+1))
            
            if(ch_index % 2 == 0):
                step_index_start = 1
            else:
                step_index_start = num_steps + 1
                
            # load segments & markers
            for step_index in range(num_steps):
                proteusapi.SendScpi(":INST:CHAN {}".format(ch_index+1))
                file_name = file_path+base_name+"_"+ch_name+"_{:04d}.bin".format(step_index+num_offset)
#                    file_name = r"C:\Users\crow108\Documents\Python\segments16bitCSV\TwentyCyclesSine_16Bit2048pts.csv"
                proteusapi.loadSegment(step_index_start + step_index, file_name)
                mark_file_name = file_path+base_name+"_"+ch_name+"_{:04d}.mrk".format(step_index+num_offset)
#                    mark_file_name = r"C:\Users\crow108\Documents\Python\markers\marker_test.mrk"
                proteusapi.SendBinScpi(":MARK:DATA:FNAM 0 , #", mark_file_name)
            
            for step_index in range(num_steps):
                proteusapi.SendScpi(":TASK:SEL {}".format(step_index+1))
                proteusapi.SendScpi(":TASK:DEF:TYPE SING")
                proteusapi.SendScpi(":TASK:DEF:LOOP 1")
                proteusapi.SendScpi(":TASK:DEF:SEQ 1")
                proteusapi.SendScpi(":TASK:DEF:SEGM {}".format(step_index+step_index_start))
                #proteusapi.SendScpi(":TASK:DEF:IDLE FIRS")
                proteusapi.SendScpi(":TASK:DEF:IDLE:DC 32768")
#                    proteusapi.SendScpi(":TASK:DEF:ENAB INT")
                proteusapi.SendScpi(":TASK:DEF:ENAB TRIG1")
                proteusapi.SendScpi(":TASK:DEF:ABOR NONE")
                proteusapi.SendScpi(":TASK:DEF:JUMP EVEN")
                proteusapi.SendScpi(":TASK:DEF:DEST NEXT")
                proteusapi.SendScpi(":TASK:DEF:NEXT1 {}".format((step_index+1)%num_steps + step_index_start))
                proteusapi.SendScpi(":TASK:DEF:NEXT2 0")
            
                
        for ch_index, _ in enumerate(self.channel_list):
            proteusapi.SendScpi(":INST:CHAN {}".format(ch_index+1))
            
            proteusapi.SendScpi(":TRIG:SOUR:ENAB TRG1") # Set tigger enable signal to TRIG1 (CH specific)
            proteusapi.SendScpi(":TRIG:SEL EXT1") # Select trigger for programming (CH specific)
            proteusapi.SendScpi(":TRIG:LEV 0") # Set trigger level 
            proteusapi.SendScpi(":TRIG:COUN 1") # Set number of waveform cycles (1) to generate (CH specific)
#                SendScpi(inst, ":TRIG:TIM 200e-9")
            proteusapi.SendScpi(":TRIG:IDLE DC") # Set output idle level to DC (CH specific)
            proteusapi.SendScpi(":TRIG:IDLE:LEV {0}".format(0)) # Set DC level in DAC value (CH specific)
            proteusapi.SendScpi(":TRIG:STAT ON") # Enable trigger state (CH specific)
            proteusapi.SendScpi(":INIT:CONT OFF") # Enable trigger mode (CH specific)
#                SendScpi(inst, ":INIT:CONT ON") # Enable trigger mode (CH specific)
            
#                SendScpi(inst, ":TRIG:SOUR:ENAB INT") # Set tigger enable signal to TRIG1 (CH specific)
#                SendScpi(inst, ":TRIG:SEL NT1") # Select trigger for programming (CH specific)
##                SendScpi(inst, ":TRIG:LEV 0") # Set trigger level 
#                SendScpi(inst, ":TRIG:COUN 1") # Set number of waveform cycles (1) to generate (CH specific)
#                SendScpi(inst, ":TRIG:TIM 200e-9")
#                SendScpi(inst, ":TRIG:IDLE DC") # Set output idle level to DC (CH specific)
#                SendScpi(inst, ":TRIG:IDLE:LEV {0}".format(0)) # Set DC level in DAC value (CH specific)
#                SendScpi(inst, ":TRIG:STAT ON") # Enable trigger state (CH specific)
#                SendScpi(inst, ":INIT:CONT OFF") # Enable trigger mode (CH specific)
            
        for ch_index, _ in enumerate(self.channel_list):
            proteusapi.SendScpi(":TASK:SEL 1")
        for ch_index, _ in enumerate(self.channel_list):
            proteusapi.SendScpi(":TRIG:STAT ON") # Enable trigger state (CH specific)
            
            
        amp = [1, 1, 1, 1]
        offset = [0, 0, 0, 0]
        for ch_index, _ in enumerate(self.channel_list):
            # Setting up amplitudes and offsets
            proteusapi.SendScpi(":INST:CHAN {}".format(ch_index+1))
            proteusapi.SendScpi(":VOLT {}".format(amp[ch_index]))
            proteusapi.SendScpi(":VOLT:OFFS {}".format(offset[ch_index]))
            proteusapi.SendScpi(":SOUR:FUNC:MODE TASK")
#                proteusapi.SendScpi(":SOUR:FUNC:MODE ARB")
            
            # connect ouput
            proteusapi.SendScpi(":OUTP ON")
            
            # enble markers
            proteusapi.SendScpi(":MARK:MASK 65535")
            proteusapi.SendScpi(":MARK:SEL 1")
            proteusapi.SendScpi(":MARK:STAT ON")
            proteusapi.SendScpi(":MARK:SEL 2")
            proteusapi.SendScpi(":MARK:STAT ON")

    
    def load_sequence_old(self, instr_addr, base_name='foo', file_path=os.getcwd(), num_offset=0):
        ''' 
        DESCRIPTION: loads multi channel INPUT:
        OUTPUT:
        TODO:
        '''
        sclk = 1e9
#        file_length = self.sequence_length
        num_steps = self.num_steps
        if not file_path.endswith("\\"): file_path+= "\\"
        print("loading {}".format(file_path))        
        
        def ScpiCommands(inst):
#            trig_lev = instFunction.getSclkTrigLev(inst)
            # get hw option
            instFunction.SendScpi(inst, "*OPT?")
            # reset - must!
            instFunction.SendScpi(inst, "*RST")
            for ch_index, _ in enumerate(self.channel_list):
                instFunction.SendScpi(inst, ":INST:CHAN {}".format(ch_index+1))
                # set sampling DAC freq.
                instFunction.SendScpi(inst, ":FREQ:RAST {0}".format(sclk))
                # delete all segments in RAM
                instFunction.SendScpi(inst, ":TRAC:DEL:ALL")
                # enable task mode
                instFunction.SendScpi(inst, ":SOUR:FUNC:MODE ARB")
#                # common segment defs
                instFunction.SendScpi(inst, ":TRAC:DEF:TYPE NORM")
                instFunction.SendScpi(inst, ":TRIG:STAT OFF")
                
                
            for ch_index, _ in enumerate(self.channel_list):
                ch_name = "ch" + str(ch_index+1)
                print("loading "+ch_name)
                # select channel
                instFunction.SendScpi(inst, ":INST:CHAN {}".format(ch_index+1))
                
                if(ch_index % 2 != 0):
                    step_index_start = 1
                else:
                    step_index_start = num_steps + 1
                    
                # load segments & markers
                for step_index in range(num_steps):
                    instFunction.SendScpi(inst, ":INST:CHAN {}".format(ch_index+1))
                    file_name = file_path+base_name+"_"+ch_name+"_{:04d}.bin".format(step_index+num_offset)
#                    file_name = r"C:\Users\crow108\Documents\Python\segments16bitCSV\TwentyCyclesSine_16Bit2048pts.csv"
                    instFunction.loadSegment(inst, step_index_start + step_index, file_name)
                    mark_file_name = file_path+base_name+"_"+ch_name+"_{:04d}.mrk".format(step_index+num_offset)
#                    mark_file_name = r"C:\Users\crow108\Documents\Python\markers\marker_test.mrk"
                    instFunction.SendBinScpi(inst, ":MARK:DATA:FNAM 0 , #", mark_file_name)
                
                for step_index in range(num_steps):
                    instFunction.SendScpi(inst, ":TASK:SEL {}".format(step_index+1))
                    instFunction.SendScpi(inst, ":TASK:DEF:TYPE SING")
                    instFunction.SendScpi(inst, ":TASK:DEF:LOOP 1")
                    instFunction.SendScpi(inst, ":TASK:DEF:SEQ 1")
                    instFunction.SendScpi(inst, ":TASK:DEF:SEGM {}".format(step_index+step_index_start))
                    instFunction.SendScpi(inst, ":TASK:DEF:IDLE FIRS")
                    instFunction.SendScpi(inst, ":TASK:DEF:IDLE:DC 32768")
#                    instFunction.SendScpi(inst, ":TASK:DEF:ENAB INT")
                    instFunction.SendScpi(inst, ":TASK:DEF:ENAB TRIG1")
                    instFunction.SendScpi(inst, ":TASK:DEF:ABOR NONE")
                    instFunction.SendScpi(inst, ":TASK:DEF:JUMP EVEN")
                    instFunction.SendScpi(inst, ":TASK:DEF:DEST NEXT")
                    instFunction.SendScpi(inst, ":TASK:DEF:NEXT1 {}".format((step_index+1)%num_steps + 1))
                    instFunction.SendScpi(inst, ":TASK:DEF:NEXT2 0")
                
                    
            for ch_index, _ in enumerate(self.channel_list):
                instFunction.SendScpi(inst, ":INST:CHAN {}".format(ch_index+1))
                
                instFunction.SendScpi(inst, ":TRIG:SOUR:ENAB TRG1") # Set tigger enable signal to TRIG1 (CH specific)
                instFunction.SendScpi(inst, ":TRIG:SEL EXT1") # Select trigger for programming (CH specific)
                instFunction.SendScpi(inst, ":TRIG:LEV 0") # Set trigger level 
                instFunction.SendScpi(inst, ":TRIG:COUN 1") # Set number of waveform cycles (1) to generate (CH specific)
                instFunction.SendScpi(inst, ":TRIG:IDLE DC") # Set output idle level to DC (CH specific)
                instFunction.SendScpi(inst, ":TRIG:IDLE:LEV {0}".format(0)) # Set DC level in DAC value (CH specific)
                instFunction.SendScpi(inst, ":TRIG:STAT ON") # Enable trigger state (CH specific)
                instFunction.SendScpi(inst, ":INIT:CONT OFF") # Enable trigger mode (CH specific)
#                SendScpi(inst, ":INIT:CONT ON") # Enable trigger mode (CH specific)
                
#                SendScpi(inst, ":TRIG:SOUR:ENAB INT") # Set tigger enable signal to TRIG1 (CH specific)
#                SendScpi(inst, ":TRIG:SEL NT1") # Select trigger for programming (CH specific)
##                SendScpi(inst, ":TRIG:LEV 0") # Set trigger level 
#                SendScpi(inst, ":TRIG:COUN 1") # Set number of waveform cycles (1) to generate (CH specific)
#                SendScpi(inst, ":TRIG:TIM 200e-9")
#                SendScpi(inst, ":TRIG:IDLE DC") # Set output idle level to DC (CH specific)
#                SendScpi(inst, ":TRIG:IDLE:LEV {0}".format(0)) # Set DC level in DAC value (CH specific)
#                SendScpi(inst, ":TRIG:STAT ON") # Enable trigger state (CH specific)
#                SendScpi(inst, ":INIT:CONT OFF") # Enable trigger mode (CH specific)
                
            for ch_index, _ in enumerate(self.channel_list):
                instFunction.SendScpi(inst, ":TASK:SEL 1")
            for ch_index, _ in enumerate(self.channel_list):
                instFunction.SendScpi(inst, ":TRIG:STAT ON") # Enable trigger state (CH specific)
                
                
            amp = [1, 1, 1, 1]
            offset = [0, 0, 0, 0]
            for ch_index, _ in enumerate(self.channel_list):
                # Setting up amplitudes and offsets
                instFunction.SendScpi(inst, ":INST:CHAN {}".format(ch_index+1))
                instFunction.SendScpi(inst, ":VOLT {}".format(amp[ch_index]))
                instFunction.SendScpi(inst, ":VOLT:OFFS {}".format(offset[ch_index]))
                instFunction.SendScpi(inst, ":SOUR:FUNC:MODE TASK")
#                instFunction.SendScpi(inst, ":SOUR:FUNC:MODE ARB")
                
                # connect ouput
                instFunction.SendScpi(inst, ":OUTP ON")
                
#                 enble markers
                instFunction.SendScpi(inst, ":MARK:MASK 65535")
                instFunction.SendScpi(inst, ":MARK:SEL 1")
                instFunction.SendScpi(inst, ":MARK:STAT ON")
                instFunction.SendScpi(inst, ":MARK:SEL 2")
                instFunction.SendScpi(inst, ":MARK:STAT ON")
        
        # End of ScpiCommands
        
        # Initializing the instrument
        admin = instFunction.loadDLL()
        # following line prompts for input; replace with succeeding 2 lines.
        #slotId = instFunction.getSlotId(admin) 
        admin.Open()
        slotId = np.uint32(3)
        
    
        if not slotId:
            print("Invalid choice!")
        else:
            inst = admin.OpenInstrument(slotId) 
            if not inst:
                print("Failed to Open instrument with slot-Id {0}".format(slotId))
                print("\n")
            else:
                instId = inst.InstrId
                ###########  CALL THE SCPI ###########
                ScpiCommands(inst) #     <<<-------   #
                ######################################
                rc = admin.CloseInstrument(instId)
                instFunction.Validate(rc,__name__,instFunction.inspect.currentframe().f_back.f_lineno)
        rc = admin.Close()
        instFunction.Validate(rc,__name__,instFunction.inspect.currentframe().f_back.f_lineno)
        
    def load_sequence2(self, instr_addr, base_name='foo', file_path=os.getcwd(), num_offset=0):
        ''' 
        DESCRIPTION: loads multi channel INPUT:
        OUTPUT:
        TODO:
        '''
        file_length = self.sequence_length
        num_steps = self.num_steps
        if not file_path.endswith("\\"): file_path+= "\\"
        print("loading {}".format(file_path))        
        
        def ScpiCommands(inst):
            trig_lev = instFunction.getSclkTrigLev(inst)
            # get hw option
            instFunction.SendScpi(inst, "*OPT?")
            # reset - must!
            instFunction.SendScpi(inst, "*RST")
#            # set sampling DAC freq.
#            instFunction.SendScpi(inst, ":FREQ:RAST {0}".format(instFunction.sclk))
            for ch_index, _ in enumerate(self.channel_list):
                instFunction.SendScpi(inst, ":INST:CHAN {}".format(ch_index+1))
                instFunction.SendScpi(inst, ":SOUR:VOLT 1.0")
                instFunction.SendScpi(inst, ":INIT:CONT ON")
                # delete all segments in RAM
                instFunction.SendScpi(inst, ":TRAC:DEL:ALL")
                # enable task mode
#                instFunction.SendScpi(inst, ":SOUR:FUNC:MODE TASK")
                
                instFunction.SendScpi(inst, ":SOUR:FUNC:MODE ARB")
                # common segment defs
                instFunction.SendScpi(inst, ":TRAC:DEF:TYPE NORM")
                
                ch_name = "ch" + str(ch_index+1)
                ch_name = 'ch1'
                print("loading "+ch_name)
                # select channel
                instFunction.SendScpi(inst, ":INST:CHAN {}".format(ch_index+1))
                # load segments & markers
                for step_index in range(num_steps):
                    file_name = file_path+base_name+"_"+ch_name+"_{:04d}.bin".format(step_index+num_offset)
#                    file_name = r'C:\arbsequences\strong_dispersive_withPython\test_pulse_ringupdown_bin\foo_ch1_0004.bin'
                    instFunction.loadSegment(inst, step_index+1, file_name)
#                    mark_file_name = file_path+base_name+"_"+ch_name+"_{:04d}.mrk".format(step_index+num_offset)
###                    mark_file_name = r'C:\Users\marka\Documents\Python\markers\Waveform_test.mrk'
#                    instFunction.SendBinScpi(inst, ":MARK:DATA:FNAM {} , #".format(ch_index+1), mark_file_name)
                instFunction.SendScpi(inst, ":SOUR:FUNC:SEG 3")
                instFunction.SendScpi(inst, ":OUTP ON")
                # create tasks
            
            for ch_index, _ in enumerate(self.channel_list):
#                ch_index = 1
                instFunction.SendScpi(inst, ":INST:CHAN {}".format(ch_index+1))
                instFunction.SendScpi(inst, ":SOUR:FUNC:MODE TASK")
                for step_index in range(num_steps):
                    instFunction.SendScpi(inst, ":TASK:SEL {}".format(step_index+1))
                    instFunction.SendScpi(inst, ":TASK:DEF:TYPE SING")
                    instFunction.SendScpi(inst, ":TASK:DEF:LOOP 1")
                    instFunction.SendScpi(inst, ":TASK:DEF:SEGM {}".format(step_index+1))
                    instFunction.SendScpi(inst, ":TASK:DEF:IDLE:DC 32768")
                    instFunction.SendScpi(inst, ":TASK:DEF:ENAB NONE")
#                    instFunction.SendScpi(inst, ":TASK:DEF:ENAB TRIG1")
                    instFunction.SendScpi(inst, ":TASK:DEF:DEST NEXT")
                    instFunction.SendScpi(inst, ":TASK:DEF:NEXT1 {}".format((step_index+1)%num_steps + 1))
#            
#            for ch_index, _ in enumerate(self.channel_list):
#                instFunction.SendScpi(inst, ":INST:CHAN {}".format(ch_index+1))
#                instFunction.SendScpi(inst, ":TRIG:SOUR:ENAB TRG1") # Set tigger enable signal to TRIG1 (CH specific)
#                instFunction.SendScpi(inst, ":TRIG:SEL EXT1") # Select trigger for programming (CH specific)
#                instFunction.SendScpi(inst, ":TRIG:LEV 0") # Set trigger level
#                instFunction.SendScpi(inst, ":TRIG:COUN 1") # Set number of waveform cycles (1) to generate (CH specific)
#                instFunction.SendScpi(inst, ":TRIG:IDLE DC") # Set output idle level to DC (CH specific)
#                instFunction.SendScpi(inst, ":TRIG:IDLE:LEV {0}".format(trig_lev)) # Set DC level in DAC value (CH specific)
#                instFunction.SendScpi(inst, ":TRIG:STAT ON") # Enable trigger state (CH specific)
                
                
#            amp = [0.5, 0.5, 0.5, 0.5]
#            offset = [0, 0, 0, 0]
#            for ch_index, _ in enumerate(self.channel_list):
#                # Setting up amplitudes and offsets
#                instFunction.SendScpi(inst, ":INST:CHAN {}".format(ch_index+1))
##                instFunction.SendScpi(inst, ":VOLT {}".format(amp[ch_index]))
##                instFunction.SendScpi(inst, ":VOLT:OFFS {}".format(offset[ch_index]))
#                
#                # connect ouput
#                instFunction.SendScpi(inst, ":OUTP ON")
#                
#                # enble markers
##                instFunction.SendScpi(inst, ":MARK:SEL 1")
##                instFunction.SendScpi(inst, ":MARK:STAT ON")
##                instFunction.SendScpi(inst, ":MARK:SEL 2")
##                instFunction.SendScpi(inst, ":MARK:STAT ON")
#        
        # End of ScpiCommands
        
        # Initializing the instrument
        admin = instFunction.loadDLL()
        slotId = instFunction.getSlotId(admin)
    
        if not slotId:
            print("Invalid choice!")
        else:
            inst = admin.OpenInstrument(slotId) 
            if not inst:
                print("Failed to Open instrument with slot-Id {0}".format(slotId))
                print("\n")
            else:
                instId = inst.InstrId
                ###########  CALL THE SCPI ###########
                ScpiCommands(inst) #     <<<-------   #
                ######################################
                rc = admin.CloseInstrument(instId)
                instFunction.Validate(rc,__name__,instFunction.inspect.currentframe().f_back.f_lineno)
        rc = admin.Close()
        instFunction.Validate(rc,__name__,instFunction.inspect.currentframe().f_back.f_lineno)

    def convert_to_tabor_format(self):
        '''
        DESCRIPTION: converts the sequence structure to a loadable format
        INPUT: populated Sequence
        OUTPUT: array of size [4, num_steps, sequence_length] in binarized form with markers
        '''
        tabor_format = np.zeros((4,self.num_steps, self.sequence_length))
        for ch_index, (channel, mark1, mark2) in enumerate(self.channel_list):
            ## loop through ch 1-4
            single_channel_binary  = np.array(2**12 *channel,dtype='int')
            single_channel_binary += np.array(2**14 *mark1,dtype='int')
            single_channel_binary += np.array(2**15 *mark2,dtype='int')
            tabor_format[ch_index] = single_channel_binary
        ##END loop through channels
        return tabor_format
    ##END convert_to_tabor_format
##END Sequence 


def gen_pulse(dest_wave, pulse):
    ## consider renaming to insert_pulse()
    '''
    DESCRIPTION: generates pulse on one wave
            Note, this does not add constant pulese through all steps; that's handled by add_sweep('none')
    INPUT: 
        Pulse object (contains start,duration, etc)
    OUTPUT:
        in-place adjustment to dest_wave
    NOTES:
    TODO:
    '''
    ## Decompose pulse object
    start = pulse.start
    dur = pulse.duration
    amp = pulse.amplitude
    if dur <0:
        dur = abs(dur)
        start -= dur

    ##  Create output
    if pulse.ssm_bool:
        ssm_freq = pulse.ssm_freq    
        phase = pulse.phase
    
        # start times depend on start and duration because curves should pick up same absolute phase( may be shifted for cos/sin/etc), ie two pulses placed front to back should continue overall
        times = np.arange(start,start+dur)
        ang_freq = 2*np.pi*(ssm_freq*1E9)/SAMPLE_RATE # convert to units of SAMPLE_RATE
        phase_rad = phase/180.0*np.pi 
        addition = amp*np.sin(ang_freq*times + phase_rad)
    else: 
        addition = amp* np.ones(dur)    
        
    if pulse.gaussian_bool:
        argument = -(times-start-dur/2)**2
        argument /=     2*(dur*0.2)**2 # 0.847 gives Gauss(start +dur/2) = 0.5
        gauss_envelope = np.exp(argument);
        addition *= gauss_envelope

    try: 
        dest_wave[start:start+dur] += addition
    except ValueError:
        print( "Over-extended pulse (ignored):\n {0}".format(pulse.toString()))
#END gen_pulse


def some_Fun():
    '''
    DESCRIPTION: 
    INPUT:
    OUTPUT:
    TODO:
    '''
    pass

'''
def rabi_seq():
    file_length= 8000 # becomes global FILELENGTH
    num_steps = 101# becomes global NUMSTEPS
    #WAVE,MARK1, MARK2 = initialize(file_length, num_steps)
    ALL_CHANNELS = initialize_wx(file_length, num_steps)
    # ALL_CHANNELS is 4-array for Ch 1,2. Each elem is a tuple of (channel, M1,M2)
    #       each tuple elem. is a seq_len X num_samples matrix.

    ## channels
    p = Pulse(start=5795, duration=0,  amplitude=0.5, ssm_freq=0.200, phase=0)
    add_sweep(ALL_CHANNELS, channel=1, sweep_name='width', start=0 , stop= 200, initial_pulse=p )
    p.phase = 98.0
    add_sweep(ALL_CHANNELS, channel=2, sweep_name='width', start=0 , stop= 200, initial_pulse=p )
   
    readout = Pulse(start=6000,duration=1000,amplitude=1)
    add_sweep(ALL_CHANNELS, channel=3, sweep_name='none',initial_pulse=readout)

    ## markers
    gate = Pulse(start=5790, duration=10, amplitude=1)
    add_sweep(ALL_CHANNELS, channel=1, marker=1, sweep_name='width', start=0, stop=220, initial_pulse=gate)
    trigger = Pulse(start=2000, duration=1000, amplitude=1)
    add_sweep(ALL_CHANNELS, channel=3, marker=1, sweep_name='none', initial_pulse=trigger)
    
    return ALL_CHANNELS
    ## send to ARB
    dir_name = r"C:\Arb Sequences\EUR_sequences\mixerOrthogonality_98deg\piTime_23ns\tmp"
    write_sequence(ALL_CHANNELS, file_path=dir_name, use_range_01=False)
##END rabi_seq
'''


def create_gate(seq_matrix,width=5):
    '''
    DESCRIPTION: for all times (ts) and for all steps (ss): if any amplitude exists, extend in time by width
    INPUT: seq_matrix of size [sequence_steps, samples]
    OUTPUT: binary mask with same size as input
    ## KNOWN BUG: if pulse_end + width > num_samples will create error.
    '''
    mask_ss, mask_ts= np.where(seq_matrix != 0)
    gate = seq_matrix.copy()
    gate[ (mask_ss, mask_ts)] = 1
    gate[ (mask_ss, mask_ts-width)] = 1
    gate[ (mask_ss, mask_ts+width)] = 1
   
    return gate
##END create_gate
