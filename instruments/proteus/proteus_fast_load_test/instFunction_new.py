import os
# import sys
import inspect
import clr
# import ctypes
import numpy as np

maxScpiResponse = 65535


def readFiles(inst, segName):
    res = SendScpi(inst, ":SYST:INF:MODel?")
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

    return (bin_dat, seg_len)


def getSclkTrigLev(inst):
    res = SendScpi(inst, ":SYST:INF:MODel?")
    if res.RespStr == "P9082M":
        # 8 bit device
        trig_lev = 128
    else:
        # 16 bit device
        trig_lev = 32768
    return (trig_lev)


def loadSegment(inst, segNum, seg_file_path, query_err=False):
    bin_dat, seg_len = readFiles(inst, seg_file_path)
    print(bin_dat)
    SendScpi(inst, ":TRACe:DEF {0},{1}".format(segNum, seg_len))
    SendScpi(inst, ":TRACe:SEL {0}".format(segNum))
    inDatLength = len(bin_dat)
    inDatOffset = 0
    res = inst.WriteBinaryData(
        ":TRAC:DATA 0,#", bin_dat, inDatLength, inDatOffset)

    if (res.ErrCode != 0):
        print("Error {0} ".format(res.ErrCode))

    if len(res.RespStr) > 0:
        print("{0}".format(res.RespStr))

    if query_err:
        err = inst.SendScpi(':SYST:ERR?')
        if not err.RespStr.startswith('0'):
            print(err.RespStr)
            err = inst.SendScpi('*CLS')


def loadSegmentData(inst, segNum, segData, query_err=False):
    SendScpi(inst, ":TRACe:DEF {0},{1}".format(segNum, len(segData)))
    SendScpi(inst, ":TRACe:SEL {0}".format(segNum))
    inDatLength = len(segData)
    inDatOffset = 0
    res = inst.WriteBinaryData(
        ":TRAC:DATA 0,#", segData, inDatLength, inDatOffset)

    if (res.ErrCode != 0):
        print("Error {0} ".format(res.ErrCode))

    if len(res.RespStr) > 0:
        print("{0}".format(res.RespStr))

    if query_err:
        err = inst.SendScpi(':SYST:ERR?')
        if not err.RespStr.startswith('0'):
            print(err.RespStr)
            err = inst.SendScpi('*CLS')


def loadDLL():

    # Load .NET DLL into memory
    # The R lets python interpret the string RAW
    # So you can put in Windows paths easy
    # clr.AddReference(R'D:\Projects\Alexey\ProteusAwg\PyScpiTest\TEPAdmin.dll')

    winpath = os.environ['WINDIR'] + "\\System32\\"
    clr.AddReference(winpath + R'TEPAdmin.dll')
    from TaborElec.Proteus.CLI.Admin import CProteusAdmin
    from TaborElec.Proteus.CLI.Admin import IProteusInstrument
    return CProteusAdmin(OnLoggerEvent)


def SendBinScpi(inst, prefix, path, query_err=False):
    try:
        print(prefix)
        inBinDat = bytearray(path, "utf8")
        inBinDatSz = np.uint64(len(inBinDat))
        DummyParam = np.uint64(0)
        res = inst.WriteBinaryData(prefix, inBinDat, inBinDatSz, DummyParam)
        if (res.ErrCode != 0):
            print("Error {0} ".format(res.ErrCode))

        if len(res.RespStr) > 0:
            print("{0}".format(res.RespStr))
        if query_err:
            err = inst.SendScpi(':SYST:ERR?')
            if not err.RespStr.startswith('0'):
                print(err.RespStr)
                err = inst.SendScpi('*CLS')

        print("\n")
        return res
    except Exception as e:
        print(e)
        return res


def SendScpi(inst, line, query_err=False):
    try:
        print(line)
        line = line + "\n"
        inBinDat = bytearray(line, "utf8")
        inBinDatSz = np.uint64(len(inBinDat))
        outBinDatSz = np.uint64([maxScpiResponse])
        outBinDat = bytearray(outBinDatSz)
        res = inst.ProcessScpi(inBinDat, inBinDatSz, outBinDat, outBinDatSz)
        print("made it 2 three")
        if (res.ErrCode != 0):
            print("Error {0} ".format(res.ErrCode))
        if len(res.RespStr) > 0:
            print("{0}".format(res.RespStr))
        if query_err:
            err = inst.SendScpi(':SYST:ERR?')
            if not err.RespStr.startswith('0'):
                print(err.RespStr)
                err = inst.SendScpi('*CLS')
        # print("\n")
        return res
    except Exception as e:
        print("error", e)
        res = None
        return res


def OnLoggerEvent(sender, e):
    print(e.Message.Trim())
    if (e.Level <= LogLevel.Warning):
        print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
        print(e.Message.Trim())
        print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~")


def Validate(rc, condExpr, funcName="", lineNumber=0):
    _ = condExpr

    # cond = (rc == 0)

    if rc != 0:
        errMsg = "Assertion \"{0}\" Failed at line {1} of {2}."
        errMsg = errMsg.format(rc, lineNumber, funcName)
        raise Exception(errMsg)


def ReadFromAsciiFile(inst, fname):
    try:
        # Open the text file using a stream reader.
        StreamReader = open(fname, 'r')
        # Read the stream to a string, and write the string to the console.
        for line in StreamReader.readlines():
            print(line)
            inBinDat = bytearray(line, "utf8")
            inBinDatSz = np.uint64(len(inBinDat))
            outBinDatSz = np.uint64([maxScpiResponse])
            outBinDat = bytearray(outBinDatSz[0])
            res = inst.ProcessScpi(inBinDat, inBinDatSz, outBinDat, outBinDatSz)
            if (res.ErrCode != 0):
                print("Error {0} ", format(res.ErrCode))
            else:
                if (len(res.RespStr)>0):
                    print("{0}", format(res.RespStr))
            print("\n")
        StreamReader.close()
    except Exception as e:
        print(e)


def getSlotId(admin):
    try:
        rc = admin.Open()
        Validate(rc, __name__, inspect.currentframe().f_back.f_lineno)

        slotIds = admin.GetSlotIds()
        n = 0
        for i in range(0, slotIds.Length, 1):
            slotId = slotIds[i]
            slotInfo = admin.GetSlotInfo(slotId)
            if slotInfo:
                if not slotInfo.IsDummySlot:
                    n = n + 1
                    print("{0}. Slot-ID {1} [chassis {2}, slot {3}], IsDummy={4}, IsInUse={5}, IDN=\'{6}\'".
                        format(i + 1,slotId,slotInfo.ChassisIndex,slotInfo.SlotNumber,
                               'Yes' if slotInfo.IsDummySlot !=0 else 'No',
                               'Yes' if slotInfo.IsSlotInUse !=0 else 'No',
                               slotInfo.GetIdnStr()))
                else:
                    dummy = 1
                    # print("{0}. Slot-ID {1} - Failed to acquire Slot Info".
                    # .format(i + 1,slotId))

        if n == 1:
            sel = slotIds[0]
        else:
            sel = input("Please select slot-Id:")
        slotId = np.uint32(sel)
    except Exception as e:
        print(e)
    return slotId
