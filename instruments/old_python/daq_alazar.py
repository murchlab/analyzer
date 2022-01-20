# -*- coding: utf-8 -*-
"""
Created on Sat Jan 25 12:43:51 2020

@author: P. M. Harrington, 25 January 2020
"""

from __future__ import division
import ctypes
import numpy as np
import os
import time
import matplotlib.pyplot as plt
import atsapi as ats
import srs_dg535
from Nop_class import Nop

def get_alazar_parameters(daq_params=None):
    alazar_params = Nop()
    
    #
    alazar_params.post_trigger_samples = 2048
    alazar_params.samples_per_sec = 1e9
    alazar_params.buffer_count = 64 # 64 for ATS9870, found in SDK manual
    
    #
    alazar_params.num_total_records = daq_params.num_patterns * daq_params.num_records_per_pattern    
    alazar_params.records_per_buffer = min(1024, alazar_params.num_total_records)    
    alazar_params.samples_per_buffer = alazar_params.post_trigger_samples * alazar_params.records_per_buffer    
    alazar_params.buffers_per_acquisition = int(np.ceil(alazar_params.num_total_records/alazar_params.records_per_buffer))
    
    print("Patterns: {}".format(daq_params.num_patterns))
    print("Records per pattern: {}".format(daq_params.num_records_per_pattern))
    print("Buffers per acquistion: {}".format(alazar_params.buffers_per_acquisition))
    print("DAQ samples per pattern: {}".format(alazar_params.post_trigger_samples))
    
    return alazar_params

def rotate_iq(angle_deg=0., rec=[None, None]):
    rec_rotated = [None, None]
    
    ch_cmplx = rec[0] + 1j*rec[1]
    ch_cmplx_rot = abs(ch_cmplx)*np.exp(1j*np.angle(ch_cmplx))*np.exp(1j*np.pi*angle_deg/180)
    rec_rotated[0] = np.real(ch_cmplx_rot)
    rec_rotated[1] = np.imag(ch_cmplx_rot)
    
    return rec_rotated

# Configures a board for acquisition
def configure_board(alazar_params, board):
    # TODO: Select clock parameters as required to generate this
    # sample rate
    #
    # For example: if samples_per_sec is 100e6 (100 MS/s), then you can
    # either:
    #  - select clock source INTERNAL_CLOCK and sample rate
    #    SAMPLE_RATE_100MSPS
    #  - or select clock source FAST_EXTERNAL_CLOCK, sample rate
    #    SAMPLE_RATE_USER_DEF, and connect a 100MHz signal to the
    #    EXT CLK BNC connector
    
    samples_per_sec = alazar_params.samples_per_sec #1000000000.0
    board.setCaptureClock(ats.INTERNAL_CLOCK,
                          ats.SAMPLE_RATE_250MSPS,
                          ats.CLOCK_EDGE_RISING,
                          0)
    
    # TODO: Select channel A input parameters as required.
    board.inputControlEx(ats.CHANNEL_A,
                         ats.DC_COUPLING,
                         ats.INPUT_RANGE_PM_100_MV,
                         ats.IMPEDANCE_50_OHM)
    
    # TODO: Select channel A bandwidth limit as required.
    board.setBWLimit(ats.CHANNEL_A, 0)
    
    
    # TODO: Select channel B input parameters as required.
    board.inputControlEx(ats.CHANNEL_B,
                         ats.DC_COUPLING,
                         ats.INPUT_RANGE_PM_100_MV,
                         ats.IMPEDANCE_50_OHM)
    
    # TODO: Select channel B bandwidth limit as required.
    board.setBWLimit(ats.CHANNEL_B, 0)
    
    # TODO: Select trigger inputs and levels as required.
    board.setTriggerOperation(ats.TRIG_ENGINE_OP_J,
                              ats.TRIG_ENGINE_J,
                              ats.TRIG_EXTERNAL,
                              ats.TRIGGER_SLOPE_POSITIVE,
                              135,
                              ats.TRIG_ENGINE_K,
                              ats.TRIG_DISABLE,
                              ats.TRIGGER_SLOPE_POSITIVE,
                              128)

#    # TODO: Select external trigger parameters as required.
#    board.setExternalTrigger(ats.DC_COUPLING,
#                             ats.ETR_1V)

    # TODO: Set trigger delay as required.
    triggerDelay_sec = 0
    triggerDelay_samples = int(triggerDelay_sec * samples_per_sec + 0.5)
    board.setTriggerDelay(triggerDelay_samples)

    # TODO: Set trigger timeout as required.
    #
    # NOTE: The board will wait for a for this amount of time for a
    # trigger event.  If a trigger event does not arrive, then the
    # board will automatically trigger. Set the trigger timeout value
    # to 0 to force the board to wait forever for a trigger event.
    #
    # IMPORTANT: The trigger timeout value should be set to zero after
    # appropriate trigger parameters have been determined, otherwise
    # the board may trigger if the timeout interval expires before a
    # hardware trigger event arrives.
    triggerTimeout_sec = 0
    triggerTimeout_clocks = int(triggerTimeout_sec / 10e-6 + 0.5)
    board.setTriggerTimeOut(triggerTimeout_clocks)

    # Configure AUX I/O connector as required
    board.configureAuxIO(ats.AUX_OUT_TRIGGER,
                         0)
    
def acquire_data(daq_params, alazar_params, board):
    rec_avg_all = []
    rec_readout = []
    
    # No pre-trigger samples in NPT mode
    preTriggerSamples = 0

    # TODO: Select the number of samples per record.
    post_trigger_samples = alazar_params.post_trigger_samples

    # TODO: Select the number0 of records per DMA buffer.
    records_per_buffer = alazar_params.records_per_buffer #2**10 # up to 2**14

    # TODO: Select the number of buffers per acquisition.
    buffers_per_acquisition = alazar_params.buffers_per_acquisition
    
    records_per_acquisition = records_per_buffer * buffers_per_acquisition
    
    # TODO: Select the active channels.
    channels = ats.CHANNEL_A | ats.CHANNEL_B
    channelCount = 0
    for c in ats.channels:
        channelCount += (c & channels == c)

    # TODO: Should data be saved to file?
    saveData = False
    dataFile = None
    if saveData:
        dataFile = open(os.path.join(os.path.dirname(__file__),
                                     "data.bin"), 'wb')

    # Compute the number of bytes per record and per buffer 
    memorySize_samples, bitsPerSample = board.getChannelInfo()
    bytesPerSample = (bitsPerSample.value + 7) // 8
    samplesPerRecord = preTriggerSamples + post_trigger_samples
    bytesPerRecord = bytesPerSample * samplesPerRecord
    bytesPerBuffer = bytesPerRecord * records_per_buffer * channelCount

    # TODO: Select number of DMA buffers to allocate
    buffer_count = alazar_params.buffer_count

    # Allocate DMA buffers

    sample_type = ctypes.c_uint8
    if bytesPerSample > 1:
        sample_type = ctypes.c_uint16

    buffers = []
    for i in range(buffer_count):
        buffers.append(ats.DMABuffer(board.handle, sample_type, bytesPerBuffer))
    
    # Set the record size
    board.setRecordSize(preTriggerSamples, post_trigger_samples)

    # Configure the board to make an NPT AutoDMA acquisition
    board.beforeAsyncRead(channels,
                          -preTriggerSamples,
                          samplesPerRecord,
                          records_per_buffer,
                          records_per_acquisition,
                          ats.ADMA_EXTERNAL_STARTCAPTURE | ats.ADMA_NPT)

    index_avg_start = daq_params.readout_start
    index_avg_end = daq_params.readout_start + daq_params.readout_duration - 1

    index_ch = [None]*2
    index_ch[0] = np.arange(0,post_trigger_samples*records_per_buffer) # channel A
    index_ch[1] = post_trigger_samples*records_per_buffer + np.arange(0,post_trigger_samples*records_per_buffer) # channel B
    
    rec_all_raw = [None]*2
    rec_avg_all = [None]*2
    rec_readout = [[]]*2

    # Post DMA buffers to board
    for buffer in buffers:
        board.postAsyncBuffer(buffer.addr, buffer.size_bytes)

    start = time.clock() # Keep track of when acquisition started
    
    # start SRS DG535 triggers
    srs_dg535.set_trigger_level('high')
    
    try:
        board.startCapture() # Start the acquisition
        print("Capturing %d buffers. Press <enter> to abort" %
              buffers_per_acquisition)
        buffersCompleted = 0
        bytesTransferred = 0
        while (buffersCompleted < buffers_per_acquisition and not
               ats.enter_pressed()):
            # Wait for the buffer at the head of the list of available
            # buffers to be filled by the board.
            buffer = buffers[buffersCompleted % len(buffers)]
            board.waitAsyncBufferComplete(buffer.addr, timeout_ms=5000)
            buffersCompleted += 1
            bytesTransferred += buffer.size_bytes

            #
            for idx, idx_ch in enumerate(index_ch):
                rec_all_raw[idx] = np.reshape(buffer.buffer[idx_ch], (records_per_buffer, post_trigger_samples))
                
            #
            rec_all = rotate_iq(daq_params.iq_angle_deg, rec_all_raw)
            
            #
            for idx in [0, 1]:
                rec_avg_all[idx] = np.mean(rec_all[idx], axis=0) # is this just the avg of the last loop?
                rec_readout[idx] = np.concatenate((rec_readout[idx], np.mean(rec_all[idx][:,index_avg_start:index_avg_end], axis=1)))
            
            # NOTE:
            #
            # While you are processing this buffer, the board is already
            # filling the next available buffer(s).
            #
            # You MUST finish processing this buffer and post it back to the
            # board before the board fills all of its available DMA buffers
            # and on-board memory.
            #
            # Samples are arranged in the buffer as follows:
            # S0A, S0B, ..., S1A, S1B, ...
            # with SXY the sample number X of channel Y.
            #
            # Sample code are stored as 8-bit values.
            #
            # Sample codes are unsigned by default. As a result:
            # - 0x00 represents a negative full scale input signal.
            # - 0x80 represents a ~0V signal.
            # - 0xFF represents a positive full scale input signal.
            # Optionaly save data to file
            if dataFile:
                buffer.buffer.tofile(dataFile)

            # Add the buffer to the end of the list of available buffers.
            board.postAsyncBuffer(buffer.addr, buffer.size_bytes)
    finally:
        board.abortAsyncRead()
        
    # stop SRS DG535 triggers
    srs_dg535.set_trigger_level('low')
    
    # Compute the total transfer time, and display performance information.
    transferTime_sec = time.clock() - start
    print("Capture completed in %f sec" % transferTime_sec)
    buffersPerSec = 0
    bytesPerSec = 0
    recordsPerSec = 0
    if transferTime_sec > 0:
        buffersPerSec = buffersCompleted / transferTime_sec
        bytesPerSec = bytesTransferred / transferTime_sec
        recordsPerSec = records_per_buffer * buffersCompleted / transferTime_sec
    print("Captured %d buffers (%f buffers per sec)" %
          (buffersCompleted, buffersPerSec))
    print("Captured %d records (%f records per sec)" %
          (records_per_buffer * buffersCompleted, recordsPerSec))
    print("Transferred %d bytes (%f bytes per sec)" %
          (bytesTransferred, bytesPerSec))
    
    return (rec_avg_all, rec_readout)
    
if __name__ == "__main__":
    pass