# -*- coding: utf-8 -*-
"""
Created on Tue Oct  1 09:50:09 2019

@author: JMonroe
"""
import numpy as np
from generator import *
import os
pi = np.pi
import matplotlib.pyplot as plt

''' # original rabi before Sequence class existed
def rabi_ssb(ssb, file_path):
    file_length = 18000
    num_steps = 101
    
    # full_seq is 4-array for Ch 1,2. Each elem is a tuple of (channel, M1,M2)
    #       each tuple elem. is a seq_len X num_samples matrix.
    full_seq = initialize_wx(file_length,num_steps)
    
    ## channels
    p = Pulse(start=15995, duration=0,  amplitude=0.5, ssm_freq=ssb, phase=0)
    add_sweep(full_seq, channel=1, sweep_name='width', start=0 , stop= 200, initial_pulse=p )
    p.phase = 90.0
    add_sweep(full_seq, channel=2, sweep_name='width', start=0 , stop= 200, initial_pulse=p )
    #readout = Pulse(start=6000,duration=1000,amplitude=1)
    #add_sweep(full_seq, channel=3, sweep_name='none',initial_pulse=readout)
    
    ## markers
    channel1_channel = full_seq[0][0] # dim 0: channel 1; dim 1: [ch,m1,m2]
    ch1_m1 = create_gate(channel1_channel)
    full_seq[0][1] = ch1_m1
    
    readout = Pulse(start=16000,duration=1000,amplitude=1)
    add_sweep(full_seq, channel=1,marker=2,sweep_name='none')
    
    alazar_trigger = Pulse(start=10000, duration=500, amplitude=1)
    add_sweep(full_seq, channel=3, marker=1, sweep_name='none', initial_pulse=alazar_trigger )
    
    ## output
    if True:
        channel1_ch = full_seq[0][0]
        channel3_ch = full_seq[2][0]
        plt.imshow(channel1_ch[:,15000:16250], aspect='auto', extent=[15000,16250,100,0])
        #plt.show(False)
    #write_sequence(full_seq, file_path=file_path, use_range_01=False, num_offset=0)
##END rabi_ssb
'''

def rabi(foo):
    file_length = 8000
    num_steps = 101
    ssb = 0.110
    rabi_seq = Sequence(file_length, num_steps) #this creates something called rabi_seq that is an instance of a sequence class

    ## channels    
    p = Pulse(start=5000, duration=0, amplitude=0.5, ssm_freq=ssb, phase=0) #pulse is also a class p is an instance
    rabi_seq.add_sweep(channel=1, sweep_name='width', start=0, stop=-200,initial_pulse=p)
    p.phase = 90 #make the pulse phase 90 degrees to get the single sideband modulation
    rabi_seq.add_sweep(channel=2, sweep_name='width', start=0, stop=-200,initial_pulse=p)

    ## markers
    readout = Pulse(start=6000,duration=1000,amplitude=1)
    rabi_seq.add_sweep(channel=1,marker=2,sweep_name='none', initial_pulse=readout) #sweep type 'none' copies pulse to every pattern of the sequence
    
    alazar_trigger = Pulse(start=1000, duration=500, amplitude=1)
    rabi_seq.add_sweep(channel=3, marker=1, sweep_name='none', initial_pulse=alazar_trigger )
    
    # gates currently need to be created more manually
    #channel1_ch = rabi_seq.channel_list[0][0] #[channel name -1][0:channel, 1:marker 1, 2:marker 2]
    #ch1_m1 = create_gate(channel1_ch)
    #rabi_seq.channel_list[0][1] = ch1_m1

    ## view output
    channel1_ch = rabi_seq.channel_list[0][0] #[channel name -1][0:channel, 1:marker 1, 2:marker 2]
    channel1_m1 = rabi_seq.channel_list[0][1] # same as channel 2 m1
    channel1_m2 = rabi_seq.channel_list[0][2]
    channel2_ch = rabi_seq.channel_list[1][0]
    
    if False: ## change to True to view the sequence 
        plt.imshow(channel2_ch[0:100,4800:5100], aspect='auto', extent=[4800,5100,100,0])
        plt.show()
    if False: ## change to True to write sequence to disk (CSV format)
        write_dir = r"C:\arbsequences\100119_JTM\python_seq\rabi"
        if not os.path.exists(write_dir): 
            os.mkdir(write_dir)
            print("created dir:",write_dir)
        rabi_seq.write_sequence(base_name='foo', file_path=write_dir, use_range_01=False,num_offset=0)
        
    return [channel1_ch, channel2_ch, channel1_m1, channel1_m2]
##END rabi

    
def ramsey():#num_offset, dir_name):
    file_length= 8000 
    num_steps = 101
    ramsey_seq= Sequence(file_length, num_steps)
   
    ssb = 0.15 
    pi2_time = 23
    ## channels
    swept_pi2 = Pulse(start=5955-2*pi2_time, duration=pi2_time,  amplitude=0.5, ssm_freq=ssb, phase=0)
    fixed_pi2 = Pulse(start=5955-pi2_time, duration=pi2_time,  amplitude=0.5, ssm_freq=ssb, phase=0)
    ramsey_seq.add_sweep(channel=1, sweep_name='none', initial_pulse= fixed_pi2)
    ramsey_seq.add_sweep(channel=1, sweep_name='start', start=0 , stop= -1000, initial_pulse=swept_pi2 )
    #ch2
    swept_pi2.phase = 98.0
    fixed_pi2.phase = 98.0
    ramsey_seq.add_sweep(channel=1, sweep_name='none', initial_pulse= fixed_pi2)
    ramsey_seq.add_sweep(channel=1, sweep_name='start', start=0 , stop= -1000, initial_pulse=swept_pi2 )
    #ch3
    weak_amp = 0.1
    weak = Pulse(start=6000,duration=1000,amplitude=weak_amp)
    readout = Pulse(start=6000,duration=1000,amplitude=1)
    ramsey_seq.add_sweep(channel=3, sweep_name='none',initial_pulse=readout)

    ## markers
    readout = Pulse(start=6000,duration=1000,amplitude=1)
    ramsey_seq.add_sweep(channel=1,marker=2,sweep_name='none')

    alazar_trigger = Pulse(start=2000, duration=1000, amplitude=1)
    ramsey_seq.add_sweep(channel=3, marker=1, sweep_name='none', initial_pulse=alazar_trigger )

    ## view    
    if True:
        channel1_ch = ramsey_seq.channel_list[0][0]
        channel3_ch = ramsey_seq.channel_list[2][0]
        for i in range(4):
            plt.plot(channel1_ch[i, 5800:6100]+i)
        #plt.imshow(channel1_ch[0:10,5800:6100], aspect='auto', extent=[4500,5500,100,0])
        plt.show()
        
    #write_sequence(ALL_CHANNELS, file_path=dir_name, use_range_01=False, num_offset=num_offset)
##END ramsey_ssb

    
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
    #rabi()
    #ramsey()
    pass
