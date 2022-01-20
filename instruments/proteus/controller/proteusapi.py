import os
import sys
import inspect
import clr
import ctypes
import numpy as np
import pathlib
from System import Array, Byte

self_path = str(pathlib.Path(__file__).parent.absolute())
if self_path not in sys.path:
    sys.path.append(self_path)
import daemon


winpath = os.environ['WINDIR'] + "\\System32\\"
clr.AddReference(winpath + R'TEPAdmin.dll')  
from TaborElec.Proteus.CLI.Admin import TaskInfo
from TaborElec.Proteus.CLI import *


maxScpiResponse = 65535

def loadDLL():

    # Load .NET DLL into memory
    # The R lets python interpret the string RAW so you can put in Windows paths easy
    #clr.AddReference(R'D:\Projects\Alexey\ProteusAwg\PyScpiTest\TEPAdmin.dll') 

    winpath = os.environ['WINDIR'] + "\\System32\\"
    clr.AddReference(winpath + R'TEPAdmin.dll')  
    from TaborElec.Proteus.CLI.Admin import CProteusAdmin
    from TaborElec.Proteus.CLI.Admin import IProteusInstrument
    return CProteusAdmin(OnLoggerEvent);


def OnLoggerEvent(sender,e):
    print(e.Message.Trim())
    if (e.Level <= LogLevel.Warning):
        print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
        print(e.Message.Trim())
        print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~")


logger = daemon.logger
class Proteus():
    
    def __init__(self):
        self.admin = None
        self.slotIds = np.array([3, 5], dtype=np.uint32)
        self.inst_list = []
        self.error = None
        # Initializing the proteus admin
        try:
            logger('Initializing proteus admin...')
            self.admin = loadDLL()
            self.admin.Open()
        except Exception as err:
            self.error = err
            logger(str(err))
        try:
            for slotId in self.slotIds:
                logger(f"Opening instrument slotId = {slotId}")
                inst = self.admin.OpenInstrument(slotId)
                if inst:
                    self.inst_list.append(inst)
                else:
                    raise Exception('Opening instrument failed')
            logger('Successful')
        except Exception as err:
            self.error = err
            logger(str(err))
            
    def close(self):
        try:
            for inst in self.inst_list:
                if inst:
                    instId = inst.InstrId
                    self.admin.CloseInstrument(instId)
            self.admin.Close()
        except Exception as err:
            self.error = err
            logger(str(err))
            
    def SendScpi(self, line, inst_index=0):
        try:
            logger(line)
            line += "\n"
            inBinDat = bytearray(line, "utf8")
            inBinDatSz = np.uint64(len(inBinDat))
            outBinDatSz = np.uint64([maxScpiResponse])
            outBinDat = bytearray(outBinDatSz[0])
            res = self.inst_list[inst_index].ProcessScpi(inBinDat, inBinDatSz, outBinDat, outBinDatSz)
            if (res.ErrCode != 0):
                logger("Error {0} ".format(res.ErrCode))
            if (len(res.RespStr)>0):
                logger("{0}".format(res.RespStr))
            return res
        except Exception as e: 
            logger(e)
            return res


    def readFiles(self, segName, inst_index=0):
        res = self.SendScpi(":SYST:INF:MODel?", inst_index=inst_index)
        if ".csv" in segName:
            fileType = "csv"
        if ".bin" in segName:
            fileType = "bin"
        if res.RespStr == "P9082M":
            # 8 bit device
            if fileType == "bin":
                bin_dat = np.fromfile(file=segName, dtype=np.uint8)
            else:
                bin_dat = np.loadtxt(fname=segName, dtype=np.uint8, delimiter=',')
            seg_len = len(bin_dat)
        else:
            # 16 bit device
            if fileType == "bin":
                bin_dat = np.fromfile(file=segName, dtype=np.uint8)
            else:   
                bin_dat = np.loadtxt(fname=segName, dtype=np.uint16, delimiter=',')
            bin_dat = bin_dat.view(dtype=np.uint8)
            seg_len = int(len(bin_dat) / 2)
            
        return(bin_dat, seg_len);
        
    def getSclkTrigLev(self, inst_index=0):
        res = self.SendScpi(":SYST:INF:MODel?", inst_index=inst_index)
        if res.RespStr == "P9082M":
            # 8 bit device
            trig_lev = 128
        else:
            # 16 bit device
            trig_lev = 32768
        return(trig_lev);
        
    def WriteBinaryData(self, prefix, bin_dat, inst_index=0):
        try:
            logger(prefix)
            inDatLength = len(bin_dat)
            inDatOffset = 0
            res = self.inst_list[inst_index].WriteBinaryData(prefix, bin_dat, inDatLength, inDatOffset)
            if (res.ErrCode != 0):
                logger("Error {0} ".format(res.ErrCode))
            else:
                if (len(res.RespStr)>0):
                    logger("{0}".format(res.RespStr))
            return res
        except Exception as e: 
            logger(e)
            return res
        
    def loadTaskTable(self, num_steps, dummy_header=True, inst_index=0):
        segNum_offset = 256
        
        dummy_offset = 0
        if dummy_header:
            dummy_offset = 1
        
        for ch_index in range(4):
            self.SendScpi(":INST:CHAN {}".format(ch_index+1), inst_index=inst_index)
            
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
            res = self.WriteBinaryData(':TASK:DATA 0,#', tableBinDat)
        if (res.ErrCode != 0):
            logger("Error {0} ".format(res.ErrCode))
        else:
            if (len(res.RespStr)>0):
                logger("{0}".format(res.RespStr))
        return res
        
    
    def loadSegData(self, segNum, seg_data, inst_index=0):
        bin_dat = seg_data.view(np.uint8)
        seg_len = int(len(bin_dat) / 2)
        
        self.SendScpi(":TRACe:DEF {0},{1}".format(segNum, seg_len), inst_index=inst_index)
        self.SendScpi(":TRACe:SEL {0}".format(segNum), inst_index=inst_index)  
        inDatLength = len(bin_dat)
        inDatOffset = 0
        res = self.inst_list[inst_index].WriteBinaryData(":TRAC:DATA 0,#", bin_dat, inDatLength, inDatOffset)
        
        if (res.ErrCode != 0):
            logger("Error {0} ".format(res.ErrCode))
        else:
            if (len(res.RespStr) > 0):
                logger("{0}".format(res.RespStr))
        return res


    def loadMarkData(self, mark_data, inst_index=0):
        
        inDatLength = len(mark_data)
        inDatOffset = 0
        res = self.inst_list[inst_index].WriteBinaryData(":MARK:DATA 0,#", mark_data, inDatLength, inDatOffset)
        
        if (res.ErrCode != 0):
            logger("Error {0} ".format(res.ErrCode))
        else:
            if (len(res.RespStr) > 0):
                logger("{0}".format(res.RespStr))
        return res
        
    def start_from(self, step_index=0, inst_index=0):
        # step_index starts from 0
        # dummy_header has to be enabled
        for ch_index in range(4):
            self.SendScpi(":INST:CHAN {}".format(ch_index+1), inst_index=inst_index)
            self.SendScpi(":TASK:SEL {}".format(1), inst_index=inst_index)
            self.SendScpi(":TASK:DEF:NEXT1 {}".format(2 + step_index), inst_index=inst_index)
#        next1_list = []
#        for ch_index in range(4):
#            self.SendScpi(":INST:CHAN {}".format(ch_index+1), inst_index=inst_index)
#            self.SendScpi(":TASK:SEL {}".format(1), inst_index=inst_index)
#            res = self.SendScpi(":TASK:DEF:NEXT1?", inst_index=inst_index)
#            next1_list.append(res.RespStr)
#        rep = f"NEXT1 = {next1_list}"
#        logger(rep)
#        return rep
            return "no error"
    
        
    def loadSegment(self, segNum, seg_file_path, inst_index=0):
        bin_dat, seg_len = self.readFiles(seg_file_path, inst_index=inst_index) 
        self.SendScpi(":TRACe:DEF {0},{1}".format(segNum, seg_len), inst_index=inst_index)
        self.SendScpi(":TRACe:SEL {0}".format(segNum), inst_index=inst_index)  
        inDatLength = len(bin_dat)
        inDatOffset = 0
        res = self.inst_list[inst_index].WriteBinaryData(":TRAC:DATA 0,#", bin_dat, inDatLength, inDatOffset)
        
        if (res.ErrCode != 0):
            logger("Error {0} ".format(res.ErrCode))
        else:
            if (len(res.RespStr) > 0):
                logger("{0}".format(res.RespStr))
                
#    def loadSegment(inst, segNum, seg_file_path):
#        bin_dat, seg_len = readFiles(inst, seg_file_path) 
#        SendScpi(inst, ":TRACe:DEF {0},{1}".format(segNum, seg_len))
#        SendScpi(inst, ":TRACe:SEL {0}".format(segNum))  
#        inDatLength = len(bin_dat)
#        inDatOffset = 0
#        res = inst.WriteBinaryData(":TRAC:DATA 0,#", bin_dat, inDatLength, inDatOffset)
#        
#        if (res.ErrCode != 0):
#            print("Error {0} ".format(res.ErrCode))
#        else:
#            if (len(res.RespStr) > 0):
#                print("{0}".format(res.RespStr))
                
    def SendBinScpi(self, prefix, path, inst_index=0):
        try:
            logger(prefix)
            inBinDat = bytearray(path, "utf8")
            inBinDatSz = np.uint64(len(inBinDat))
            DummyParam = np.uint64(0)
            res = self.inst_list[inst_index].WriteBinaryData(prefix,inBinDat,inBinDatSz,DummyParam)
            if (res.ErrCode != 0):
                logger("Error {0} ".format(res.ErrCode))
            else:
                if (len(res.RespStr)>0):
                    logger("{0}".format(res.RespStr))
            return res
        except Exception as e: 
            logger(e)
            return res
        
    def ReadFromAsciiFile(self, fname, inst_index=0):
        try:
            # Open the text file using a stream reader.
            StreamReader = open(fname, 'r')
            # Read the stream to a string, and write the string to the console.
            for line in StreamReader.readlines():
                logger(line)
                inBinDat = bytearray(line, "utf8")
                inBinDatSz = np.uint64(len(inBinDat))
                outBinDatSz = np.uint64([maxScpiResponse])
                outBinDat = bytearray(outBinDatSz[0])
                res = self.inst_list[inst_index].ProcessScpi(inBinDat, inBinDatSz, outBinDat, outBinDatSz)
                if (res.ErrCode != 0):
                    logger("Error {0} ", format(res.ErrCode))
                else:
                    if (len(res.RespStr)>0):
                        logger("{0}", format(res.RespStr))
            StreamReader.close()
        except Exception as e: 
            logger(e)
    
            
    def list_inst(self):
        return str(self.inst_list)
    
    def handler(self, arg_dict):
        fun_dict = {
            'list_inst': lambda: self.list_inst(),
            'SendScpi': lambda: self.SendScpi(arg_dict['line'], arg_dict['inst_index']),
            'loadSegment': lambda: self.loadSegment(arg_dict['segNum'], arg_dict['seg_file_path'], arg_dict['inst_index']),
            'SendBinScpi': lambda: self.SendBinScpi(arg_dict['prefix'], arg_dict['path'], arg_dict['inst_index']),
            'loadTaskTable': lambda: self.loadTaskTable(arg_dict['num_steps'], arg_dict['dummy_header'], arg_dict['inst_index']),
            'loadSegData': lambda: self.loadSegData(arg_dict['segNum'], arg_dict['seg_data'], arg_dict['inst_index']),
            'loadMarkData': lambda: self.loadMarkData(arg_dict['mark_data'], arg_dict['inst_index']),
            'start_from': lambda: self.start_from(arg_dict['step_index'], arg_dict['inst_index'])
            }
        try:
            res = fun_dict[arg_dict['command']]()
        except Exception as err:
            return str(err)
        return str(res)

      
def list_inst():
    command = b'proteus '
    command += daemon.data_pack({'command': 'list_inst'})
    rep = daemon.request(command)
    return rep


def SendScpi(line, inst_index=0):
    command = b'proteus '
    command += daemon.data_pack({'command': 'SendScpi', 'line': line, 'inst_index': inst_index})
    rep = daemon.request(command)
    return rep


def loadSegment(segNum, seg_file_path, inst_index=0):
    command = b'proteus '
    arg_dict = {
            'command': 'loadSegment',
            'segNum': segNum,
            'seg_file_path': seg_file_path,
            'inst_index': inst_index
    }
    command += daemon.data_pack(arg_dict)
    rep = daemon.request(command)
    return rep


def SendBinScpi(prefix, path, inst_index=0):
    command = b'proteus '
    arg_dict = {
            'command': 'SendBinScpi',
            'prefix': prefix,
            'path': path,
            'inst_index': inst_index
    }
    command += daemon.data_pack(arg_dict)
    rep = daemon.request(command)
    return rep

def loadTaskTable(num_steps, dummy_header=True, inst_index=0):
    command = b'proteus '
    arg_dict = {
            'command': 'loadTaskTable',
            'num_steps': num_steps,
            'dummy_header': dummy_header,
            'inst_index': inst_index
    }
    command += daemon.data_pack(arg_dict)
    rep = daemon.request(command)
    return rep

def loadSegData(segNum, seg_data, inst_index=0):
    command = b'proteus '
    arg_dict = {
            'command': 'loadSegData',
            'segNum': segNum,
            'seg_data': seg_data,
            'inst_index': inst_index
    }
    command += daemon.data_pack(arg_dict)
    rep = daemon.request(command)
    return rep

def loadMarkData(mark_data, inst_index=0):
    command = b'proteus '
    arg_dict = {
            'command': 'loadMarkData',
            'mark_data': mark_data,
            'inst_index': inst_index
    }
    command += daemon.data_pack(arg_dict)
    rep = daemon.request(command)
    return rep

def start_from(step_index=0, inst_index=0):
    command = b'proteus '
    arg_dict = {
            'command': 'start_from',
            'step_index': step_index,
            'inst_index': inst_index
    }
    command += daemon.data_pack(arg_dict)
    rep = daemon.request(command)
    return rep
