import numpy as np
import sys
sys.path.append(r"C:\Users\crow104\Documents\Python Scripts\sequence_generator")
from generator import *
import os
pi = np.pi
import matplotlib.pyplot as plt


def rabi(): #this is pulsed readout to ring up and ring down cavity dfor e state
     # set BNC to 5.0625 GhZ
    file_length = 8000
    num_steps = 101
    the_seq = Sequence(file_length, num_steps) #this creates something called the_seq that is an instance of a sequence class

    ## channels   
    rabi_time = 100
    ssm_ge = .0595
        
    pi2_ge = Pulse(start=6995, duration=0, amplitude=1, ssm_freq=ssm_ge, phase=0) #pulse is also a class p is an instance
    the_seq.add_sweep(channel=1, sweep_name='width', start=0, stop=-rabi_time,initial_pulse=pi2_ge)
    pi2_ge.phase = 90
    the_seq.add_sweep(channel=2,  sweep_name='width', start=0, stop=-rabi_time,initial_pulse=pi2_ge)
    #p.phase = 90 #make the pulse phase 90 degrees to get the single sideband modulation
    #rabi_seq.add_sweep(channel=2, sweep_name='width', start=0, stop=-200,initial_pulse=p)

    #main readout
    main_pulse = Pulse(start = 7000,duration = 1000, amplitude= 1 )
    the_seq.add_sweep(channel=4,  sweep_name='none',initial_pulse=main_pulse)
    
    
    ## markers
    alazar_trigger = Pulse(start=file_length-7000, duration=500, amplitude=1)
    the_seq.add_sweep(channel=3, marker=1, sweep_name='none', initial_pulse=alazar_trigger )
    

    ##create the gate for ch1 an ch2
    the_seq.add_gate(source_1=1, source_2=2, destination_tuple=(1,1))
    
    channel1_channel = the_seq.channel_list[0][0] # dim 0: channel 1; dim 1: [ch,m1,m2]
    channel2_channel = the_seq.channel_list[1][0] # dim 0: channel 1; dim 1: [ch,m1,m2]
    both_ch1_ch2 = channel1_channel**2 + channel2_channel**2
    qubit_gate = create_gate(both_ch1_ch2)
    the_seq.channel_list[0][1] = qubit_gate

    ## view output
    if True:
        channel1_ch = the_seq.channel_list[0][0] #[channel name -1][0:channel, 1:marker 1, 2:marker 2]
        channel2_ch = the_seq.channel_list[1][0]
        channel3_ch = the_seq.channel_list[2][0]
        channel4_ch = the_seq.channel_list[3][0]
        plt.imshow(channel2_ch[0:200,6000:7000], aspect='auto', extent=[6000,7000,200,0])
#        plt.show()
        
    ## write output
#    write_dir = r"C:\Data\2019\encircling\python_loading"
#    the_seq.write_sequence(base_name='foo', file_path=write_dir, use_range_01=False,num_offset=0)
    ## write output
#    write_dir = r"C:\arbsequences\strong_dispersive_withPython\test_pulse_ringupdown"
#    ringupdown_seq.write_sequence(base_name='foo', file_path=write_dir, use_range_01=False,num_offset=0)
    write_dir = r"C:\arbsequences\strong_dispersive_withPython\test_pulse_ringupdown_bin"
# 
    the_seq.write_sequence(base_name='foo', file_path=write_dir, use_range_01=False,num_offset=0, write_binary=True)
    the_seq.load_sequence('128.252.134.4', base_name='foo', file_path=write_dir, num_offset=0)
##END geom
    
    
def T1(): #this is pulsed readout to ring up and ring down cavity dfor e state
    file_length = 38000
    num_steps = 101
    the_seq = Sequence(file_length, num_steps) #this creates something called the_seq that is an instance of a sequence class

    ## channels   
    pi_time = 39
    ssm_ge = 0.0595
    T1_scan_duration= 30000
    
    pi2_ge = Pulse(start=36995, duration=-pi_time, amplitude=1, ssm_freq=ssm_ge, phase=0) #pulse is also a class p is an instance
    the_seq.add_sweep(channel=1, sweep_name='start', start=0, stop=-T1_scan_duration,initial_pulse=pi2_ge)
    pi2_ge.phase = 90
    the_seq.add_sweep(channel=2,  sweep_name='start', start=0, stop=-T1_scan_duration,initial_pulse=pi2_ge)
    #p.phase = 90 #make the pulse phase 90 degrees to get the single sideband modulation
    #rabi_seq.add_sweep(channel=2, sweep_name='width', start=0, stop=-200,initial_pulse=p)
    
    
    #main readout
    main_pulse = Pulse(start = 37000,duration = 1000, amplitude= 1 )
    the_seq.add_sweep(channel=4,  sweep_name='none',initial_pulse=main_pulse)
    
    
    ## markers
    alazar_trigger = Pulse(start=file_length-7000, duration=500, amplitude=1)
    the_seq.add_sweep(channel=3, marker=1, sweep_name='none', initial_pulse=alazar_trigger )
    

    ##create the gate for ch1 an ch2
    the_seq.add_gate(source_1=1, source_2=2, destination_tuple=(1,1))
    
    channel1_channel = the_seq.channel_list[0][0] # dim 0: channel 1; dim 1: [ch,m1,m2]
    channel2_channel = the_seq.channel_list[1][0] # dim 0: channel 1; dim 1: [ch,m1,m2]
    both_ch1_ch2 = channel1_channel**2 + channel2_channel**2
    qubit_gate = create_gate(both_ch1_ch2)
    the_seq.channel_list[0][1] = qubit_gate

    ## view output
    if True:
        channel1_ch = the_seq.channel_list[0][0] #[channel name -1][0:channel, 1:marker 1, 2:marker 2]
        channel2_ch = the_seq.channel_list[1][0]
        channel3_ch = the_seq.channel_list[2][0]
        channel4_ch = the_seq.channel_list[3][0]
        plt.imshow(channel2_ch[0:200,6000:7000], aspect='auto', extent=[6000,7000,200,0])
#        plt.show()
        
    ## write output
#    write_dir = r"C:\Data\2019\encircling\python_loading"
#    the_seq.write_sequence(base_name='foo', file_path=write_dir, use_range_01=False,num_offset=0)
    ## write output
#    write_dir = r"C:\arbsequences\strong_dispersive_withPython\test_pulse_ringupdown"
#    ringupdown_seq.write_sequence(base_name='foo', file_path=write_dir, use_range_01=False,num_offset=0)
    write_dir = r"C:\arbsequences\strong_dispersive_withPython\test_pulse_ringupdown_bin"
# 
    the_seq.write_sequence(base_name='foo', file_path=write_dir, use_range_01=False,num_offset=0, write_binary=True)
    the_seq.load_sequence('128.252.134.4', base_name='foo', file_path=write_dir, num_offset=0)
##END geom
    
def rabief(): #this is pulsed readout to ring up and ring down cavity dfor e state
     # set BNC to 5.0625 GhZ
    file_length = 8000
    num_steps = 101
    the_seq = Sequence(file_length, num_steps) #this creates something called the_seq that is an instance of a sequence class

    ## channels
    pi_time = 38
    rabi_time = 400
    ssm_ge = .0595
    ssm_ef = .25753
    
        
    pi2_ge = Pulse(start=6995, duration=-pi_time, amplitude=1, ssm_freq=ssm_ge, phase=0) #pulse is also a class p is an instance
    the_seq.add_sweep(channel=1,  sweep_name='none',initial_pulse=pi2_ge)
    pi2_ge.phase = 90
    the_seq.add_sweep(channel=2,  sweep_name='none',initial_pulse=pi2_ge)
    
    #p.phase = 90 #make the pulse phase 90 degrees to get the single sideband modulation
    #rabi_seq.add_sweep(channel=2, sweep_name='width', start=0, stop=-200,initial_pulse=p)
    
    pi2_ef = Pulse(start=6995-pi_time-5, duration=0, amplitude=1, ssm_freq=ssm_ef, phase=90) 
    the_seq.add_sweep(channel=1, sweep_name='width', start=0, stop=-rabi_time,initial_pulse=pi2_ef)
    pi2_ef.phase = 0
    the_seq.add_sweep(channel=2,  sweep_name='width', start=0, stop=-rabi_time,initial_pulse=pi2_ef)
    
    pi2_ge = Pulse(start=6995-pi_time-10, duration=-pi_time, amplitude=1, ssm_freq=ssm_ge, phase=0) 
    the_seq.add_sweep(channel=1, sweep_name='start', start=0, stop=-rabi_time,initial_pulse=pi2_ge)
    pi2_ge.phase = 90
    the_seq.add_sweep(channel=2,  sweep_name='start', start=0, stop=-rabi_time,initial_pulse=pi2_ge)
    #main readout
    
    main_pulse = Pulse(start = 7000,duration = 1000, amplitude= 1 )
    the_seq.add_sweep(channel=4,  sweep_name='none',initial_pulse=main_pulse)
    
    
    ## markers
    alazar_trigger = Pulse(start=file_length-7000, duration=500, amplitude=1)
    the_seq.add_sweep(channel=3, marker=1, sweep_name='none', initial_pulse=alazar_trigger )
    

    ##create the gate for ch1 an ch2
    the_seq.add_gate(source_1=1, source_2=2, destination_tuple=(1,1))
    
    channel1_channel = the_seq.channel_list[0][0] # dim 0: channel 1; dim 1: [ch,m1,m2]
    channel2_channel = the_seq.channel_list[1][0] # dim 0: channel 1; dim 1: [ch,m1,m2]
    both_ch1_ch2 = channel1_channel**2 + channel2_channel**2
    qubit_gate = create_gate(both_ch1_ch2)
    the_seq.channel_list[0][1] = qubit_gate

    ## view output
    if True:
        channel1_ch = the_seq.channel_list[0][0] #[channel name -1][0:channel, 1:marker 1, 2:marker 2]
        channel2_ch = the_seq.channel_list[1][0]
        channel3_ch = the_seq.channel_list[2][0]
        channel4_ch = the_seq.channel_list[3][0]
        plt.imshow(channel2_ch[0:200,6000:7000], aspect='auto', extent=[6000,7000,200,0])
#        plt.show()
        
    ## write output
#    write_dir = r"C:\Data\2019\encircling\python_loading"
#    the_seq.write_sequence(base_name='foo', file_path=write_dir, use_range_01=False,num_offset=0)
    ## write output
#    write_dir = r"C:\arbsequences\strong_dispersive_withPython\test_pulse_ringupdown"
#    ringupdown_seq.write_sequence(base_name='foo', file_path=write_dir, use_range_01=False,num_offset=0)
    write_dir = r"C:\arbsequences\strong_dispersive_withPython\test_pulse_ringupdown_bin"
# 
    the_seq.write_sequence(base_name='foo', file_path=write_dir, use_range_01=False,num_offset=0, write_binary=True)
    the_seq.load_sequence('128.252.134.4', base_name='foo', file_path=write_dir, num_offset=0)
##END geom

def rabi2f(): #this is pulsed readout to ring up and ring down cavity dfor e state
    # set BNC to 5.0625 GhZ
    file_length = 8000
    num_steps = 101
    the_seq = Sequence(file_length, num_steps) #this creates something called the_seq that is an instance of a sequence class

    ## channels   
    rabi_time = 4000
    
    ssm_gf = 0.09872
    
    
    
    
    
    
    
    
    
    
    
    
    
    #ssm_ef = 0.22
    #pi_fe_time = 60
    
    
    #pi2_fe = Pulse(start=6995, duration=-pi_fe_time, amplitude=1, ssm_freq=ssm_ef, phase=90) #pulse is also a class p is an instance
    #the_seq.add_sweep(channel=1,  sweep_name='none',initial_pulse=pi2_fe)
    #pi2_fe.phase = 0
    #the_seq.add_sweep(channel=2,  sweep_name='none',initial_pulse=pi2_fe)
    
        
    pi2_gf = Pulse(start=6995, duration=0, amplitude=1, ssm_freq=ssm_gf, phase=90) #pulse is also a class p is an instance
    the_seq.add_sweep(channel=1, sweep_name='width', start=0, stop=-rabi_time,initial_pulse=pi2_gf)
    pi2_gf.phase = 0
    the_seq.add_sweep(channel=2,  sweep_name='width', start=0, stop=-rabi_time,initial_pulse=pi2_gf)
    #p.phase = 90 #make the pulse phase 90 degrees to get the single sideband modulation
    #rabi_seq.add_sweep(channel=2, sweep_name='width', start=0, stop=-200,initial_pulse=p)

    #main readout
    main_pulse = Pulse(start = 7000,duration = 1000, amplitude= 1 )
    the_seq.add_sweep(channel=4,  sweep_name='none',initial_pulse=main_pulse)
    
    
    ## markers
    alazar_trigger = Pulse(start=file_length-7000, duration=500, amplitude=1)
    the_seq.add_sweep(channel=3, marker=1, sweep_name='none', initial_pulse=alazar_trigger )
    

    ##create the gate for ch1 an ch2
    the_seq.add_gate(source_1=1, source_2=2, destination_tuple=(1,1))
    
    channel1_channel = the_seq.channel_list[0][0] # dim 0: channel 1; dim 1: [ch,m1,m2]
    channel2_channel = the_seq.channel_list[1][0] # dim 0: channel 1; dim 1: [ch,m1,m2]
    both_ch1_ch2 = channel1_channel**2 + channel2_channel**2
    qubit_gate = create_gate(both_ch1_ch2)
    the_seq.channel_list[0][1] = qubit_gate

    ## view output
    if True:
        channel1_ch = the_seq.channel_list[0][0] #[channel name -1][0:channel, 1:marker 1, 2:marker 2]
        channel2_ch = the_seq.channel_list[1][0]
        channel3_ch = the_seq.channel_list[2][0]
        channel4_ch = the_seq.channel_list[3][0]
        plt.imshow(channel2_ch[0:200,6000:7000], aspect='auto', extent=[6000,7000,200,0])
#        plt.show()
        
    ## write output
#    write_dir = r"C:\Data\2019\encircling\python_loading"
#    the_seq.write_sequence(base_name='foo', file_path=write_dir, use_range_01=False,num_offset=0)
    ## write output
#    write_dir = r"C:\arbsequences\strong_dispersive_withPython\test_pulse_ringupdown"
#    ringupdown_seq.write_sequence(base_name='foo', file_path=write_dir, use_range_01=False,num_offset=0)
    write_dir = r"C:\arbsequences\strong_dispersive_withPython\test_pulse_ringupdown_bin"
# 
    the_seq.write_sequence(base_name='foo', file_path=write_dir, use_range_01=False,num_offset=0, write_binary=True)
    the_seq.load_sequence('128.252.134.4', base_name='foo', file_path=write_dir, num_offset=0)
##END geom

def T12f(): #this is pulsed readout to ring up and ring down cavity dfor e state
    # set BNC to 5.0625 GhZ
    file_length = 68000
    num_steps = 101
    the_seq = Sequence(file_length, num_steps) #this creates something called the_seq that is an instance of a sequence class

    ## channels   
    pi_time = 1200
    ssm_gf = 0.09872
    T1_scan_duration= 60000
    
    pi2_gf = Pulse(start=66995, duration=-pi_time, amplitude=1, ssm_freq=ssm_gf, phase=90) #pulse is also a class p is an instance
    the_seq.add_sweep(channel=1, sweep_name='start', start=0, stop=-T1_scan_duration,initial_pulse=pi2_gf)
    pi2_gf.phase = 0
    the_seq.add_sweep(channel=2,  sweep_name='start', start=0, stop=-T1_scan_duration,initial_pulse=pi2_gf)
    #p.phase = 90 #make the pulse phase 90 degrees to get the single sideband modulation
    #rabi_seq.add_sweep(channel=2, sweep_name='width', start=0, stop=-200,initial_pulse=p)
    
    
    #main readout
    main_pulse = Pulse(start = 67000,duration = 1000, amplitude= 1 )
    the_seq.add_sweep(channel=4,  sweep_name='none',initial_pulse=main_pulse)
    
    
    ## markers
    alazar_trigger = Pulse(start=file_length-7000, duration=500, amplitude=1)
    the_seq.add_sweep(channel=3, marker=1, sweep_name='none', initial_pulse=alazar_trigger )
    

    ##create the gate for ch1 an ch2
    the_seq.add_gate(source_1=1, source_2=2, destination_tuple=(1,1))
    
    channel1_channel = the_seq.channel_list[0][0] # dim 0: channel 1; dim 1: [ch,m1,m2]
    channel2_channel = the_seq.channel_list[1][0] # dim 0: channel 1; dim 1: [ch,m1,m2]
    both_ch1_ch2 = channel1_channel**2 + channel2_channel**2
    qubit_gate = create_gate(both_ch1_ch2)
    the_seq.channel_list[0][1] = qubit_gate

    ## view output
    if True:
        channel1_ch = the_seq.channel_list[0][0] #[channel name -1][0:channel, 1:marker 1, 2:marker 2]
        channel2_ch = the_seq.channel_list[1][0]
        channel3_ch = the_seq.channel_list[2][0]
        channel4_ch = the_seq.channel_list[3][0]
        plt.imshow(channel2_ch[0:200,66000:67000], aspect='auto', extent=[66000,67000,200,0])
#        plt.show()
        
    ## write output
#    write_dir = r"C:\Data\2019\encircling\python_loading"
#    the_seq.write_sequence(base_name='foo', file_path=write_dir, use_range_01=False,num_offset=0)
    ## write output
#    write_dir = r"C:\arbsequences\strong_dispersive_withPython\test_pulse_ringupdown"
#    ringupdown_seq.write_sequence(base_name='foo', file_path=write_dir, use_range_01=False,num_offset=0)
    write_dir = r"C:\arbsequences\strong_dispersive_withPython\test_pulse_ringupdown_bin"
# 
    the_seq.write_sequence(base_name='foo', file_path=write_dir, use_range_01=False,num_offset=0, write_binary=True)
    the_seq.load_sequence('128.252.134.4', base_name='foo', file_path=write_dir, num_offset=0)
##END geom
    
    
def T12f_eg(): #this is pulsed readout to ring up and ring down cavity dfor e state
    # set BNC to 5.0625 GhZ
    file_length = 68000
    num_steps = 101
    the_seq = Sequence(file_length, num_steps) #this creates something called the_seq that is an instance of a sequence class

    ## channels   
    pi_time_gf = 380
    ssm_gf = 0.0601
    pi_time_ge = 39
    ssm_ge = 0.0595
    T1_scan_duration= 60000
    
    pi2_ge = Pulse(start=66995, duration=-pi_time_ge, amplitude=1, ssm_freq=ssm_ge, phase=0) #pulse is also a class p is an instance
    the_seq.add_sweep(channel=1,  sweep_name='none',initial_pulse=pi2_ge)
    pi2_ge.phase = 90
    the_seq.add_sweep(channel=2,  sweep_name='none',initial_pulse=pi2_ge)
    
    pi2_gf = Pulse(start=66990-pi_time_ge, duration=-pi_time_gf, amplitude=1, ssm_freq=ssm_gf, phase=90) #pulse is also a class p is an instance
    the_seq.add_sweep(channel=1, sweep_name='start', start=0, stop=-T1_scan_duration,initial_pulse=pi2_gf)
    pi2_gf.phase = 0
    the_seq.add_sweep(channel=2,  sweep_name='start', start=0, stop=-T1_scan_duration,initial_pulse=pi2_gf)
    #p.phase = 90 #make the pulse phase 90 degrees to get the single sideband modulation
    #rabi_seq.add_sweep(channel=2, sweep_name='width', start=0, stop=-200,initial_pulse=p)
    
    
    #main readout
    main_pulse = Pulse(start = 67000,duration = 1000, amplitude= 1 )
    the_seq.add_sweep(channel=4,  sweep_name='none',initial_pulse=main_pulse)
    
    
    ## markers
    alazar_trigger = Pulse(start=file_length-7000, duration=500, amplitude=1)
    the_seq.add_sweep(channel=3, marker=1, sweep_name='none', initial_pulse=alazar_trigger )
    

    ##create the gate for ch1 an ch2
    the_seq.add_gate(source_1=1, source_2=2, destination_tuple=(1,1))
    
    channel1_channel = the_seq.channel_list[0][0] # dim 0: channel 1; dim 1: [ch,m1,m2]
    channel2_channel = the_seq.channel_list[1][0] # dim 0: channel 1; dim 1: [ch,m1,m2]
    both_ch1_ch2 = channel1_channel**2 + channel2_channel**2
    qubit_gate = create_gate(both_ch1_ch2)
    the_seq.channel_list[0][1] = qubit_gate

    ## view output
    if True:
        channel1_ch = the_seq.channel_list[0][0] #[channel name -1][0:channel, 1:marker 1, 2:marker 2]
        channel2_ch = the_seq.channel_list[1][0]
        channel3_ch = the_seq.channel_list[2][0]
        channel4_ch = the_seq.channel_list[3][0]
        plt.imshow(channel2_ch[0:200,66000:67000], aspect='auto', extent=[66000,67000,200,0])
#        plt.show()
        
    ## write output
#    write_dir = r"C:\Data\2019\encircling\python_loading"
#    the_seq.write_sequence(base_name='foo', file_path=write_dir, use_range_01=False,num_offset=0)
    ## write output
#    write_dir = r"C:\arbsequences\strong_dispersive_withPython\test_pulse_ringupdown"
#    ringupdown_seq.write_sequence(base_name='foo', file_path=write_dir, use_range_01=False,num_offset=0)
    write_dir = r"C:\arbsequences\strong_dispersive_withPython\test_pulse_ringupdown_bin"
# 
    the_seq.write_sequence(base_name='foo', file_path=write_dir, use_range_01=False,num_offset=0, write_binary=True)
    the_seq.load_sequence('128.252.134.4', base_name='foo', file_path=write_dir, num_offset=0)
##END geom
    
    
def T12f_fe(): #this is pulsed readout to ring up and ring down cavity dfor e state
    # set BNC to 5.0625 GhZ
    file_length = 68000
    num_steps = 101
    the_seq = Sequence(file_length, num_steps) #this creates something called the_seq that is an instance of a sequence class

    ## channels   
    pi_time_gf = 380
    ssm_gf = 0.0601
    pi_time_ge = 39
    ssm_ge = 0.0595
    ssm_ef= 0.2575
    pi_time_ef = 153
    T1_scan_duration= 60000
    
    pi2_ge = Pulse(start=66995, duration=-pi_time_ef, amplitude=1, ssm_freq=ssm_ef, phase=90) #pulse is also a class p is an instance
    the_seq.add_sweep(channel=1,  sweep_name='none',initial_pulse=pi2_ge)
    pi2_ge.phase = 0
    the_seq.add_sweep(channel=2,  sweep_name='none',initial_pulse=pi2_ge)
    
    pi2_ef = Pulse(start=66990-pi_time_ef, duration=-pi_time_gf, amplitude=1, ssm_freq=ssm_gf, phase=90) #pulse is also a class p is an instance
    the_seq.add_sweep(channel=1, sweep_name='start', start=0, stop=-T1_scan_duration,initial_pulse=pi2_ef)
    pi2_ef.phase = 0
    the_seq.add_sweep(channel=2,  sweep_name='start', start=0, stop=-T1_scan_duration,initial_pulse=pi2_ef)
    #p.phase = 90 #make the pulse phase 90 degrees to get the single sideband modulation
    #rabi_seq.add_sweep(channel=2, sweep_name='width', start=0, stop=-200,initial_pulse=p)
    
    
    #main readout
    main_pulse = Pulse(start = 67000,duration = 1000, amplitude= 1 )
    the_seq.add_sweep(channel=4,  sweep_name='none',initial_pulse=main_pulse)
    
    
    ## markers
    alazar_trigger = Pulse(start=file_length-7000, duration=500, amplitude=1)
    the_seq.add_sweep(channel=3, marker=1, sweep_name='none', initial_pulse=alazar_trigger )
    

    ##create the gate for ch1 an ch2
    the_seq.add_gate(source_1=1, source_2=2, destination_tuple=(1,1))
    
    channel1_channel = the_seq.channel_list[0][0] # dim 0: channel 1; dim 1: [ch,m1,m2]
    channel2_channel = the_seq.channel_list[1][0] # dim 0: channel 1; dim 1: [ch,m1,m2]
    both_ch1_ch2 = channel1_channel**2 + channel2_channel**2
    qubit_gate = create_gate(both_ch1_ch2)
    the_seq.channel_list[0][1] = qubit_gate

    ## view output
    if True:
        channel1_ch = the_seq.channel_list[0][0] #[channel name -1][0:channel, 1:marker 1, 2:marker 2]
        channel2_ch = the_seq.channel_list[1][0]
        channel3_ch = the_seq.channel_list[2][0]
        channel4_ch = the_seq.channel_list[3][0]
        plt.imshow(channel2_ch[0:200,66000:67000], aspect='auto', extent=[66000,67000,200,0])
#        plt.show()
        
    ## write output
#    write_dir = r"C:\Data\2019\encircling\python_loading"
#    the_seq.write_sequence(base_name='foo', file_path=write_dir, use_range_01=False,num_offset=0)
    ## write output
#    write_dir = r"C:\arbsequences\strong_dispersive_withPython\test_pulse_ringupdown"
#    ringupdown_seq.write_sequence(base_name='foo', file_path=write_dir, use_range_01=False,num_offset=0)
    write_dir = r"C:\arbsequences\strong_dispersive_withPython\test_pulse_ringupdown_bin"
# 
    the_seq.write_sequence(base_name='foo', file_path=write_dir, use_range_01=False,num_offset=0, write_binary=True)
    the_seq.load_sequence('128.252.134.4', base_name='foo', file_path=write_dir, num_offset=0)
##END geom
    
def T12f_gf(): #this is pulsed readout to ring up and ring down cavity dfor e state
    # set BNC to 5.0625 GhZ
    file_length = 68000
    num_steps = 101
    the_seq = Sequence(file_length, num_steps) #this creates something called the_seq that is an instance of a sequence class

    ## channels   
    pi_time_gf = 380
    ssm_gf = 0.0601
    pi_time_ge = 39
    ssm_ge = 0.0595
    ssm_ef= 0.2575
    pi_time_ef = 153
    T1_scan_duration= 60000
    
    pi2_ge = Pulse(start=66995, duration=-pi_time_gf, amplitude=1, ssm_freq=ssm_gf, phase=90) #pulse is also a class p is an instance
    the_seq.add_sweep(channel=1,  sweep_name='none',initial_pulse=pi2_ge)
    pi2_ge.phase = 0
    the_seq.add_sweep(channel=2,  sweep_name='none',initial_pulse=pi2_ge)
    
    pi2_gf = Pulse(start=66990-pi_time_gf, duration=-pi_time_gf, amplitude=1, ssm_freq=ssm_gf, phase=90) #pulse is also a class p is an instance
    the_seq.add_sweep(channel=1, sweep_name='start', start=0, stop=-T1_scan_duration,initial_pulse=pi2_gf)
    pi2_gf.phase = 0
    the_seq.add_sweep(channel=2,  sweep_name='start', start=0, stop=-T1_scan_duration,initial_pulse=pi2_gf)
    #p.phase = 90 #make the pulse phase 90 degrees to get the single sideband modulation
    #rabi_seq.add_sweep(channel=2, sweep_name='width', start=0, stop=-200,initial_pulse=p)
    
    
    #main readout
    main_pulse = Pulse(start = 67000,duration = 1000, amplitude= 1 )
    the_seq.add_sweep(channel=4,  sweep_name='none',initial_pulse=main_pulse)
    
    
    ## markers
    alazar_trigger = Pulse(start=file_length-7000, duration=500, amplitude=1)
    the_seq.add_sweep(channel=3, marker=1, sweep_name='none', initial_pulse=alazar_trigger )
    

    ##create the gate for ch1 an ch2
    the_seq.add_gate(source_1=1, source_2=2, destination_tuple=(1,1))
    
    channel1_channel = the_seq.channel_list[0][0] # dim 0: channel 1; dim 1: [ch,m1,m2]
    channel2_channel = the_seq.channel_list[1][0] # dim 0: channel 1; dim 1: [ch,m1,m2]
    both_ch1_ch2 = channel1_channel**2 + channel2_channel**2
    qubit_gate = create_gate(both_ch1_ch2)
    the_seq.channel_list[0][1] = qubit_gate

    ## view output
    if True:
        channel1_ch = the_seq.channel_list[0][0] #[channel name -1][0:channel, 1:marker 1, 2:marker 2]
        channel2_ch = the_seq.channel_list[1][0]
        channel3_ch = the_seq.channel_list[2][0]
        channel4_ch = the_seq.channel_list[3][0]
        plt.imshow(channel2_ch[0:200,66000:67000], aspect='auto', extent=[66000,67000,200,0])
#        plt.show()
        
    ## write output
#    write_dir = r"C:\Data\2019\encircling\python_loading"
#    the_seq.write_sequence(base_name='foo', file_path=write_dir, use_range_01=False,num_offset=0)
    ## write output
#    write_dir = r"C:\arbsequences\strong_dispersive_withPython\test_pulse_ringupdown"
#    ringupdown_seq.write_sequence(base_name='foo', file_path=write_dir, use_range_01=False,num_offset=0)
    write_dir = r"C:\arbsequences\strong_dispersive_withPython\test_pulse_ringupdown_bin"
# 
    the_seq.write_sequence(base_name='foo', file_path=write_dir, use_range_01=False,num_offset=0, write_binary=True)
    the_seq.load_sequence('128.252.134.4', base_name='foo', file_path=write_dir, num_offset=0)
##END geom
def T1f_ge_ef(): #this is pulsed readout to ring up and ring down cavity dfor e state
    # set BNC to 5.0625 GhZ
    file_length = 78000
    num_steps = 101
    the_seq = Sequence(file_length, num_steps) #this creates something called the_seq that is an instance of a sequence class

    ## channels   
    pi_time_ge = 39
    ssm_ge = 0.0595
    ssm_ef= 0.2575
    pi_time_ef = 130
    T1_scan_duration= 60000
#    pi2_ge1 = Pulse(start=66995, duration=-pi_time_ge, amplitude=1, ssm_freq=ssm_ge, phase=0) #pulse is also a class p is an instance
#    the_seq.add_sweep(channel=1,  sweep_name='none',initial_pulse=pi2_ge1)
#    pi2_ge1.phase = 90
#    the_seq.add_sweep(channel=2,  sweep_name='none',initial_pulse=pi2_ge1)
#    
    
    pi2_ef = Pulse(start=76995, duration=-pi_time_ef, amplitude=1, ssm_freq=ssm_ef, phase=90) #pulse is also a class p is an instance
    the_seq.add_sweep(channel=1, sweep_name='start', start=0, stop=-T1_scan_duration,initial_pulse=pi2_ef)
    pi2_ef.phase = 0
    the_seq.add_sweep(channel=2,  sweep_name='start', start=0, stop=-T1_scan_duration,initial_pulse=pi2_ef)
    #p.phase = 90 #make the pulse phase 90 degrees to get the single sideband modulation
    #rabi_seq.add_sweep(channel=2, sweep_name='width', start=0, stop=-200,initial_pulse=p)
    pi2_ge = Pulse(start=76995-5-pi_time_ef, duration=-pi_time_ge, amplitude=1, ssm_freq=ssm_ge, phase=0) #pulse is also a class p is an instance
    the_seq.add_sweep(channel=1, sweep_name='start', start=0, stop=-T1_scan_duration,initial_pulse=pi2_ge)
    pi2_ge.phase = 90
    the_seq.add_sweep(channel=2,  sweep_name='start', start=0, stop=-T1_scan_duration,initial_pulse=pi2_ge)
    
    #main readout
    main_pulse = Pulse(start = 77000,duration = 1000, amplitude= 1 )
    the_seq.add_sweep(channel=4,  sweep_name='none',initial_pulse=main_pulse)
    
    
    ## markers
    alazar_trigger = Pulse(start=file_length-7000, duration=500, amplitude=1)
    the_seq.add_sweep(channel=3, marker=1, sweep_name='none', initial_pulse=alazar_trigger )
    

    ##create the gate for ch1 an ch2
    the_seq.add_gate(source_1=1, source_2=2, destination_tuple=(1,1))
    
    channel1_channel = the_seq.channel_list[0][0] # dim 0: channel 1; dim 1: [ch,m1,m2]
    channel2_channel = the_seq.channel_list[1][0] # dim 0: channel 1; dim 1: [ch,m1,m2]
    both_ch1_ch2 = channel1_channel**2 + channel2_channel**2
    qubit_gate = create_gate(both_ch1_ch2)
    the_seq.channel_list[0][1] = qubit_gate

    ## view output
    if True:
        channel1_ch = the_seq.channel_list[0][0] #[channel name -1][0:channel, 1:marker 1, 2:marker 2]
        channel2_ch = the_seq.channel_list[1][0]
        channel3_ch = the_seq.channel_list[2][0]
        channel4_ch = the_seq.channel_list[3][0]
        plt.imshow(channel2_ch[0:200,76500:77000], aspect='auto', extent=[76500,77000,200,0])
#        plt.show()
        
    ## write output
#    write_dir = r"C:\Data\2019\encircling\python_loading"
#    the_seq.write_sequence(base_name='foo', file_path=write_dir, use_range_01=False,num_offset=0)
    ## write output
#    write_dir = r"C:\arbsequences\strong_dispersive_withPython\test_pulse_ringupdown"
#    ringupdown_seq.write_sequence(base_name='foo', file_path=write_dir, use_range_01=False,num_offset=0)
    write_dir = r"C:\arbsequences\strong_dispersive_withPython\test_pulse_ringupdown_bin"
# 
    the_seq.write_sequence(base_name='foo', file_path=write_dir, use_range_01=False,num_offset=0, write_binary=True)
    the_seq.load_sequence('128.252.134.4', base_name='foo', file_path=write_dir, num_offset=0)
##END geom
    
if __name__ == '__main__':
    pass
    #pulsed_readout_ramsey_GE()
    #rabi_gaussian()
    #Ramsey()
    #T1()
    #prep_GEF_pulsereadout()
    #rabi()
    #rabief()
    #rabi2f()
    #T12f()
    #T12f_eg()
    #T1_ge_ef()
    #T12f_fe()
    #T12f_gf()
    T1f_ge_ef()