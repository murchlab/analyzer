#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Feb  2 16:26:29 2020

@author: crow104

This script exists to 
"""
import numpy as np
import sys
sys.path.append(r"C:\Users\crow104\Documents\Python Scripts\sequence_generator")
from generator_nonHermian import *
import os
pi = np.pi
import matplotlib.pyplot as plt

def geom_ge_to_f_adia(ramsey_time=4000): #this is pulsed readout to ring up and ring down cavity dfor e state
    file_length = 18000
    num_steps = 101
    ringupdown_seq = Sequence(file_length, num_steps) #this creates something called rabi_seq that is an instance of a sequence class

    ## channels   
    pi_ge_time= 40
    pi2_ge_time=20
    ge_amp=1
    pi2_ef_time= 34
    ef_amp=1
    ssm_ge = .110
    ssm_ef= .208
    readout_amp = 1#0.1 # set this to 0.1 for the dispersive readout
    scale_factor= 0 # this is for another readout that is always on, to test dephasing
    
    pi_ge = Pulse(start=14900-ramsey_time, duration=-pi_ge_time, amplitude=ge_amp, ssm_freq=ssm_ge, phase=0) #pulse is also a class p is an instance
    ringupdown_seq.add_sweep(channel=1, sweep_name='none', initial_pulse=pi_ge)
    pi_ge.phase = 90
    ringupdown_seq.add_sweep(channel=2, sweep_name='none',initial_pulse=pi_ge)
    
    pi2_ef = Pulse(start=14930-ramsey_time, duration=-pi2_ef_time, amplitude=ef_amp, ssm_freq=ssm_ef, phase=90) #pulse is also a class p is an instance
    ringupdown_seq.add_sweep(channel=1, sweep_name='none',initial_pulse=pi2_ef)
    pi2_ef.phase = 0
    ringupdown_seq.add_sweep(channel=2, sweep_name='none',initial_pulse=pi2_ef)
    
     
    pi2_ge = Pulse(start=14960-ramsey_time, duration=-pi2_ge_time, amplitude=ge_amp, ssm_freq=ssm_ge, phase=0) #pulse is also a class p is an instance
    ringupdown_seq.add_sweep(channel=1, sweep_name='none',initial_pulse=pi2_ge)
    pi2_ge.phase = 90
    ringupdown_seq.add_sweep(channel=2, sweep_name='none',initial_pulse=pi2_ge)
    #p.phase = 90 #make the pulse phase 90 degrees to get the single sideband modulation
    #rabi_seq.add_sweep(channel=2, sweep_name='width', start=0, stop=-200,initial_pulse=p)
   
    #adiabatic sweep
    H_ge = Pulse(start=14960, duration=-ramsey_time, amplitude=0.125*ge_amp, ssm_freq=ssm_ge,phase=270,phase_ini=0,t_loop=ramsey_time,ff=1) #pulse is also a class p is an instance
    ringupdown_seq.add_sweep(channel=1, sweep_name='none',initial_pulse=H_ge)
    H_ge.phase = 0
    ringupdown_seq.add_sweep(channel=2,  sweep_name='none',initial_pulse=H_ge)
    
    H_ge = Pulse(start=14960, duration=-ramsey_time, amplitude=0.125*ge_amp, ssm_freq=ssm_ge,phase=180,phase_ini=pi/2,t_loop=ramsey_time,ff=1) #pulse is also a class p is an instance
    ringupdown_seq.add_sweep(channel=1, sweep_name='none',initial_pulse=H_ge)
    H_ge.phase = 270
    ringupdown_seq.add_sweep(channel=2,  sweep_name='none',initial_pulse=H_ge)
    #end
    
    pi32_ge = Pulse(start=15020, duration=-pi2_ge_time-pi_ge_time, amplitude=ge_amp, ssm_freq=ssm_ge, phase=0) #pulse is also a class p is an instance
    ringupdown_seq.add_sweep(channel=1, sweep_name='none',initial_pulse=pi32_ge)
    pi32_ge.phase = 90
    ringupdown_seq.add_sweep(channel=2, sweep_name='none',initial_pulse=pi32_ge)
    
    pi2_ef = Pulse(start=15050, duration=-pi2_ef_time, amplitude=ef_amp, ssm_freq=ssm_ef, phase=90) #pulse is also a class p is an instance
    ringupdown_seq.add_sweep(channel=1, sweep_name='phase',start=0,stop=360,initial_pulse=pi2_ef)
    pi2_ef.phase = 0
    ringupdown_seq.add_sweep(channel=2, sweep_name='phase',start=0,stop=360,initial_pulse=pi2_ef)
        
    pi_ge = Pulse(start=15080, duration=-pi_ge_time, amplitude=ge_amp, ssm_freq=ssm_ge, phase=0) #pulse is also a class p is an instance
    ringupdown_seq.add_sweep(channel=1, sweep_name='none', initial_pulse=pi_ge)
    pi_ge.phase = 90
    ringupdown_seq.add_sweep(channel=2, sweep_name='none',initial_pulse=pi_ge)
    #additional readout leakage
    
#    constant_pulse = Pulse(start = 5100-pre_time,duration = -5000, amplitude= readout_amp*scale_factor )
#    ringupdown_seq.add_sweep(channel=4, sweep_name='none',initial_pulse=constant_pulse)
    
    #main readout
    
    #pre_pulse = Pulse(start = 5100,duration = -pre_time, amplitude=pre3_amp )
    #ringupdown_seq.add_sweep(channel=3, sweep_name='none',initial_pulse=pre_pulse)
    #pre_pulse = Pulse(start = 5100,duration = -pre_time, amplitude=pre4_amp )
    #ringupdown_seq.add_sweep(channel=4, sweep_name='none',initial_pulse=pre_pulse)
    
    main_pulse = Pulse(start = 15100,duration = 1000, amplitude= readout_amp )
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
        #plt.imshow(channel1_ch[0:200,00:8000], aspect='auto', extent=[00,8000,200,0])
        #plt.show()
        
    ## write output
    #write_dir = r"C:\arbsequences\strong_dispersive_withPython\test_pulse_ringupdown"
   # ringupdown_seq.write_sequence(base_name='foo', file_path=write_dir, use_range_01=False,num_offset=0)

    write_dir = r"C:\arbsequences\strong_dispersive_withPython\adiabatic"
# 
    ringupdown_seq.write_sequence(base_name='foo', file_path=write_dir, use_range_01=False,num_offset=0)
     
    
def geom_ge_to_f(ramsey_time=400): #this is pulsed readout to ring up and ring down cavity dfor e state
    file_length = 18000
    num_steps = 101
    ringupdown_seq = Sequence(file_length, num_steps) #this creates something called rabi_seq that is an instance of a sequence class

    ## channels   
    pi_ge_time= 41
    pi2_ge_time=20
    ge_amp=1
    pi2_ef_time= 34
    ef_amp=1
    ssm_ge = .110
    ssm_ef= .208
    readout_amp = 1#0.1 # set this to 0.1 for the dispersive readout
    scale_factor= 0 # this is for another readout that is always on, to test dephasing
    
    pi_ge = Pulse(start=14900-ramsey_time, duration=-pi_ge_time, amplitude=ge_amp, ssm_freq=ssm_ge, phase=0) #pulse is also a class p is an instance
    ringupdown_seq.add_sweep(channel=1, sweep_name='none', initial_pulse=pi_ge)
    pi_ge.phase = 90
    ringupdown_seq.add_sweep(channel=2, sweep_name='none',initial_pulse=pi_ge)
    
    pi2_ef = Pulse(start=14930-ramsey_time, duration=-pi2_ef_time, amplitude=ef_amp, ssm_freq=ssm_ef, phase=90) #pulse is also a class p is an instance
    ringupdown_seq.add_sweep(channel=1, sweep_name='none',initial_pulse=pi2_ef)
    pi2_ef.phase = 0
    ringupdown_seq.add_sweep(channel=2, sweep_name='none',initial_pulse=pi2_ef)
    
     
    pi2_ge = Pulse(start=14960-ramsey_time, duration=-pi2_ge_time, amplitude=ge_amp, ssm_freq=ssm_ge, phase=0) #pulse is also a class p is an instance
    ringupdown_seq.add_sweep(channel=1, sweep_name='none',initial_pulse=pi2_ge)
    pi2_ge.phase = 90
    ringupdown_seq.add_sweep(channel=2, sweep_name='none',initial_pulse=pi2_ge)
    #p.phase = 90 #make the pulse phase 90 degrees to get the single sideband modulation
    #rabi_seq.add_sweep(channel=2, sweep_name='width', start=0, stop=-200,initial_pulse=p)
   
    #adiabatic sweep
    H_ge = Pulse(start=14960, duration=-ramsey_time, amplitude=0.125*ge_amp, ssm_freq=ssm_ge,phase=270) #pulse is also a class p is an instance
    ringupdown_seq.add_sweep(channel=1, sweep_name='none',initial_pulse=H_ge)
    H_ge.phase = 0
    ringupdown_seq.add_sweep(channel=2,  sweep_name='none',initial_pulse=H_ge)
    
    #end
    
    pi32_ge = Pulse(start=15020, duration=-pi2_ge_time-pi_ge_time, amplitude=ge_amp, ssm_freq=ssm_ge, phase=0) #pulse is also a class p is an instance
    ringupdown_seq.add_sweep(channel=1, sweep_name='none',initial_pulse=pi32_ge)
    pi32_ge.phase = 90
    ringupdown_seq.add_sweep(channel=2, sweep_name='none',initial_pulse=pi32_ge)
    
    pi2_ef = Pulse(start=15050, duration=-pi2_ef_time, amplitude=ef_amp, ssm_freq=ssm_ef, phase=90) #pulse is also a class p is an instance
    ringupdown_seq.add_sweep(channel=1, sweep_name='phase',start=0,stop=360,initial_pulse=pi2_ef)
    pi2_ef.phase = 0
    ringupdown_seq.add_sweep(channel=2, sweep_name='phase',start=0,stop=360,initial_pulse=pi2_ef)
        
    pi_ge = Pulse(start=15080, duration=-pi_ge_time, amplitude=ge_amp, ssm_freq=ssm_ge, phase=0) #pulse is also a class p is an instance
    ringupdown_seq.add_sweep(channel=1, sweep_name='none', initial_pulse=pi_ge)
    pi_ge.phase = 90
    ringupdown_seq.add_sweep(channel=2, sweep_name='none',initial_pulse=pi_ge)
    #additional readout leakage
    
#    constant_pulse = Pulse(start = 5100-pre_time,duration = -5000, amplitude= readout_amp*scale_factor )
#    ringupdown_seq.add_sweep(channel=4, sweep_name='none',initial_pulse=constant_pulse)
    
    #main readout
    
    #pre_pulse = Pulse(start = 5100,duration = -pre_time, amplitude=pre3_amp )
    #ringupdown_seq.add_sweep(channel=3, sweep_name='none',initial_pulse=pre_pulse)
    #pre_pulse = Pulse(start = 5100,duration = -pre_time, amplitude=pre4_amp )
    #ringupdown_seq.add_sweep(channel=4, sweep_name='none',initial_pulse=pre_pulse)
    
    main_pulse = Pulse(start = 15100,duration = 1000, amplitude= readout_amp )
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
        #plt.imshow(channel1_ch[0:200,00:8000], aspect='auto', extent=[00,8000,200,0])
        #plt.show()
        
    ## write output
    #write_dir = r"C:\arbsequences\strong_dispersive_withPython\test_pulse_ringupdown"
   # ringupdown_seq.write_sequence(base_name='foo', file_path=write_dir, use_range_01=False,num_offset=0)

    write_dir = r"C:\arbsequences\strong_dispersive_withPython\adiabatic"
# 
    ringupdown_seq.write_sequence(base_name='foo', file_path=write_dir, use_range_01=False,num_offset=0)
     
    
if __name__ == '__main__':
    pass
    geom_ge_to_f_adia()