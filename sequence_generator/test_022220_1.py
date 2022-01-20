import os
import sys
import inspect
import sys
import clr
import ctypes
import numpy as np
import proteus

slotId = np.uint32(4)
maxScpiResponse = 65535

#### Set Sample Clock ####
sclk = 9.0e9

datapath = r"C:\Users\marka\Documents\Python"

if (datapath):
    datapath = datapath +"\\"
print(datapath);
 
#### read files ####
#Waveform Segments
fileType = "bin" #<---- Set to csv or bin
#seg_file_path1 = datapath + 'segments8bitBin\Waveform_1.seg'
#seg_file_path2 = datapath + 'segments8bitBin\Waveform_2.seg'
#seg_file_path3 = datapath + 'segments8bitBin\Waveform_3.seg'
#seg_file_path4 = datapath + 'segments8bitBin\Waveform_4.seg'

seg_file_path1 = r'C:\arbsequences\strong_dispersive_withPython\test_pulse_ringupdown_bin\foo_ch1_0001.bin'
seg_file_path2 = r'C:\arbsequences\strong_dispersive_withPython\test_pulse_ringupdown_bin\foo_ch1_0002.bin'
seg_file_path3 = r'C:\arbsequences\strong_dispersive_withPython\test_pulse_ringupdown_bin\foo_ch1_0003.bin'
seg_file_path4 = r'C:\arbsequences\strong_dispersive_withPython\test_pulse_ringupdown_bin\foo_ch1_0004.bin'

#Waveform Markers
marker_file_path1 = datapath + 'markers\Waveform_test.mrk'

def main():    
    
    admin = proteus.loadDLL()
    slotId = proteus.getSlotId(admin)
    
    if not slotId:
        print("Invalid choice!")
    else:
        inst = admin.OpenInstrument(slotId) 
        if  not inst:
            print("Failed to Open instrument with slot-Id {0}".format(slotId))
            print("\n")
        else:
            instId = inst.InstrId
            ###########  CALL THE SCPI ###########
            TestScpiApi(inst) #     <<<-------   #
            ######################################
            rc = admin.CloseInstrument(instId)
            proteus.Validate(rc,__name__,inspect.currentframe().f_back.f_lineno)
    rc = admin.Close()
    proteus.Validate(rc,__name__,inspect.currentframe().f_back.f_lineno)

def TestScpiApi(inst):

    trig_lev = proteus.getSclkTrigLev(inst)

    # select intstrument to work
    proteus.SendScpi(inst, ":INST:ACTive 1")
    # get hw option
    proteus.SendScpi(inst, "*OPT?")
    # reset - must!
    proteus.SendScpi(inst, "*RST")
    # select channel
    proteus.SendScpi(inst, ":INST:CHAN 1")
    # set sampling DAC freq.
    proteus.SendScpi(inst, ":FREQ:RAST {0}".format(sclk))
    # Vpp for output = 1V
#    proteus.SendScpi(inst, ":SOUR:VOLT 1.5")
#    proteus.SendScpi(inst, ":SOUR:VOLT -0.03")
    # Arbitrary waveform generation, no trigger
    proteus.SendScpi(inst, ":INIT:CONT ON")
    # delete all segments in RAM
    proteus.SendScpi(inst, ":TRAC:DEL:ALL")
    # define user mode
    #proteus.SendScpi(inst, ":SOUR:FUNC:MODE ARB")
    proteus.SendScpi(inst, ":SOUR:FUNC:MODE TASK")
    # common segment defs
    proteus.SendScpi(inst, ":TRAC:DEF:TYPE NORM")

    # load segment 1
    proteus.loadSegment(inst, 1, seg_file_path1)
    proteus.SendBinScpi(inst, ":MARK:DATA:FNAM 0 , #", marker_file_path1)
    # load segment 2
    proteus.loadSegment(inst, 2, seg_file_path2)
    proteus.SendBinScpi(inst, ":MARK:DATA:FNAM 0 , #", marker_file_path1)
    # load segment 3
    proteus.loadSegment(inst, 3, seg_file_path3)
    proteus.SendBinScpi(inst, ":MARK:DATA:FNAM 0 , #", marker_file_path1)
    # load segment 4
    proteus.loadSegment(inst, 4, seg_file_path4)
    proteus.SendBinScpi(inst, ":MARK:DATA:FNAM 0 , #", marker_file_path1)
    
    # create tasks
    for i in range(4):
        proteus.SendScpi(inst, ":TASK:SEL {}".format(i+1))
        proteus.SendScpi(inst, ":TASK:DEF:TYPE SING")
        proteus.SendScpi(inst, ":TASK:DEF:LOOP 1")
        proteus.SendScpi(inst, ":TASK:DEF:SEGM {}".format(i+1))
        proteus.SendScpi(inst, ":TASK:DEF:IDLE:DC 32768")
        proteus.SendScpi(inst, ":TASK:DEF:ENAB TRIG1")
        proteus.SendScpi(inst, ":TASK:DEF:DEST NEXT")
        proteus.SendScpi(inst, ":TASK:DEF:NEXT1 {}".format((i+1)%4 + 1))
 
    # enable task mode

    proteus.SendScpi(inst, ":TRIG:SOUR:ENAB TRG1") # Set tigger enable signal to TRIG1 (CH specific)
    proteus.SendScpi(inst, ":TRIG:SEL EXT1") # Select trigger for programming (CH specific)
    proteus.SendScpi(inst, ":TRIG:LEV 0") # Set trigger level
    proteus.SendScpi(inst, ":TRIG:COUN 1") # Set number of waveform cycles (1) to generate (CH specific)
    proteus.SendScpi(inst, ":TRIG:IDLE DC") # Set output idle level to DC (CH specific)
    proteus.SendScpi(inst, ":TRIG:IDLE:LEV {0}".format(trig_lev)) # Set DC level in DAC value (CH specific)
    proteus.SendScpi(inst, ":TRIG:STAT ON") # Enable trigger state (CH specific)
    proteus.SendScpi(inst, ":INIT:CONT OFF") # Enable trigger mode (CH specific)
    
    proteus.SendScpi(inst, ":INST:CHAN 1")
    proteus.SendScpi(inst, ":VOLT 0.8")
    proteus.SendScpi(inst, ":VOLT:OFFS 0")
    
    
    # connect ouput
    proteus.SendScpi(inst, ":OUTP ON")
    
    # enble markers ch 1
    proteus.SendScpi(inst, ":MARK:SEL 1")
    proteus.SendScpi(inst, ":MARK:STAT ON")
    proteus.SendScpi(inst, ":MARK:SEL 2")
    proteus.SendScpi(inst, ":MARK:STAT ON")
       

if __name__ == '__main__': 
    main()
