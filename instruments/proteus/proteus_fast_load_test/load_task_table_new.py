import os
import clr
import sys
import numpy as np

# import inspect
# import ctypes


def ScpiCommands(
        inst,
        sampling_clock,
        channel_list,
        num_steps,
        base_name,
        file_path,
        num_offset):

    res = inst.SendScpi('*IDN?')
    print(res.RespStr)

    res = inst.SendScpi('*OPT?')
    print(res.RespStr)

    # reset - must!
    instFunction.SendScpi(inst, "*CLS")
    instFunction.SendScpi(inst, "*RST")

    query_syst_err = True

    for ch_index, _ in enumerate(channel_list):
        instFunction.SendScpi(
            inst, ":INST:CHAN {0}".format(ch_index + 1), query_syst_err)
        # set sampling DAC freq.
        instFunction.SendScpi(
            inst, ":FREQ:RAST {0}".format(sampling_clock), query_syst_err)
        # delete all segments in RAM
        instFunction.SendScpi(inst, ":TRAC:DEL:ALL", query_syst_err)
        # enable task mode
        instFunction.SendScpi(inst, ":SOUR:FUNC:MODE ARB", query_syst_err)
        # common segment defs
        instFunction.SendScpi(inst, ":TRAC:DEF:TYPE NORM", query_syst_err)
        instFunction.SendScpi(inst, ":TRIG:STAT OFF", query_syst_err)

    for ch_index, _ in enumerate(channel_list):
        ch_name = "ch" + str(ch_index+1)
        print("loading "+ch_name)
        # select channel
        instFunction.SendScpi(
            inst, ":INST:CHAN {0}".format(ch_index + 1), query_syst_err)

        if(ch_index % 2 != 0):
            step_index_start = 1
        else:
            step_index_start = num_steps + 1

        # load segments & markers
        for step_index in range(num_steps):
            instFunction.SendScpi(
                inst, ":INST:CHAN {0}".format(ch_index + 1), query_syst_err)

            # download wave-file
            file_name = file_path + base_name + "_" + ch_name
            file_name += "_{:04d}.bin".format(step_index + num_offset)
            instFunction.loadSegment(
                inst, step_index_start + step_index, file_name, query_syst_err)

            # download markers file:
            mark_file_name = file_path + base_name + "_" + ch_name
            mark_file_name += "_{:04d}.mrk".format(step_index+num_offset)
            instFunction.SendBinScpi(
                inst, ":MARK:DATA:FNAM 0, #", mark_file_name, query_syst_err)

        taskInfo = TaskInfo()
        tasks_bindat = np.empty(
            TaskInfo.SerializedSize * num_steps, dtype=np.uint8)

        for step_index in range(num_steps):
            # instFunction.SendScpi(inst, ":TASK:SEL {}".format(step_index+1))

            # instFunction.SendScpi(inst, ":TASK:DEF:TYPE SING")
            taskInfo.TaskState = TaskStateType.Single

            # instFunction.SendScpi(inst, ":TASK:DEF:LOOP 1")
            taskInfo.TaskLoopCount = np.uint32(1)

            # instFunction.SendScpi(inst, ":TASK:DEF:SEQ 1")
            taskInfo.SeqLoopCount = np.uint32(1)

            seg_num = np.uint32(step_index + step_index_start)
            # instFunction.SendScpi(inst, ":TASK:DEF:SEGM {0}".format(seg_num))
            taskInfo.SegNb = np.uint32(seg_num)

            # instFunction.SendScpi(inst, ":TASK:DEF:IDLE FIRS")
            taskInfo.TaskIdleWaveform = IdleWaveform.FirstPoint

            # instFunction.SendScpi(inst, ":TASK:DEF:IDLE:DC 32768")
            taskInfo.TaskDcVal = np.uint16(32768)

            # instFunction.SendScpi(inst, ":TASK:DEF:ENAB TRIG1")
            taskInfo.TaskEnableSignal = EnableSignalType.ExternTrig1

            # instFunction.SendScpi(inst, ":TASK:DEF:ABOR NONE")
            # taskInfo.TaskAbortSignal = AbortSignalType.None

            # Use np.int32(0) instead of AbortSignalType.None
            # (Python recognizes 'None' as reserved word)
            taskInfo.TaskAbortSignal = np.int32(0)

            # instFunction.SendScpi(inst, ":TASK:DEF:JUMP EVEN")
            taskInfo.TaskAbortJump = ReactMode.Eventually

            # instFunction.SendScpi(inst, ":TASK:DEF:DEST NEXT")
            taskInfo.TaskCondJumpDest = TaskCondJump.Next1Task

            next_task = np.uint32((step_index + 1) % num_steps + 1)
            # instFunction.SendScpi(inst, ":TASK:DEF:NEXT1 " + next_task)
            taskInfo.NextTask1 = next_task

            # instFunction.SendScpi(inst, ":TASK:DEF:NEXT2 0")
            taskInfo.NextTask1 = np.uint32(0)

            buff_offset = np.int32(step_index * TaskInfo.SerializedSize)
            taskInfo.Serialize(tasks_bindat, buff_offset)

        res = inst.WriteBinaryData(':TASK:DATA 0,#', tasks_bindat)
        if res.ErrCode != 0:
            err_str = "Download task-table failed with error: "
            err_str += '{0} {1}'.format(res.ErrCode, res.RespStr)
            raise RuntimeError(err_str)

        if query_syst_err:
            res = inst.SendScpi(':SYST:ERR?')
            if not res.RespStr.startswith('0'):
                print(res.RespStr)
                res = inst.SendScpi('*CLS')

    for ch_index, _ in enumerate(channel_list):
        instFunction.SendScpi(
            inst, ":INST:CHAN {}".format(ch_index + 1), query_syst_err)

        # Set trigger enable signal to TRIG1 (CH specific):
        instFunction.SendScpi(inst, ":TRIG:SOUR:ENAB TRG1", query_syst_err)

        # Select trigger for programming (CH specific):
        instFunction.SendScpi(inst, ":TRIG:SEL EXT1", query_syst_err)

        # Set trigger level:
        instFunction.SendScpi(inst, ":TRIG:LEV 0", query_syst_err)

        # Set number of waveform cycles (1) to generate (CH specific):
        instFunction.SendScpi(inst, ":TRIG:COUN 1", query_syst_err)

        # Set output idle level to DC (CH specific):
        instFunction.SendScpi(inst, ":TRIG:IDLE DC", query_syst_err)

        # Set DC level in DAC value (CH specific):
        instFunction.SendScpi(
            inst, ":TRIG:IDLE:LEV {0}".format(0), query_syst_err)

        # Enable trigger state (CH specific):
        instFunction.SendScpi(inst, ":TRIG:STAT ON", query_syst_err)

        # Enable trigger mode (CH specific):
        instFunction.SendScpi(inst, ":INIT:CONT OFF", query_syst_err)

    for ch_index, _ in enumerate(channel_list):
        instFunction.SendScpi(inst, ":TASK:SEL 1", query_syst_err)

    for ch_index, _ in enumerate(channel_list):
        # Enable trigger state (CH specific):
        instFunction.SendScpi(inst, ":TRIG:STAT ON", query_syst_err)

    amp = [1, 1, 1, 1]
    offset = [0, 0, 0, 0]
    for ch_index, _ in enumerate(channel_list):
        # Setting up amplitudes and offsets
        instFunction.SendScpi(
            inst, ":INST:CHAN {}".format(ch_index + 1), query_syst_err)
        instFunction.SendScpi(
            inst, ":VOLT {}".format(amp[ch_index]), query_syst_err)
        instFunction.SendScpi(
            inst, ":VOLT:OFFS {}".format(offset[ch_index]), query_syst_err)
        instFunction.SendScpi(inst, ":SOUR:FUNC:MODE TASK", query_syst_err)

        # connect output
        instFunction.SendScpi(inst, ":OUTP ON", query_syst_err)

        # enable markers
        instFunction.SendScpi(inst, ":MARK:MASK 65535", query_syst_err)
        instFunction.SendScpi(inst, ":MARK:SEL 1", query_syst_err)
        instFunction.SendScpi(inst, ":MARK:STAT ON", query_syst_err)
        instFunction.SendScpi(inst, ":MARK:SEL 2", query_syst_err)
        instFunction.SendScpi(inst, ":MARK:STAT ON", query_syst_err)


def load_sequence_old(
        inst,
        base_name='foo\\foo',
        file_path=os.getcwd(),
        num_offset=0):
    '''
    DESCRIPTION: loads multi channel INPUT:
    OUTPUT:
    TODO:
    '''
    sampling_clock = 1e9
    # file_length = self.sequence_length
    num_steps = 100
    channel_list = [1, 2]

    if not file_path.endswith("\\"):
        file_path += "\\"

    print("loading {}".format(file_path))

    ScpiCommands(
        inst,
        sampling_clock,
        channel_list,
        num_steps,
        base_name,
        file_path,
        num_offset)


if __name__ == '__main__':

    # Select appropriate slot
    slotId = np.uint32(3)

    sys.path.append(os.getcwd())

    import instFunction_new as instFunction

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
    inst = None

    try:
        admin = CProteusAdmin()
        if not admin:
            raise RuntimeError("CProteusAdmin() failed")

        if not admin.IsOpen():
            rc = admin.Open()
            if 0 != rc:
                raise RuntimeError("admin.Open() = {0}".format(rc))

        inst = admin.OpenInstrument(slotId)
        if not inst:
            errStr = "admin.OpenInstrument(slotId={0}) failed".format(slotId)
            raise RuntimeError(errStr)

        load_sequence_old(inst, file_path=files_dir)

        rc = admin.CloseInstrument(slotId)
        if 0 != rc:
            errStr = "admin.CloseInstrument(slotId={0})={1}".format(slotId, rc)
            raise RuntimeError(errStr)

    finally:
        if admin is not None:
            admin.Close()
