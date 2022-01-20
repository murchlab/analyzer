# -*- coding: utf-8 -*-
"""
Sequence programs: sequence writer parameters and functions

@author: P. M. Harrington, 24 January 2020
"""

import numpy as np
import matplotlib.pyplot as plt
import generator as gen
import wx_programs
import expt_parameters

class Nop():
    pass

def setup_seq_writer():
    sw_setup = Nop()
    sw_setup.write_dir = r"C:\Data\2020\ep_metrology\dum"    
    sw_setup.load = True
    sw_setup.write = sw_setup.load
    sw_setup.show_figs = True
    
    sw_setup.address_awg = wx_programs.get_wx_address()
    
    return sw_setup

def get_pattern_parameters():
    pat = expt_parameters.get_pattern_parameters()
    return pat

def get_expt_cal():
    expt_cal = expt_parameters.get_expt_cal()
    return expt_cal

def add_iq_pulse_sweep(seq=None, pulse=None, sweep_name='none', start=0, stop=0, rotation_axis='+x', channel_pair='ch1ch2'):
    if pulse.ssm_freq is not None:
        if pulse.ssm_freq<0.:
            channel_phases = [90., 0.]
        else:
            channel_phases = [0., 90.]
    else:
        channel_phases = [0., 90.]
        
    if rotation_axis=='+x':
        pass
    elif rotation_axis=='+y':
        channel_phases = [x-90 for x in channel_phases]
    elif rotation_axis=='-x':
        channel_phases = [x-180 for x in channel_phases]
    elif rotation_axis=='-y':
        channel_phases = [x-270 for x in channel_phases]
        
    if channel_pair is 'ch1ch2':
        channel_pair_vals = [1, 2]
    elif channel_pair is 'ch3ch4':
        channel_pair_vals = [3, 4]
        
    for channel, phase_deg in zip(channel_pair_vals, channel_phases):
        pulse.phase = phase_deg
        seq.add_sweep(channel=channel,
                      sweep_name=sweep_name,
                      start=start,
                      stop=stop,
                      initial_pulse=pulse)
    return seq
    
def add_readout_markers_and_gates(seq=None, pat=None):
    # readout pulse
    main_pulse = gen.Pulse(start=pat.readout_start,
                           duration=pat.readout_duration,
                           amplitude=pat.readout_amplitude)
    
    seq.add_sweep(channel=1,
                  marker=2,
                  sweep_name='none',
                  initial_pulse=main_pulse)
    
    ## markers
    readout_trigger = gen.Pulse(start=pat.readout_trig_start,
                               duration=pat.readout_trig_duration,
                               amplitude=1)
    seq.add_sweep(channel=3, 
                  marker=1, 
                  sweep_name='none', 
                  initial_pulse=readout_trigger)
    
    # create the gate for ch1 an ch2
    seq.add_gate(source_1=1, source_2=2, destination_tuple=(1,1))
    
    channel1_channel = seq.channel_list[0][0] # dim 0: channel 1; dim 1: [ch,m1,m2]
    channel2_channel = seq.channel_list[1][0] # dim 0: channel 1; dim 1: [ch,m1,m2]
    both_ch1_ch2 = channel1_channel**2 + channel2_channel**2
    ch1ch2_gate = gen.create_gate(both_ch1_ch2)
    seq.channel_list[0][1] = ch1ch2_gate
    
    return seq

def write_patterns_to_disk(sw_setup=None, seq=None, num_offset=0):
    if sw_setup.write:
        seq.write_sequence(base_name='foo',
                           file_path=sw_setup.write_dir,
                           use_range_01=False,
                           num_offset=num_offset,
                           write_binary=True)

def make_seq_plots(sw_setup=None, pat=None, seq=None):

    if sw_setup.show_figs:
        channel1_ch = seq.channel_list[0][0] #[channel name -1][0:channel, 1:marker 1, 2:marker 2]
        channel2_ch = seq.channel_list[1][0]
        channel3_ch = seq.channel_list[2][0]
        channel4_ch = seq.channel_list[3][0]
        
        plt.figure()
        start_idx = 6000
        plt.imshow(channel2_ch[0:pat.num_patterns,start_idx:pat.final_pulse_end],
                   aspect='auto',
                   extent=[start_idx,pat.final_pulse_end,pat.num_patterns,0])
        
        t_start = pat.readout_start - 200
        t_end = pat.readout_start + 50
        times = np.arange(t_start, t_end)
        
        if pat.num_patterns==1:
            pat_index_plot = [0, 0]
        else:
            pat_index_plot = [1, pat.num_patterns-1]
            
        f, ax = plt.subplots(len(pat_index_plot), 2, figsize=(5,len(pat_index_plot)*2))
            
        print(pat_index_plot)
        for ch in range(2):
            for k, pat_idx in enumerate(pat_index_plot):
                ax[k, ch].plot(times, seq.channel_list[ch][0][pat_idx,t_start:t_end])
                ax[k, ch].set_ylim(-1, +1)
                ax[k, ch].set_title("Ch {}, pat# {}".format(ch+1,pat_idx+1))
        plt.show()
        
        plt.figure()
        plt.plot(seq.channel_list[0][0][1,0:200])
        plt.show()

def write_folder_to_awg(sw_setup=None, pat=None, seq=None):
    # make dummy sequence
    #the_seq = gen.Sequence(pat.pat_length, pat.num_patterns)
    
    # load from folder
    seq.load_sequence(sw_setup.address_awg,
                          base_name='foo',
                          file_path=sw_setup.write_dir,
                          num_offset=0)
    
def do_final_programs(sw_setup=None, pat=None, seq=None):
    
    # add readout pulses, triggers, and marker gates
    seq = add_readout_markers_and_gates(seq=seq, pat=pat)

    # display output
    make_seq_plots(sw_setup=sw_setup, pat=pat, seq=seq)
    
    print("Patterns: {}".format(pat.num_patterns))
    key_in = input("Continue? (y/n)")
    
    if key_in=="n":
        return
    else:
        # write and load patterns
        write_patterns_to_disk(sw_setup=sw_setup, seq=seq, num_offset=0)
        write_folder_to_awg(sw_setup=sw_setup, pat=pat, seq=seq)
        wx_programs.wx_set_and_amplitude_and_offset()