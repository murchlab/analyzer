# -*- coding: utf-8 -*-
"""
Created on Wed Jun 19 12:11:40 2019

@author: crow104
"""
import numpy as np
from main import *
import os
pi = np.pi
import matplotlib.pyplot as plt

def ramsey_ssb(ssb,num_offset, dir_name):
    # included as short-cut for using iPython    
    file_length= 8000 # becomes global FILELENGTH
    num_steps = 51# becomes global NUMSTEPS
    #WAVE,MARK1, MARK2 = initialize(file_length, num_steps)
    ALL_CHANNELS = initialize_wx(file_length, num_steps)
    # ALL_CHANNELS is 4-array for Ch 1,2. Each elem is a tuple of (channel, M1,M2)
    #       each tuple elem. is a seq_len X num_samples matrix.
    pi = np.pi
    
    ## channels
    print("generating Ramsey with SSB {}".format(ssb))
    swept_pi2 = Pulse(start=5955-2*23, duration=23,  amplitude=0.5, ssm_freq=ssb, phase=0)
    fixed_pi2 = Pulse(start=5955-23, duration=23,  amplitude=0.5, ssm_freq=ssb, phase=0)
    add_sweep(ALL_CHANNELS, channel=1, sweep_name='none', initial_pulse= fixed_pi2)
    add_sweep(ALL_CHANNELS, channel=1, sweep_name='start', start=0 , stop= -1000, initial_pulse=swept_pi2 )
    #ch2
    swept_pi2.phase = 98.0
    fixed_pi2.phase = 98.0
    add_sweep(ALL_CHANNELS, channel=1, sweep_name='none', initial_pulse= fixed_pi2)
    add_sweep(ALL_CHANNELS, channel=1, sweep_name='start', start=0 , stop= -1000, initial_pulse=swept_pi2 )
    #ch3
    weak_amp = 0.1
    weak = Pulse(start=6000,duration=1000,amplitude=weak_amp)
    readout = Pulse(start=6000,duration=1000,amplitude=1)
    add_sweep(ALL_CHANNELS, channel=3, sweep_name='none',initial_pulse=readout)

    ## markers
    channel1_channel = ALL_CHANNELS[0][0] # dim 0: channel 1; dim 1: [ch,m1,m2]
    ch1_m1 = create_gate(channel1_channel)
    ALL_CHANNELS[0][1] = ch1_m1
    
    alazar_trigger = Pulse(start=2000, duration=1000, amplitude=1)
    add_sweep(ALL_CHANNELS, channel=3, marker=1, sweep_name='none', initial_pulse=alazar_trigger )

    ## view    
    if False:
        channel1_ch = ALL_CHANNELS[0][0]
        channel3_ch = ALL_CHANNELS[2][0]
        plt.imshow(channel1_ch[:,5000:6250], aspect='auto')
        plt.show(False)
        
    write_sequence(ALL_CHANNELS, file_path=dir_name, use_range_01=False, num_offset=num_offset)
##END ramsey_ssb
    
    
def theta_to_amplitude(theta_rads,pi_time=23, pi_amp=1):
    return pi_amp *theta_rads/pi
##END theta_to_amp
    

def EUR_exp():
    file_length= 8000 # becomes global FILELENGTH
    num_steps = 51# becomes global NUMSTEPS
    #WAVE,MARK1, MARK2 = initialize(file_length, num_steps)
    
    ssb = 0.200
    pi_time = 23
    buffer = 5 # time in ns
    weak_duration = 100
    weak_amp = 0.15
    stark_shift_phase_rad = 10 /180*pi
    
    num_theta_rhos = 11
    
    for i,theta_rho in enumerate(np.linspace(0.0*pi, 1.0*pi, num_theta_rhos)):
          i=1
          ## define pulses that we'll need
          readout_start = 6000
          readout = Pulse(duration=1000, start=readout_start, amplitude=1)
          #add_sweep(ALL_CHANNELS, channel=3, sweep_name='none',initial_pulse=readout)
          
          theta_f = 0.5*pi
          prep_f_amp = theta_to_amplitude(theta_f)
          f_time = readout_start -buffer -pi_time
          prep_f = Pulse(duration=pi_time, start=f_time, amplitude=prep_f_amp , ssm_freq=ssb, phase=stark_shift_phase_rad)
          
          theta_a = 0.25*pi
          prep_a_amp = theta_to_amplitude(theta_a)
          unprep_a_time = f_time -buffer -pi_time
          unprep_a = Pulse(duration=pi_time, start=unprep_a_time, amplitude=-1*prep_a_amp , ssm_freq=ssb, phase=stark_shift_phase_rad)
          
          # weak measurement
          weak_start_time = unprep_a_time -buffer -weak_duration
          weak_a = Pulse(duration=weak_duration, start=weak_start_time, amplitude=weak_amp)
          
          prep_a_time = weak_start_time -buffer -pi_time
          prep_a = Pulse(duration=pi_time, start=prep_a_time, amplitude=prep_a_amp , ssm_freq=ssb, phase=0)
          
          theta_rho = 0.5*pi
          prep_rho_amp = theta_to_amplitude(theta_rho)
          prep_rho_time = prep_a_time -buffer -pi_time
          prep_rho = Pulse(duration=pi_time, start=prep_rho_time, amplitude=prep_rho_amp , ssm_freq=ssb, phase=0)
          
          alazar_trigger = Pulse(start=2000, duration=1000, amplitude=1)
          
          ## and now build the sequence in sequential order:
          eur = Sequence(file_length, num_steps)
          eur.insert_bothChannels(prep_rho,i)
          eur.insert_bothChannels(prep_a,i)
          eur.insert_waveform(3,weak_a,i)
          eur.insert_bothChannels(unprep_a,i)
          eur.insert_bothChannels(prep_f,i)
          eur.insert_waveform(3,readout,i)
          print(i)
    #END step loop
    # insert CH1/2 gate for all steps in sequence.
#    channel1_channel = eur.all_data[0][0] # dim 0: channel 1; dim 1: choose [ch,m1,m2]
#    ch1_m1 = create_gate(channel1_channel)
#    eur.all_data[0][1] = ch1_m1
        
    return eur
    ## once CH1/2 waveform is built add the gate to CH1/2 M1
##END EUR_exp
    
def test_pulse():
    num_steps = 51
    eur= EUR_exp()
    
    ch1 = eur.all_data[0][0]
    mn,mx =5700,6000
    xs = np.arange(mn,mx,1)
    #plt.imshow(ch1,aspect='auto')
    plt.plot(xs,ch1[1][mn:mx])
    plt.ylim([-1,1])
    plt.show(False)
    return 0;
        
    ## create dir
    dir_name = r"C:\Arb Sequences\EUR_sequences\mixerOrthogonality_98deg\piTime_23ns\python_seq"
    #dir_name = os.path.join(dir_name,"ramsey_1us_sweep_SSB_-198,202")
    dir_name = os.path.join(dir_name,"tmp")
    if not os.path.exists(dir_name):
        os.makedirs(dir_name)
    
    ssb_list = np.linspace(0.2, 0.202, 5)
    print(ssb_list)
    for i,ssb in enumerate(ssb_list):
        ramsey_ssb(ssb, i*num_steps, dir_name)
        #break
##END main
        
        
if __name__ == '__main__':
    eur = test_pulse()