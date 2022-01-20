import numpy as np
from generator import *
import os
pi = np.pi
import matplotlib.pyplot as plt


def rabi():
    file_length = 8000
    num_steps = 101
    geophase_seq = Sequence(file_length, num_steps) #this creates something called rabi_seq that is an instance of a sequence class

    ## channels    
    pi_ge_time = 64
    pi2_ef_time  = 16
    pi2_ef_amp = 0.5
    pi2_ge_time = 32
    ssm_ge = .110
    ssm_ef = 0.188
    
    #this is the first pi pulse in the sequence
    pi_ge = Pulse(start=5000, duration=-64, amplitude=1, ssm_freq=ssm_ge, phase=0) #pulse is also a class p is an instance
    geophase_seq.add_sweep(channel=1, sweep_name='none',initial_pulse=pi_ge)
    pi_ge.phase = 90
    geophase_seq.add_sweep(channel=2, sweep_name='none',initial_pulse=pi_ge)
    #p.phase = 90 #make the pulse phase 90 degrees to get the single sideband modulation
    #rabi_seq.add_sweep(channel=2, sweep_name='width', start=0, stop=-200,initial_pulse=p)
    
    pi2_ef = Pulse(start=5000+pi2_ef_time, duration=-pi2_ef_time, amplitude=0.5, ssm_freq=ssm_ge, phase=90)
    geophase_seq.add_sweep(channel=1, sweep_name='none',initial_pulse=pi2_ef)
    pi2_ef.phase = 0
    geophase_seq.add_sweep(channel=2, sweep_name='none',initial_pulse=pi2_ef)
    
    pi2_ge = Pulse(start=5000+pi2_ef_time+pi2_ge_time, duration=-pi2_ge_time, amplitude=1, ssm_freq=ssm_ge, phase=0) #pulse is also a class p is an instance
    geophase_seq.add_sweep(channel=1, sweep_name='none',initial_pulse=pi2_ge)
    pi2_ge.phase = 90
    geophase_seq.add_sweep(channel=2, sweep_name='none',initial_pulse=pi2_ge)
    
    pi2_ge = Pulse(start=5000+pi2_ef_time+2*pi2_ge_time, duration=-pi2_ge_time, amplitude=1, ssm_freq=ssm_ge, phase=0) #pulse is also a class p is an instance
    geophase_seq.add_sweep(channel=1, sweep_name='phase',start=0, stop=360,initial_pulse=pi2_ge)
    pi2_ge.phase = 90
    geophase_seq.add_sweep(channel=2, sweep_name='phase', start=0, stop=360,initial_pulse=pi2_ge)
    
    pi2_ef.start=8220
    geophase_seq.add_sweep(channel=2, sweep_name='none',initial_pulse=pi2_ef)
    pi2_ef.phase = 0
    geophase_seq.add_sweep(channel=1, sweep_name='none',initial_pulse=pi2_ef)
    
    pi_ge.start=8290 
    geophase_seq.add_sweep(channel=2, sweep_name='none',initial_pulse=pi_ge)
    pi_ge.phase = 90
    geophase_seq.add_sweep(channel=1, sweep_name='none',initial_pulse=pi_ge)
    ## markers
    readout = Pulse(start=6000,duration=1000,amplitude=1)
    rabi_seq.add_sweep(channel=1,marker=2,sweep_name='none', initial_pulse=readout) #sweep type 'none' copies pulse to every pattern of the sequence
    
    alazar_trigger = Pulse(start=1000, duration=500, amplitude=1)
    rabi_seq.add_sweep(channel=3, marker=1, sweep_name='none', initial_pulse=alazar_trigger )

    ## view output
    if False:
        channel1_ch = rabi_seq.channel_list[0][0] #[channel name -1][0:channel, 1:marker 1, 2:marker 2]
        channel2_ch = rabi_seq.channel_list[1][0]
        channel3_ch = rabi_seq.channel_list[2][0]
        plt.imshow(channel2_ch[0:100,4800:5100], aspect='auto', extent=[4800,5100,100,0])
        plt.show()
        
    ## write output
    write_dir = r"C:\arbsequences\strong_dispersive_withPython\sweep_pulse4_phase"
    geophase_seq.write_sequence(base_name='foo', file_path=write_dir, use_range_01=False,num_offset=0)
        
if __name__ == '__main__':
    rabi()
 
