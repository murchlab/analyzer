# -*- coding: utf-8 -*-
"""
Created on Mon Aug 24 22:18:53 2020

@author: J. Monroe
"""

import numpy as np
pi = np.pi
import matplotlib.pyplot as plt
import sys
import time
generator_path = r"C:\Users\crow108\Documents\Python Scripts\sequence_generator"
if generator_path not in sys.path:
    sys.path.append(generator_path)
from generator import Pulse, Sequence

controller_path = r"C:\Users\Crow108\Documents\Python\controller"
if controller_path  not in sys.path:
    sys.path.append(controller_path)
import proteusapi


def reset_proteus_clock(clock_GSs=1):
    sclk = clock_GSs*1E9
    
    for ch_index in range(4):
        proteusapi.SendScpi(":INST:CHAN {}".format(ch_index+1))
        proteusapi.SendScpi(":FREQ:RAST {0}".format(sclk))
##END set_proteus_clock
        

std_qubit_amp = 0.8

std_cavity_amp = 0.9
pi_time = 266


 #22
ssm = .100

mixer_orthogonality_deg = 85 # set for qubit mixer LXF0307 (1625)



def rabi(show_seq_matrix=True): 
    file_length = 8*4096
    num_steps = 51
    this_seq = Sequence(file_length, num_steps) 

    ## channels   
    rabi_time = 1001      
    readout_amp = 1 
    readout_start = 5000
    readout_duration = 3600 #3600
    b = 5 # buffer
    
    # qubit pulses
    rabi_pulse = Pulse(start=readout_start-b, duration=0, amplitude=1, ssm_freq=ssm, phase=0) 
    this_seq.add_sweep(channel=1, sweep_name='width', start=0, stop=-rabi_time, initial_pulse=rabi_pulse)
    rabi_pulse.phase = mixer_orthogonality_deg
    this_seq.add_sweep(channel=2,  sweep_name='width', start=0, stop=-rabi_time, initial_pulse=rabi_pulse)

    # readout pulse
    readout_pulse = Pulse(start =readout_start,duration=readout_duration, amplitude= readout_amp )
    this_seq.add_sweep(channel=4, sweep_name='none',initial_pulse=readout_pulse)
    
    ## markers
    #alazar_trigger = Pulse(start=readout_start-1000, duration=500, amplitude=1)
    alazar_trigger = Pulse(start=readout_start-1000, duration=500, amplitude=1)
    this_seq.add_sweep(channel=3, marker=1, sweep_name='none', initial_pulse=alazar_trigger )

    ## view output
    if show_seq_matrix:
        seq_matrix = this_seq.channel_list[0][0] #[channel name -1][0:channel, 1:marker 1, 2:marker 2]
        start = readout_start-rabi_time-10
        end = readout_start + 10
        plt.imshow(seq_matrix[: , start:end], aspect='auto', extent=[start,end,num_steps-1,0])
        seq_matrix = this_seq.channel_list[3][0] 
        plt.imshow(seq_matrix[:, start:end ], aspect='auto', alpha=0.4, extent=[start,end,num_steps-1,0])
        
        plt.show()
        
    # write output
#    this_seq.load_sequence(amp=[std_qubit_amp, std_qubit_amp, 1, std_cavity_amp] )
    this_seq.load_sequence(amp=[std_qubit_amp, std_qubit_amp, 1, std_cavity_amp] )
##END rabi
    
def rabi_test_032121(show_seq_matrix=True): 
    ssm = .1
    file_length = 4096
    num_steps = 11
    this_seq = Sequence(file_length, num_steps) 

    ## channels   
    rabi_time =1001
    readout_amp = 1 
    readout_start = 2000
    readout_duration = 300 #3600
    b = 5 # buffer
    
    # qubit pulses
    rabi_pulse = Pulse(start=readout_start-b, duration=0, amplitude=1, ssm_freq=ssm, phase=0) 
    this_seq.add_sweep(channel=1, sweep_name='width', start=0, stop=-rabi_time, initial_pulse=rabi_pulse)
#    rabi_pulse.phase = mixer_orthogonality_deg
    this_seq.add_sweep(channel=2,  sweep_name='width', start=0, stop=-rabi_time, initial_pulse=rabi_pulse)

    # readout pulse
    readout_pulse = Pulse(start =readout_start,duration=readout_duration, amplitude= readout_amp )
    this_seq.add_sweep(channel=4, sweep_name='none',initial_pulse=readout_pulse)
    
    ## markers
    #alazar_trigger = Pulse(start=readout_start-1000, duration=500, amplitude=1)
    alazar_trigger = Pulse(start=readout_start-1000, duration=500, amplitude=1)
    this_seq.add_sweep(channel=3, marker=1, sweep_name='none', initial_pulse=alazar_trigger )

    ## view output
    if show_seq_matrix:
        seq_matrix = this_seq.channel_list[0][0] #[channel name -1][0:channel, 1:marker 1, 2:marker 2]
        start = readout_start-rabi_time-10
        end = readout_start + 10
        plt.imshow(seq_matrix[: , start:end], aspect='auto', extent=[start,end,num_steps-1,0])
        seq_matrix = this_seq.channel_list[3][0] 
        plt.imshow(seq_matrix[:, start:end ], aspect='auto', alpha=0.4, extent=[start,end,num_steps-1,0])
        
        plt.show()
        
    # write output
    this_seq.load_sequence(amp=[std_qubit_amp, std_qubit_amp, 1, std_cavity_amp] )
    
    
def pi_noPi(): #this is pulsed readout to ring up and ring down cavity dfor e state
    file_length = 2*4096
    num_steps = 3
    this_seq = Sequence(file_length, num_steps) #this creates something called rabi_seq that is an instance of a this_seq class

    ## channels   
    readout_amp = 1 
    readout_start = 4000
    readout_duration = 3600
    b = 5 # buffer
    
    # qubit pulses
    pi_start = readout_start-b-pi_time
    qubit_pulse = Pulse(start=pi_start, duration=pi_time, amplitude=0, ssm_freq=ssm, phase=0) 
    this_seq.add_sweep(channel=1, sweep_name='amplitude', start=0, stop=1,initial_pulse=qubit_pulse)
    qubit_pulse.phase = mixer_orthogonality_deg
    this_seq.add_sweep(channel=2,  sweep_name='amplitude', start=0, stop=1,initial_pulse=qubit_pulse)
    
    # readout pulse
    readout_pulse = Pulse(start =readout_start,duration=readout_duration, amplitude= readout_amp )
    this_seq.add_sweep(channel=4, sweep_name='none',initial_pulse=readout_pulse)
    
    ## markers
    alazar_trigger = Pulse(start=readout_start-1000, duration=500, amplitude=1)
    this_seq.add_sweep(channel=3, marker=1, sweep_name='none', initial_pulse=alazar_trigger )

    ## view output
    if True:
        seq_matrix = this_seq.channel_list[0][0] #[channel name -1][0:channel, 1:marker 1, 2:marker 2]
        start = pi_start-10
        end = readout_start + 10
        plt.imshow(seq_matrix[: , start:end], aspect='auto', extent=[start,end,num_steps-1,0])
        seq_matrix = this_seq.channel_list[3][0] 
        plt.imshow(seq_matrix[:, start:end ], aspect='auto', alpha=0.4, extent=[start,end,num_steps-1,0])
        plt.show()
        
    ## write output
    this_seq.load_sequence(inst_index=0, amp=[std_qubit_amp, std_qubit_amp, 1, std_cavity_amp] )
##END pi_noPi
   
    
def no_pi_pi_ge_pi_ef(): #this is pulsed readout to ring up and ring down cavity dfor e state
    file_length = 2*4096
    num_steps = 3
    this_seq = Sequence(file_length, num_steps) #this creates something called rabi_seq that is an instance of a this_seq class

    ## channels   
    ssm_ge = ssm
    ssm_ef = 0.145
    readout_amp = 1 
    readout_start = 4000
    readout_duration = 3600
    b = 5 # buffer
    
    # qubit pulses
    pi_start = readout_start-2*(b+pi_time)
    pi_ge = Pulse(start=pi_start, duration=pi_time, amplitude=1, ssm_freq=ssm_ge, phase=0) 
    # insert_waveform( channel_num, pulse, step_index )
    this_seq.insert_waveform(1, pi_ge, 1)
    this_seq.insert_waveform(1, pi_ge, 2)
    pi_ge.phase = mixer_orthogonality_deg
    this_seq.insert_waveform(2, pi_ge, 1)
    this_seq.insert_waveform(2, pi_ge, 2)
    
    pi_start = readout_start-(b+pi_time)
    pi_ef = Pulse(start=pi_start, duration=pi_time, amplitude=1, ssm_freq=ssm_ef, phase=0) 
    this_seq.insert_waveform(1, pi_ef, 2)
    pi_ef.phase = -1*mixer_orthogonality_deg
    this_seq.insert_waveform(2, pi_ef, 2)
    
    # readout pulse
    readout_pulse = Pulse(start =readout_start,duration=readout_duration, amplitude= readout_amp )
    this_seq.add_sweep(channel=4, sweep_name='none',initial_pulse=readout_pulse)
    
    ## markers
    alazar_trigger = Pulse(start=readout_start-1000, duration=500, amplitude=1)
    this_seq.add_sweep(channel=3, marker=1, sweep_name='none', initial_pulse=alazar_trigger )

    ## view output
    if True:
        seq_matrix = this_seq.channel_list[0][0] #[channel name -1][0:channel, 1:marker 1, 2:marker 2]
        start = 3800
        end = readout_start + 10
        plt.imshow(seq_matrix[: , start:end], aspect='auto', extent=[start,end,num_steps-1,0])
        seq_matrix = this_seq.channel_list[3][0] 
        plt.imshow(seq_matrix[:, start:end ], aspect='auto', alpha=0.4, extent=[start,end,num_steps-1,0])
        plt.show()
        
    ## write output
    this_seq.load_sequence(inst_index=0, amp=[std_qubit_amp, std_qubit_amp, 1, std_cavity_amp] )
##END rabi

 
    
def ssm_sweep():
    file_length = 4*4096
    num_steps = 51
    this_seq = Sequence(file_length, num_steps) 

    ## channels   
    ssm_base = ssm
    ssm_span = 0.1
    readout_amp = 1 
    readout_start = 10000
    readout_duration = 3600
    b = 5 # buffer
    
    # qubit pulse
    pi_pulse = Pulse(start=readout_start-(pi_time+b), duration=pi_time, amplitude=1, ssm_freq=ssm_base, phase=0) 
    this_seq.add_sweep(channel=1, sweep_name='ssm', start=-ssm_span/2, stop=ssm_span/2, initial_pulse=pi_pulse)
    pi_pulse.phase = mixer_orthogonality_deg
    this_seq.add_sweep(channel=2,  sweep_name='ssm', start=-ssm_span/2, stop=ssm_span/2, initial_pulse=pi_pulse)
    
    # readout pulse
    readout_pulse = Pulse(start =readout_start,duration=readout_duration, amplitude= readout_amp )
    this_seq.add_sweep(channel=4, sweep_name='none',initial_pulse=readout_pulse )
#    main_pulse = Pulse(start =3800,duration = 1800, amplitude= readout_amp )
#    this_seq.add_sweep(channel=4, sweep_name='none',initial_pulse=main_pulse)
    
    ## markers
    alazar_trigger = Pulse(start=readout_start-1000, duration=500, amplitude=1)
    this_seq.add_sweep(channel=3, marker=1, sweep_name='none', initial_pulse=alazar_trigger )

#    # qubit pulse gate
#    this_seq.add_gate(source_1=1, source_2=2, destination_tuple=(1,1))

    ## view output
    if True:
        seq_matrix = this_seq.channel_list[0][0] #[channel name -1][0:channel, 1:marker 1, 2:marker 2]
        st, en = 5750,6050
        plt.imshow(seq_matrix[: , st:en], aspect='auto', extent=[st,en,num_steps-1,0])
        seq_matrix = this_seq.channel_list[3][0] 
        plt.imshow(seq_matrix[:, st:en], aspect='auto', alpha=0.4, extent=[st,en,num_steps-1,0])
        plt.show()
        
    ## write output
    this_seq.load_sequence(inst_index=0, amp=[std_qubit_amp, std_qubit_amp, 1, std_cavity_amp] )
##END ssm_sweep
    
    
def ssm_ef_sweep():
    file_length = 4*4096
    num_steps = 51
    this_seq = Sequence(file_length, num_steps) #this creates something called rabi_seq that is an instance of a this_seq class

    ## channels   
    ssm_ge = ssm
    ssm_ef = 0.145
    ssm_span = 0.050
    readout_amp = 1 
    readout_start = 6000
    readout_duration = 3600
    b = 5 # buffer
    
    # qubit pulse
    pi_pulse = Pulse(start=readout_start-2*(pi_time+b), duration=pi_time, amplitude=1, ssm_freq=ssm_ge, phase=0) 
    this_seq.add_sweep(channel=1, sweep_name='none', start=-ssm_span/2, stop=ssm_span/2, initial_pulse=pi_pulse)
    pi_pulse.phase = mixer_orthogonality_deg
    this_seq.add_sweep(channel=2,  sweep_name='none', start=-ssm_span/2, stop=ssm_span/2, initial_pulse=pi_pulse)
    
    pi_pulse = Pulse(start=readout_start-(pi_time+b), duration=pi_time, amplitude=1, ssm_freq=ssm_ef, phase=0) 
    this_seq.add_sweep(channel=1, sweep_name='ssm', start=-ssm_span/2, stop=ssm_span/2, initial_pulse=pi_pulse)
    pi_pulse.phase = -1*mixer_orthogonality_deg
    this_seq.add_sweep(channel=2,  sweep_name='ssm', start=-ssm_span/2, stop=ssm_span/2, initial_pulse=pi_pulse)
    
    # readout pulse
    readout = Pulse(start =readout_start,duration=readout_duration, amplitude= readout_amp )
    this_seq.add_sweep(channel=4, sweep_name='none',initial_pulse=readout)
    
    ## markers
    alazar_trigger = Pulse(start=readout_start-1000, duration=500, amplitude=1)
    this_seq.add_sweep(channel=3, marker=1, sweep_name='none', initial_pulse=alazar_trigger )

    ## view output
    if True:
        seq_matrix = this_seq.channel_list[0][0] #[channel name -1][0:channel, 1:marker 1, 2:marker 2]
        st, en = 5750,6050
        plt.imshow(seq_matrix[: , st:en], aspect='auto', extent=[st,en,num_steps-1,0])
        seq_matrix = this_seq.channel_list[3][0] 
        plt.imshow(seq_matrix[:, st:en], aspect='auto', alpha=0.4, extent=[st,en,num_steps-1,0])
        plt.show()
        
    ## write output
    this_seq.load_sequence(inst_index=0, amp=[std_qubit_amp, std_qubit_amp, 1, std_cavity_amp] )
##END ssm_ef_sweep
    

def cavity_amp():
    file_length = 4*4096
    num_steps = 51
    this_seq = Sequence(file_length, num_steps) 

    ## channels   
#    ssm_ef = 0.145
    readout_start = 6000
    readout_duration = 3600
    b = 5 # buffer
    
    # qubit pulse
#    # pi on ge
#    pi_pulse = Pulse(start=readout_start-2*(pi_time+b), duration=pi_time, amplitude=1, ssm_freq=ssm, phase=0) 
#    this_seq.add_sweep(channel=1, sweep_name='none',  initial_pulse=pi_pulse)
#    pi_pulse.phase = mixer_orthogonality_deg
#    this_seq.add_sweep(channel=2,  sweep_name='none', initial_pulse=pi_pulse)
#    
#    # rabi on ef
#    rabi_pulse = Pulse(start=readout_start-pi_time-b, duration=pi_time, amplitude=1, ssm_freq=ssm_ef, phase=0) 
#    this_seq.add_sweep(channel=1, sweep_name='none', initial_pulse=rabi_pulse)
#    rabi_pulse.phase = -1*mixer_orthogonality_deg # address lower sideband
#    this_seq.add_sweep(channel=2, sweep_name='none', initial_pulse=rabi_pulse)
    
    # readout pulse
    readout_pulse = Pulse(start =readout_start,duration=readout_duration, amplitude= 0)
    this_seq.add_sweep(channel=4, sweep_name='amplitude', start=0, stop=1,initial_pulse=readout_pulse )
    
    ## markers
    alazar_trigger = Pulse(start=readout_start-1000, duration=500, amplitude=1)
    this_seq.add_sweep(channel=3, marker=1, sweep_name='none', initial_pulse=alazar_trigger )

#    # qubit pulse gate
#    this_seq.add_gate(source_1=1, source_2=2, destination_tuple=(1,1))

    ## view output
    if True:
        seq_matrix = this_seq.channel_list[0][0] #[channel name -1][0:channel, 1:marker 1, 2:marker 2]
        st, en = 5750,6050
        plt.imshow(seq_matrix[: , st:en], aspect='auto', extent=[st,en,num_steps-1,0])
        seq_matrix = this_seq.channel_list[3][0] 
        plt.imshow(seq_matrix[:, st:en], aspect='auto', alpha=0.4, extent=[st,en,num_steps-1,0])
        plt.show()
    
    ## write output
    this_seq.load_sequence(inst_index=0, amp=[std_qubit_amp, std_qubit_amp, 1, std_cavity_amp] )
##END cavity_amp

    

def rabi_ef():
    file_length = 4*4096
    num_steps = 51
    this_seq = Sequence(file_length, num_steps) #this creates something called rabi_seq that is an instance of a this_seq class

    ## channels   
    rabi_time = 351    
    ssm_ge = ssm
    ssm_ef = .196 #.218 # optimized with ssm sweep 
    readout_amp = 1 
    readout_start = 6000
    readout_duration = 3600
    b = 5 # buffer
    
    # qubit pulses
    # pi on ge
#    pi_pulse = Pulse(start=readout_start-2*(pi_time+b), duration=pi_time, amplitude=1, ssm_freq=ssm_ge, phase=0) 
#    this_seq.add_sweep(channel=1, sweep_name='start', start=0, stop=-rabi_time,initial_pulse=pi_pulse)
#    pi_pulse.phase = mixer_orthogonality_deg
#    this_seq.add_sweep(channel=2,  sweep_name='start', start=0, stop=-rabi_time,initial_pulse=pi_pulse)
    
    # rabi on ef
    rabi_pulse = Pulse(start=readout_start-pi_time-b, duration=0, amplitude=1, ssm_freq=ssm_ef, phase=0) 
    this_seq.add_sweep(channel=1, sweep_name='width', start=0, stop=-rabi_time,initial_pulse=rabi_pulse)
    rabi_pulse.phase = -1*mixer_orthogonality_deg # address lower sideband
    this_seq.add_sweep(channel=2,  sweep_name='width', start=0, stop=-rabi_time,initial_pulse=rabi_pulse)
    
    # pi on ge
    pi_pulse = Pulse(start=readout_start-pi_time, duration=pi_time, amplitude=1, ssm_freq=ssm_ge, phase=0) 
    this_seq.add_sweep(channel=1, sweep_name='none', start=0, stop=-rabi_time,initial_pulse=pi_pulse)
    pi_pulse.phase = mixer_orthogonality_deg
    this_seq.add_sweep(channel=2,  sweep_name='none', start=0, stop=-rabi_time,initial_pulse=pi_pulse)
#    
    # readout pulse
    main_pulse = Pulse(start =readout_start,duration=readout_duration, amplitude= readout_amp )
    this_seq.add_sweep(channel=4, sweep_name='none',initial_pulse=main_pulse)
#    main_pulse = Pulse(start =3800,duration = 1800, amplitude= readout_amp )
#    this_seq.add_sweep(channel=4, sweep_name='none',initial_pulse=main_pulse)
    
    ## markers
   # alazar_trigger = Pulse(start=file_length-7000, duration=500, amplitude=1)
    alazar_trigger = Pulse(start=readout_start-1000, duration=500, amplitude=1)
    this_seq.add_sweep(channel=3, marker=1, sweep_name='none', initial_pulse=alazar_trigger )

#    # qubit pulse gate
#    this_seq.add_gate(source_1=1, source_2=2, destination_tuple=(1,1))

    ## view output
    if True:
        seq_matrix = this_seq.channel_list[0][0] #[channel name -1][0:channel, 1:marker 1, 2:marker 2]
        plt.imshow(seq_matrix[: , 5700:6100], aspect='auto', extent=[5850,6100,50,0])
        seq_matrix = this_seq.channel_list[3][0] 
        plt.imshow(seq_matrix[:, 5700:6100 ], aspect='auto', alpha=0.4, extent=[5850,6100,50,0])
        plt.show()
        
    ## write output
    this_seq.load_sequence(inst_index=0, amp=[std_qubit_amp, std_qubit_amp, 1, std_cavity_amp] )
##END rabi_ef
    

def rabi_amplitude():
    file_length = 2*4096
    num_steps = 51
    this_seq = Sequence(file_length, num_steps)

    ## channels   
    readout_amp = 1 
    pi_time = 100
    
    # qubit pulses
    rabi_pulse = Pulse(start=2000-pi_time, duration=pi_time, amplitude=0, ssm_freq=ssm, phase=0) 
    this_seq.add_sweep(channel=1, sweep_name='amplitude', start=0, stop=1,initial_pulse=rabi_pulse)
    rabi_pulse.phase = mixer_orthogonality_deg
    this_seq.add_sweep(channel=2,  sweep_name='amplitude', start=0, stop=1,initial_pulse=rabi_pulse)
    
    # readout pulse
    main_pulse = Pulse(start =2000,duration = 3600, amplitude= readout_amp )
    this_seq.add_sweep(channel=4, sweep_name='none',initial_pulse=main_pulse)
#    main_pulse = Pulse(start =3800,duration = 1800, amplitude= readout_amp )
#    this_seq.add_sweep(channel=4, sweep_name='none',initial_pulse=main_pulse)
    

    alazar_trigger = Pulse(start=2000-1000, duration=500, amplitude=1)
    this_seq.add_sweep(channel=3, marker=1, sweep_name='none', initial_pulse=alazar_trigger )

    # qubit pulse gate
    this_seq.add_gate(source_1=1, source_2=2, destination_tuple=(1,1))
#    channel1_channel = this_seq.channel_list[0][0] # dim 0: channel 1; dim 1: [ch,m1,m2]
#    channel2_channel = this_seq.channel_list[1][0] # dim 0: channel 1; dim 1: [ch,m1,m2]
#    both_ch1_ch2 = channel1_channel**2 + channel2_channel**2
#    qubit_gate = create_gate(both_ch1_ch2)
#    this_seq.channel_list[0][1] = qubit_gate

    ## view output
    if True:
        seq_matrix = this_seq.channel_list[0][0] #[channel name -1][0:channel, 1:marker 1, 2:marker 2]
        #plt.imshow(seq_matrix[0:200,4800:5050], aspect='auto', extent=[4800,5050,200,0])
        plt.imshow(seq_matrix, aspect='auto')
        seq_matrix = this_seq.channel_list[3][0] 
        plt.imshow(seq_matrix[:, : ], aspect='auto', alpha=0.4)
        plt.show()
        
    ## write output
#    write_dir = r"C:\arbsequences\strong_dispersive_withPython\test_pulse_ringupdown_bin"
#    this_seq.write_sequence(base_name='foo', file_path=write_dir, use_range_01=False,num_offset=0, write_binary=True)
#    this_seq.load_sequence(inst_index=0, amp=[1,1,1,std_cavity_amp] )
    
#    set_amplitudes.set_proteus_amplitude2( amps=[1.3,1.3,1,0.45] )
##END rabi_amp
    
    
def T1():
    file_length = 8*32768 #131072 # 131k ~ 2**17
    num_steps = 51
    this_seq = Sequence(file_length, num_steps)

    ## channels   
    readout_amp = 1 
    T1_time = 220000
    readout_start = 225000
    readout_dur = 3600
    
    # qubit pulses
    rabi_pulse = Pulse(start=readout_start-pi_time, duration=pi_time, amplitude=1, ssm_freq=ssm, phase=0) 
    this_seq.add_sweep(channel=1, sweep_name='start', start=0, stop=-T1_time,initial_pulse=rabi_pulse)
    rabi_pulse.phase = mixer_orthogonality_deg
    this_seq.add_sweep(channel=2,  sweep_name='start', start=0, stop=-T1_time,initial_pulse=rabi_pulse)
    
    # readout pulse
    main_pulse = Pulse(start=readout_start,duration = readout_dur, amplitude= readout_amp )
    this_seq.add_sweep(channel=4, sweep_name='none',initial_pulse=main_pulse)
    
    ## markers
    alazar_trigger = Pulse(start=readout_start-1000, duration=500, amplitude=1)
    this_seq.add_sweep(channel=3, marker=1, sweep_name='none', initial_pulse=alazar_trigger )

    # qubit pulse gate
#    this_seq.add_gate(source_1=1, source_2=2, destination_tuple=(1,1))

    ## view output
    if True:
        seq_matrix = this_seq.channel_list[0][0] #[channel name -1][0:channel, 1:marker 1, 2:marker 2]
        start = readout_start-T1_time
        plt.imshow(seq_matrix[0:200,start:readout_start+100], aspect='auto', extent=[start,readout_start+100,51,0])
        plt.show()
        
    ## write output
    this_seq.load_sequence(inst_index=0, amp=[std_qubit_amp, std_qubit_amp, 1, std_cavity_amp] )
#    this_seq.load_sequence_new(amp=[std_qubit_amp,std_qubit_amp, 1, std_cavity_amp])
    
##END T1    
    
    
def test_prot(use_echo=False, num_steps=None, file_length=None,show_plot=True): #this is pulsed readout to ring up and ring down cavity dfor e state
    if not file_length:
        file_length =2*4096
    if not num_steps:
        num_steps = 51  
    this_seq = Sequence(file_length, num_steps) #this creates something called rabi_seq that is an instance of a this_seq class

    ## channels   
    pi_time = 400 #93
    rabi_amp = 1
    readout_amp = 1 
    T2_time = 1000*2
    readout_start = 3000
    readout_dur = 1000 #3600
    b = 0 # buffer
    
    # qubit pulses
    fixed_pi2_start = readout_start -pi_time//2 - b
#    fixed_pi2_pulse = Pulse(start=fixed_pi2_start, duration=pi_time//2, amplitude=rabi_amp, ssm_freq=ssm, phase=0) 
#    this_seq.add_sweep(channel=1, sweep_name='phase', start=0, stop=360*5, initial_pulse=fixed_pi2_pulse)
#    fixed_pi2_pulse.phase = mixer_orthogonality_deg 
#    this_seq.add_sweep(channel=2, sweep_name='phase', start=0, stop=360*5,initial_pulse=fixed_pi2_pulse)
    
    if use_echo:
        echo_start = fixed_pi2_start - pi_time - b
        echo_pulse = Pulse(start=echo_start, duration=pi_time, amplitude=rabi_amp, ssm_freq=ssm, phase=0) 
        this_seq.add_sweep(channel=1, sweep_name='start', start=0, stop=-T2_time/2,initial_pulse=echo_pulse)
        echo_pulse.phase = mixer_orthogonality_deg
        this_seq.add_sweep(channel=2,  sweep_name='start', start=0, stop=-T2_time/2,initial_pulse=echo_pulse)
        
        sweep_start = echo_start - pi_time//2 - b
    else:
        sweep_start = fixed_pi2_start - pi_time//2 - b
    
    sweep_pulse = Pulse(start=sweep_start, duration=pi_time//2, amplitude=rabi_amp, ssm_freq=ssm, phase=0) 
    this_seq.add_sweep(channel=1, sweep_name='start', start=0, stop=-T2_time,initial_pulse=sweep_pulse)
    sweep_pulse.phase = mixer_orthogonality_deg
    this_seq.add_sweep(channel=2,  sweep_name='start', start=0, stop=-T2_time,initial_pulse=sweep_pulse)
    
    # readout pulse
    main_pulse = Pulse(start =readout_start,duration = readout_dur, amplitude= readout_amp )
    this_seq.add_sweep(channel=4, sweep_name='none',initial_pulse=main_pulse)
    
    
    ## markers
    alazar_trigger = Pulse(start=readout_start-1000, duration=500, amplitude=1)
    this_seq.add_sweep(channel=3, marker=1, sweep_name='none', initial_pulse=alazar_trigger )

    ## view output
    if show_plot:
        seq_matrix = this_seq.channel_list[0][0] #[channel name -1][0:channel, 1:marker 1, 2:marker 2]
        plt.imshow(seq_matrix[: ,:], aspect='auto', extent=[0,file_length,num_steps,0])
        seq_matrix = this_seq.channel_list[3][0]
        plt.imshow(seq_matrix[: ,:], aspect='auto', extent=[0,file_length,num_steps,0], alpha=0.4)
        plt.show()
        
    ## write output
    this_seq.load_sequence(inst_index=0, amp=[0.45, 0.45,1,1.3], verbose=show_plot )
##END test_prot
    
    
def T2(use_echo=False, show_plot=True): #this is pulsed readout to ring up and ring down cavity dfor e state
    file_length = 65536*2 ## must be power of 2
    num_steps = 51
    this_seq = Sequence(file_length, num_steps) #this creates something called rabi_seq that is an instance of a this_seq class

    ## channels   
#    pi_time = 18
    rabi_amp = 1
    readout_amp = 1 
    T2_time = 20000
    readout_start = 110000
    readout_dur = 3600
    b = 10 # buffer
    
    # qubit pulses
    fixed_pi2_start = readout_start -pi_time//2 - b  #sets when to start the first pi/2 pulse
    fixed_pi2_pulse = Pulse(start=fixed_pi2_start, duration=pi_time//2, amplitude=rabi_amp, ssm_freq=ssm, phase=0) 
    this_seq.add_sweep(channel=1, sweep_name='none', start=0, stop=360*2, initial_pulse=fixed_pi2_pulse)
    fixed_pi2_pulse.phase = mixer_orthogonality_deg
    this_seq.add_sweep(channel=2, sweep_name='none', start=0, stop=360*2,initial_pulse=fixed_pi2_pulse)
    
    if use_echo:
        echo_start = fixed_pi2_start - pi_time - b
        echo_pulse = Pulse(start=echo_start, duration=pi_time, amplitude=rabi_amp, ssm_freq=ssm, phase=0) 
        this_seq.add_sweep(channel=1, sweep_name='start', start=0, stop=-T2_time/2,initial_pulse=echo_pulse)
        echo_pulse.phase = mixer_orthogonality_deg
        this_seq.add_sweep(channel=2,  sweep_name='start', start=0, stop=-T2_time/2,initial_pulse=echo_pulse)
        
        sweep_start = echo_start - pi_time//2 - b
    else:
        sweep_start = fixed_pi2_start - pi_time//2 - b
    
    sweep_pulse = Pulse(start=sweep_start, duration=pi_time//2, amplitude=rabi_amp, ssm_freq=ssm, phase=0) 
    this_seq.add_sweep(channel=1, sweep_name='start', start=0, stop=-T2_time,initial_pulse=sweep_pulse)
    sweep_pulse.phase = mixer_orthogonality_deg
    this_seq.add_sweep(channel=2,  sweep_name='start', start=0, stop=-T2_time,initial_pulse=sweep_pulse)
    
    # readout pulse
    main_pulse = Pulse(start =readout_start,duration = readout_dur, amplitude= readout_amp )
    this_seq.add_sweep(channel=4, sweep_name='none',initial_pulse=main_pulse)
    
    ## markers
    alazar_trigger = Pulse(start=readout_start-1000, duration=500, amplitude=1)
    this_seq.add_sweep(channel=3, marker=1, sweep_name='none', initial_pulse=alazar_trigger )

    ## view output
    if show_plot:
        seq_matrix = this_seq.channel_list[0][0] #[channel name -1][0:channel, 1:marker 1, 2:marker 2]
        start = readout_start-T2_time
        end = readout_start + 100
        plt.imshow(seq_matrix[: ,start:end], aspect='auto', extent=[start,end,num_steps,0])
        seq_matrix = this_seq.channel_list[3][0]
        plt.imshow(seq_matrix[: ,start:end], aspect='auto', extent=[start,end,num_steps,0], alpha=0.4)
        plt.show()
        
    ## write output
    this_seq.load_sequence(inst_index=0, amp=[std_qubit_amp, std_qubit_amp, 1, std_cavity_amp], verbose=show_plot )
##END T2
    
    
def T2_CPMG(N_refocus=0, show_plot=True):
    file_length = 65536*2 ## must be power of 2
    num_steps = 51 
    this_seq = Sequence(file_length, num_steps) #this creates something called rabi_seq that is an instance of a this_seq class

    ## channels   
#    pi_time = 18
    rabi_amp = 1
    readout_amp = 1 
    T2_time = 80000
    readout_start = 110000
    readout_dur = 3600
    b = 10 # buffer
    dt = T2_time/(N_refocus+1) # free evolution period between pulses‰‰
    
    # qubit pulses
    fixed_pi2_start = readout_start -pi_time//2 - b
    fixed_pi2_pulse = Pulse(start=fixed_pi2_start, duration=pi_time//2, amplitude=rabi_amp, ssm_freq=ssm, phase=0) 
    this_seq.add_sweep(channel=1, sweep_name='none', initial_pulse=fixed_pi2_pulse)
    fixed_pi2_pulse.phase = mixer_orthogonality_deg 
    this_seq.add_sweep(channel=2, sweep_name='none', initial_pulse=fixed_pi2_pulse)
    
    echo_start = fixed_pi2_start  -b
    for nth_pulse in range(1,N_refocus+1):
        echo_start -= pi_time + b
        echo_pulse = Pulse(start=echo_start, duration=pi_time, amplitude=rabi_amp, ssm_freq=ssm, phase=0)
        nth_deltaT = (nth_pulse)*  dt
        this_seq.add_sweep(channel=1, sweep_name='start', start=0, stop=-nth_deltaT,initial_pulse=echo_pulse)
        echo_pulse.phase = mixer_orthogonality_deg
        this_seq.add_sweep(channel=2,  sweep_name='start', start=0, stop=-nth_deltaT,initial_pulse=echo_pulse)
    
    sweep_start = echo_start -pi_time//2 -b
    sweep_pulse = Pulse(start=sweep_start, duration=pi_time//2, amplitude=rabi_amp, ssm_freq=ssm, phase=0)
    final_del = T2_time
    this_seq.add_sweep(channel=1, sweep_name='start', start=0, stop=-final_del,initial_pulse=sweep_pulse)
    sweep_pulse.phase = mixer_orthogonality_deg
    this_seq.add_sweep(channel=2,  sweep_name='start', start=0, stop=-final_del,initial_pulse=sweep_pulse)
    
    # readout pulse
    readout_pulse = Pulse(start=readout_start, duration=readout_dur, amplitude=readout_amp )
    this_seq.add_sweep(channel=4, sweep_name='none',initial_pulse=readout_pulse)
    
    ## markers
    alazar_trigger = Pulse(start=readout_start-1000, duration=500, amplitude=1)
    this_seq.add_sweep(channel=3, marker=1, sweep_name='none', initial_pulse=alazar_trigger )

    ## view output
    if show_plot:
        seq_matrix = this_seq.channel_list[0][0] #[channel name -1][0:channel, 1:marker 1, 2:marker 2]
        x = readout_start - T2_time
        y = readout_start + 100
        plt.imshow(seq_matrix[: ,x:y], aspect='auto', extent=[x,y,num_steps,0])
        seq_matrix = this_seq.channel_list[3][0]
        plt.imshow(seq_matrix[: ,x:y], aspect='auto', extent=[x,y,num_steps,0], alpha=0.4)
        plt.show()       

    ## write output
    this_seq.load_sequence(inst_index=0, amp=[std_qubit_amp, std_qubit_amp, 1, std_cavity_amp], verbose=show_plot )
##END T2_CMPG
    
    
def sweep_readout_amp(): 
    file_length = 65536#80000
    num_steps = 51
    this_seq = Sequence(file_length, num_steps) 
    ## constats   
    readout_start = 50000

    ## channels   
    
    # readout pulse
    cavity_pulse = Pulse(start=readout_start, duration=3600, amplitude=0, phase=0) 
    start_amp, stop_amp = 0.1, 1.0
    this_seq.add_sweep(channel=4, sweep_name='amplitude', start=start_amp, stop=stop_amp,initial_pulse=cavity_pulse)
    print(f"Sweep amplitude from {start_amp*100}% to {stop_amp*100}%")
    
    ## markers
    alazar_trigger = Pulse(start=readout_start-1000, duration=500, amplitude=1)
    this_seq.add_sweep(channel=3, marker=1, sweep_name='none', initial_pulse=alazar_trigger )

    ## view output
    if True:
        seq_matrix = this_seq.channel_list[3][0] #[channel name -1][0:channel, 1:marker 1, 2:marker 2]
        #plt.imshow(seq_matrix[0:200,4800:5050], aspect='auto', extent=[4800,5050,200,0])
        plt.imshow(seq_matrix, aspect='auto')
        plt.show()
    
    ## write output    
    this_seq.load_sequence(amp=[std_qubit_amp,std_qubit_amp, 1, 1.2])
##END phase_sweep
    
    
def always_on(): 
    file_length = 131072
    num_steps = 3
    this_seq = Sequence(file_length, num_steps) #this creates something called rabi_seq that is an instance of a this_seq class

    ## channels   
    rabi_amp = 1
    readout_amp = 1 
    
    # qubit pulses
    rabi_pulse = Pulse(start=0, duration=file_length, amplitude=rabi_amp, ssm_freq=ssm, phase=0) 
    this_seq.add_sweep(channel=1, sweep_name='none', initial_pulse=rabi_pulse)
    rabi_pulse.phase = mixer_orthogonality_deg
    this_seq.add_sweep(channel=2,  sweep_name='none', initial_pulse=rabi_pulse)
    
    # readout pulse
    main_pulse = Pulse(start =50,duration = file_length-100, amplitude= readout_amp )
    this_seq.add_sweep(channel=4, sweep_name='none',initial_pulse=main_pulse)
    
    ## markers
    alazar_trigger = Pulse(start=0, duration=500, amplitude=1)
    this_seq.add_sweep(channel=3, marker=1, sweep_name='none', initial_pulse=alazar_trigger )

    ## view output
    if True:
        seq_matrix = this_seq.channel_list[0][0] #[channel name -1][0:channel, 1:marker 1, 2:marker 2]
        #plt.imshow(seq_matrix[0:200,4800:5050], aspect='auto', extent=[4800,5050,200,0])
        plt.imshow(seq_matrix, aspect='auto')
        plt.show()
        
    ## write output
    #this_seq.load_sequence(inst_index=0, amp=[1,1,1,0.5] )
    #this_seq.load_sequence_new(amp=[std_qubit_amp,std_qubit_amp,1,std_cavity_amp])
    this_seq.load_sequence(amp=[std_qubit_amp,std_qubit_amp,1,1.0])
    
##END always_on
    
    
    
def pi_seq(): #this is pulsed readout to ring up and ring down cavity dfor e state
    file_length = 2*4096
    num_steps = 3
    this_seq = Sequence(file_length, num_steps) #this creates something called rabi_seq that is an instance of a this_seq class

    ## channels   
    readout_amp = 1 
    readout_start = 4000
    readout_duration = 3600
    b = 5 # buffer
    
    # qubit pulses
    pi_start = readout_start-b-pi_time
    qubit_pulse = Pulse(start=pi_start, duration=pi_time, amplitude=0, ssm_freq=ssm, phase=0) 
    this_seq.add_sweep(channel=1, sweep_name='amplitude', start=0.9, stop=1,initial_pulse=qubit_pulse)
    qubit_pulse.phase = mixer_orthogonality_deg
    this_seq.add_sweep(channel=2,  sweep_name='amplitude', start=0.9, stop=1,initial_pulse=qubit_pulse)
    
    # readout pulse
    readout_pulse = Pulse(start =readout_start,duration=readout_duration, amplitude= readout_amp )
    this_seq.add_sweep(channel=4, sweep_name='none',initial_pulse=readout_pulse)
    
    ## markers
    alazar_trigger = Pulse(start=readout_start-1000, duration=500, amplitude=1)
    this_seq.add_sweep(channel=3, marker=1, sweep_name='none', initial_pulse=alazar_trigger )

    ## view output
    if True:
        seq_matrix = this_seq.channel_list[0][0] #[channel name -1][0:channel, 1:marker 1, 2:marker 2]
        start = pi_start-10
        end = readout_start + 10
        plt.imshow(seq_matrix[: , start:end], aspect='auto', extent=[start,end,num_steps-1,0])
        seq_matrix = this_seq.channel_list[3][0] 
        plt.imshow(seq_matrix[:, start:end ], aspect='auto', alpha=0.4, extent=[start,end,num_steps-1,0])
        plt.show()
        
    ## write output
    this_seq.load_sequence(inst_index=0, amp=[std_qubit_amp, std_qubit_amp, 1, std_cavity_amp] )
##END rabi  
