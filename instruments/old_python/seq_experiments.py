# -*- coding: utf-8 -*-
"""
Sequence experiments

@author: P. M. Harrington, 24 January 2020
"""

import numpy as np
import matplotlib.pyplot as plt
import expt_parameters
from seq_programs import *
import generator as gen
import wx_programs
    
def t1decay_ef(num_patterns=101, sweep_time=5000): # PMH 
    sw_setup = setup_seq_writer()
    pat = get_pattern_parameters()
    expt_cal = expt_parameters.get_expt_cal()
    
    #
    seq = gen.Sequence(pat.pat_length, num_patterns)
    
    # pi ge
    p = gen.Pulse(start=pat.final_pulse_end-expt_cal.pi_time.ef,
                  duration=-expt_cal.pi_time.ge,
                  amplitude=expt_cal.pi_amp.ge,
                  ssm_freq=expt_cal.ssm.ge)
    seq = add_iq_pulse_sweep(seq=seq,
                             pulse=p,
                             sweep_name='start',
                             start=0,
                             stop=-sweep_time,
                             channel_pair=expt_cal.channel_pair.ge)
    
    # pi ge
    p = gen.Pulse(start=pat.final_pulse_end,
                  duration=-expt_cal.pi_time.ef,
                  amplitude=expt_cal.pi_amp.ef,
                  ssm_freq=expt_cal.ssm.ef)
    seq = add_iq_pulse_sweep(seq=seq,
                             pulse=p,
                             sweep_name='start',
                             start=0,
                             stop=-sweep_time,
                             channel_pair=expt_cal.channel_pair.ef)
    
    # add readout pulses, triggers, and marker gates
    seq = add_readout_markers_and_gates(seq=seq, pat=pat)
    
    #
    the_seq = seq
    
    #
    print("Patterns: {}".format(the_seq.num_steps))
    the_seq.write_sequence()
    the_seq.load_sequence(sw_setup.address_awg)
    wx_programs.wx_set_and_amplitude_and_offset()
    
    #END
    
def g_e_f(): # PMH 
    sw_setup = setup_seq_writer()
    pat = get_pattern_parameters()
    expt_cal = expt_parameters.get_expt_cal()

    #
    num_patterns = 1
    end_time = pat.final_pulse_end
    
    # no pulse
    seq = gen.Sequence(pat.pat_length, num_patterns)
    p = gen.Pulse(start=end_time,
                  duration=-10,
                  amplitude=0)
    seq = add_iq_pulse_sweep(seq=seq,
                             pulse=p,
                             sweep_name='none')
    
    # add readout pulses, triggers, and marker gates
    seq = add_readout_markers_and_gates(seq=seq, pat=pat)
    
    #
    the_seq = seq
    
    # pi-ge
    seq = gen.Sequence(pat.pat_length, num_patterns)
    p = gen.Pulse(start=end_time,
                  duration=-expt_cal.pi_time.ge,
                  amplitude=expt_cal.pi_amp.ge,
                  ssm_freq=expt_cal.ssm.ge,
                  phase=0)
    seq = add_iq_pulse_sweep(seq=seq,
                             pulse=p,
                             sweep_name='none',
                             channel_pair=expt_cal.channel_pair.ge)
    
    # add readout pulses, triggers, and marker gates
    seq = add_readout_markers_and_gates(seq=seq, pat=pat)
    
    #
    the_seq = the_seq.__add__(seq)
    
    # pi-ge, pi-ef
    seq = gen.Sequence(pat.pat_length, num_patterns)
    p = gen.Pulse(start=end_time-expt_cal.pi_time.ef,
                  duration=-expt_cal.pi_time.ge,
                  amplitude=expt_cal.pi_amp.ge,
                  ssm_freq=expt_cal.ssm.ge,
                  phase=0)
    seq = add_iq_pulse_sweep(seq=seq,
                                 pulse=p,
                                 sweep_name='none',
                                 channel_pair=expt_cal.channel_pair.ge)
    p = gen.Pulse(start=end_time,
                  duration=-expt_cal.pi_time.ef,
                  amplitude=expt_cal.pi_amp.ef,
                  ssm_freq=expt_cal.ssm.ef,
                  phase=0)
    seq = add_iq_pulse_sweep(seq=seq,
                                 pulse=p,
                                 sweep_name='none',
                                 channel_pair=expt_cal.channel_pair.ef)
    
    # add readout pulses, triggers, and marker gates
    seq = add_readout_markers_and_gates(seq=seq, pat=pat)
    
    #
    the_seq = the_seq.__add__(seq)
    
    #
    print("Patterns: {}".format(the_seq.num_steps))
    the_seq.write_sequence()
    the_seq.load_sequence(sw_setup.address_awg)
    wx_programs.wx_set_and_amplitude_and_offset()
    
    #END
    
def pi_ef_cal_amp(num_patterns=101, sweep_start_stop=[0, 1]): # PMH 
    sw_setup = setup_seq_writer()
    pat = get_pattern_parameters()
    expt_cal = expt_parameters.get_expt_cal()
    
    #
    seq = gen.Sequence(pat.pat_length, num_patterns)
    
    # pi ge
    p = gen.Pulse(start=pat.final_pulse_end-expt_cal.pi_time.ef,
                  duration=-expt_cal.pi_time.ge,
                  amplitude=expt_cal.pi_amp.ge,
                  ssm_freq=expt_cal.ssm.ge,
                  phase=0)
    seq = add_iq_pulse_sweep(seq=seq,
                             pulse=p,
                             sweep_name='none',
                             channel_pair=expt_cal.channel_pair.ge)
    
    # pi ef
    p = gen.Pulse(start=pat.final_pulse_end,
                  duration=-expt_cal.pi_time.ef,
                  amplitude=0,
                  ssm_freq=expt_cal.ssm.ef)
    seq = add_iq_pulse_sweep(seq=seq,
                             pulse=p,
                             sweep_name='amplitude',
                             start=sweep_start_stop[0],
                             stop=sweep_start_stop[1],
                             channel_pair=expt_cal.channel_pair.ge)
    
    # add readout pulses, triggers, and marker gates
    seq = add_readout_markers_and_gates(seq=seq, pat=pat)
    
    #
    the_seq = seq
    
    #
    print("Patterns: {}".format(the_seq.num_steps))
    the_seq.write_sequence()
    the_seq.load_sequence(sw_setup.address_awg)
    wx_programs.wx_set_and_amplitude_and_offset()
    
    #END
    
def ramsey_ef_prep_e(num_patterns=51, sweep_time=500): # PMH 
    sw_setup = setup_seq_writer()
    pat = get_pattern_parameters()
    expt_cal = expt_parameters.get_expt_cal()
    
    #
    ssm_clock = expt_cal.ssm.ef + 0.010
    
    #
    seq = gen.Sequence(pat.pat_length, num_patterns)
    
    # pi ge
    p = gen.Pulse(start=pat.final_pulse_end-expt_cal.pi_time.ef,
                  duration=-expt_cal.pi_time.ge,
                  amplitude=expt_cal.pi_amp.ge,
                  ssm_freq=expt_cal.ssm.ge,
                  phase=0)
    seq = add_iq_pulse_sweep(seq=seq,
                             pulse=p,
                             sweep_name='start',
                             start=0,
                             stop=-sweep_time)
    # pi/2 ef
    p = gen.Pulse(start=pat.final_pulse_end-expt_cal.pi_time.ef/2,
                  duration=-expt_cal.pi_time.ef/2,
                  amplitude=expt_cal.pi_amp.ef,
                  ssm_freq=ssm_clock,
                  phase=0,
                  clock_freq=ssm_clock)
    seq = add_iq_pulse_sweep(seq=seq,
                             pulse=p,
                             sweep_name='start',
                             start=0,
                             stop=-sweep_time)
    # pi/2 ef
    p = gen.Pulse(start=pat.final_pulse_end,
                  duration=-expt_cal.pi_time.ef/2,
                  amplitude=expt_cal.pi_amp.ef,
                  ssm_freq=expt_cal.ssm.ef,
                  clock_freq=ssm_clock)
    seq = add_iq_pulse_sweep(seq=seq,
                             pulse=p,
                             sweep_name='none')
    
    # add readout pulses, triggers, and marker gates
    seq = add_readout_markers_and_gates(seq=seq, pat=pat)
    
    #
    the_seq = seq
    
    #
    print("Patterns: {}".format(the_seq.num_steps))
    the_seq.write_sequence()
    the_seq.load_sequence(sw_setup.address_awg)
    wx_programs.wx_set_and_amplitude_and_offset()
    
    #END
    
def rabi_ef_prep_e(num_patterns=51, sweep_time=200, rabi_amp=0.5): # PMH 
    sw_setup = setup_seq_writer()
    pat = get_pattern_parameters()
    expt_cal = expt_parameters.get_expt_cal()
    
    #
    seq = gen.Sequence(pat.pat_length, num_patterns)
    
    # pi ge
    p = gen.Pulse(start=pat.final_pulse_end,
                  duration=-expt_cal.pi_time.ge,
                  amplitude=expt_cal.pi_amp.ge,
                  ssm_freq=expt_cal.ssm.ge,
                  phase=0)
    seq = add_iq_pulse_sweep(seq=seq,
                             pulse=p,
                             sweep_name='start',
                             start=0,
                             stop=-sweep_time,
                             channel_pair=expt_cal.channel_pair.ge)

    # rabi ef
    p = gen.Pulse(start=pat.final_pulse_end,
                  duration=0,
                  amplitude=rabi_amp,
                  ssm_freq=expt_cal.ssm.ef,
                  phase=0)
    seq = add_iq_pulse_sweep(seq=seq,
                             pulse=p,
                             sweep_name='width',
                             start=0,
                             stop=-sweep_time,
                             channel_pair=expt_cal.channel_pair.ef)
    # add readout pulses, triggers, and marker gates
    seq = add_readout_markers_and_gates(seq=seq, pat=pat)
    
    #
    the_seq = seq
    
    #
    print("Patterns: {}".format(the_seq.num_steps))
    the_seq.write_sequence()
    the_seq.load_sequence(sw_setup.address_awg)
    wx_programs.wx_set_and_amplitude_and_offset()
    
    #END
    
def rabi_ef_prep_f(num_patterns=51, sweep_time=200, rabi_amp=0.5, rabi_ssb_freq=None): # PMH 
    sw_setup = setup_seq_writer()
    pat = get_pattern_parameters()
    expt_cal = expt_parameters.get_expt_cal()
    
    if rabi_ssb_freq is None:
        rabi_ssb_freq = expt_cal.ssm.ef
        
    #
    seq = gen.Sequence(pat.pat_length, num_patterns)
    
    # pi ge
    p = gen.Pulse(start=pat.final_pulse_end-expt_cal.pi_time.ef,
                  duration=-expt_cal.pi_time.ge,
                  amplitude=expt_cal.pi_amp.ge,
                  ssm_freq=expt_cal.ssm.ge,
                  phase=0)
    seq = add_iq_pulse_sweep(seq=seq,
                             pulse=p,
                             sweep_name='start',
                             start=0,
                             stop=-sweep_time,
                             channel_pair=expt_cal.channel_pair.ge)
    # pi ef
    p = gen.Pulse(start=pat.final_pulse_end,
                  duration=-expt_cal.pi_time.ef,
                  amplitude=expt_cal.pi_amp.ef,
                  ssm_freq=expt_cal.ssm.ef,
                  phase=0)
    seq = add_iq_pulse_sweep(seq=seq,
                             pulse=p,
                             sweep_name='start',
                             start=0,
                             stop=-sweep_time,
                             channel_pair=expt_cal.channel_pair.ef)
    # rabi ef
    p = gen.Pulse(start=pat.final_pulse_end,
                  duration=0,
                  amplitude=rabi_amp,
                  ssm_freq=rabi_ssb_freq,
                  phase=0)
    seq = add_iq_pulse_sweep(seq=seq,
                             pulse=p,
                             sweep_name='width',
                             start=0,
                             stop=-sweep_time,
                             channel_pair='ch1ch2')
    # add readout pulses, triggers, and marker gates
    seq = add_readout_markers_and_gates(seq=seq, pat=pat)
    
    #
    the_seq = seq
    
    #
    print("Patterns: {}".format(the_seq.num_steps))
    the_seq.write_sequence()
    the_seq.load_sequence(sw_setup.address_awg)
    wx_programs.wx_set_and_amplitude_and_offset()
    
    #END
    
def rabi_ef_prep_f_fnotf(num_patterns=51, sweep_time=200, rabi_amp=0.5, rabi_ssb_freq=None): # PMH 
    sw_setup = setup_seq_writer()
    pat = get_pattern_parameters()
    expt_cal = expt_parameters.get_expt_cal()
    
    if rabi_ssb_freq is None:
        rabi_ssb_freq = expt_cal.ssm.ef
    
    #
    t_end = pat.final_pulse_end
    t_wait = 0 # delay between pulses
    t_p = expt_cal.pi_time.ef
    
    ## without pi-pulse f
    #
    seq = gen.Sequence(pat.pat_length, num_patterns)
    
    # pi ge
    start = t_end - t_wait - t_p
    p = gen.Pulse(start=start,
                  duration=-expt_cal.pi_time.ge,
                  amplitude=expt_cal.pi_amp.ge,
                  ssm_freq=expt_cal.ssm.ge,
                  phase=0)
    seq = add_iq_pulse_sweep(seq=seq,
                             pulse=p,
                             sweep_name='start',
                             start=0,
                             stop=-sweep_time,
                             channel_pair=expt_cal.channel_pair.ge)
    # pi ef
    start = t_end
    p = gen.Pulse(start=start,
                  duration=-expt_cal.pi_time.ef,
                  amplitude=expt_cal.pi_amp.ef,
                  ssm_freq=expt_cal.ssm.ef,
                  phase=0)
    seq = add_iq_pulse_sweep(seq=seq,
                             pulse=p,
                             sweep_name='start',
                             start=0,
                             stop=-sweep_time,
                             channel_pair=expt_cal.channel_pair.ef)
    # rabi ef
    start = t_end
    p = gen.Pulse(start=start,
                  duration=0,
                  amplitude=rabi_amp,
                  ssm_freq=rabi_ssb_freq,
                  phase=0)
    seq = add_iq_pulse_sweep(seq=seq,
                             pulse=p,
                             sweep_name='width',
                             start=0,
                             stop=-sweep_time,
                             channel_pair='ch1ch2')
    # add readout pulses, triggers, and marker gates
    seq = add_readout_markers_and_gates(seq=seq, pat=pat)
    
    #
    the_seq = seq
    
    ## with pi-pulse f    
    #
    seq = gen.Sequence(pat.pat_length, num_patterns)
    
    # pi ge
    start = t_end - t_wait - t_p - t_wait - t_p
    p = gen.Pulse(start=start,
                  duration=-expt_cal.pi_time.ge,
                  amplitude=expt_cal.pi_amp.ge,
                  ssm_freq=expt_cal.ssm.ge,
                  phase=0)
    seq = add_iq_pulse_sweep(seq=seq,
                             pulse=p,
                             sweep_name='start',
                             start=0,
                             stop=-sweep_time,
                             channel_pair=expt_cal.channel_pair.ge)
    # pi ef
    start = t_end - t_wait - t_p
    p = gen.Pulse(start=start,
                  duration=-t_p,
                  amplitude=expt_cal.pi_amp.ef,
                  ssm_freq=expt_cal.ssm.ef,
                  phase=0)
    seq = add_iq_pulse_sweep(seq=seq,
                             pulse=p,
                             sweep_name='start',
                             start=0,
                             stop=-sweep_time,
                             channel_pair=expt_cal.channel_pair.ef)
    # rabi ef
    start = t_end - t_wait - t_p
    p = gen.Pulse(start=start,
                  duration=0,
                  amplitude=rabi_amp,
                  ssm_freq=rabi_ssb_freq,
                  phase=0)
    seq = add_iq_pulse_sweep(seq=seq,
                             pulse=p,
                             sweep_name='width',
                             start=0,
                             stop=-sweep_time,
                             channel_pair='ch1ch2')
    
    # pi ef
    start = t_end
    p = gen.Pulse(start=start,
                  duration=-t_p,
                  amplitude=expt_cal.pi_amp.ef,
                  ssm_freq=expt_cal.ssm.ef,
                  phase=0)
    seq = add_iq_pulse_sweep(seq=seq,
                             pulse=p,
                             sweep_name='start',
                             start=0,
                             stop=-sweep_time,
                             channel_pair=expt_cal.channel_pair.ef)
    # add readout pulses, triggers, and marker gates
    seq = add_readout_markers_and_gates(seq=seq, pat=pat)
    
    #
    the_seq.__add__(seq)
    
    #
    print("Patterns: {}".format(the_seq.num_steps))
    the_seq.write_sequence()
    the_seq.load_sequence(sw_setup.address_awg)
    wx_programs.wx_set_and_amplitude_and_offset()
    
    #END
    
def pi_ge_cal_amp(num_patterns=101, sweep_start_stop=[0, 1]): # PMH 
    sw_setup = setup_seq_writer()
    pat = get_pattern_parameters()
    expt_cal = expt_parameters.get_expt_cal()
    
    #
    seq = gen.Sequence(pat.pat_length, num_patterns)
    
    # pi ge
    p = gen.Pulse(start=pat.final_pulse_end,
                  duration=-expt_cal.pi_time.ge,
                  amplitude=0,
                  ssm_freq=expt_cal.ssm.ge)
    seq = add_iq_pulse_sweep(seq=seq,
                             pulse=p,
                             sweep_name='amplitude',
                             start=sweep_start_stop[0],
                             stop=sweep_start_stop[1],
                             channel_pair='ch3ch4')
    
    # add readout pulses, triggers, and marker gates
    seq = add_readout_markers_and_gates(seq=seq, pat=pat)
    
    #
    the_seq = seq
    
    #
    print("Patterns: {}".format(the_seq.num_steps))
    the_seq.write_sequence()
    the_seq.load_sequence(sw_setup.address_awg)
    wx_programs.wx_set_and_amplitude_and_offset()
    
    #END
    
def t1decay_ge(num_patterns=101, sweep_time=5000): # PMH 
    sw_setup = setup_seq_writer()
    pat = get_pattern_parameters()
    expt_cal = expt_parameters.get_expt_cal()
    
    #
    seq = gen.Sequence(pat.pat_length, num_patterns)
    
    # pi ge
    p = gen.Pulse(start=pat.final_pulse_end,
                  duration=-expt_cal.pi_time.ge,
                  amplitude=expt_cal.pi_amp.ge,
                  ssm_freq=expt_cal.ssm.ge)
    seq = add_iq_pulse_sweep(seq=seq,
                             pulse=p,
                             sweep_name='start',
                             start=0,
                             stop=-sweep_time)
    
    # add readout pulses, triggers, and marker gates
    seq = add_readout_markers_and_gates(seq=seq, pat=pat)
    
    #
    the_seq = seq
    
    #
    print("Patterns: {}".format(the_seq.num_steps))
    the_seq.write_sequence()
    the_seq.load_sequence(sw_setup.address_awg)
    wx_programs.wx_set_and_amplitude_and_offset()
    
    #END
    
def ramsey_ge_t1decay_ge(num_patterns_each=101, sweep_time_ramsey=5000, sweep_time_t1decay=5000): # PMH 
    sw_setup = setup_seq_writer()
    pat = get_pattern_parameters()
    expt_cal = expt_parameters.get_expt_cal()

    #
    ssm_clock = expt_cal.ssm.ge + 0.005
    
    #
    seq = gen.Sequence(pat.pat_length, num_patterns_each)
    
    # pi/2 ge
    p = gen.Pulse(start=pat.final_pulse_end-expt_cal.pi_time.ge/2,
                  duration=-expt_cal.pi_time.ge/2,
                  amplitude=expt_cal.pi_amp.ge,
                  ssm_freq=expt_cal.ssm.ge,
                  phase=0,
                  clock_freq=ssm_clock)
    seq = add_iq_pulse_sweep(seq=seq,
                             pulse=p,
                             sweep_name='start',
                             start=0,
                             stop=-sweep_time_ramsey)
    # pi/2 ge
    p = gen.Pulse(start=pat.final_pulse_end,
                  duration=-expt_cal.pi_time.ge/2,
                  amplitude=expt_cal.pi_amp.ge,
                  ssm_freq=expt_cal.ssm.ge,
                  clock_freq=ssm_clock)
    seq = add_iq_pulse_sweep(seq=seq,
                             pulse=p,
                             sweep_name='none')
    
    # add readout pulses, triggers, and marker gates
    seq = add_readout_markers_and_gates(seq=seq, pat=pat)
    
    #
    the_seq = seq
    
    #
    seq = gen.Sequence(pat.pat_length, num_patterns_each)
    
    # pi ge
    p = gen.Pulse(start=pat.final_pulse_end,
                  duration=-expt_cal.pi_time.ge,
                  amplitude=expt_cal.pi_amp.ge,
                  ssm_freq=expt_cal.ssm.ge,
                  clock_freq=ssm_clock)
    seq = add_iq_pulse_sweep(seq=seq,
                             pulse=p,
                             sweep_name='start',
                             start=0,
                             stop=-sweep_time_t1decay)
    
    # add readout pulses, triggers, and marker gates
    seq = add_readout_markers_and_gates(seq=seq, pat=pat)
    
    #
    the_seq = the_seq.__add__(seq)
    
    
    #
    print("Patterns: {}".format(the_seq.num_steps))
    the_seq.write_sequence()
    the_seq.load_sequence(sw_setup.address_awg)
    wx_programs.wx_set_and_amplitude_and_offset()
    
    #END
    
def ramsey_ge(num_patterns=101, sweep_time=500): # PMH 
    sw_setup = setup_seq_writer()
    pat = get_pattern_parameters()
    expt_cal = expt_parameters.get_expt_cal()

    #
    ssm_clock = expt_cal.ssm.ge + 0.010
    
    #
    end_time = pat.final_pulse_end
    
    #
    seq = gen.Sequence(pat.pat_length, num_patterns)

    
    # pi/2 ge
    p = gen.Pulse(start=end_time-expt_cal.pi_time.ge/2,
                  duration=-expt_cal.pi_time.ge/2,
                  amplitude=expt_cal.pi_amp.ge,
                  ssm_freq=expt_cal.ssm.ge,
                  phase=0,
                  clock_freq=ssm_clock)
    seq = add_iq_pulse_sweep(seq=seq,
                             pulse=p,
                             sweep_name='start',
                             start=0,
                             stop=-sweep_time)
    
    # pi/2 ge
    p = gen.Pulse(start=end_time,
                  duration=-expt_cal.pi_time.ge/2,
                  amplitude=expt_cal.pi_amp.ge,
                  ssm_freq=expt_cal.ssm.ge,
                  clock_freq=ssm_clock)
    seq = add_iq_pulse_sweep(seq=seq,
                             pulse=p,
                             sweep_name='none')
    
    # add readout pulses, triggers, and marker gates
    seq = add_readout_markers_and_gates(seq=seq, pat=pat)
    
    #
    the_seq = seq
    
    #
    print("Patterns: {}".format(the_seq.num_steps))
    the_seq.write_sequence()
    the_seq.load_sequence(sw_setup.address_awg)
    wx_programs.wx_set_and_amplitude_and_offset()
    
    #END
    
def rabi_ge(num_patterns=51, sweep_time=100): # PMH 
    sw_setup = setup_seq_writer()
    pat = get_pattern_parameters()
    expt_cal = expt_parameters.get_expt_cal()

    #
    pat.num_patterns = num_patterns
    ssm_clock = expt_cal.ssm.ge
    
    
    #
    end_time = pat.final_pulse_end
    rabi_amp = expt_cal.pi_amp.ge
    
    #
    seq = gen.Sequence(pat.pat_length, pat.num_patterns)
    
    # pi ge
    p = gen.Pulse(start=end_time,
                  duration=0,
                  amplitude=rabi_amp,
                  ssm_freq=expt_cal.ssm.ge,
                  phase=0)
    seq = add_iq_pulse_sweep(seq=seq,
                                 pulse=p,
                                 sweep_name='width',
                                 start=0,
                                 stop=-sweep_time,
                                 channel_pair='ch3ch4')
    # add readout pulses, triggers, and marker gates
    seq = add_readout_markers_and_gates(seq=seq, pat=pat)
    
    #
    the_seq = seq
    
    #
    print("Patterns: {}".format(the_seq.num_steps))
    the_seq.write_sequence()
    the_seq.load_sequence(sw_setup.address_awg)
    wx_programs.wx_set_and_amplitude_and_offset()

    #END

def calibrate_mixer_readout(): # PMH 
    sw_setup = setup_seq_writer()
    pat = get_pattern_parameters()
    expt_cal = expt_parameters.get_expt_cal()

    #
    num_patterns = 3
    
    #
    seq = gen.Sequence(pat.pat_length, num_patterns)
    
    # readout pulse
    main_pulse = gen.Pulse(start=0,
                           duration=pat.pat_length,
                           amplitude=pat.readout_amplitude)
    
    seq.add_sweep(channel=1,
                  marker=2,
                  sweep_name='none',
                  initial_pulse=main_pulse)
    
    ## markers
    readout_trigger = gen.Pulse(start=0,
                               duration=pat.pat_length,
                               amplitude=1)
    seq.add_sweep(channel=3, 
                  marker=1, 
                  sweep_name='none', 
                  initial_pulse=readout_trigger)
    
    #
    the_seq = seq
    
    #
    print("Patterns: {}".format(the_seq.num_steps))
    the_seq.write_sequence()
    the_seq.load_sequence(sw_setup.address_awg)
    wx_programs.wx_set_and_amplitude_and_offset()
    
def calibrate_mixer_ch1ch2(mixer_orthog_deg=90.): # PMH 
    sw_setup = setup_seq_writer()
    pat = get_pattern_parameters()
    expt_cal = expt_parameters.get_expt_cal()

    #
    num_patterns = 3
    pulse_amp = 0.25
    pulse_ssb = expt_cal.ssm.ef
    
    #
    end_time = pat.final_pulse_end
    
    #
    seq = gen.Sequence(pat.pat_length, num_patterns)
    
    # pi ge
    p = gen.Pulse(start=pat.pat_length,
                  duration=-pat.pat_length,
                  amplitude=pulse_amp,
                  ssm_freq=pulse_ssb,
                  phase=0)
    seq = add_iq_pulse_sweep(seq=seq,
                                 pulse=p,
                                 sweep_name='none',
                                 channel_pair='ch3ch4')
    
    # add readout pulses, triggers, and marker gates
    seq = add_readout_markers_and_gates(seq=seq, pat=pat)
    
    #
    the_seq = seq
    
    #
    print("Patterns: {}".format(the_seq.num_steps))
    the_seq.write_sequence()
    the_seq.load_sequence(sw_setup.address_awg)
    wx_programs.wx_set_and_amplitude_and_offset()
    wx_programs.set_run_mode_continuous()
    
if __name__=="__main__":
    pass