import numpy as np
import sys
sys.path.append(r"C:\Users\crow108\Documents\Python Scripts\sequence_generator")
from generator import *
import os
pi = np.pi
import matplotlib.pyplot as plt

def prep_GEF_pulsereadout( post4_amp = 0.85, post3_amp = 0.95): #this is pulsed readout to ring up and ring down cavity dfor e state
    file_length = 8000
    num_steps = 1
    ringupdown_seq = Sequence(file_length, num_steps) #this creates something called rabi_seq that is an instance of a sequence class

    ## channels    
    pi_ge_time = 40
    pi_ef_time  = 68
    ef_amp = 1
    ge_amp=1
    ssm_ge = .110
    ssm_ef = 0.208
    post_time = 50
    readout_amp = 0.01
    
    
    #FIRST PREP IS G, followed by readouts
  #  pi_ge = Pulse(start=5020, duration=-pi_ge_time, amplitude=ge_amp, ssm_freq=ssm_ge, phase=0) #pulse is also a class p is an instance
  #  ringupdown_seq.add_sweep(channel=1, sweep_name='none',initial_pulse=pi_ge)
  #  pi_ge.phase = 90
  #  ringupdown_seq.add_sweep(channel=2, sweep_name='none',initial_pulse=pi_ge)
    
   # pi_ef = Pulse(start=5090, duration=-pi_ef_time, amplitude=ef_amp, ssm_freq=ssm_ef, phase=90) #pulse is also a class p is an instance
   # ringupdown_seq.add_sweep(channel=1, sweep_name='none',initial_pulse=pi_ef)
   # pi_ef.phase = 0
   # ringupdown_seq.add_sweep(channel=2, sweep_name='none',initial_pulse=pi_ef)
#    pre_pulse = Pulse(start = 4700,duration = -pre_time, amplitude=scaling_factor*pre3_amp )
#    ringupdown_seq.add_sweep(channel=3, sweep_name='none',initial_pulse=pre_pulse)
#    pre_pulse = Pulse(start = 4700,duration = -pre_time, amplitude=scaling_factor*pre4_amp )
#    ringupdown_seq.add_sweep(channel=4, sweep_name='none',initial_pulse=pre_pulse)
    
#    main_pulse = Pulse(start = 4800,duration = -100, amplitude=scaling_factor*readout_amp )
#    ringupdown_seq.add_sweep(channel=4, sweep_name='none',initial_pulse=main_pulse)
#    
#    post_pulse = Pulse(start = 4830,duration = -post_time, amplitude=scaling_factor*post3_amp )
#    ringupdown_seq.add_sweep(channel=3, sweep_name='none',initial_pulse=post_pulse)
#    post_pulse.amplitude=scaling_factor*post4_amp
#    ringupdown_seq.add_sweep(channel=4, sweep_name='none',initial_pulse=post_pulse)
     
    #second readout
    
#    pre_pulse = Pulse(start = 5100,duration = -pre_time, amplitude=pre3_amp )
#    ringupdown_seq.add_sweep(channel=3, sweep_name='none',initial_pulse=pre_pulse)
#    pre_pulse = Pulse(start = 5100,duration = -pre_time, amplitude=pre4_amp )
#    ringupdown_seq.add_sweep(channel=4, sweep_name='none',initial_pulse=pre_pulse)
    
    main_pulse = Pulse(start = 5100,duration = 100, amplitude= readout_amp )
    ringupdown_seq.add_sweep(channel=4, sweep_name='none',initial_pulse=main_pulse)
    
    post_pulse = Pulse(start = 5200,duration = post_time, amplitude=readout_amp*post3_amp )
    ringupdown_seq.add_sweep(channel=3, sweep_name='none',initial_pulse=post_pulse)
    post_pulse.amplitude=readout_amp*post4_amp
    ringupdown_seq.add_sweep(channel=4, sweep_name='none',initial_pulse=post_pulse)
    
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
        #plt.imshow(channel1_ch[0:100,4600:5200], aspect='auto', extent=[4800,5100,100,0])
       # plt.show()
        
    ## write output
    write_dir = r"C:\arbsequences\strong_dispersive_withPython\GEF pulse readout"
    ringupdown_seq.write_sequence(base_name='foo', file_path=write_dir, use_range_01=False,num_offset=0)
    
    
    
    ringupdown_seq = Sequence(file_length, num_steps)
    #SECOND PREP IS E, followed by readouts
    
    pi_ge = Pulse(start=5020, duration=-pi_ge_time, amplitude=ge_amp, ssm_freq=ssm_ge, phase=0) #pulse is also a class p is an instance
    ringupdown_seq.add_sweep(channel=1, sweep_name='none',initial_pulse=pi_ge)
    pi_ge.phase = 90
    ringupdown_seq.add_sweep(channel=2, sweep_name='none',initial_pulse=pi_ge)
    
  #  pi_ef = Pulse(start=5090, duration=-pi_ef_time, amplitude=ef_amp, ssm_freq=ssm_ef, phase=90) #pulse is also a class p is an instance
  #  ringupdown_seq.add_sweep(channel=1, sweep_name='none',initial_pulse=pi_ef)
   # pi_ef.phase = 0
 #   ringupdown_seq.add_sweep(channel=2, sweep_name='none',initial_pulse=pi_ef)
#    ringupdown_seq.add_sweep(channel=2, sweep_name='none',initial_pulse=pi_ge)
#    pre_pulse = Pulse(start = 4700,duration = -pre_time, amplitude=scaling_factor*pre3_amp )
#    ringupdown_seq.add_sweep(channel=3, sweep_name='none',initial_pulse=pre_pulse)
#    pre_pulse = Pulse(start = 4700,duration = -pre_time, amplitude=scaling_factor*pre4_amp )
#    ringupdown_seq.add_sweep(channel=4, sweep_name='none',initial_pulse=pre_pulse)
#    
#    main_pulse = Pulse(start = 4800,duration = -100, amplitude=scaling_factor*readout_amp )
#    ringupdown_seq.add_sweep(channel=4, sweep_name='none',initial_pulse=main_pulse)
#    
#    post_pulse = Pulse(start = 4830,duration = -post_time, amplitude=scaling_factor*post3_amp )
#    ringupdown_seq.add_sweep(channel=3, sweep_name='none',initial_pulse=post_pulse)
#    post_pulse.amplitude=scaling_factor*post4_amp
#    ringupdown_seq.add_sweep(channel=4, sweep_name='none',initial_pulse=post_pulse)
#     
#    #second readout
#    
#    pre_pulse = Pulse(start = 5100,duration = -pre_time, amplitude=pre3_amp )
#    ringupdown_seq.add_sweep(channel=3, sweep_name='none',initial_pulse=pre_pulse)
#    pre_pulse = Pulse(start = 5100,duration = -pre_time, amplitude=pre4_amp )
#    ringupdown_seq.add_sweep(channel=4, sweep_name='none',initial_pulse=pre_pulse)
    
    main_pulse = Pulse(start = 5100,duration = 100, amplitude= readout_amp)
    ringupdown_seq.add_sweep(channel=4, sweep_name='none',initial_pulse=main_pulse)
    
    post_pulse = Pulse(start = 5200,duration = post_time, amplitude=readout_amp*post3_amp )
    ringupdown_seq.add_sweep(channel=3, sweep_name='none',initial_pulse=post_pulse)
    post_pulse.amplitude=readout_amp*post4_amp
    ringupdown_seq.add_sweep(channel=4, sweep_name='none',initial_pulse=post_pulse)
    
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
       # plt.imshow(channel1_ch[0:100,4600:5200], aspect='auto', extent=[4800,5100,100,0])
       # plt.show()
        
    ## write output
    write_dir = r"C:\arbsequences\strong_dispersive_withPython\GEF pulse readout"
    ringupdown_seq.write_sequence(base_name='foo', file_path=write_dir, use_range_01=False,num_offset=1)

     #THIRD PREP IS F, followed by readouts
     
    ringupdown_seq = Sequence(file_length, num_steps)
    
    #this is the first pi/2 pulse in the sequence
    pi_ge = Pulse(start=5020, duration=-pi_ge_time, amplitude=ge_amp, ssm_freq=ssm_ge, phase=0) #pulse is also a class p is an instance
    ringupdown_seq.add_sweep(channel=1, sweep_name='none',initial_pulse=pi_ge)
    pi_ge.phase = 90
    ringupdown_seq.add_sweep(channel=2, sweep_name='none',initial_pulse=pi_ge)
    #p.phase = 90 #make the pulse phase 90 degrees to get the single sideband modulation
    #rabi_seq.add_sweep(channel=2, sweep_name='width', start=0, stop=-200,initial_pulse=p)
    pi_ef = Pulse(start=5090, duration=-pi_ef_time, amplitude=ef_amp, ssm_freq=ssm_ef, phase=90) #pulse is also a class p is an instance
    ringupdown_seq.add_sweep(channel=1, sweep_name='none',initial_pulse=pi_ef)
    pi_ef.phase = 0
    ringupdown_seq.add_sweep(channel=2, sweep_name='none',initial_pulse=pi_ef)
#    
#    pre_pulse = Pulse(start = 4700,duration = -pre_time, amplitude=scaling_factor*pre3_amp )
#    ringupdown_seq.add_sweep(channel=3, sweep_name='none',initial_pulse=pre_pulse)
#    pre_pulse = Pulse(start = 4700,duration = -pre_time, amplitude=scaling_factor*pre4_amp )
#    ringupdown_seq.add_sweep(channel=4, sweep_name='none',initial_pulse=pre_pulse)
#    
#    main_pulse = Pulse(start = 4800,duration = -100, amplitude=scaling_factor*readout_amp )
#    ringupdown_seq.add_sweep(channel=4, sweep_name='none',initial_pulse=main_pulse)
#    
#    post_pulse = Pulse(start = 4830,duration = -post_time, amplitude=scaling_factor*post3_amp )
#    ringupdown_seq.add_sweep(channel=3, sweep_name='none',initial_pulse=post_pulse)
#    post_pulse.amplitude=scaling_factor*post4_amp
#    ringupdown_seq.add_sweep(channel=4, sweep_name='none',initial_pulse=post_pulse)
    
    #second readout
    
#    pre_pulse = Pulse(start = 5100,duration = -pre_time, amplitude=pre3_amp )
#    ringupdown_seq.add_sweep(channel=3, sweep_name='none',initial_pulse=pre_pulse)
#    pre_pulse = Pulse(start = 5100,duration = -pre_time, amplitude=pre4_amp )
#    ringupdown_seq.add_sweep(channel=4, sweep_name='none',initial_pulse=pre_pulse)
    
    main_pulse = Pulse(start = 5100,duration = 100, amplitude= readout_amp )
    ringupdown_seq.add_sweep(channel=4, sweep_name='none',initial_pulse=main_pulse)
    
    post_pulse = Pulse(start = 5200,duration = post_time, amplitude=readout_amp*post3_amp )
    ringupdown_seq.add_sweep(channel=3, sweep_name='none',initial_pulse=post_pulse)
    post_pulse.amplitude=readout_amp*post4_amp
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
        #plt.imshow(channel1_ch[0:100,4600:5200], aspect='auto', extent=[4800,5100,100,0])
       # plt.show()
        
    ## write output

    write_dir = r"C:\arbsequences\strong_dispersive_withPython\GEF pulse readout"
    ringupdown_seq.write_sequence(base_name='foo', file_path=write_dir, use_range_01=False,num_offset=2)
#    ringupdown_seq.load_sequence('128.252.134.4', base_name='foo', file_path=write_dir, num_offset=0)
##END geom

    
def pulsed_readout_ramsey_EF(): #this is pulsed readout to ring up and ring down cavity dfor e state
    file_length = 8000
    num_steps = 101
    ringupdown_seq = Sequence(file_length, num_steps) #this creates something called rabi_seq that is an instance of a sequence class

    ## channels    
    pi_ge_time = 40
    pi2_ef_time  = 34
    pi2_ef_amp = 1
    ssm_ge = .110
    ssm_ef = 0.208
    post4_amp = 0.85
    post3_amp = 0.95
    post_time = 50
    readout_amp = 0.02
    
    
    
    #this is the first pi/2 pulse in the sequence
    pi_ge = Pulse(start=4820, duration=-pi_ge_time, amplitude=1, ssm_freq=ssm_ge, phase=0) #pulse is also a class p is an instance
    ringupdown_seq.add_sweep(channel=1, sweep_name='none',initial_pulse=pi_ge)
    pi_ge.phase = 90
    ringupdown_seq.add_sweep(channel=2, sweep_name='none',initial_pulse=pi_ge)
    #p.phase = 90 #make the pulse phase 90 degrees to get the single sideband modulation
    #rabi_seq.add_sweep(channel=2, sweep_name='width', start=0, stop=-200,initial_pulse=p)
    pi2_ef = Pulse(start=4860, duration=-pi2_ef_time, amplitude=pi2_ef_amp, ssm_freq=ssm_ef, phase=90) #pulse is also a class p is an instance
    ringupdown_seq.add_sweep(channel=1, sweep_name='none',initial_pulse=pi2_ef)
    pi2_ef.phase = 0
    ringupdown_seq.add_sweep(channel=2, sweep_name='none',initial_pulse=pi2_ef)
    
    main_pulse = Pulse(start = 4960,duration = -100, amplitude=readout_amp)
    ringupdown_seq.add_sweep(channel=4, sweep_name='none',initial_pulse=main_pulse)
    
    post_pulse = Pulse(start = 5010,duration = -post_time, amplitude=readout_amp*post3_amp )
    ringupdown_seq.add_sweep(channel=3, sweep_name='none',initial_pulse=post_pulse)
    post_pulse.amplitude=readout_amp*post4_amp
    ringupdown_seq.add_sweep(channel=4, sweep_name='none',initial_pulse=post_pulse)
    
    pi2_ef = Pulse(start=5050, duration=-pi2_ef_time, amplitude=pi2_ef_amp, ssm_freq=ssm_ef, phase=90) #pulse is also a class p is an instance
    ringupdown_seq.add_sweep(channel=1, sweep_name='phase',start=0,stop=1800,initial_pulse=pi2_ef)
    pi2_ef.phase = 0
    ringupdown_seq.add_sweep(channel=2, sweep_name='phase',start=0,stop=1800,initial_pulse=pi2_ef)
       #this is the second  pi/2 pulse in the sequence
    pi_ge = Pulse(start=5090, duration=-pi_ge_time, amplitude=1, ssm_freq=ssm_ge, phase=0) #pulse is also a class p is an instance
    ringupdown_seq.add_sweep(channel=1, sweep_name='none',initial_pulse=pi_ge)
    pi_ge.phase = 90
    ringupdown_seq.add_sweep(channel=2, sweep_name='none',initial_pulse=pi_ge)
    
    
    #second readout
    
    main_pulse = Pulse(start = 5100,duration = 1000, amplitude= 1 )
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
        plt.imshow(channel1_ch[0:100,4600:5200], aspect='auto', extent=[4800,5100,100,0])
        plt.show()
        
    ## write output
    write_dir = r"C:\arbsequences\strong_dispersive_withPython\test_pulse_ringupdown_bin"
    ringupdown_seq.write_sequence(base_name='foo', file_path=write_dir, use_range_01=False,num_offset=0, write_binary=True)
    ringupdown_seq.load_sequence('128.252.134.4', base_name='foo', file_path=write_dir, num_offset=0)
##END geom
    
def pulsed_readout_rabi_EF_test(): #this is pulsed readout to ring up and ring down cavity dfor e state
    file_length = 8000
    num_steps = 101
    ringupdown_seq = Sequence(file_length, num_steps) #this creates something called rabi_seq that is an instance of a sequence class

    ## channels  
    rabi_time=100
    pi_ge_time = 22
    pi2_ef_time  = 8
    pi2_ef_amp = 0.5
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
    pi_ge = Pulse(start=4670, duration=-pi_ge_time, amplitude=1, ssm_freq=ssm_ge, phase=0) #pulse is also a class p is an instance
    ringupdown_seq.add_sweep(channel=1, sweep_name='start',start=0,stop=-rabi_time,initial_pulse=pi_ge)
    pi_ge.phase = 90
    ringupdown_seq.add_sweep(channel=2, sweep_name='start',start=0,stop=-rabi_time,initial_pulse=pi_ge)
    #p.phase = 90 #make the pulse phase 90 degrees to get the single sideband modulation
    #rabi_seq.add_sweep(channel=2, sweep_name='width', start=0, stop=-200,initial_pulse=p)
    
    pre_pulse = Pulse(start = 4700,duration = -pre_time, amplitude=scaling_factor*pre3_amp )
    ringupdown_seq.add_sweep(channel=3, sweep_name='start',start=0,stop=-rabi_time,initial_pulse=pre_pulse)
    pre_pulse = Pulse(start = 4700,duration = -pre_time, amplitude=scaling_factor*pre4_amp )
    ringupdown_seq.add_sweep(channel=4, sweep_name='start',start=0,stop=-rabi_time,initial_pulse=pre_pulse)
    
    main_pulse = Pulse(start = 4800,duration = -100, amplitude=scaling_factor*readout_amp )
    ringupdown_seq.add_sweep(channel=4, sweep_name='start',start=0,stop=-rabi_time,initial_pulse=main_pulse)
    
    post_pulse = Pulse(start = 4830,duration = -post_time, amplitude=scaling_factor*post3_amp )
    ringupdown_seq.add_sweep(channel=3, sweep_name='start',start=0,stop=-rabi_time,initial_pulse=post_pulse)
    post_pulse.amplitude=scaling_factor*post4_amp
    ringupdown_seq.add_sweep(channel=4, sweep_name='start',start=0,stop=-rabi_time,initial_pulse=post_pulse)
    
    rabi_ef = Pulse(start=5040, duration=0, amplitude=pi2_ef_amp, ssm_freq=ssm_ef, phase=90) #pulse is also a class p is an instance
    ringupdown_seq.add_sweep(channel=1, sweep_name='width',start=0,stop=-rabi_time,initial_pulse=rabi_ef)
    rabi_ef.phase = 0
    ringupdown_seq.add_sweep(channel=2, sweep_name='width',start=0,stop=-rabi_time,initial_pulse=rabi_ef)
       #this is the second  pi/2 pulse in the sequence
    pi_ge = Pulse(start=5040, duration=pi_ge_time, amplitude=1, ssm_freq=ssm_ge, phase=0) #pulse is also a class p is an instance
    ringupdown_seq.add_sweep(channel=1, sweep_name='none',initial_pulse=pi_ge)
    pi_ge.phase = 90
    ringupdown_seq.add_sweep(channel=2, sweep_name='none',initial_pulse=pi_ge)
    
    
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
        plt.imshow(channel1_ch[0:100,4600:5200], aspect='auto', extent=[4800,5100,100,0])
        plt.show()
        
    ## write output
    write_dir = r"C:\arbsequences\strong_dispersive_withPython\test_pulse_ringupdown"
    ringupdown_seq.write_sequence(base_name='foo', file_path=write_dir, use_range_01=False,num_offset=0)
##END geom
    
def pulsed_readout_rabi_EF_test_2(): #this is pulsed readout to ring up and ring down cavity dfor e state
    file_length = 8000
    num_steps = 101
    ringupdown_seq = Sequence(file_length, num_steps) #this creates something called rabi_seq that is an instance of a sequence class

    ## channels  
    rabi_time=100
    pi_ge_time = 22
    pi_ef_time=17
    pi2_ef_time  = 8
    pi2_ef_amp = 0.5
    ssm_ge = .110
    ssm_ef = 0.188
    pre3_amp = 0.8
    pre_time = 30
    pre4_amp = 0.1
    post4_amp = -0.4
    post3_amp = -.2
    post_time = pre_time
    readout_amp = 0.1
    scaling_factor = 0.8
    
    
    
    #this is the first pi/2 pulse in the sequence
    pi_ge = Pulse(start=4650, duration=-pi_ge_time, amplitude=1, ssm_freq=ssm_ge, phase=0) #pulse is also a class p is an instance
    ringupdown_seq.add_sweep(channel=1, sweep_name='start',start=0,stop=-rabi_time,initial_pulse=pi_ge)
    pi_ge.phase = 90
    ringupdown_seq.add_sweep(channel=2, sweep_name='start',start=0,stop=-rabi_time,initial_pulse=pi_ge)
    #p.phase = 90 #make the pulse phase 90 degrees to get the single sideband modulation
    #rabi_seq.add_sweep(channel=2, sweep_name='width', start=0, stop=-200,initial_pulse=p)
    pi_ef = Pulse(start=4670, duration=-pi_ef_time, amplitude=pi2_ef_amp, ssm_freq=ssm_ef, phase=90) #pulse is also a class p is an instance
    ringupdown_seq.add_sweep(channel=1, sweep_name='start',start=0,stop=-rabi_time,initial_pulse=pi_ef)
    pi_ef.phase = 0
    ringupdown_seq.add_sweep(channel=2, sweep_name='start',start=0,stop=-rabi_time,initial_pulse=pi_ef)
    
    pre_pulse = Pulse(start = 4700,duration = -pre_time, amplitude=scaling_factor*pre3_amp )
    ringupdown_seq.add_sweep(channel=3, sweep_name='start',start=0,stop=-rabi_time,initial_pulse=pre_pulse)
    pre_pulse = Pulse(start = 4700,duration = -pre_time, amplitude=scaling_factor*pre4_amp )
    ringupdown_seq.add_sweep(channel=4, sweep_name='start',start=0,stop=-rabi_time,initial_pulse=pre_pulse)
    
    main_pulse = Pulse(start = 4800,duration = -100, amplitude=scaling_factor*readout_amp )
    ringupdown_seq.add_sweep(channel=4, sweep_name='start',start=0,stop=-rabi_time,initial_pulse=main_pulse)
    
    post_pulse = Pulse(start = 4830,duration = -post_time, amplitude=scaling_factor*post3_amp )
    ringupdown_seq.add_sweep(channel=3, sweep_name='start',start=0,stop=-rabi_time,initial_pulse=post_pulse)
    post_pulse.amplitude=scaling_factor*post4_amp
    ringupdown_seq.add_sweep(channel=4, sweep_name='start',start=0,stop=-rabi_time,initial_pulse=post_pulse)
    
    rabi_ef = Pulse(start=5040, duration=0, amplitude=pi2_ef_amp, ssm_freq=ssm_ef, phase=90) #pulse is also a class p is an instance
    ringupdown_seq.add_sweep(channel=1, sweep_name='width',start=0,stop=-rabi_time,initial_pulse=rabi_ef)
    rabi_ef.phase = 0
    ringupdown_seq.add_sweep(channel=2, sweep_name='width',start=0,stop=-rabi_time,initial_pulse=rabi_ef)
       #this is the second  pi/2 pulse in the sequence
    pi_ge = Pulse(start=5040, duration=pi_ge_time, amplitude=1, ssm_freq=ssm_ge, phase=0) #pulse is also a class p is an instance
    ringupdown_seq.add_sweep(channel=1, sweep_name='none',initial_pulse=pi_ge)
    pi_ge.phase = 90
    ringupdown_seq.add_sweep(channel=2, sweep_name='none',initial_pulse=pi_ge)
    
    
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
        plt.imshow(channel1_ch[0:100,4600:5200], aspect='auto', extent=[4800,5100,100,0])
        plt.show()
        
    ## write output
    write_dir = r"C:\arbsequences\strong_dispersive_withPython\test_pulse_ringupdown"
    ringupdown_seq.write_sequence(base_name='foo', file_path=write_dir, use_range_01=False,num_offset=0)
##END geom
    
def pulsed_readout_rabi_GE_test(): #this is pulsed readout to ring up and ring down cavity dfor e state
    file_length = 8000
    num_steps = 101
    ringupdown_seq = Sequence(file_length, num_steps) #this creates something called rabi_seq that is an instance of a sequence class

    ## channels  
    rabi_time=100
    pi_ge_time = 22
    pi2_ef_time  = 8
    pi2_ef_amp = 0.5
    ssm_ge = .110
    ssm_ef = 0.188
    pre3_amp = 0.8
    pre_time = 30
    pre4_amp = 0.1
    post4_amp = -0.4
    post3_amp = -.2
    post_time = pre_time
    readout_amp = 0.1
    scaling_factor = 1
    
    
    
    #this is the first pi/2 pulse in the sequence
    pi_ge = Pulse(start=4670, duration=-pi_ge_time, amplitude=1, ssm_freq=ssm_ge, phase=0) #pulse is also a class p is an instance
    ringupdown_seq.add_sweep(channel=1, sweep_name='start',start=0,stop=-rabi_time,initial_pulse=pi_ge)
    pi_ge.phase = 90
    ringupdown_seq.add_sweep(channel=2, sweep_name='start',start=0,stop=-rabi_time,initial_pulse=pi_ge)
    #p.phase = 90 #make the pulse phase 90 degrees to get the single sideband modulation
    #rabi_seq.add_sweep(channel=2, sweep_name='width', start=0, stop=-200,initial_pulse=p)
    
    pre_pulse = Pulse(start = 4700,duration = -pre_time, amplitude=scaling_factor*pre3_amp )
    ringupdown_seq.add_sweep(channel=3, sweep_name='start',start=0,stop=-rabi_time,initial_pulse=pre_pulse)
    pre_pulse = Pulse(start = 4700,duration = -pre_time, amplitude=scaling_factor*pre4_amp )
    ringupdown_seq.add_sweep(channel=4, sweep_name='start',start=0,stop=-rabi_time,initial_pulse=pre_pulse)
    
    main_pulse = Pulse(start = 4800,duration = -100, amplitude=scaling_factor*readout_amp )
    ringupdown_seq.add_sweep(channel=4, sweep_name='start',start=0,stop=-rabi_time,initial_pulse=main_pulse)
    
    post_pulse = Pulse(start = 4830,duration = -post_time, amplitude=scaling_factor*post3_amp )
    ringupdown_seq.add_sweep(channel=3, sweep_name='start',start=0,stop=-rabi_time,initial_pulse=post_pulse)
    post_pulse.amplitude=scaling_factor*post4_amp
    ringupdown_seq.add_sweep(channel=4, sweep_name='start',start=0,stop=-rabi_time,initial_pulse=post_pulse)
    
    rabi_ge = Pulse(start=5040, duration=0, amplitude=1, ssm_freq=ssm_ge, phase=0) #pulse is also a class p is an instance
    ringupdown_seq.add_sweep(channel=1, sweep_name='width',start=0,stop=-rabi_time,initial_pulse=rabi_ge)
    rabi_ge.phase = 90
    ringupdown_seq.add_sweep(channel=2, sweep_name='width',start=0,stop=-rabi_time,initial_pulse=rabi_ge)
    
    
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
        plt.imshow(channel1_ch[0:200,4500:5100], aspect='auto', extent=[4500,5100,100,0])
        plt.show()
        
    ## write output
    write_dir = r"C:\arbsequences\strong_dispersive_withPython\test_pulse_ringupdown"
    ringupdown_seq.write_sequence(base_name='foo', file_path=write_dir, use_range_01=False,num_offset=0)
##END geom
def pulsed_readout_rabi_GE_test_2(): #this is pulsed readout to ring up and ring down cavity dfor e state
    file_length = 8000
    num_steps = 101
    ringupdown_seq = Sequence(file_length, num_steps) #this creates something called rabi_seq that is an instance of a sequence class

    ## channels  
    rabi_time=100
    pi_ge_time = 22
    pi2_ef_time  = 8
    pi2_ef_amp = 0.5
    ssm_ge = .110
    ssm_ef = 0.188
    pre3_amp = 0.8
    pre_time = 30
    pre4_amp = 0.1
    post4_amp = -0.3
    post3_amp = -0.6
    post_time = pre_time
    readout_amp = 0.1
    scaling_factor = 0
    

    
    pre_pulse = Pulse(start = 4700,duration = -pre_time, amplitude=scaling_factor*pre3_amp )
    ringupdown_seq.add_sweep(channel=3, sweep_name='start',start=0,stop=-rabi_time,initial_pulse=pre_pulse)
    pre_pulse = Pulse(start = 4700,duration = -pre_time, amplitude=scaling_factor*pre4_amp )
    ringupdown_seq.add_sweep(channel=4, sweep_name='start',start=0,stop=-rabi_time,initial_pulse=pre_pulse)
    
    main_pulse = Pulse(start = 4800,duration = -100, amplitude=scaling_factor*readout_amp )
    ringupdown_seq.add_sweep(channel=4, sweep_name='start',start=0,stop=-rabi_time,initial_pulse=main_pulse)
    
    post_pulse = Pulse(start = 4830,duration = -post_time, amplitude=scaling_factor*post3_amp )
    ringupdown_seq.add_sweep(channel=3, sweep_name='start',start=0,stop=-rabi_time,initial_pulse=post_pulse)
    post_pulse.amplitude=scaling_factor*post4_amp
    ringupdown_seq.add_sweep(channel=4, sweep_name='start',start=0,stop=-rabi_time,initial_pulse=post_pulse)
    
    rabi_ge = Pulse(start=5040, duration=0, amplitude=1, ssm_freq=ssm_ge, phase=0) #pulse is also a class p is an instance
    ringupdown_seq.add_sweep(channel=1, sweep_name='width',start=0,stop=-rabi_time,initial_pulse=rabi_ge)
    rabi_ge.phase = 90
    ringupdown_seq.add_sweep(channel=2, sweep_name='width',start=0,stop=-rabi_time,initial_pulse=rabi_ge)
    
    
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
        plt.imshow(channel1_ch[0:200,4500:5100], aspect='auto', extent=[4500,5100,100,0])
        plt.show()
        
    ## write output
    write_dir = r"C:\arbsequences\strong_dispersive_withPython\test_pulse_ringupdown"
    ringupdown_seq.write_sequence(base_name='foo', file_path=write_dir, use_range_01=False,num_offset=0)
##END geom
    
def Epop(): #this is pulsed readout to ring up and ring down cavity dfor e state
    file_length = 8000
    num_steps = 101
    ringupdown_seq = Sequence(file_length, num_steps) #this creates something called rabi_seq that is an instance of a sequence class

    ## channels  
    rabi_time=100
    pi_ge_time = 22
    pi2_ef_time  = 8
    pi2_ef_amp = 0.5
    ssm_ge = .110
    ssm_ef = 0.188
    pre3_amp = 0.8
    pre_time = 30
    pre4_amp = 0.1
    post4_amp = -0.4
    post3_amp = -.2
    post_time = pre_time
    readout_amp = 0.1
    scaling_factor = 1
    
    
    
    #this is the first pi/2 pulse in the sequence
    pi_ge = Pulse(start=4670, duration=-pi_ge_time, amplitude=1, ssm_freq=ssm_ge, phase=0) #pulse is also a class p is an instance
    ringupdown_seq.add_sweep(channel=1, sweep_name='none',initial_pulse=pi_ge)
    pi_ge.phase = 90
    ringupdown_seq.add_sweep(channel=2, sweep_name='none',initial_pulse=pi_ge)
    #p.phase = 90 #make the pulse phase 90 degrees to get the single sideband modulation
    #rabi_seq.add_sweep(channel=2, sweep_name='width', start=0, stop=-200,initial_pulse=p)
    
    pre_pulse = Pulse(start = 4700,duration = -pre_time, amplitude=0 )
    ringupdown_seq.add_sweep(channel=3, sweep_name='amplitude',start=0,stop=scaling_factor*pre3_amp, initial_pulse=pre_pulse)
    pre_pulse = Pulse(start = 4700,duration = -pre_time, amplitude=0 )
    ringupdown_seq.add_sweep(channel=4, sweep_name='amplitude',start=0,stop=scaling_factor*pre4_amp,initial_pulse=pre_pulse)
    
    main_pulse = Pulse(start = 4800,duration = -100, amplitude=0 )
    ringupdown_seq.add_sweep(channel=4, sweep_name='amplitude',start=0,stop=scaling_factor*readout_amp,initial_pulse=main_pulse)
    
    post_pulse = Pulse(start = 4830,duration = -post_time, amplitude=0 )
    ringupdown_seq.add_sweep(channel=3, sweep_name='amplitude',start=0,stop=scaling_factor*post3_amp,initial_pulse=post_pulse)
    ringupdown_seq.add_sweep(channel=4, sweep_name='amplitude',start=0,stop=scaling_factor*post3_amp,initial_pulse=post_pulse)
        
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
        plt.imshow(channel1_ch[0:200,4500:5100], aspect='auto', extent=[4500,5100,100,0])
        plt.show()
        
    ## write output
    write_dir = r"C:\arbsequences\strong_dispersive_withPython\test_pulse_ringupdown"
    ringupdown_seq.write_sequence(base_name='foo', file_path=write_dir, use_range_01=False,num_offset=0)

    
def Fpop_G(): #this is pulsed readout to ring up and ring down cavity dfor e state
    file_length = 8000
    num_steps = 101
    ringupdown_seq = Sequence(file_length, num_steps) #this creates something called rabi_seq that is an instance of a sequence class

    ## channels  
    rabi_time=100
    pi_ge_time = 22
    pi2_ef_time  = 8
    pi_ef_time=17
    pi2_ef_amp = 0.5
    ssm_ge = .110
    ssm_ef = 0.188
    pre3_amp = 0.8
    pre_time = 30
    pre4_amp = 0.1
    post4_amp = -0.4
    post3_amp = -.2
    post_time = pre_time
    readout_amp = 0.1
    scaling_factor = 1
    
    
     #this is the first pi/2 pulse in the sequence
    pi_ge = Pulse(start=4650, duration=-pi_ge_time, amplitude=1, ssm_freq=ssm_ge, phase=0) #pulse is also a class p is an instance
    ringupdown_seq.add_sweep(channel=1, sweep_name='none',initial_pulse=pi_ge)
    pi_ge.phase = 90
    ringupdown_seq.add_sweep(channel=2, sweep_name='none',initial_pulse=pi_ge)
    #p.phase = 90 #make the pulse phase 90 degrees to get the single sideband modulation
    #rabi_seq.add_sweep(channel=2, sweep_name='width', start=0, stop=-200,initial_pulse=p)
    pi_ef = Pulse(start=4670, duration=-pi_ef_time, amplitude=pi2_ef_amp, ssm_freq=ssm_ef, phase=90) #pulse is also a class p is an instance
    ringupdown_seq.add_sweep(channel=1, sweep_name='none',initial_pulse=pi_ef)
    pi_ef.phase = 0
    ringupdown_seq.add_sweep(channel=2, sweep_name='none',initial_pulse=pi_ef)
    
    pre_pulse = Pulse(start = 4700,duration = -pre_time, amplitude=0 )
    ringupdown_seq.add_sweep(channel=3, sweep_name='amplitude',start=0,stop=scaling_factor*pre3_amp, initial_pulse=pre_pulse)
    pre_pulse = Pulse(start = 4700,duration = -pre_time, amplitude=0 )
    ringupdown_seq.add_sweep(channel=4, sweep_name='amplitude',start=0,stop=scaling_factor*pre4_amp,initial_pulse=pre_pulse)
    
    main_pulse = Pulse(start = 4800,duration = -100, amplitude=0 )
    ringupdown_seq.add_sweep(channel=4, sweep_name='amplitude',start=0,stop=scaling_factor*readout_amp,initial_pulse=main_pulse)
    
    post_pulse = Pulse(start = 4830,duration = -post_time, amplitude=0 )
    ringupdown_seq.add_sweep(channel=3, sweep_name='amplitude',start=0,stop=scaling_factor*post3_amp,initial_pulse=post_pulse)
    ringupdown_seq.add_sweep(channel=4, sweep_name='amplitude',start=0,stop=scaling_factor*post3_amp,initial_pulse=post_pulse)
        
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
        plt.imshow(channel1_ch[0:200,4500:5100], aspect='auto', extent=[4500,5100,100,0])
        plt.show()
        
    ## write output
    write_dir = r"C:\arbsequences\strong_dispersive_withPython\test_pulse_ringupdown"
    ringupdown_seq.write_sequence(base_name='foo', file_path=write_dir, use_range_01=False,num_offset=0)
    #this is the first pi/2 pulse in the sequence
    
def Fpop_E(): #this is pulsed readout to ring up and ring down cavity dfor e state
    file_length = 8000
    num_steps = 101
    ringupdown_seq = Sequence(file_length, num_steps) #this creates something called rabi_seq that is an instance of a sequence class

     ## channels  
    rabi_time=100
    pi_ge_time = 22
    pi2_ef_time  = 8
    pi_ef_time=17
    pi2_ef_amp = 0.5
    ssm_ge = .110
    ssm_ef = 0.188
    pre3_amp = 0.8
    pre_time = 30
    pre4_amp = 0.1
    post4_amp = -0.4
    post3_amp = -.2
    post_time = pre_time
    readout_amp = 0.1
    scaling_factor = 1
    
    
     #this is the first pi/2 pulse in the sequence
    pi_ge = Pulse(start=4650, duration=-pi_ge_time, amplitude=1, ssm_freq=ssm_ge, phase=0) #pulse is also a class p is an instance
    ringupdown_seq.add_sweep(channel=1, sweep_name='none',initial_pulse=pi_ge)
    pi_ge.phase = 90
    ringupdown_seq.add_sweep(channel=2, sweep_name='none',initial_pulse=pi_ge)
    #p.phase = 90 #make the pulse phase 90 degrees to get the single sideband modulation
    #rabi_seq.add_sweep(channel=2, sweep_name='width', start=0, stop=-200,initial_pulse=p)
    pi_ef = Pulse(start=4670, duration=-pi_ef_time, amplitude=pi2_ef_amp, ssm_freq=ssm_ef, phase=90) #pulse is also a class p is an instance
    ringupdown_seq.add_sweep(channel=1, sweep_name='none',initial_pulse=pi_ef)
    pi_ef.phase = 0
    ringupdown_seq.add_sweep(channel=2, sweep_name='none',initial_pulse=pi_ef)
    
    pre_pulse = Pulse(start = 4700,duration = -pre_time, amplitude=0 )
    ringupdown_seq.add_sweep(channel=3, sweep_name='amplitude',start=0,stop=scaling_factor*pre3_amp, initial_pulse=pre_pulse)
    pre_pulse = Pulse(start = 4700,duration = -pre_time, amplitude=0 )
    ringupdown_seq.add_sweep(channel=4, sweep_name='amplitude',start=0,stop=scaling_factor*pre4_amp,initial_pulse=pre_pulse)
    
    main_pulse = Pulse(start = 4800,duration = -100, amplitude=0 )
    ringupdown_seq.add_sweep(channel=4, sweep_name='amplitude',start=0,stop=scaling_factor*readout_amp,initial_pulse=main_pulse)
    
    post_pulse = Pulse(start = 4830,duration = -post_time, amplitude=0 )
    ringupdown_seq.add_sweep(channel=3, sweep_name='amplitude',start=0,stop=scaling_factor*post3_amp,initial_pulse=post_pulse)
    ringupdown_seq.add_sweep(channel=4, sweep_name='amplitude',start=0,stop=scaling_factor*post3_amp,initial_pulse=post_pulse)
        
    #second readout
    pi_ef = Pulse(start=4850, duration=-pi_ef_time, amplitude=pi2_ef_amp, ssm_freq=ssm_ef, phase=90) #pulse is also a class p is an instance
    ringupdown_seq.add_sweep(channel=1, sweep_name='none',initial_pulse=pi_ef)
    pi_ef.phase = 0
    ringupdown_seq.add_sweep(channel=2, sweep_name='none',initial_pulse=pi_ef) 
    ## markers
    
    pre_pulse = Pulse(start = 5100,duration = -pre_time, amplitude=pre3_amp )
    ringupdown_seq.add_sweep(channel=3, sweep_name='none',initial_pulse=pre_pulse)
    pre_pulse = Pulse(start = 5100,duration = -pre_time, amplitude=pre4_amp )
    ringupdown_seq.add_sweep(channel=4, sweep_name='none',initial_pulse=pre_pulse)
    
    main_pulse = Pulse(start = 5100,duration = 1000, amplitude= readout_amp )
    ringupdown_seq.add_sweep(channel=4, sweep_name='none',initial_pulse=main_pulse)
   
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
        plt.imshow(channel1_ch[0:200,4500:5100], aspect='auto', extent=[4500,5100,100,0])
        plt.show()
        
    ## write output
    write_dir = r"C:\arbsequences\strong_dispersive_withPython\test_pulse_ringupdown"
    ringupdown_seq.write_sequence(base_name='foo', file_path=write_dir, use_range_01=False,num_offset=0)
    #this is the first pi/2 pulse in the sequence
    ## channels  
    
def pulsed_readout_ramsey_EF_conti(): #this is pulsed readout to ring up and ring down cavity dfor e state
    file_length = 8000
    num_steps = 101
    ringupdown_seq = Sequence(file_length, num_steps) #this creates something called rabi_seq that is an instance of a sequence class

    ## channels    
    pi_ge_time = 22
    pi2_ef_time  = 8
    pi2_ef_amp = 0.5
    ssm_ge = .110
    ssm_ef = 0.188
    pre3_amp = 0.8
    pre_time = 30
    pre4_amp = 0.1
    post4_amp = -0.4
    post3_amp = -.2
    post_time = pre_time
    readout_amp = 0.1
    scaling_factor = 0.6
    
    
    
    #this is the first pi/2 pulse in the sequence
    pi_ge = Pulse(start=4660, duration=-pi_ge_time, amplitude=1, ssm_freq=ssm_ge, phase=0) #pulse is also a class p is an instance
    ringupdown_seq.add_sweep(channel=1, sweep_name='none',initial_pulse=pi_ge)
    pi_ge.phase = 90
    ringupdown_seq.add_sweep(channel=2, sweep_name='none',initial_pulse=pi_ge)
    #p.phase = 90 #make the pulse phase 90 degrees to get the single sideband modulation
    #rabi_seq.add_sweep(channel=2, sweep_name='width', start=0, stop=-200,initial_pulse=p)
    pi2_ef = Pulse(start=4670, duration=-pi2_ef_time, amplitude=pi2_ef_amp, ssm_freq=ssm_ef, phase=90) #pulse is also a class p is an instance
    ringupdown_seq.add_sweep(channel=1, sweep_name='none',initial_pulse=pi2_ef)
    pi2_ef.phase = 0
    ringupdown_seq.add_sweep(channel=2, sweep_name='none',initial_pulse=pi2_ef)
    
    main_pulse = Pulse(start = 4800,duration = -130, amplitude=scaling_factor*readout_amp )
    ringupdown_seq.add_sweep(channel=4, sweep_name='none',initial_pulse=main_pulse)
    
    post_pulse = Pulse(start = 4830,duration = -post_time, amplitude=scaling_factor*post3_amp )
    ringupdown_seq.add_sweep(channel=3, sweep_name='none',initial_pulse=post_pulse)
    post_pulse.amplitude=scaling_factor*post4_amp
    ringupdown_seq.add_sweep(channel=4, sweep_name='none',initial_pulse=post_pulse)
    
    pi2_ef = Pulse(start=5040, duration=-pi2_ef_time, amplitude=pi2_ef_amp, ssm_freq=ssm_ef, phase=90) #pulse is also a class p is an instance
    ringupdown_seq.add_sweep(channel=1, sweep_name='phase',start=0,stop=1800,initial_pulse=pi2_ef)
    pi2_ef.phase = 0
    ringupdown_seq.add_sweep(channel=2, sweep_name='phase',start=0,stop=1800,initial_pulse=pi2_ef)
       #this is the second  pi/2 pulse in the sequence
    pi_ge = Pulse(start=5040, duration=pi_ge_time, amplitude=1, ssm_freq=ssm_ge, phase=0) #pulse is also a class p is an instance
    ringupdown_seq.add_sweep(channel=1, sweep_name='none',initial_pulse=pi_ge)
    pi_ge.phase = 90
    ringupdown_seq.add_sweep(channel=2, sweep_name='none',initial_pulse=pi_ge)
    
    
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
        plt.imshow(channel1_ch[0:100,4600:5200], aspect='auto', extent=[4800,5100,100,0])
        plt.show()
        
    ## write output
    write_dir = r"C:\arbsequences\strong_dispersive_withPython\test_pulse_ringupdown"
    ringupdown_seq.write_sequence(base_name='foo', file_path=write_dir, use_range_01=False,num_offset=0)
    
def pulsed_readout_ramsey_GE(): #this is pulsed readout to ring up and ring down cavity dfor e state
    file_length = 8000
    num_steps = 101
    ringupdown_seq = Sequence(file_length, num_steps) #this creates something called rabi_seq that is an instance of a sequence class

    ## channels    
    pi_ge_time = 40
    pi2_ge_time = 20
    ssm_ge = .110
    post4_amp = 0.85
    post3_amp = 0.95
    post_time = 50
    readout_amp=0.01
    
    
    #this is the first pi/2 pulse in the sequence
    pi2_ge = Pulse(start=4880, duration=-pi2_ge_time, amplitude=1, ssm_freq=ssm_ge, phase=0) #pulse is also a class p is an instance
    ringupdown_seq.add_sweep(channel=1, sweep_name='none',initial_pulse=pi2_ge)
    pi2_ge.phase = 90
    ringupdown_seq.add_sweep(channel=2, sweep_name='none',initial_pulse=pi2_ge)
    #p.phase = 90 #make the pulse phase 90 degrees to get the single sideband modulation
    #rabi_seq.add_sweep(channel=2, sweep_name='width', start=0, stop=-200,initial_pulse=p)
    
    main_pulse = Pulse(start = 4980,duration = -100, amplitude=readout_amp )
    ringupdown_seq.add_sweep(channel=4, sweep_name='none',initial_pulse=main_pulse)
    
    post_pulse = Pulse(start = 5030,duration = -post_time, amplitude=readout_amp*post3_amp )
    ringupdown_seq.add_sweep(channel=3, sweep_name='none',initial_pulse=post_pulse)
    post_pulse.amplitude=readout_amp*post4_amp
    ringupdown_seq.add_sweep(channel=4, sweep_name='none',initial_pulse=post_pulse)
    
       #this is the second  pi/2 pulse in the sequence
    pi2_ge = Pulse(start=5090, duration=-pi2_ge_time, amplitude=1, ssm_freq=ssm_ge, phase=0) #pulse is also a class p is an instance
    ringupdown_seq.add_sweep(channel=1, sweep_name='phase',start=0, stop=1800,initial_pulse=pi2_ge)
    pi2_ge.phase = 90
    ringupdown_seq.add_sweep(channel=2, sweep_name='phase',start=0, stop=1800,initial_pulse=pi2_ge)
    
    
    #second readout
    
    main_pulse = Pulse(start = 5100,duration = 1000, amplitude=1 )
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
        plt.imshow(channel1_ch[0:100,4700:6000], aspect='auto', extent=[4800,5100,100,0])
        plt.show()
        
    ## write output
    write_dir = r"C:\arbsequences\strong_dispersive_withPython\test_pulse_ringupdown_bin"
    ringupdown_seq.write_sequence(base_name='foo', file_path=write_dir, use_range_01=False,num_offset=0, write_binary=True)
    ringupdown_seq.load_sequence('128.252.134.4', base_name='foo', file_path=write_dir, num_offset=0)
    
def pulsed_readout_ramsey_GE_conti(): #this is pulsed readout to ring up and ring down cavity dfor e state
    file_length = 8000
    num_steps = 101
    ringupdown_seq = Sequence(file_length, num_steps) #this creates something called rabi_seq that is an instance of a sequence class

    ## channels    
    pi_ge_time = 22
    pi2_ge_time = 11
    pi2_ef_time  = 8
    pi2_ef_amp = 0.5
    ssm_ge = .110
    ssm_ef = 0.188
    pre3_amp = 0.8
    pre_time = 30
    pre4_amp = 0.1
    post4_amp = -0.4
    post3_amp = -.2
    post_time = pre_time
    readout_amp = 0.1
    scaling_factor = 0.6
    
    
    
    #this is the first pi/2 pulse in the sequence
    pi2_ge = Pulse(start=4880, duration=-pi2_ge_time, amplitude=1, ssm_freq=ssm_ge, phase=0) #pulse is also a class p is an instance
    ringupdown_seq.add_sweep(channel=1, sweep_name='none',initial_pulse=pi2_ge)
    pi2_ge.phase = 90
    ringupdown_seq.add_sweep(channel=2, sweep_name='none',initial_pulse=pi2_ge)
    #p.phase = 90 #make the pulse phase 90 degrees to get the single sideband modulation
    #rabi_seq.add_sweep(channel=2, sweep_name='width', start=0, stop=-200,initial_pulse=p)
    
    main_pulse = Pulse(start = 5010,duration = -130, amplitude=scaling_factor*readout_amp )
    ringupdown_seq.add_sweep(channel=4, sweep_name='none',initial_pulse=main_pulse)
    
    post_pulse = Pulse(start = 5040,duration = -post_time, amplitude=scaling_factor*post3_amp )
    ringupdown_seq.add_sweep(channel=3, sweep_name='none',initial_pulse=post_pulse)
    post_pulse.amplitude=scaling_factor*post4_amp
    ringupdown_seq.add_sweep(channel=4, sweep_name='none',initial_pulse=post_pulse)
    
       #this is the second  pi/2 pulse in the sequence
    pi2_ge = Pulse(start=5040, duration=pi2_ge_time, amplitude=1, ssm_freq=ssm_ge, phase=0) #pulse is also a class p is an instance
    ringupdown_seq.add_sweep(channel=1, sweep_name='phase',start=0, stop=1800,initial_pulse=pi2_ge)
    pi2_ge.phase = 90
    ringupdown_seq.add_sweep(channel=2, sweep_name='phase',start=0, stop=1800,initial_pulse=pi2_ge)
    
    
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
        plt.imshow(channel1_ch[0:100,4700:6000], aspect='auto', extent=[4800,5100,100,0])
        plt.show()
        
    ## write output
    write_dir = r"C:\arbsequences\strong_dispersive_withPython\test_pulse_ringupdown"
    ringupdown_seq.write_sequence(base_name='foo', file_path=write_dir, use_range_01=False,num_offset=0)
    
def ramsey_GE(): #this is pulsed readout to ring up and ring down cavity dfor e state
    file_length = 8000
    num_steps = 101
    ringupdown_seq = Sequence(file_length, num_steps) #this creates something called rabi_seq that is an instance of a sequence class

    ## channels  
    ramsey_time=5000
    pi_ge_time = 28
    pi2_ge_time = 14
    ge_amp=.5
    
    ssm_ge = 0.110
    ssm_ef = 0.210
    pre3_amp = 0.8
    pre_time = 30
    pre4_amp = 0.1
    post4_amp = -0.4
    post3_amp = -.2
    post_time = pre_time
    readout_amp = 1
    scaling_factor = 0
    
    
    
    #this is the first pi/2 pulse in the sequence
    pi2_ge = Pulse(start=5040, duration=-pi2_ge_time, amplitude=ge_amp, ssm_freq=ssm_ge, phase=0) #pulse is also a class p is an instance
    ringupdown_seq.add_sweep(channel=1, sweep_name='start',start=0, stop=-ramsey_time, initial_pulse=pi2_ge)
    pi2_ge.phase = 90
    ringupdown_seq.add_sweep(channel=2, sweep_name='start',start=0, stop=-ramsey_time, initial_pulse=pi2_ge)
    #p.phase = 90 #make the pulse phase 90 degrees to get the single sideband modulation
    #rabi_seq.add_sweep(channel=2, sweep_name='width', start=0, stop=-200,initial_pulse=p)
    
       #this is the second  pi/2 pulse in the sequence
    pi2_ge = Pulse(start=5040, duration=pi2_ge_time, amplitude=ge_amp, ssm_freq=ssm_ge, phase=0) #pulse is also a class p is an instance
    ringupdown_seq.add_sweep(channel=1, sweep_name='none',initial_pulse=pi2_ge)
    pi2_ge.phase = 90
    ringupdown_seq.add_sweep(channel=2, sweep_name='none',initial_pulse=pi2_ge)
    
    
    #second readout
    
    #pre_pulse = Pulse(start = 5100,duration = -pre_time, amplitude=pre3_amp )
    #ringupdown_seq.add_sweep(channel=3, sweep_name='none',initial_pulse=pre_pulse)
    #pre_pulse = Pulse(start = 5100,duration = -pre_time, amplitude=pre4_amp )
    #ringupdown_seq.add_sweep(channel=4, sweep_name='none',initial_pulse=pre_pulse)
    
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
        plt.imshow(channel1_ch[0:100,4700:6000], aspect='auto', extent=[4700,6000,100,0])
        plt.show()
        
    ## write output
    write_dir = r"C:\arbsequences\strong_dispersive_withPython\test_pulse_ringupdown" 
    ringupdown_seq.write_sequence(base_name='foo', file_path=write_dir, use_range_01=False,num_offset=0, write_binary=True)
    ringupdown_seq.load_sequence('128.252.134.4', base_name='foo', file_path=write_dir, num_offset=0)
##END geom
def T1(): #this is pulsed readout to ring up and ring down cavity dfor e state
    file_length = 38000
    num_steps = 101
    ringupdown_seq = Sequence(file_length, num_steps) #this creates something called rabi_seq that is an instance of a sequence class

    ## channels   
    sweep_time = 30000
    pi_pulse_time = 30
    ssm_ge = .110
    pre3_amp = 0.8
    pre_time = 30
    pre4_amp = 0.1
    readout_amp = 1
    
    the_pulse = Pulse(start=35050, duration=pi_pulse_time, amplitude=1, ssm_freq=ssm_ge, phase=0) #pulse is also a class p is an instance
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
    
    main_pulse = Pulse(start = 35100,duration = 1000, amplitude= readout_amp )
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
  #  write_dir = r"C:\arbsequences\strong_dispersive_withPython\test_pulse_ringupdown"
  #  ringupdown_seq.write_sequence(base_name='foo', file_path=write_dir, use_range_01=False,num_offset=0)
    write_dir = r"C:\arbsequences\strong_dispersive_withPython\test_pulse_ringupdown_bin"
    ringupdown_seq.write_sequence(base_name='foo', file_path=write_dir, use_range_01=False,num_offset=0, write_binary=True)
    ringupdown_seq.load_sequence('128.252.134.4', base_name='foo', file_path=write_dir, num_offset=0)
##END geom
    
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
    
def rabi_constant(scale_factor=0.0005): #this is pulsed readout to ring up and ring down cavity dfor e state
    file_length = 8000
    num_steps = 101
    ringupdown_seq = Sequence(file_length, num_steps) #this creates something called rabi_seq that is an instance of a sequence class

    ## channels   
    rabi_time = 500
    ge_amp=1
    ssm_ge = .110
    pre3_amp = 0.8
    pre_time = 30
    pre4_amp = 1
    readout_amp = 1#0.1 # set this to 0.1 for the dispersive readout
    
    pi2_ge = Pulse(start=5050, duration=0, amplitude=ge_amp, ssm_freq=ssm_ge, phase=0) #pulse is also a class p is an instance
    ringupdown_seq.add_sweep(channel=1, sweep_name='width', start=0, stop=-rabi_time,initial_pulse=pi2_ge)
    pi2_ge.phase = 90
    ringupdown_seq.add_sweep(channel=2,  sweep_name='width', start=0, stop=-rabi_time,initial_pulse=pi2_ge)
    #p.phase = 90 #make the pulse phase 90 degrees to get the single sideband modulation
    #rabi_seq.add_sweep(channel=2, sweep_name='width', start=0, stop=-200,initial_pulse=p)

    constant_pulse = Pulse(start = 5050,duration = -5000, amplitude= readout_amp*scale_factor )
    ringupdown_seq.add_sweep(channel=4, sweep_name='none',initial_pulse=constant_pulse)
#    #main readout
#    
#    pre_pulse = Pulse(start = 5100,duration = -pre_time, amplitude=pre3_amp )
#    ringupdown_seq.add_sweep(channel=3, sweep_name='none',initial_pulse=pre_pulse)
#    
#    pre_pulse = Pulse(start = 5100,duration = -pre_time, amplitude=pre4_amp )
#    ringupdown_seq.add_sweep(channel=4, sweep_name='none',initial_pulse=pre_pulse)
    
    main_pulse = Pulse(start = 5100,duration = 1000, amplitude= readout_amp )
    ringupdown_seq.add_sweep(channel=1,marker=2, sweep_name='none',initial_pulse=main_pulse)
   
    
    ## markers
    alazar_trigger = Pulse(start=file_length-7000, duration=500, amplitude=1)
    ringupdown_seq.add_sweep(channel=3, marker=1, sweep_name='none', initial_pulse=alazar_trigger )
    
    ##create the gate for ch1 an ch2
    ringupdown_seq.add_gate(source_1=1, source_2=2, destination_tuple=(1,1))
    
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
        plt.imshow(channel2_ch[0:200,4800:5050], aspect='auto', extent=[4800,5050,200,0])
        plt.show()
        
    ## write output
#    write_dir = r"C:\arbsequences\strong_dispersive_withPython\test_pulse_ringupdown"
#    ringupdown_seq.write_sequence(base_name='foo', file_path=write_dir, use_range_01=False,num_offset=0)
    write_dir = r"C:\arbsequences\strong_dispersive_withPython\test_pulse_ringupdown_bin"
# 
    ringupdown_seq.write_sequence(base_name='foo', file_path=write_dir, use_range_01=False,num_offset=0, write_binary=True)
    ringupdown_seq.load_sequence('128.252.134.4', base_name='foo', file_path=write_dir, num_offset=0)
##END geom
    
def ramsey_constant(): 
    file_length = 8000
    num_steps = 101
    ringupdown_seq = Sequence(file_length, num_steps) #this creates something called rabi_seq that is an instance of a sequence class

    ## channels    
    pi2_ge_time = 20
    ramsey_time = 500
    ssm_ge = 0.110
    pre3_amp = 0.8
    pre_time = 30
    pre4_amp = 0.1
    post4_amp = -0.4
    post3_amp = -.2
    post_time = pre_time
    readout_amp = 1
    scale_factor = 0.00025
    
    
    
    #this is the first pi/2 pulse in the sequence
    pi2_ge = Pulse(start=5030, duration=-pi2_ge_time, amplitude=1, ssm_freq=ssm_ge, phase=0) #pulse is also a class p is an instance
    ringupdown_seq.add_sweep(channel=1, sweep_name='start', start=0, stop=-ramsey_time,initial_pulse=pi2_ge)
    pi2_ge.phase = 90
    ringupdown_seq.add_sweep(channel=2,  sweep_name='start', start=0, stop=-ramsey_time,initial_pulse=pi2_ge)
    #p.phase = 90 #make the pulse phase 90 degrees to get the single sideband modulation
    #rabi_seq.add_sweep(channel=2, sweep_name='width', start=0, stop=-200,initial_pulse=p)

    
    pi2_ge = Pulse(start=5060, duration=-pi2_ge_time, amplitude=1, ssm_freq=ssm_ge, phase=0) #pulse is also a class p is an instance
    ringupdown_seq.add_sweep(channel=1, sweep_name='phase',start=0,stop=1800,initial_pulse=pi2_ge)
    pi2_ge.phase = 90
    ringupdown_seq.add_sweep(channel=2,  sweep_name='phase',start=0,stop=1800,initial_pulse=pi2_ge)

#    
#    pre_pulse = Pulse(start = 5100,duration = -pre_time, amplitude=pre3_amp )
#    ringupdown_seq.add_sweep(channel=3, sweep_name='none',initial_pulse=pre_pulse)
#    pre_pulse = Pulse(start = 5100,duration = -pre_time, amplitude=pre4_amp )
#    ringupdown_seq.add_sweep(channel=4, sweep_name='none',initial_pulse=pre_pulse)
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
#    write_dir = r"C:\arbsequences\strong_dispersive_withPython\test_pulse_ringupdown"
#    ringupdown_seq.write_sequence(base_name='foo', file_path=write_dir, use_range_01=False,num_offset=0)
    write_dir = r"C:\arbsequences\strong_dispersive_withPython\test_pulse_ringupdown_bin"
# 
    ringupdown_seq.write_sequence(base_name='foo', file_path=write_dir, use_range_01=False,num_offset=0, write_binary=True)
    ringupdown_seq.load_sequence('128.252.134.4', base_name='foo', file_path=write_dir, num_offset=0)
##END geom
    
def ramseyef_constant(): #this is pulsed readout to ring up and ring down cavity dfor e state
    file_length = 8000
    num_steps = 101
    ringupdown_seq = Sequence(file_length, num_steps) #this creates something called rabi_seq that is an instance of a sequence class

    ## channels   
    ramsey_time = 500
    pi_ge_time= 40
    ge_amp=1
    pi2_ef_time= 34
    ef_amp=1
    ssm_ge = .110
    ssm_ef= .208
    readout_amp = 1#0.1 # set this to 0.1 for the dispersive readout
    scale_factor= 0.00025 # this is for another readout that is always on, to test dephasing
    
    pi_ge = Pulse(start=4930, duration=-pi_ge_time, amplitude=ge_amp, ssm_freq=ssm_ge, phase=0) #pulse is also a class p is an instance
    ringupdown_seq.add_sweep(channel=1, sweep_name='start',start=0,stop=-ramsey_time, initial_pulse=pi_ge)
    pi_ge.phase = 90
    ringupdown_seq.add_sweep(channel=2, sweep_name='start',start=0,stop=-ramsey_time ,initial_pulse=pi_ge)
    
    pi2_ef = Pulse(start=4970, duration=-pi2_ef_time, amplitude=ef_amp, ssm_freq=ssm_ef, phase=90) #pulse is also a class p is an instance
    ringupdown_seq.add_sweep(channel=1, sweep_name='start', start=0, stop=-ramsey_time,initial_pulse=pi2_ef)
    pi2_ef.phase = 0
    ringupdown_seq.add_sweep(channel=2, sweep_name='start', start=0, stop=-ramsey_time,initial_pulse=pi2_ef)
    #p.phase = 90 #make the pulse phase 90 degrees to get the single sideband modulation
    #rabi_seq.add_sweep(channel=2, sweep_name='width', start=0, stop=-200,initial_pulse=p)
    pi2_ef = Pulse(start=5010, duration=-pi2_ef_time, amplitude=ef_amp, ssm_freq=ssm_ef, phase=90) #pulse is also a class p is an instance
    ringupdown_seq.add_sweep(channel=1, sweep_name='phase',start=0,stop=1800,initial_pulse=pi2_ef)
    pi2_ef.phase = 0
    ringupdown_seq.add_sweep(channel=2, sweep_name='phase',start=0,stop=1800,initial_pulse=pi2_ef)
    
    pi_ge = Pulse(start=5050, duration=-pi_ge_time, amplitude=ge_amp, ssm_freq=ssm_ge, phase=0) #pulse is also a class p is an instance
    ringupdown_seq.add_sweep(channel=1, sweep_name='none',initial_pulse=pi_ge)
    pi_ge.phase = 90
    ringupdown_seq.add_sweep(channel=2, sweep_name='none',initial_pulse=pi_ge)
    
    #additional readout leakage
    
    constant_pulse = Pulse(start = 5050,duration = -5000, amplitude= readout_amp*scale_factor )
    ringupdown_seq.add_sweep(channel=4, sweep_name='none',initial_pulse=constant_pulse)
    
    #main readout
    
    #pre_pulse = Pulse(start = 5100,duration = -pre_time, amplitude=pre3_amp )
    #ringupdown_seq.add_sweep(channel=3, sweep_name='none',initial_pulse=pre_pulse)
    #pre_pulse = Pulse(start = 5100,duration = -pre_time, amplitude=pre4_amp )
    #ringupdown_seq.add_sweep(channel=4, sweep_name='none',initial_pulse=pre_pulse)
    
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
        plt.imshow(channel1_ch[0:200,00:6000], aspect='auto', extent=[00,6000,200,0])
        plt.show()
        
    ## write output
    #write_dir = r"C:\arbsequences\strong_dispersive_withPython\test_pulse_ringupdown"
   # ringupdown_seq.write_sequence(base_name='foo', file_path=write_dir, use_range_01=False,num_offset=0)

    write_dir = r"C:\arbsequences\strong_dispersive_withPython\test_pulse_ringupdown_bin"
# 
    ringupdown_seq.write_sequence(base_name='foo', file_path=write_dir, use_range_01=False,num_offset=0, write_binary=True)
    ringupdown_seq.load_sequence('128.252.134.4', base_name='foo', file_path=write_dir, num_offset=0)
##END geom
    
def ramseygf_constant(): #this is pulsed readout to ring up and ring down cavity dfor e state
    file_length = 8000
    num_steps = 101
    ringupdown_seq = Sequence(file_length, num_steps) #this creates something called rabi_seq that is an instance of a sequence class

    ## channels   
    ramsey_time = 500
    pi2_ge_time= 20
    ge_amp=1
    pi_ef_time= 68
    ef_amp=1
    ssm_ge = .110
    ssm_ef= .208
    readout_amp = 1#0.1 # set this to 0.1 for the dispersive readout
    scale_factor= 0.00025 # this is for another readout that is always on, to test dephasing
    
    pi_ge = Pulse(start=4890, duration=-pi2_ge_time, amplitude=ge_amp, ssm_freq=ssm_ge, phase=0) #pulse is also a class p is an instance
    ringupdown_seq.add_sweep(channel=1, sweep_name='start',start=0,stop=-ramsey_time, initial_pulse=pi_ge)
    pi_ge.phase = 90
    ringupdown_seq.add_sweep(channel=2, sweep_name='start',start=0,stop=-ramsey_time ,initial_pulse=pi_ge)
    
    pi2_ef = Pulse(start=4960, duration=-pi_ef_time, amplitude=ef_amp, ssm_freq=ssm_ef, phase=90) #pulse is also a class p is an instance
    ringupdown_seq.add_sweep(channel=1, sweep_name='start', start=0, stop=-ramsey_time,initial_pulse=pi2_ef)
    pi2_ef.phase = 0
    ringupdown_seq.add_sweep(channel=2, sweep_name='start', start=0, stop=-ramsey_time,initial_pulse=pi2_ef)
    #p.phase = 90 #make the pulse phase 90 degrees to get the single sideband modulation
    #rabi_seq.add_sweep(channel=2, sweep_name='width', start=0, stop=-200,initial_pulse=p)
    pi2_ef = Pulse(start=5030, duration=-pi_ef_time, amplitude=ef_amp, ssm_freq=ssm_ef, phase=90) #pulse is also a class p is an instance
    ringupdown_seq.add_sweep(channel=1, sweep_name='none',initial_pulse=pi2_ef)
    pi2_ef.phase = 0
    ringupdown_seq.add_sweep(channel=2, sweep_name='none',initial_pulse=pi2_ef)
    
    pi_ge = Pulse(start=5050, duration=-pi2_ge_time, amplitude=ge_amp, ssm_freq=ssm_ge, phase=0) #pulse is also a class p is an instance
    ringupdown_seq.add_sweep(channel=1, sweep_name='phase',start=0,stop=1800,initial_pulse=pi_ge)
    pi_ge.phase = 90
    ringupdown_seq.add_sweep(channel=2, sweep_name='phase',start=0,stop=1800,initial_pulse=pi_ge)
    
    #additional readout leakage
    
    constant_pulse = Pulse(start = 5050,duration = -5000, amplitude= readout_amp*scale_factor )
    ringupdown_seq.add_sweep(channel=4, sweep_name='none',initial_pulse=constant_pulse)
    
    #main readout
    
    #pre_pulse = Pulse(start = 5100,duration = -pre_time, amplitude=pre3_amp )
    #ringupdown_seq.add_sweep(channel=3, sweep_name='none',initial_pulse=pre_pulse)
    #pre_pulse = Pulse(start = 5100,duration = -pre_time, amplitude=pre4_amp )
    #ringupdown_seq.add_sweep(channel=4, sweep_name='none',initial_pulse=pre_pulse)
    
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
        plt.imshow(channel1_ch[0:200,00:6000], aspect='auto', extent=[00,6000,200,0])
        plt.show()
        
    ## write output
    #write_dir = r"C:\arbsequences\strong_dispersive_withPython\test_pulse_ringupdown"
   # ringupdown_seq.write_sequence(base_name='foo', file_path=write_dir, use_range_01=False,num_offset=0)

    write_dir = r"C:\arbsequences\strong_dispersive_withPython\test_pulse_ringupdown_bin"
# 
    ringupdown_seq.write_sequence(base_name='foo', file_path=write_dir, use_range_01=False,num_offset=0, write_binary=True)
    ringupdown_seq.load_sequence('128.252.134.4', base_name='foo', file_path=write_dir, num_offset=0)
    
def rabi(): #this is pulsed readout to ring up and ring down cavity dfor e state
    file_length = 2*4096
    num_steps = 51
    ringupdown_seq = Sequence(file_length, num_steps) #this creates something called rabi_seq that is an instance of a sequence class

    ## channels   
    rabi_time = 1000
    ge_amp=1
    ssm_ge = .110
    pre3_amp = 0.8
    pre_time = 30
    pre4_amp = 1
    readout_amp = 1#0.1 # set this to 0.1 for the dispersive readout
    scale_factor=0
    
    pi2_ge = Pulse(start=1000, duration=0, amplitude=ge_amp, ssm_freq=ssm_ge, phase=0) #pulse is also a class p is an instance
    ringupdown_seq.add_sweep(channel=1, sweep_name='width', start=0, stop=-rabi_time,initial_pulse=pi2_ge)
    pi2_ge.phase = 90
    ringupdown_seq.add_sweep(channel=4,  sweep_name='width', start=0, stop=-rabi_time,initial_pulse=pi2_ge)
    #p.phase = 90 #make the pulse phase 90 degrees to get the single sideband modulation
    #rabi_seq.add_sweep(channel=2, sweep_name='width', start=0, stop=-200,initial_pulse=p)

#    constant_pulse = Pulse(start = 5100-pre_time,duration = -5000, amplitude= readout_amp*scale_factor )
#    ringupdown_seq.add_sweep(channel=4, sweep_name='none',initial_pulse=constant_pulse)
#    #main readout
#    
#    pre_pulse = Pulse(start = 5100,duration = -pre_time, amplitude=pre3_amp )
#    ringupdown_seq.add_sweep(channel=3, sweep_name='none',initial_pulse=pre_pulse)
#    
#    pre_pulse = Pulse(start = 5100,duration = -pre_time, amplitude=pre4_amp )
#    ringupdown_seq.add_sweep(channel=4, sweep_name='none',initial_pulse=pre_pulse)
    
#     readout pulse
#    main_pulse = Pulse(start =2000,duration = 1800, amplitude= readout_amp )
#    ringupdown_seq.add_sweep(channel=4, sweep_name='none',initial_pulse=main_pulse)
    
    
    ## markers
    alazar_trigger = Pulse(start=file_length-7000, duration=500, amplitude=1)
    ringupdown_seq.add_sweep(channel=3, marker=1, sweep_name='none', initial_pulse=alazar_trigger )
    
    
    ##create the gate for ch1 an ch2
#    ringupdown_seq.add_gate(source_1=1, source_2=2, destination_tuple=(1,1))
    
#    channel1_channel = ringupdown_seq.channel_list[0][0] # dim 0: channel 1; dim 1: [ch,m1,m2]
#    channel2_channel = ringupdown_seq.channel_list[1][0] # dim 0: channel 1; dim 1: [ch,m1,m2]
#    both_ch1_ch2 = channel1_channel**2 + channel2_channel**2
#    qubit_gate = create_gate(both_ch1_ch2)
#    ringupdown_seq.channel_list[0][1] = qubit_gate

    ## view output
    if True:
        channel1_ch = ringupdown_seq.channel_list[0][0] #[channel name -1][0:channel, 1:marker 1, 2:marker 2]
        channel1_ma = ringupdown_seq.channel_list[0][1]
        channel2_ch = ringupdown_seq.channel_list[1][0]
        channel3_ch = ringupdown_seq.channel_list[2][0]
        channel4_ch = ringupdown_seq.channel_list[3][0]
        #plt.imshow(channel2_ch[0:200,4800:5050], aspect='auto', extent=[4800,5050,200,0])
        plt.imshow(channel1_ch, aspect='auto')
        plt.show()
        
    ## write output
#    write_dir = r"C:\arbsequences\strong_dispersive_withPython\test_pulse_ringupdown"
#    ringupdown_seq.write_sequence(base_name='foo', file_path=write_dir, use_range_01=False,num_offset=0)
    write_dir = r"C:\arbsequences\strong_dispersive_withPython\test_pulse_ringupdown_bin"
# 
#    ringupdown_seq.write_sequence(base_name='foo', file_path=write_dir, use_range_01=False,num_offset=0, write_binary=True)
#    ringupdown_seq.load_sequence_old('128.252.134.4', base_name='foo', file_path=write_dir, num_offset=0)
    ringupdown_seq.load_sequence()
##END rabi
    
    
def rabi_90(): #this is pulsed readout to ring up and ring down cavity dfor e state
    file_length = 8000
    num_steps = 101
    ringupdown_seq = Sequence(file_length, num_steps) #this creates something called rabi_seq that is an instance of a sequence class

    ## channels   
    rabi_time = 500
    ge_amp=.5
    pi2_ge_time=14
    ssm_ge = .110
    pre3_amp = 0.8
    pre_time = 30
    pre4_amp = 1
    readout_amp = 1#0.1 # set this to 0.1 for the dispersive readout
    scale_factor=0
    
    pi2_ge = Pulse(start=5080-pi2_ge_time, duration=-pi2_ge_time, amplitude=ge_amp, ssm_freq=ssm_ge, phase=0) #pulse is also a class p is an instance
    ringupdown_seq.add_sweep(channel=1, sweep_name='start', start=0, stop=-rabi_time,initial_pulse=pi2_ge)
    pi2_ge.phase = 90
    ringupdown_seq.add_sweep(channel=2,  sweep_name='start', start=0, stop=-rabi_time,initial_pulse=pi2_ge)
    
    H_ge = Pulse(start=5080, duration=-pi2_ge_time, amplitude=ge_amp, ssm_freq=ssm_ge, phase=90) #pulse is also a class p is an instance
    ringupdown_seq.add_sweep(channel=1, sweep_name='width', start=0, stop=-rabi_time,initial_pulse=H_ge)
    H_ge.phase = 180
    ringupdown_seq.add_sweep(channel=2,  sweep_name='width', start=0, stop=-rabi_time,initial_pulse=H_ge)
    #p.phase = 90 #make the pulse phase 90 degrees to get the single sideband modulation
    #rabi_seq.add_sweep(channel=2, sweep_name='width', start=0, stop=-200,initial_pulse=p)

#    constant_pulse = Pulse(start = 5100-pre_time,duration = -5000, amplitude= readout_amp*scale_factor )
#    ringupdown_seq.add_sweep(channel=4, sweep_name='none',initial_pulse=constant_pulse)
#    #main readout
#    
#    pre_pulse = Pulse(start = 5100,duration = -pre_time, amplitude=pre3_amp )
#    ringupdown_seq.add_sweep(channel=3, sweep_name='none',initial_pulse=pre_pulse)
#    
#    pre_pulse = Pulse(start = 5100,duration = -pre_time, amplitude=pre4_amp )
#    ringupdown_seq.add_sweep(channel=4, sweep_name='none',initial_pulse=pre_pulse)
    
    main_pulse = Pulse(start = 5100,duration = 1000, amplitude= readout_amp )
    ringupdown_seq.add_sweep(channel=4, sweep_name='none',initial_pulse=main_pulse)
    
    
    ## markers
    alazar_trigger = Pulse(start=file_length-7000, duration=500, amplitude=1)
    ringupdown_seq.add_sweep(channel=3, marker=1, sweep_name='none', initial_pulse=alazar_trigger )
    
    ##create the gate for ch1 an ch2
    ringupdown_seq.add_gate(source_1=1, source_2=2, destination_tuple=(1,1))
    
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
        plt.imshow(channel2_ch[0:200,4800:5050], aspect='auto', extent=[4800,5050,200,0])
        plt.show()
        
    ## write output
#    write_dir = r"C:\arbsequences\strong_dispersive_withPython\test_pulse_ringupdown"
#    ringupdown_seq.write_sequence(base_name='foo', file_path=write_dir, use_range_01=False,num_offset=0)
    write_dir = r"C:\arbsequences\strong_dispersive_withPython\test_pulse_ringupdown_bin"
# 
    ringupdown_seq.write_sequence(base_name='foo', file_path=write_dir, use_range_01=False,num_offset=0, write_binary=True)
    ringupdown_seq.load_sequence('128.252.134.4', base_name='foo', file_path=write_dir, num_offset=0)
##END geom


def rabi_test(): #this is pulsed readout to ring up and ring down cavity dfor e state
    file_length = 2048
    num_steps = 10
    ringupdown_seq = Sequence(file_length, num_steps) #this creates something called rabi_seq that is an instance of a sequence class

    ## channels   
    rabi_time = 1024
    ssm_ge = .110
    pre3_amp = 0.8
    pre_time = 30
    pre4_amp = 0.1
    readout_amp = 0.1#0.1 # set this to 0.1 for the dispersive readout
    scale_factor=0
    
    
    pi2_ge = Pulse(start=2000, duration=0, amplitude=1, ssm_freq=ssm_ge, phase=0) #pulse is also a class p is an instance
    ringupdown_seq.add_sweep(channel=1, sweep_name='width', start=0, stop=-rabi_time,initial_pulse=pi2_ge)
    ringupdown_seq.add_sweep(channel=3, sweep_name='width', start=0, stop=-rabi_time,initial_pulse=pi2_ge)
    pi2_ge.phase = 90
    ringupdown_seq.add_sweep(channel=2,  sweep_name='width', start=0, stop=-rabi_time,initial_pulse=pi2_ge)
    ringupdown_seq.add_sweep(channel=4, sweep_name='width', start=0, stop=-rabi_time,initial_pulse=pi2_ge)
    #p.phase = 90 #make the pulse phase 90 degrees to get the single sideband modulation
    #rabi_seq.add_sweep(channel=2, sweep_name='width', start=0, stop=-200,initial_pulse=p)

#    constant_pulse = Pulse(start = 5100-pre_time,duration = -5000, amplitude= readout_amp*scale_factor )
#    ringupdown_seq.add_sweep(channel=4, sweep_name='none',initial_pulse=constant_pulse)
#
#    #main readout
#    
#    pre_pulse = Pulse(start = 5100,duration = -pre_time, amplitude=pre3_amp )
#    ringupdown_seq.add_sweep(channel=3, sweep_name='none',initial_pulse=pre_pulse)
#    
#    pre_pulse = Pulse(start = 5100,duration = -pre_time, amplitude=pre4_amp )
#    ringupdown_seq.add_sweep(channel=4, sweep_name='none',initial_pulse=pre_pulse)
#    
#    main_pulse = Pulse(start = 5100,duration = 1000, amplitude= readout_amp )
#    ringupdown_seq.add_sweep(channel=4, sweep_name='none',initial_pulse=main_pulse)
#    
#    
#    ## markers
#    alazar_trigger = Pulse(start=file_length-7000, duration=500, amplitude=1)
#    ringupdown_seq.add_sweep(channel=3, marker=1, sweep_name='none', initial_pulse=alazar_trigger )
    
    ##create the gate for ch1 an ch2
    ringupdown_seq.add_gate(source_1=1, source_2=2, destination_tuple=(1,1))
    
    channel1_channel = ringupdown_seq.channel_list[0][0] # dim 0: channel 1; dim 1: [ch,m1,m2]
    channel2_channel = ringupdown_seq.channel_list[1][0] # dim 0: channel 1; dim 1: [ch,m1,m2]
    both_ch1_ch2 = channel1_channel**2 + channel2_channel**2
    qubit_gate = create_gate(both_ch1_ch2)
    ringupdown_seq.channel_list[0][1] = qubit_gate
    ringupdown_seq.channel_list[0][2] = qubit_gate
    ringupdown_seq.channel_list[1][1] = qubit_gate
    ringupdown_seq.channel_list[2][2] = qubit_gate
    ringupdown_seq.channel_list[3][1] = qubit_gate
    ringupdown_seq.channel_list[3][2] = qubit_gate

    ## view output
    if True:
        channel1_ch = ringupdown_seq.channel_list[0][0] #[channel name -1][0:channel, 1:marker 1, 2:marker 2]
        channel2_ch = ringupdown_seq.channel_list[1][0]
        channel3_ch = ringupdown_seq.channel_list[2][0]
        channel4_ch = ringupdown_seq.channel_list[3][0]
        plt.imshow(channel1_ch, aspect='auto', extent=[0,8000,100,0])
        plt.show()
        
    ## write output
    write_dir = r"C:\arbsequences\strong_dispersive_withPython\test_pulse_ringupdown_bin"
    ringupdown_seq.write_sequence(base_name='foo', file_path=write_dir, use_range_01=False,num_offset=0, write_binary=True)
    ringupdown_seq.load_sequence('128.252.134.4', base_name='foo', file_path=write_dir, num_offset=0)
##END geom
    

def rabi_test_20200803(): #this is pulsed readout to ring up and ring down cavity dfor e state
    file_length = 4096
    num_steps = 21
    ringupdown_seq = Sequence(file_length, num_steps) #this creates something called rabi_seq that is an instance of a sequence class

    ## channels   
    rabi_time = 2000
    ssm_ge = 0.1
    pre3_amp = 0.8
    pre_time = 30
    pre4_amp = 0.1
    readout_amp = 0.1#0.1 # set this to 0.1 for the dispersive readout
    scale_factor=0
    
    pi2_ge = Pulse(start=2000, duration=0, amplitude=1, ssm_freq=ssm_ge, phase=0) #pulse is also a class p is an instance
    ringupdown_seq.add_sweep(channel=1, sweep_name='width', start=0, stop=rabi_time,initial_pulse=pi2_ge)
    phase=90
    ringupdown_seq.add_sweep(channel=2,  sweep_name='width', start=0, stop=rabi_time,initial_pulse=pi2_ge)
    
    ringupdown_seq.add_sweep(channel=3, sweep_name='none', start=0, stop=-rabi_time,initial_pulse=pi2_ge)
    ringupdown_seq.add_sweep(channel=4, sweep_name='none', start=0, stop=-rabi_time,initial_pulse=pi2_ge)
    
    channel1_channel = ringupdown_seq.channel_list[0][0] # dim 0: channel 1; dim 1: [ch,m1,m2]
    channel2_channel = ringupdown_seq.channel_list[1][0] # dim 0: channel 1; dim 1: [ch,m1,m2]
    both_ch1_ch2 = channel1_channel**2 + channel2_channel**2
    qubit_gate = create_gate(both_ch1_ch2)
    ringupdown_seq.channel_list[0][1] = qubit_gate
    ringupdown_seq.channel_list[0][2] = qubit_gate
    
    #p.phase = 90 #make the pulse phase 90 degrees to get the single sideband modulation
    #rabi_seq.add_sweep(channel=2, sweep_name='width', start=0, stop=-200,initial_pulse=p)

#    constant_pulse = Pulse(start = 5100-pre_time,duration = -5000, amplitude= readout_amp*scale_factor )
#    ringupdown_seq.add_sweep(channel=4, sweep_name='none',initial_pulse=constant_pulse)
#
#    #main readout
#    
#    pre_pulse = Pulse(start = 5100,duration = -pre_time, amplitude=pre3_amp )
#    ringupdown_seq.add_sweep(channel=3, sweep_name='none',initial_pulse=pre_pulse)
#    
#    pre_pulse = Pulse(start = 5100,duration = -pre_time, amplitude=pre4_amp )
#    ringupdown_seq.add_sweep(channel=4, sweep_name='none',initial_pulse=pre_pulse)
#    
#    main_pulse = Pulse(start = 5100,duration = 1000, amplitude= readout_amp )
#    ringupdown_seq.add_sweep(channel=4, sweep_name='none',initial_pulse=main_pulse)
#    
#    
#    ## markers
#    alazar_trigger = Pulse(start=file_length-7000, duration=500, amplitude=1)
#    ringupdown_seq.add_sweep(channel=3, marker=1, sweep_name='none', initial_pulse=alazar_trigger )
    
    ##create the gate for ch1 an ch2
#    ringupdown_seq.add_gate(source_1=1, source_2=2, destination_tuple=(1,1))
#    
#    channel1_channel = ringupdown_seq.channel_list[0][0] # dim 0: channel 1; dim 1: [ch,m1,m2]
#    channel2_channel = ringupdown_seq.channel_list[1][0] # dim 0: channel 1; dim 1: [ch,m1,m2]
#    both_ch1_ch2 = channel1_channel**2 + channel2_channel**2
#    qubit_gate = create_gate(both_ch1_ch2)
#    ringupdown_seq.channel_list[0][1] = qubit_gate
#    ringupdown_seq.channel_list[0][2] = qubit_gate
#    ringupdown_seq.channel_list[1][1] = qubit_gate
#    ringupdown_seq.channel_list[2][2] = qubit_gate
#    ringupdown_seq.channel_list[3][1] = qubit_gate
#    ringupdown_seq.channel_list[3][2] = qubit_gate

    ## view output
    if True:
        channel1_ch = ringupdown_seq.channel_list[0][0] #[channel name -1][0:channel, 1:marker 1, 2:marker 2]
        channel2_ch = ringupdown_seq.channel_list[1][0]
        channel3_ch = ringupdown_seq.channel_list[2][0]
        channel4_ch = ringupdown_seq.channel_list[3][0]
        
        plt.imshow(channel1_ch, aspect='auto', extent=[0,8000,100,0])
        plt.show()
        plt.imshow(channel2_ch, aspect='auto', extent=[0,8000,100,0])
        plt.show()
        
    ## write output
    write_dir = r"C:\arbsequences\strong_dispersive_withPython\test_pulse_ringupdown_bin"
    ringupdown_seq.write_sequence(base_name='foo', file_path=write_dir, use_range_01=False,num_offset=0, write_binary=True)
    ringupdown_seq.load_sequence('xxxx', base_name='foo', file_path=write_dir, num_offset=0)
##END geom
    
    
def rabi_gaussian(): 
    file_length = 8000
    ringupdown_seq = Sequence(file_length, num_steps) 
    
    ## channels   
    rabi_time = 500
    ssm_ge = .110
    pre3_amp = 0.8
    pre_time = 30
    pre4_amp = 0.1
    num_steps = 101
    readout_amp = 0.1#0.1 # set this to 0.1 for the dispersive readout
    #, ssm_freq=ssm_ge
    pi2_ge = Pulse(start=5050, duration=-80, amplitude=0, ssm_freq=ssm_ge, phase=0,gaussian_bool=True) #pulse is also a class p is an instance
    ringupdown_seq.add_sweep(channel=1, sweep_name='amplitude', start=0, stop=1,initial_pulse=pi2_ge)
    pi2_ge.phase = 90
    ringupdown_seq.add_sweep(channel=2,  sweep_name='amplitude', start=0, stop=1,initial_pulse=pi2_ge)
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
    #ringupdown_seq.add_gate(source_1=1, source_2=2, destination_tuple=(1,1))
    channel1_channel = ringupdown_seq.channel_list[0][0] # dim 0: channel 1; dim 1: [ch,m1,m2]
    channel2_channel = ringupdown_seq.channel_list[1][0] # dim 0: channel 1; dim 1: [ch,m1,m2]
    both_ch1_ch2 = channel1_channel**2 + channel2_channel**2
    qubit_gate = create_gate(both_ch1_ch2)
    ringupdown_seq.channel_list[0][1] = qubit_gate
    ringupdown_seq.channel_list[0][2] = qubit_gate
    ringupdown_seq.channel_list[1][1] = qubit_gate

    ## view output
    if True:
        channel1_ch = ringupdown_seq.channel_list[0][0] #[channel name -1][0:channel, 1:marker 1, 2:marker 2]
        channel2_ch = ringupdown_seq.channel_list[1][0]
        channel3_ch = ringupdown_seq.channel_list[2][0]
        channel4_ch = ringupdown_seq.channel_list[3][0]
        plt.imshow(channel1_ch[0:200,5000:5100], aspect='auto', extent=[5000,5100,200,0])
        #plt.plot(channel1_ch[num_steps-1][5000:5100])
        plt.show()
        
    ## write output
    write_dir = r"C:\arbsequences\strong_dispersive_withPython\test_pulse_ringupdown"
    ringupdown_seq.write_sequence(base_name='foo', file_path=write_dir, use_range_01=False,num_offset=0)
##END geom
    
    
def rabief(): #this is pulsed readout to ring up and ring down cavity dfor e state
    file_length = 8000
    num_steps = 101
    ringupdown_seq = Sequence(file_length, num_steps) #this creates something called rabi_seq that is an instance of a sequence class

    ## channels   
    rabi_time = 400
    ge_amp=1
    ef_amp=1
    pi_ge_time= 41
    ssm_ge = .110
    ssm_ef= .208
    pre3_amp = 0.8
    pre_time = 30
    pre4_amp = 0.1
    readout_amp = 1#0.1 # set this to 0.1 for the dispersive readout
    
    pi_ge = Pulse(start=5020, duration=-pi_ge_time, amplitude=ge_amp, ssm_freq=ssm_ge, phase=0) #pulse is also a class p is an instance
    ringupdown_seq.add_sweep(channel=1, sweep_name='start',start=0,stop=-rabi_time, initial_pulse=pi_ge)
    pi_ge.phase = 90
    ringupdown_seq.add_sweep(channel=2, sweep_name='start',start=0,stop=-rabi_time ,initial_pulse=pi_ge)
    
    rabi_ef = Pulse(start=5025, duration=0, amplitude=ef_amp, ssm_freq=ssm_ef, phase=90) #pulse is also a class p is an instance
    ringupdown_seq.add_sweep(channel=1, sweep_name='width', start=0, stop=-rabi_time,initial_pulse=rabi_ef)
    rabi_ef.phase = 0
    ringupdown_seq.add_sweep(channel=2, sweep_name='width', start=0, stop=-rabi_time,initial_pulse=rabi_ef)
    #p.phase = 90 #make the pulse phase 90 degrees to get the single sideband modulation
    #rabi_seq.add_sweep(channel=2, sweep_name='width', start=0, stop=-200,initial_pulse=p)

    pi_ge = Pulse(start=5050, duration=-pi_ge_time, amplitude=ge_amp, ssm_freq=ssm_ge, phase=0) #pulse is also a class p is an instance
    ringupdown_seq.add_sweep(channel=1, sweep_name='none',initial_pulse=pi_ge)
    pi_ge.phase = 90
    ringupdown_seq.add_sweep(channel=2, sweep_name='none',initial_pulse=pi_ge)
    
    #main readout
    
    #pre_pulse = Pulse(start = 5100,duration = -pre_time, amplitude=pre3_amp )
    #ringupdown_seq.add_sweep(channel=3, sweep_name='none',initial_pulse=pre_pulse)
    #pre_pulse = Pulse(start = 5100,duration = -pre_time, amplitude=pre4_amp )
    #ringupdown_seq.add_sweep(channel=4, sweep_name='none',initial_pulse=pre_pulse)
    
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
        plt.imshow(channel1_ch[0:200,2800:6000], aspect='auto', extent=[2800,6000,200,0])
        plt.show()
        
    ## write output
    #write_dir = r"C:\arbsequences\strong_dispersive_withPython\test_pulse_ringupdown"
    #ringupdown_seq.write_sequence(base_name='foo', file_path=write_dir, use_range_01=False,num_offset=0)
    write_dir = r"C:\arbsequences\strong_dispersive_withPython\test_pulse_ringupdown_bin"
# 
    ringupdown_seq.write_sequence(base_name='foo', file_path=write_dir, use_range_01=False,num_offset=0, write_binary=True)
    ringupdown_seq.load_sequence('128.252.134.4', base_name='foo', file_path=write_dir, num_offset=0)
##END geom
    
def rabief_test(file_length = 8000, ssm_ef=.046): #this is pulsed readout to ring up and ring down cavity dfor e state
    num_steps = 101
    ringupdown_seq = Sequence(file_length, num_steps) #this creates something called rabi_seq that is an instance of a sequence class

    ## channels   
    ge_amp=1
    ef_amp=1
    rabi_time = 400
    pi_ge_time= 41
    ssm_ge = .110
    pre3_amp = 0.8
    pre_time = 30
    pre4_amp = 0.1
    readout_amp = 1#0.1 # set this to 0.1 for the dispersive readout
    
    pi_ge = Pulse(start=5020, duration=-pi_ge_time, amplitude=ge_amp, ssm_freq=ssm_ge, phase=0) #pulse is also a class p is an instance
    ringupdown_seq.add_sweep(channel=1, sweep_name='start',start=0,stop=-rabi_time, initial_pulse=pi_ge)
    pi_ge.phase = 90
    ringupdown_seq.add_sweep(channel=2, sweep_name='start',start=0,stop=-rabi_time ,initial_pulse=pi_ge)
    
    rabi_ef = Pulse(start=5025, duration=0, amplitude=ef_amp, ssm_freq=ssm_ef, phase=90) #pulse is also a class p is an instance
    ringupdown_seq.add_sweep(channel=1, sweep_name='width', start=0, stop=-rabi_time,initial_pulse=rabi_ef)
    rabi_ef.phase = 0
    ringupdown_seq.add_sweep(channel=2, sweep_name='width', start=0, stop=-rabi_time,initial_pulse=rabi_ef)
    #p.phase = 90 #make the pulse phase 90 degrees to get the single sideband modulation
    #rabi_seq.add_sweep(channel=2, sweep_name='width', start=0, stop=-200,initial_pulse=p)

    pi_ge = Pulse(start=5050, duration=-pi_ge_time, amplitude=ge_amp, ssm_freq=ssm_ge, phase=0) #pulse is also a class p is an instance
    ringupdown_seq.add_sweep(channel=1, sweep_name='none',initial_pulse=pi_ge)
    pi_ge.phase = 90
    ringupdown_seq.add_sweep(channel=2, sweep_name='none',initial_pulse=pi_ge)
    
    #main readout
    
    #pre_pulse = Pulse(start = 5100,duration = -pre_time, amplitude=pre3_amp )
    #ringupdown_seq.add_sweep(channel=3, sweep_name='none',initial_pulse=pre_pulse)
    #pre_pulse = Pulse(start = 5100,duration = -pre_time, amplitude=pre4_amp )
    #ringupdown_seq.add_sweep(channel=4, sweep_name='none',initial_pulse=pre_pulse)
    
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
    if False:
        channel1_ch = ringupdown_seq.channel_list[0][0] #[channel name -1][0:channel, 1:marker 1, 2:marker 2]
        channel2_ch = ringupdown_seq.channel_list[1][0]
        channel3_ch = ringupdown_seq.channel_list[2][0]
        channel4_ch = ringupdown_seq.channel_list[3][0]
        plt.imshow(channel1_ch[0:200,2800:6000], aspect='auto', extent=[2800,6000,200,0])
        plt.show()
        
    ## write output
    #write_dir = r"C:\arbsequences\strong_dispersive_withPython\test_pulse_ringupdown"
    #ringupdown_seq.write_sequence(base_name='foo', file_path=write_dir, use_range_01=False,num_offset=0)
    write_dir = r"C:\arbsequences\strong_dispersive_withPython\test_pulse_ringupdown_bin"
# 
    ringupdown_seq.write_sequence(base_name='foo', file_path=write_dir, use_range_01=False,num_offset=0, write_binary=True)
    ringupdown_seq.load_sequence('128.252.134.4', base_name='foo', file_path=write_dir, num_offset=0)
##END geom
    
def rabiefTemp(): #this is pulsed readout to ring up and ring down cavity dfor e state
    file_length = 8000
    num_steps = 101
    ringupdown_seq = Sequence(file_length, num_steps) #this creates something called rabi_seq that is an instance of a sequence class

    ## channels   
    rabi_time = 100
    pi_ge_time= 19
    ssm_ge = .110
    ssm_ef= .046
    pre3_amp = 0.8
    pre_time = 30
    pre4_amp = 0.1
    readout_amp = .1#0.1 # set this to 0.1 for the dispersive readout
    
   
    
    rabi_ef = Pulse(start=5025, duration=0, amplitude=0.9, ssm_freq=ssm_ef, phase=90) #pulse is also a class p is an instance
    ringupdown_seq.add_sweep(channel=1, sweep_name='width', start=0, stop=-rabi_time,initial_pulse=rabi_ef)
    rabi_ef.phase = 0
    ringupdown_seq.add_sweep(channel=2, sweep_name='width', start=0, stop=-rabi_time,initial_pulse=rabi_ef)
    #p.phase = 90 #make the pulse phase 90 degrees to get the single sideband modulation
    #rabi_seq.add_sweep(channel=2, sweep_name='width', start=0, stop=-200,initial_pulse=p)

    pi_ge = Pulse(start=5050, duration=-pi_ge_time, amplitude=1, ssm_freq=ssm_ge, phase=0) #pulse is also a class p is an instance
    ringupdown_seq.add_sweep(channel=1, sweep_name='none',initial_pulse=pi_ge)
    pi_ge.phase = 90
    ringupdown_seq.add_sweep(channel=2, sweep_name='none',initial_pulse=pi_ge)
    
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
        plt.imshow(channel1_ch[0:200,2800:6000], aspect='auto', extent=[2800,6000,200,0])
        plt.show()
        
    ## write output
    write_dir = r"C:\arbsequences\strong_dispersive_withPython\test_pulse_ringupdown"
    ringupdown_seq.write_sequence(base_name='foo', file_path=write_dir, use_range_01=False,num_offset=0)
##END geom
    
def ramseyef(): #this is pulsed readout to ring up and ring down cavity dfor e state
    file_length = 8000
    num_steps = 101
    ringupdown_seq = Sequence(file_length, num_steps) #this creates something called rabi_seq that is an instance of a sequence class

    ## channels   
    ramsey_time = 2000
    pi_ge_time= 40
    ge_amp=1
    pi2_ef_time= 34
    ef_amp=1
    ssm_ge = .110
    ssm_ef= .208
    readout_amp = 1#0.1 # set this to 0.1 for the dispersive readout
    scale_factor= 0.01 # this is for another readout that is always on, to test dephasing
    
    pi_ge = Pulse(start=4930, duration=-pi_ge_time, amplitude=ge_amp, ssm_freq=ssm_ge, phase=0) #pulse is also a class p is an instance
    ringupdown_seq.add_sweep(channel=1, sweep_name='start',start=0,stop=-ramsey_time, initial_pulse=pi_ge)
    pi_ge.phase = 90
    ringupdown_seq.add_sweep(channel=2, sweep_name='start',start=0,stop=-ramsey_time ,initial_pulse=pi_ge)
    
    pi2_ef = Pulse(start=4970, duration=-pi2_ef_time, amplitude=ef_amp, ssm_freq=ssm_ef, phase=90) #pulse is also a class p is an instance
    ringupdown_seq.add_sweep(channel=1, sweep_name='start', start=0, stop=-ramsey_time,initial_pulse=pi2_ef)
    pi2_ef.phase = 0
    ringupdown_seq.add_sweep(channel=2, sweep_name='start', start=0, stop=-ramsey_time,initial_pulse=pi2_ef)
    #p.phase = 90 #make the pulse phase 90 degrees to get the single sideband modulation
    #rabi_seq.add_sweep(channel=2, sweep_name='width', start=0, stop=-200,initial_pulse=p)
    pi2_ef = Pulse(start=5010, duration=-pi2_ef_time, amplitude=ef_amp, ssm_freq=ssm_ef, phase=90) #pulse is also a class p is an instance
    ringupdown_seq.add_sweep(channel=1, sweep_name='phase',start=0,stop=1800,initial_pulse=pi2_ef)
    pi2_ef.phase = 0
    ringupdown_seq.add_sweep(channel=2, sweep_name='phase',start=0,stop=1800,initial_pulse=pi2_ef)
    
    pi_ge = Pulse(start=5050, duration=-pi_ge_time, amplitude=ge_amp, ssm_freq=ssm_ge, phase=0) #pulse is also a class p is an instance
    ringupdown_seq.add_sweep(channel=1, sweep_name='none',initial_pulse=pi_ge)
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
        plt.imshow(channel1_ch[0:200,00:6000], aspect='auto', extent=[00,6000,200,0])
        plt.show()
        
    ## write output
    #write_dir = r"C:\arbsequences\strong_dispersive_withPython\test_pulse_ringupdown"
   # ringupdown_seq.write_sequence(base_name='foo', file_path=write_dir, use_range_01=False,num_offset=0)

    write_dir = r"C:\arbsequences\strong_dispersive_withPython\test_pulse_ringupdown_bin"
# 
    ringupdown_seq.write_sequence(base_name='foo', file_path=write_dir, use_range_01=False,num_offset=0, write_binary=True)
    ringupdown_seq.load_sequence('128.252.134.4', base_name='foo', file_path=write_dir, num_offset=0)
##END geom
    
def geom_ge_to_f(ramsey_time=500): #this is pulsed readout to ring up and ring down cavity dfor e state
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
    
    H_ge = Pulse(start=14960, duration=-ramsey_time, amplitude=0.125*ge_amp, ssm_freq=ssm_ge, phase=270) #pulse is also a class p is an instance
    ringupdown_seq.add_sweep(channel=1, sweep_name='none',initial_pulse=H_ge)
    H_ge.phase = 0
    ringupdown_seq.add_sweep(channel=2,  sweep_name='none',initial_pulse=H_ge)
    
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
        #plt.imshow(channel1_ch[0:200,00:8000], aspect='auto', extent=[00,8000,200,0])
        #plt.show()
        
    ## write output
    #write_dir = r"C:\arbsequences\strong_dispersive_withPython\test_pulse_ringupdown"
   # ringupdown_seq.write_sequence(base_name='foo', file_path=write_dir, use_range_01=False,num_offset=0)

    write_dir = r"C:\arbsequences\strong_dispersive_withPython\test_pulse_ringupdown_bin"
# 
    ringupdown_seq.write_sequence(base_name='foo', file_path=write_dir, use_range_01=False,num_offset=0, write_binary=True)
    ringupdown_seq.load_sequence('128.252.134.4', base_name='foo', file_path=write_dir, num_offset=0)
##END geom
    
def ramseyef_long(): #this is pulsed readout to ring up and ring down cavity dfor e state
    file_length = 18000
    num_steps = 101
    ringupdown_seq = Sequence(file_length, num_steps) #this creates something called rabi_seq that is an instance of a sequence class

    ## channels   
    ramsey_time = 10000
    pi_ge_time= 28
    ge_amp=.5
    pi2_ef_time= 10
    ef_amp=1
    ssm_ge = .110
    ssm_ef= .210
    readout_amp = 1#0.1 # set this to 0.1 for the dispersive readout
    scale_factor= 0 # this is for another readout that is always on, to test dephasing
    
    pi_ge = Pulse(start=14960, duration=-pi_ge_time, amplitude=ge_amp, ssm_freq=ssm_ge, phase=0) #pulse is also a class p is an instance
    ringupdown_seq.add_sweep(channel=1, sweep_name='start',start=0,stop=-ramsey_time, initial_pulse=pi_ge)
    pi_ge.phase = 90
    ringupdown_seq.add_sweep(channel=2, sweep_name='start',start=0,stop=-ramsey_time ,initial_pulse=pi_ge)
    
    pi2_ef = Pulse(start=14990, duration=-pi2_ef_time, amplitude=ef_amp, ssm_freq=ssm_ef, phase=90) #pulse is also a class p is an instance
    ringupdown_seq.add_sweep(channel=1, sweep_name='start', start=0, stop=-ramsey_time,initial_pulse=pi2_ef)
    pi2_ef.phase = 0
    ringupdown_seq.add_sweep(channel=2, sweep_name='start', start=0, stop=-ramsey_time,initial_pulse=pi2_ef)
    #p.phase = 90 #make the pulse phase 90 degrees to get the single sideband modulation
    #rabi_seq.add_sweep(channel=2, sweep_name='width', start=0, stop=-200,initial_pulse=p)
    pi2_ef = Pulse(start=15020, duration=-pi2_ef_time, amplitude=ef_amp, ssm_freq=ssm_ef, phase=90) #pulse is also a class p is an instance
    ringupdown_seq.add_sweep(channel=1, sweep_name='none',initial_pulse=pi2_ef)
    pi2_ef.phase = 0
    ringupdown_seq.add_sweep(channel=2, sweep_name='none',initial_pulse=pi2_ef)
    
    pi_ge = Pulse(start=15050, duration=-pi_ge_time, amplitude=ge_amp, ssm_freq=ssm_ge, phase=0) #pulse is also a class p is an instance
    ringupdown_seq.add_sweep(channel=1, sweep_name='none',initial_pulse=pi_ge)
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
        plt.imshow(channel1_ch[0:200,00:6000], aspect='auto', extent=[00,6000,200,0])
        plt.show()
        
    ## write output
    #write_dir = r"C:\arbsequences\strong_dispersive_withPython\test_pulse_ringupdown"
   # ringupdown_seq.write_sequence(base_name='foo', file_path=write_dir, use_range_01=False,num_offset=0)

    write_dir = r"C:\arbsequences\strong_dispersive_withPython\test_pulse_ringupdown_bin"
# 
    ringupdown_seq.write_sequence(base_name='foo', file_path=write_dir, use_range_01=False,num_offset=0, write_binary=True)
    ringupdown_seq.load_sequence('128.252.134.4', base_name='foo', file_path=write_dir, num_offset=0)
##END geom
def ramseyef_vary(ramsey_time=500): #this is pulsed readout to ring up and ring down cavity dfor e state
    file_length = 18000
    num_steps = 101
    ringupdown_seq = Sequence(file_length, num_steps) #this creates something called rabi_seq that is an instance of a sequence class

    ## channels   
    
    pi_ge_time= 28
    ge_amp=.5
    pi2_ef_time= 10
    ef_amp=1
    ssm_ge = .110
    ssm_ef= .210
    readout_amp = 1#0.1 # set this to 0.1 for the dispersive readout
    scale_factor= 0 # this is for another readout that is always on, to test dephasing
    
    pi_ge = Pulse(start=14960-ramsey_time, duration=-pi_ge_time, amplitude=ge_amp, ssm_freq=ssm_ge, phase=0) #pulse is also a class p is an instance
    ringupdown_seq.add_sweep(channel=1, sweep_name='none', initial_pulse=pi_ge)
    pi_ge.phase = 90
    ringupdown_seq.add_sweep(channel=2, sweep_name='none',initial_pulse=pi_ge)
    
    pi2_ef = Pulse(start=14990-ramsey_time, duration=-pi2_ef_time, amplitude=ef_amp, ssm_freq=ssm_ef, phase=90) #pulse is also a class p is an instance
    ringupdown_seq.add_sweep(channel=1, sweep_name='none', initial_pulse=pi2_ef)
    pi2_ef.phase = 0
    ringupdown_seq.add_sweep(channel=2, sweep_name='none', initial_pulse=pi2_ef)
    #p.phase = 90 #make the pulse phase 90 degrees to get the single sideband modulation
    #rabi_seq.add_sweep(channel=2, sweep_name='width', start=0, stop=-200,initial_pulse=p)
    pi2_ef = Pulse(start=15020, duration=-pi2_ef_time, amplitude=ef_amp, ssm_freq=ssm_ef, phase=90) #pulse is also a class p is an instance
    ringupdown_seq.add_sweep(channel=1, sweep_name='phase',start=0,stop=360,initial_pulse=pi2_ef)
    pi2_ef.phase = 0
    ringupdown_seq.add_sweep(channel=2, sweep_name='phase',start=0,stop=360,initial_pulse=pi2_ef)
    
    pi_ge = Pulse(start=15050, duration=-pi_ge_time, amplitude=ge_amp, ssm_freq=ssm_ge, phase=0) #pulse is also a class p is an instance
    ringupdown_seq.add_sweep(channel=1, sweep_name='none',initial_pulse=pi_ge)
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
        #plt.imshow(channel1_ch[0:200,00:6000], aspect='auto', extent=[00,6000,200,0])
        #plt.show()
        
    ## write output
    #write_dir = r"C:\arbsequences\strong_dispersive_withPython\test_pulse_ringupdown"
   # ringupdown_seq.write_sequence(base_name='foo', file_path=write_dir, use_range_01=False,num_offset=0)

    write_dir = r"C:\arbsequences\strong_dispersive_withPython\test_pulse_ringupdown_bin"
# 
    ringupdown_seq.write_sequence(base_name='foo', file_path=write_dir, use_range_01=False,num_offset=0, write_binary=True)
    ringupdown_seq.load_sequence('128.252.134.4', base_name='foo', file_path=write_dir, num_offset=0)
##END geom    
def ramseyef_test(ssm_ef= .210): #this is pulsed readout to ring up and ring down cavity dfor e state
    file_length = 8000
    num_steps = 101
    ringupdown_seq = Sequence(file_length, num_steps) #this creates something called rabi_seq that is an instance of a sequence class

    ## channels   
    ramsey_time = 2000
    pi_ge_time= 28
    pi2_ef_time= 10
    ssm_ge = .110
    pre3_amp = 0.8
    pre_time = 30
    pre4_amp = 0.1
    readout_amp = 1#0.1 # set this to 0.1 for the dispersive readout
    scale_factor= 0 # this is for another readout that is always on, to test dephasing
    
    pi_ge = Pulse(start=4960, duration=-pi_ge_time, amplitude=0.5, ssm_freq=ssm_ge, phase=0) #pulse is also a class p is an instance
    ringupdown_seq.add_sweep(channel=1, sweep_name='start',start=0,stop=-ramsey_time, initial_pulse=pi_ge)
    pi_ge.phase = 90
    ringupdown_seq.add_sweep(channel=2, sweep_name='start',start=0,stop=-ramsey_time ,initial_pulse=pi_ge)
    
    pi2_ef = Pulse(start=4990, duration=-pi2_ef_time, amplitude=1, ssm_freq=ssm_ef, phase=90) #pulse is also a class p is an instance
    ringupdown_seq.add_sweep(channel=1, sweep_name='start', start=0, stop=-ramsey_time,initial_pulse=pi2_ef)
    pi2_ef.phase = 0
    ringupdown_seq.add_sweep(channel=2, sweep_name='start', start=0, stop=-ramsey_time,initial_pulse=pi2_ef)
    #p.phase = 90 #make the pulse phase 90 degrees to get the single sideband modulation
    #rabi_seq.add_sweep(channel=2, sweep_name='width', start=0, stop=-200,initial_pulse=p)
    pi2_ef = Pulse(start=5020, duration=-pi2_ef_time, amplitude=1, ssm_freq=ssm_ef, phase=90) #pulse is also a class p is an instance
    ringupdown_seq.add_sweep(channel=1, sweep_name='none',initial_pulse=pi2_ef)
    pi2_ef.phase = 0
    ringupdown_seq.add_sweep(channel=2, sweep_name='none', initial_pulse=pi2_ef)
    
    pi_ge = Pulse(start=5050, duration=-pi_ge_time, amplitude=0.5, ssm_freq=ssm_ge, phase=0) #pulse is also a class p is an instance
    ringupdown_seq.add_sweep(channel=1, sweep_name='none',initial_pulse=pi_ge)
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
        #plt.imshow(channel1_ch[0:200,00:6000], aspect='auto', extent=[00,6000,200,0])
        #plt.show()
        
    ## write output
    #write_dir = r"C:\arbsequences\strong_dispersive_withPython\test_pulse_ringupdown"
   # ringupdown_seq.write_sequence(base_name='foo', file_path=write_dir, use_range_01=False,num_offset=0)

    write_dir = r"C:\arbsequences\strong_dispersive_withPython\test_pulse_ringupdown_bin"
# 
    ringupdown_seq.write_sequence(base_name='foo', file_path=write_dir, use_range_01=False,num_offset=0, write_binary=True)
    ringupdown_seq.load_sequence('128.252.134.4', base_name='foo', file_path=write_dir, num_offset=0)
##END geom
    
def Ramsey(): 
    file_length = 18000
    num_steps = 101
    ringupdown_seq = Sequence(file_length, num_steps) #this creates something called rabi_seq that is an instance of a sequence class

    ## channels    
    pi2_ge_time = 15
    ramsey_time = 15000
    ssm_ge = 0.110
    ssm_ef = 0.046
    pre3_amp = 0.8
    pre_time = 30
    pre4_amp = 0.1
    post4_amp = -0.4
    post3_amp = -.2
    post_time = pre_time
    readout_amp = 1
    scaling_factor = 0
    
    
    
    #this is the first pi/2 pulse in the sequence
    pi2_ge = Pulse(start=15030, duration=-pi2_ge_time, amplitude=1, ssm_freq=ssm_ge, phase=0) #pulse is also a class p is an instance
    ringupdown_seq.add_sweep(channel=1, sweep_name='start', start=0, stop=-ramsey_time,initial_pulse=pi2_ge)
    pi2_ge.phase = 90
    ringupdown_seq.add_sweep(channel=2,  sweep_name='start', start=0, stop=-ramsey_time,initial_pulse=pi2_ge)
    #p.phase = 90 #make the pulse phase 90 degrees to get the single sideband modulation
    #rabi_seq.add_sweep(channel=2, sweep_name='width', start=0, stop=-200,initial_pulse=p)

    
    pi2_ge = Pulse(start=15060, duration=-pi2_ge_time, amplitude=1, ssm_freq=ssm_ge, phase=0) #pulse is also a class p is an instance
    ringupdown_seq.add_sweep(channel=1, sweep_name='none',initial_pulse=pi2_ge)
    pi2_ge.phase = 90
    ringupdown_seq.add_sweep(channel=2,  sweep_name='none',initial_pulse=pi2_ge)

#    
#    pre_pulse = Pulse(start = 5100,duration = -pre_time, amplitude=pre3_amp )
#    ringupdown_seq.add_sweep(channel=3, sweep_name='none',initial_pulse=pre_pulse)
#    pre_pulse = Pulse(start = 5100,duration = -pre_time, amplitude=pre4_amp )
#    ringupdown_seq.add_sweep(channel=4, sweep_name='none',initial_pulse=pre_pulse)
#    
    main_pulse = Pulse(start = 15100,duration = 1000, amplitude= readout_amp )
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
#    write_dir = r"C:\arbsequences\strong_dispersive_withPython\test_pulse_ringupdown"
#    ringupdown_seq.write_sequence(base_name='foo', file_path=write_dir, use_range_01=False,num_offset=0)
    write_dir = r"C:\arbsequences\strong_dispersive_withPython\test_pulse_ringupdown_bin"
# 
    ringupdown_seq.write_sequence(base_name='foo', file_path=write_dir, use_range_01=False,num_offset=0, write_binary=True)
    ringupdown_seq.load_sequence('128.252.134.4', base_name='foo', file_path=write_dir, num_offset=0)
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
    #p.phase = 90 #make the pulse phase 90 degrees to get the single sideband mod
    ulation
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
    pass
    #pulsed_readout_ramsey_GE()
    #rabi_gaussian()
    #Ramsey()
    #T1()
    #T1_constant()
    #rabi_constant()
    #ramsey_constant()
    #ramseyef_constant()
    #ramseygf_constant()
    rabi()
    #pulsed_readout_ramsey_EF_conti()
    #ramseyef()
    #pulsed_readout_rabi_EF_test()
    #pulsed_readout_rabi_EF_test_2()
    #pulsed_readout_rabi_GE_test()
    #pulsed_readout_rabi_GE_test_2()
#    rabi_test()
#    rabi_test_20200803()
    #rabief()
    #Epop()
    #Fpop_G()
    #Fpop_E()
    #ramsey_GE()
    #rabief_test()
    #prep_GEF_pulsereadout()
    #ramseyef_vary()
    #ramseyef_long()
    #geom_ge_to_f()
   #rabi_90()
#    pulsed_readout_ramsey_EF()