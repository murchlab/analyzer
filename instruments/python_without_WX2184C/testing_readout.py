# -*- coding: utf-8 -*-
"""
Created on Fri Jul 10 11:27:24 2020

@author: Crow108
"""
import numpy as np
import matplotlib.pyplot as plt
import dg535_control
import sys, time

import pyvisa
resourceManager = pyvisa.ResourceManager()

import daq_programs
plt.style.use('ggplot')

def fun(num_reps=None):
    num_pats = 1
    if not num_reps:
        num_reps = 1000
    num_reps = int(num_reps)
    ([avg_rec_chA, avg_rec_chB],[readout_chA,readout_chB]) = daq_programs.run_daq2(num_pats, num_reps, verbose=False)
    
    sample_rate = 250E6
    ns_per_sample = 1e-9 *sample_rate
    ts_us = np.linspace(0, avg_rec_chA.size/sample_rate, avg_rec_chA.size) *1E6
    
    avg_start = 700
    avg_end = avg_start + 400
    
    A_avg  = np.round( np.mean(avg_rec_chA[avg_start:avg_end]), 2)
    B_avg  = np.round( np.mean(avg_rec_chB[avg_start:avg_end]), 2) # variance is ~0.6 for 1k reps
    A_null = np.round( np.mean(avg_rec_chA[0:avg_start//2]),    2)
    B_null = np.round( np.mean(avg_rec_chB[0:avg_start//2]),    2)
    A_std  = np.round( np.std( avg_rec_chA[avg_start:avg_end]), 4)
    B_std  = np.round( np.std( avg_rec_chA[avg_start:avg_end]), 4)
    A_null_std = np.round( np.std(avg_rec_chA[0:avg_start//2]), 4)
    B_null_std = np.round( np.std(avg_rec_chB[0:avg_start//2]), 4)
    print(f"Averages A:{A_avg}, B:{B_avg}")
    print(f"Null regions: A:{A_null} +/-{A_null_std}, B:{B_null} +/- {B_null_std}")
    print(f"A std: {A_std}, B std: {B_std}" )
    
    # min max gives amplitude of sine resulting from heterodyne interference.
    #print("A min/max {0:.2f}, {1:.2f}".format( np.min(avg_rec_chA[100:]-A_avg), np.max(avg_rec_chA[100:]-A_avg)))
    #print("B min/max {0:.2f}, {1:.2f}".format( np.min(avg_rec_chB[100:]-B_avg), np.max(avg_rec_chB[100:]-B_avg)))
               
    ## Find pulse starts
#    avg_window = np.ones(100)/100. # a 1/M window to average M points via convolution.
#    rolling_avg_A = np.convolve(avg_rec_chA-127, avg_window)
#    rolling_avg_B = np.convolve(avg_rec_chB-127, avg_window)
#    derivative = np.gradient( rolling_avg_A )
#    print("Pulse start/ width [ns]", ns_per_sample  *np.argmax(derivative), ns_per_sample *(np.argmin(derivative)-np.argmax(derivative)) )
    
#    print( "Rolled avg", np.round( np.mean(rolling_avg_A[avg_start:avg_end-100]), 2) )
#    print( "Rolled std",  np.round( np.std(rolling_avg_A[avg_start:avg_end-100]), 4) )
    
    ## make plots
#    plt.plot( ts_us, rolling_avg_A[:-99], label='avg A')
#    plt.plot( ts_us, rolling_avg_B[:-99], label='avg B')
#    plt.xlabel("Time [us]")
    plt.plot(avg_rec_chA, label='A' )
    plt.plot(avg_rec_chB , label='B')
    plt.xlabel("Sample num")
    
    plt.legend()
    
    plt.ylabel("Digitizer Value")
    
    return avg_rec_chA
##END fun
    
def fun2(num_reps=None):
    num_pats = 1
    if not num_reps:
        num_reps = 1000
    num_reps = int(num_reps)
    ([avg_rec_chA, avg_rec_chB],[readout_chA,readout_chB], temp) = daq_programs.run_daq3(num_pats, num_reps, verbose=False)
    
    sample_rate = 250E6
    ns_per_sample = 1e-9 *sample_rate
    ts_us = np.linspace(0, avg_rec_chA.size/sample_rate, avg_rec_chA.size) *1E6
    
    avg_start = 700
    avg_end = avg_start + 400
    
    A_avg  = np.round( np.mean(avg_rec_chA[avg_start:avg_end]), 2)
    B_avg  = np.round( np.mean(avg_rec_chB[avg_start:avg_end]), 2) # variance is ~0.6 for 1k reps
    A_null = np.round( np.mean(avg_rec_chA[0:avg_start//2]),    2)
    B_null = np.round( np.mean(avg_rec_chB[0:avg_start//2]),    2)
    A_std  = np.round( np.std( avg_rec_chA[avg_start:avg_end]), 4)
    B_std  = np.round( np.std( avg_rec_chA[avg_start:avg_end]), 4)
    A_null_std = np.round( np.std(avg_rec_chA[0:avg_start//2]), 4)
    B_null_std = np.round( np.std(avg_rec_chB[0:avg_start//2]), 4)
    print(f"Averages A:{A_avg}, B:{B_avg}")
    print(f"Null regions: A:{A_null} +/-{A_null_std}, B:{B_null} +/- {B_null_std}")
    print(f"A std: {A_std}, B std: {B_std}" )
    
    # min max gives amplitude of sine resulting from heterodyne interference.
    #print("A min/max {0:.2f}, {1:.2f}".format( np.min(avg_rec_chA[100:]-A_avg), np.max(avg_rec_chA[100:]-A_avg)))
    #print("B min/max {0:.2f}, {1:.2f}".format( np.min(avg_rec_chB[100:]-B_avg), np.max(avg_rec_chB[100:]-B_avg)))
               
    ## Find pulse starts
#    avg_window = np.ones(100)/100. # a 1/M window to average M points via convolution.
#    rolling_avg_A = np.convolve(avg_rec_chA-127, avg_window)
#    rolling_avg_B = np.convolve(avg_rec_chB-127, avg_window)
#    derivative = np.gradient( rolling_avg_A )
#    print("Pulse start/ width [ns]", ns_per_sample  *np.argmax(derivative), ns_per_sample *(np.argmin(derivative)-np.argmax(derivative)) )
    
#    print( "Rolled avg", np.round( np.mean(rolling_avg_A[avg_start:avg_end-100]), 2) )
#    print( "Rolled std",  np.round( np.std(rolling_avg_A[avg_start:avg_end-100]), 4) )
    
    ## make plots
#    plt.plot( ts_us, rolling_avg_A[:-99], label='avg A')
#    plt.plot( ts_us, rolling_avg_B[:-99], label='avg B')
#    plt.xlabel("Time [us]")
    print(avg_rec_chA.shape)
    plt.plot(avg_rec_chA, label='A' )
    plt.plot(avg_rec_chB , label='B')
    plt.show()
    plt.xlabel("Sample num")
    array_A = temp[0][0]
    array_B = temp[0][1]
    array_avg = np.mean(array_A[np.arange(0, 999, 21)], axis=0)
    print(array_A)
    print(array_B)
    plt.imshow(array_A)
    plt.show()
    plt.plot(array_avg)
    plt.legend()
    
    
    plt.ylabel("Digitizer Value")
    
    return avg_rec_chA
    

def runn(num_reps=200, num_pats=51):
    
    readout_by_pat_A = np.zeros((num_pats,num_reps))
    readout_by_pat_B = np.zeros((num_pats,num_reps))
    
    for i in range(num_pats):
        sys.stdout.write('.'); sys.stdout.flush();
        # collect data 1 pattern at a time.
        dg535_control.rabi_seq(i, num_pats, cavity_amp_V=0.7) # 0.7 based on 08/27/20 calibration
        ([avg_rec_chA, avg_rec_chB],[readout_chA,readout_chB],[recs_vs_patA,recs_vs_patB])\
        = daq_programs.run_daq2(1, num_reps, verbose=False)        
        readout_by_pat_A[i] = readout_chA
        readout_by_pat_B[i] = readout_chB
      
    
#    plt.plot( np.mean(readout_by_pat_A, axis=1) )
    plt.plot( np.mean(readout_by_pat_B, axis=1) )
        
#    plt.figure()
#    plt.plot(readout_by_pat_A.flatten(), readout_by_pat_B.flatten(), ',')
#    plot_range = 70
#    plt.xlim(-plot_range,plot_range)
#    plt.ylim(-plot_range,plot_range)
    
    plt.show()
    
    return readout_by_pat_A, readout_by_pat_B
    

def sweep_chAmp():
    num_pats = 11
    num_reps = 100

    num_amps = 4
    amp_min = 0.3
    amp_max = 3.3
    amp_list = np.linspace(amp_min, amp_max, num_amps)
    print("amps: ", amp_list)
    
    
    readouts_chA_chAmp_patNum_repNum = np.zeros((num_amps,num_pats,num_reps))
    readouts_chB_chAmp_patNum_repNum = np.zeros((num_amps,num_pats,num_reps))
    
    for amp_index, amp in enumerate(amp_list):
        print("\nCurrent readout amp: ", amp)
        for step_idx in range(num_pats):
            #print(f"Taking data for pat # {step_idx+1}/{num_pats}\r", end='\r')
            sys.stdout.write('.'); sys.stdout.flush();
            dg535_control.rabi_seq(step_idx, num_pats, cavity_amp_V=amp)
            try:
                ([avg_rec_chA, avg_rec_chB],[readout_chA,readout_chB]) = daq_programs.run_daq2(1, num_reps, verbose=False)
            except Exception as exc:
                if "ApiPllNotLocked" in exc.args[0]:
                    print("Alazar PLL not locked, napping")
                    time.sleep(1)
                    ([avg_rec_chA, avg_rec_chB],[readout_chA,readout_chB], [recs_vs_patA,recs_vs_patB])\
                    = daq_programs.run_daq2(1, num_reps, verbose=False)
           
            readouts_chA_chAmp_patNum_repNum[amp_index,step_idx] = readout_chA
            readouts_chB_chAmp_patNum_repNum[amp_index,step_idx] = readout_chB
        
    #
    for amp_index, amp in enumerate(amp_list):
        avgI = np.mean( readouts_chA_chAmp_patNum_repNum[amp_index], axis=1 )
        avgQ = np.mean( readouts_chB_chAmp_patNum_repNum[amp_index], axis=1 )
        plt.plot(avgI,'-', label=f"{np.round(amp,1)}, I")
        plt.plot(avgQ,'--', label=f"{np.round(amp,1)}, Q")

    plt.legend()
    plt.show()
    
    return (readouts_chA_chAmp_patNum_repNum, readouts_chB_chAmp_patNum_repNum)
##END sweep_chAmp
    

def chevron_plot():
    bnc_address = 'USB0::0x03EB::0xAFFF::421-4385A0002-0619::INSTR'
    bnc_session = resourceManager.open_resource(bnc_address)
    
    num_pats = 51
    num_reps = 200
    
    freq_min_GHz = 3.630 
    freq_max_GHz = 3.645
    num_freq = 31
    freq_list = np.linspace(freq_min_GHz, freq_max_GHz, num_freq)
    
    chevron_I = np.zeros((num_freq, num_pats))
    chevron_Q = np.zeros((num_freq, num_pats))
    
    for freq_index, bnc_freq in enumerate(freq_list):
        ## sweep the BNC frequency
        #print(f"Sweeping at frequency {bnc_freq} GHz")
        #bnc_session.write(f"SOUR: Freq {bnc_freq*1E9}")
        
        ## measure average I and Q
        rec_avg_all, rec_readout, rec_avg_vs_pats =  daq_programs.run_daq2(num_pats, num_reps, False)
        I_vs_pats = rec_avg_vs_pats[0]
        Q_vs_pats = rec_avg_vs_pats[1]
        '''
        
        '''
        
        ## store data for plot
        chevron_I[freq_index] = I_vs_pats
        chevron_Q[freq_index] = Q_vs_pats
    
    print("updated")
    plt.imshow( chevron_Q )
    plt.show()
    
    return chevron_I, chevron_Q

def T1_constant(): #this is pulsed readout to ring up and ring down cavity dfor e state
    file_length = 8000
    num_steps = 101
    ringupdown_seq = Sequence(file_length, num_steps) #this creates something called rabi_seq that is an instance of a sequence class

    ## channels   
    sweep_time = 500
    pi_pulse_time = 40
    ssm_ge = .110
    pre3_amp = 0.8
    pre_time = 30
    pre4_amp = 0.1
    readout_amp = 1
    scale_factor=0.01
    
    the_pulse = Pulse(start=5050, duration=-pi_pulse_time, amplitude=1, ssm_freq=ssm_ge, phase=0) #pulse is also a class p is an instance
    ringupdown_seq.add_sweep(channel=1, sweep_name='start', start=0, stop=-sweep_time,initial_pulse=the_pulse)
    the_pulse.phase = 90
    ringupdown_seq.add_sweep(channel=2,  sweep_name='start', start=0, stop=-sweep_time,initial_pulse=the_pulse)
    #p.phase = 90 #make the pulse phase 90 degrees to get the single sideband modulation
    #rabi_seq.add_sweep(channel=2, sweep_name='width', start=0, stop=-200,initial_pulse=p)

    
    #main readout
    
    #pre_pulse = Pulse(start = 15100,duration = -pre_time, amplitude=pre3_amp )
    #ringupdown_seq.add_sweep(channel=3, sweep_name='none',initial_pulse=pre_pulse)
    #pre_pulse = Pulse(start = 15100,duration = -pre_time, amplitude=pre4_amp )
    #ringupdown_seq.add_sweep(channel=4, sweep_name='none',initial_pulse=pre_pulse)
    constant_pulse = Pulse(start = 5050,duration = -5000, amplitude= readout_amp*scale_factor )
    ringupdown_seq.add_sweep(channel=4, sweep_name='none',initial_pulse=constant_pulse)
    
    main_pulse = Pulse(start = 5100,duration = 1000, amplitude= readout_amp )
    ringupdown_seq.add_sweep(channel=1,marker=2, sweep_name='none',initial_pulse=main_pulse)
    
    
    ## markers
   
    alazar_trigger = Pulse(start=file_length-7000, duration=500, amplitude=1)
    ringupdown_seq.add_sweep(channel=3, marker=1, sweep_name='none', initial_pulse=alazar_trigger )
    
    ##create the gate for ch1 an ch2
    channel1_channel = ringupdown_seq.channel_list[0][0] # dim 0: channel 1; dim 1: [ch,m1,m2]
    channel2_channel = ringupdown_seq.channel_list[1][0] # dim 0: channel 1; dim 1: [ch,m1,m2]
    both_ch1_ch2 = channel1_channel**2 + channel2_channel**2
    qubit_gate = create_gate(both_ch1_ch2)
    ringupdown_seq.channel_list[0][1] = qubit_gate

    ## view output
    if True:
        channel1_ch = ringupdown_seq.channel_list[0][0] #[channel name -1][0:channel, 1:marker 1, 2:marker 2]
        channel2_ch = ringupdown_seq.channel_list[1][0]
        channel3_ch = ringupdown_seq.channel_list[2][0]
        channel4_ch = ringupdown_seq.channel_list[3][0]
        plt.imshow(channel1_ch[0:100,4800:6000], aspect='auto', extent=[4800,5100,100,0])
        plt.show()
        
    ## write output
   # write_dir = r"C:\arbsequences\strong_dispersive_withPython\test_pulse_ringupdown"
   # ringupdown_seq.write_sequence(base_name='foo', file_path=write_dir, use_range_01=False,num_offset=0)
    write_dir = r"C:\arbsequences\strong_dispersive_withPython\test_pulse_ringupdown_bin"
    ringupdown_seq.write_sequence(base_name='foo', file_path=write_dir, use_range_01=False,num_offset=0, write_binary=True)
    ringupdown_seq.load_sequence('128.252.134.4', base_name='foo', file_path=write_dir, num_offset=0)
##END geom

if __name__ == '__main__':
    pass
    #xs = fun()
    #rs1,rs2 = run()