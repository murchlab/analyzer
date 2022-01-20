import numpy as np
import sys
sys.path.append(r"C:\Users\crow104\Documents\Python Scripts\sequence_generator")
from generator import *
import os
pi = np.pi
import matplotlib.pyplot as plt


def pulsed_readout_ramsey(): #this is pulsed readout to ring up and ring down cavity dfor e state
    file_length = 8000
    num_steps = 51
    ringupdown_seq = Sequence(file_length, num_steps) #this creates something called rabi_seq that is an instance of a sequence class

    ## channels    
    pi_ge_time = 44
    pi2_ef_time  = 16
    pi2_ef_amp = 0.5
    pi2_ge_time = 28
    ssm_ge = .110
    ssm_ef = 0.188
    pre3_amp = 0.8
    pre_time = 30
    pre4_amp = 0.1
    post4_amp = -0.4
    post3_amp = -.2
    post_time = pre_time
    readout_amp = 0.1
    scaling_factor = .4
    
    
    
    #this is the first pi/2 pulse in the sequence
    pi2_ge = Pulse(start=4870, duration=-pi2_ge_time, amplitude=1, ssm_freq=ssm_ge, phase=0) #pulse is also a class p is an instance
    ringupdown_seq.add_sweep(channel=1, sweep_name='none',initial_pulse=pi2_ge)
    pi2_ge.phase = 90
    ringupdown_seq.add_sweep(channel=2, sweep_name='none',initial_pulse=pi2_ge)
    #p.phase = 90 #make the pulse phase 90 degrees to get the single sideband modulation
    #rabi_seq.add_sweep(channel=2, sweep_name='width', start=0, stop=-200,initial_pulse=p)
    
    
    pre_pulse = Pulse(start = 4900,duration = -pre_time, amplitude=scaling_factor*pre3_amp )
    ringupdown_seq.add_sweep(channel=3, sweep_name='none',initial_pulse=pre_pulse)
    pre_pulse = Pulse(start = 4900,duration = -pre_time, amplitude=scaling_factor*pre4_amp )
    ringupdown_seq.add_sweep(channel=4, sweep_name='none',initial_pulse=pre_pulse)
    
    main_pulse = Pulse(start = 5000,duration = -100, amplitude=scaling_factor*readout_amp )
    ringupdown_seq.add_sweep(channel=4, sweep_name='none',initial_pulse=main_pulse)
    
    post_pulse = Pulse(start = 5030,duration = -post_time, amplitude=scaling_factor*post3_amp )
    ringupdown_seq.add_sweep(channel=3, sweep_name='none',initial_pulse=post_pulse)
    post_pulse.amplitude=scaling_factor*post4_amp
    ringupdown_seq.add_sweep(channel=4, sweep_name='none',initial_pulse=post_pulse)
    
       #this is the second  pi/2 pulse in the sequence
    pi2_ge = Pulse(start=5040, duration=pi2_ge_time, amplitude=1, ssm_freq=ssm_ge, phase=0) #pulse is also a class p is an instance
    ringupdown_seq.add_sweep(channel=1, sweep_name='phase',start=0,stop=360,initial_pulse=pi2_ge)
    pi2_ge.phase = 90
    ringupdown_seq.add_sweep(channel=2, sweep_name='phase',start=0,stop=360,initial_pulse=pi2_ge)
    
    
    #second readout
    
    pre_pulse = Pulse(start = 5100,duration = -pre_time, amplitude=pre3_amp )
    ringupdown_seq.add_sweep(channel=3, sweep_name='none',initial_pulse=pre_pulse)
    pre_pulse = Pulse(start = 5100,duration = -pre_time, amplitude=pre4_amp )
    ringupdown_seq.add_sweep(channel=4, sweep_name='none',initial_pulse=pre_pulse)
    
    main_pulse = Pulse(start = 5100,duration = 1000, amplitude= readout_amp )
    ringupdown_seq.add_sweep(channel=4, sweep_name='none',initial_pulse=main_pulse)
    
    
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
    write_dir = r"C:\arbsequences\strong_dispersive_withPython\test_pulse_ringupdown"
    ringupdown_seq.write_sequence(base_name='foo', file_path=write_dir, use_range_01=False,num_offset=0)
##END geom
    
    
def rabi_200ns(): #this is pulsed readout to ring up and ring down cavity dfor e state
    file_length = 8000
    num_steps = 51
    ringupdown_seq = Sequence(file_length, num_steps) #this creates something called rabi_seq that is an instance of a sequence class

    ## channels    
    pi_ge_time = 40
    pi2_ef_time  = 16
    pi2_ef_amp = 0.5
    pi2_ge_time = 20
    ssm_ge = .110
    ssm_ef = 0.188
    pre3_amp = 0.8
    pre_time = 30
    pre4_amp = 0.1
    post4_amp = -0.4
    post3_amp = -.2
    post_time = pre_time
    readout_amp = 0.1
    
    
    
   
    pi2_ge = Pulse(start=5050, duration=0, amplitude=1, ssm_freq=ssm_ge, phase=0) #pulse is also a class p is an instance
    ringupdown_seq.add_sweep(channel=1, sweep_name='width', start=0, stop=-200,initial_pulse=pi2_ge)
    pi2_ge.phase = 90
    ringupdown_seq.add_sweep(channel=2,  sweep_name='width', start=0, stop=-200,initial_pulse=pi2_ge)
    #p.phase = 90 #make the pulse phase 90 degrees to get the single sideband modulation
    #rabi_seq.add_sweep(channel=2, sweep_name='width', start=0, stop=-200,initial_pulse=p)

    
    #main readout
    
    pre_pulse = Pulse(start = 5100,duration = -pre_time, amplitude=pre3_amp )
    ringupdown_seq.add_sweep(channel=3, sweep_name='none',initial_pulse=pre_pulse)
    pre_pulse = Pulse(start = 5100,duration = -pre_time, amplitude=pre4_amp )
    ringupdown_seq.add_sweep(channel=4, sweep_name='none',initial_pulse=pre_pulse)
    
    main_pulse = Pulse(start = 5100,duration = 1000, amplitude= readout_amp )
    ringupdown_seq.add_sweep(channel=4, sweep_name='none',initial_pulse=main_pulse)
    
    
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
    write_dir = r"C:\arbsequences\strong_dispersive_withPython\test_pulse_ringupdown"
    ringupdown_seq.write_sequence(base_name='foo', file_path=write_dir, use_range_01=False,num_offset=0)
##END geom
    
    
def Ramsey_2us(): 
    file_length = 8000
    num_steps = 51
    ringupdown_seq = Sequence(file_length, num_steps) #this creates something called rabi_seq that is an instance of a sequence class

    ## channels    
    pi2_ge_time = 14*2
    ssm_ge = .110
    ssm_ef = 0.188
    pre3_amp = 0.8
    pre_time = 30
    pre4_amp = 0.1
    post4_amp = -0.4
    post3_amp = -.2
    post_time = pre_time
    readout_amp = 0.1
    scaling_factor = 0
    
    
    
    #this is the first pi/2 pulse in the sequence
    pi2_ge = Pulse(start=5030, duration=-pi2_ge_time, amplitude=1, ssm_freq=ssm_ge, phase=0) #pulse is also a class p is an instance
    ringupdown_seq.add_sweep(channel=1, sweep_name='start', start=0, stop=-2000,initial_pulse=pi2_ge)
    pi2_ge.phase = 90
    ringupdown_seq.add_sweep(channel=2,  sweep_name='start', start=0, stop=-2000,initial_pulse=pi2_ge)
    #p.phase = 90 #make the pulse phase 90 degrees to get the single sideband modulation
    #rabi_seq.add_sweep(channel=2, sweep_name='width', start=0, stop=-200,initial_pulse=p)

    
    pi2_ge = Pulse(start=5060, duration=-pi2_ge_time, amplitude=1, ssm_freq=ssm_ge, phase=0) #pulse is also a class p is an instance
    ringupdown_seq.add_sweep(channel=1, sweep_name='none',initial_pulse=pi2_ge)
    pi2_ge.phase = 90
    ringupdown_seq.add_sweep(channel=2,  sweep_name='none',initial_pulse=pi2_ge)

    
    pre_pulse = Pulse(start = 5100,duration = -pre_time, amplitude=pre3_amp )
    ringupdown_seq.add_sweep(channel=3, sweep_name='none',initial_pulse=pre_pulse)
    pre_pulse = Pulse(start = 5100,duration = -pre_time, amplitude=pre4_amp )
    ringupdown_seq.add_sweep(channel=4, sweep_name='none',initial_pulse=pre_pulse)
    
    main_pulse = Pulse(start = 5100,duration = 1000, amplitude= readout_amp )
    ringupdown_seq.add_sweep(channel=4, sweep_name='none',initial_pulse=main_pulse)
    
    
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
    write_dir = r"C:\arbsequences\strong_dispersive_withPython\test_pulse_ringupdown"
    ringupdown_seq.write_sequence(base_name='foo', file_path=write_dir, use_range_01=False,num_offset=0)
##END geom
    
def pulsed_readout_only(): #this is pulsed readout to ring up and ring down cavity dfor e state
    file_length = 8000
    num_steps = 3
    ringupdown_seq = Sequence(file_length, num_steps) #this creates something called rabi_seq that is an instance of a sequence class

    ## channels    
    pi_ge_time = 40
    ssm_ge = .110
    pre3_amp = 0.8
    pre_time = 30
    pre4_amp = 0.1
    post4_amp = -0.4
    post3_amp = -.2
    post_time = pre_time
    readout_amp = 0.1
    
    #this is the first pi pulse in the sequence
    pi_ge = Pulse(start=4870, duration=-pi_ge_time, amplitude=1, ssm_freq=ssm_ge, phase=0) #pulse is also a class p is an instance
    ringupdown_seq.add_sweep(channel=1, sweep_name='none',initial_pulse=pi_ge)
    pi_ge.phase = 90
    ringupdown_seq.add_sweep(channel=2, sweep_name='none',initial_pulse=pi_ge)
    #p.phase = 90 #make the pulse phase 90 degrees to get the single sideband modulation
    #rabi_seq.add_sweep(channel=2, sweep_name='width', start=0, stop=-200,initial_pulse=p)
    
    
    pre_pulse = Pulse(start = 4900,duration = -pre_time, amplitude=pre3_amp )
    ringupdown_seq.add_sweep(channel=3, sweep_name='none',initial_pulse=pre_pulse)
    pre_pulse = Pulse(start = 4900,duration = -pre_time, amplitude=pre4_amp )
    ringupdown_seq.add_sweep(channel=4, sweep_name='none',initial_pulse=pre_pulse)
    
    main_pulse = Pulse(start = 5000,duration = -100, amplitude=readout_amp )
    ringupdown_seq.add_sweep(channel=4, sweep_name='none',initial_pulse=main_pulse)
    
    post_pulse = Pulse(start = 5030,duration = -post_time, amplitude=post3_amp )
    ringupdown_seq.add_sweep(channel=3, sweep_name='none',initial_pulse=post_pulse)
    post_pulse.amplitude=post4_amp
    ringupdown_seq.add_sweep(channel=4, sweep_name='none',initial_pulse=post_pulse)
    
    
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
        plt.imshow(channel4_ch[0:100,4800:5100], aspect='auto', extent=[4800,5100,100,0])
        plt.show()
        
    ## write output
    write_dir = r"C:\arbsequences\strong_dispersive_withPython\test_pulse_ringupdown"
    ringupdown_seq.write_sequence(base_name='foo', file_path=write_dir, use_range_01=False,num_offset=0)
##END geom
        
if __name__ == '__main__':
    pulsed_readout_ramsey()
    #rabi_200ns()
   # Ramsey_2us()