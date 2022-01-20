# -*- coding: utf-8 -*-
"""
Sequence experiments

@author: P. M. Harrington, 24 January 2020
"""

import numpy as np
import matplotlib.pyplot as plt
from seq_programs import *
import generator as gen
import wx_programs

def rabi_ef_prep_f_pi_at_end_choice(pi_at_end=False): # PMH 
    sw_setup = setup_seq_writer()
    pat = get_pattern_parameters()
    expt_cal = get_expt_cal()

    #
    pat.num_patterns = 101
    sweep_time = 2000
    rabi_amp = 0.065 #expt_cal.pi_amp.ef
    
    the_seq = gen.Sequence(pat.pat_length, pat.num_patterns)
    
    if pi_at_end:
        end_time = pat.final_pulse_end - expt_cal.pi_time.ef
    else:
        end_time = pat.final_pulse_end
        
    # prepare e
    p = gen.Pulse(start=end_time-expt_cal.pi_time.ef,
                  duration=-expt_cal.pi_time.ge,
                  amplitude=expt_cal.pi_amp.ge,
                  ssm_freq=expt_cal.ssm.ge,
                  phase=0)
    the_seq = add_iq_pulse_sweep(seq=the_seq,
                                 pulse=p,
                                 sweep_name='start',
                                 start=0,
                                 stop=-sweep_time)
    # prepare f
    p = gen.Pulse(start=end_time,
                  duration=-expt_cal.pi_time.ef,
                  amplitude=expt_cal.pi_amp.ef,
                  ssm_freq=expt_cal.ssm.ef,
                  phase=0)
    the_seq = add_iq_pulse_sweep(seq=the_seq,
                                 pulse=p,
                                 sweep_name='start',
                                 start=0,
                                 stop=-sweep_time)
    
    # rabi
    p = gen.Pulse(start=end_time,
                  duration=0,
                  amplitude=rabi_amp,
                  ssm_freq=expt_cal.ssm.ef,
                  phase=0)
    the_seq = add_iq_pulse_sweep(seq=the_seq,
                                 pulse=p,
                                 sweep_name='width',
                                 start=0,
                                 stop=-sweep_time)

    if pi_at_end:
        # pi ef    
        p = gen.Pulse(start=pat.final_pulse_end,
                      duration=-expt_cal.pi_time.ef,
                      amplitude=expt_cal.pi_amp.ef,
                      ssm_freq=expt_cal.ssm.ef,
                      phase=0)
        the_seq = add_iq_pulse_sweep(seq=the_seq,
                                     pulse=p,
                                     sweep_name='none',
                                     start=0,
                                     stop=-sweep_time)

    do_final_programs(sw_setup=sw_setup, pat=pat, seq=the_seq)
    print("Patterns: {}".format(pat.num_patterns))
    
    #END
    
def no_pi_to_pi_ge(): # PMH 
    sw_setup = setup_seq_writer()
    pat = get_pattern_parameters()
    expt_cal = get_expt_cal()
    the_seq = gen.Sequence(pat.pat_length, pat.num_patterns)

    #
    end_time = pat.final_pulse_end
    
    #
    p = gen.Pulse(start=end_time,
                  duration=expt_cal.pi_time.ge,
                  amplitude=0,
                  ssm_freq=expt_cal.ssm.ge,
                  phase=0)
    the_seq = add_iq_pulse_sweep(seq=the_seq,
                                 pulse=p,
                                 sweep_name='amplitude',
                                 start=0,
                                 stop=expt_cal.pi_amp.ge)
    
    do_final_programs(sw_setup=sw_setup, pat=pat, seq=the_seq)
    
    #END
    
def g_e_f(): # PMH 
    sw_setup = setup_seq_writer()
    pat = get_pattern_parameters()
    
    expt_cal = get_expt_cal()

    #
    end_time = pat.final_pulse_end
    
    # no pulse
    pat.num_patterns = 1
    the_seq = gen.Sequence(pat.pat_length, pat.num_patterns)
    p = gen.Pulse(start=end_time,
                  duration=-10,
                  amplitude=0)
    the_seq = add_iq_pulse_sweep(seq=the_seq,
                                 pulse=p,
                                 sweep_name='none')
    
    # add readout pulses, triggers, and marker gates
    the_seq = add_readout_markers_and_gates(seq=the_seq, pat=pat)
    
    #
    the_seq.write_sequence(base_name='foo',
                           file_path=sw_setup.write_dir,
                           use_range_01=False,
                           num_offset=0,
                           write_binary=True)
    
    # pi-ge
    pat.num_patterns = 1
    the_seq = gen.Sequence(pat.pat_length, pat.num_patterns)
    p = gen.Pulse(start=end_time,
                  duration=-expt_cal.pi_time.ge,
                  amplitude=expt_cal.pi_amp.ge,
                  ssm_freq=expt_cal.ssm.ge,
                  phase=0)
    the_seq = add_iq_pulse_sweep(seq=the_seq,
                                 pulse=p,
                                 sweep_name='none')
    
    # add readout pulses, triggers, and marker gates
    the_seq = add_readout_markers_and_gates(seq=the_seq, pat=pat)
    
    #
    the_seq.write_sequence(base_name='foo',
                           file_path=sw_setup.write_dir,
                           use_range_01=False,
                           num_offset=1,
                           write_binary=True)
    
    # pi-ge, pi-ef
    pat.num_patterns = 1
    the_seq = gen.Sequence(pat.pat_length, pat.num_patterns)
    p = gen.Pulse(start=end_time-expt_cal.pi_time.ef,
                  duration=-expt_cal.pi_time.ge,
                  amplitude=expt_cal.pi_amp.ge,
                  ssm_freq=expt_cal.ssm.ge,
                  phase=0)
    the_seq = add_iq_pulse_sweep(seq=the_seq,
                                 pulse=p,
                                 sweep_name='none')
    p = gen.Pulse(start=end_time,
                  duration=-expt_cal.pi_time.ef,
                  amplitude=expt_cal.pi_amp.ef,
                  ssm_freq=expt_cal.ssm.ef,
                  phase=0)
    the_seq = add_iq_pulse_sweep(seq=the_seq,
                                 pulse=p,
                                 sweep_name='none')
    
    # add readout pulses, triggers, and marker gates
    the_seq = add_readout_markers_and_gates(seq=the_seq, pat=pat)
    
    #
    the_seq.write_sequence(base_name='foo',
                           file_path=sw_setup.write_dir,
                           use_range_01=False,
                           num_offset=2,
                           write_binary=True)
    
    #
    pat.num_patterns = 3
    loading(sw_setup=sw_setup, pat=pat)
    
    #END
    
def g_e(): # PMH 
    sw_setup = setup_seq_writer()
    pat = get_pattern_parameters()
    
    expt_cal = get_expt_cal()

    #
    end_time = pat.final_pulse_end
    
    # no pulse
    pat.num_patterns = 1
    the_seq = gen.Sequence(pat.pat_length, pat.num_patterns)
    p = gen.Pulse(start=end_time,
                  duration=-10,
                  amplitude=0)
    the_seq = add_iq_pulse_sweep(seq=the_seq,
                                 pulse=p,
                                 sweep_name='none')
    
    # add readout pulses, triggers, and marker gates
    the_seq = add_readout_markers_and_gates(seq=the_seq, pat=pat)
    
    #
    the_seq.write_sequence(base_name='foo',
                           file_path=sw_setup.write_dir,
                           use_range_01=False,
                           num_offset=0,
                           write_binary=True)
    
    # pi-ge
    pat.num_patterns = 1
    the_seq = gen.Sequence(pat.pat_length, pat.num_patterns)
    p = gen.Pulse(start=end_time,
                  duration=-expt_cal.pi_time.ge,
                  amplitude=expt_cal.pi_amp.ge,
                  ssm_freq=expt_cal.ssm.ge,
                  phase=0)
    the_seq = add_iq_pulse_sweep(seq=the_seq,
                                 pulse=p,
                                 sweep_name='none')
    
    # add readout pulses, triggers, and marker gates
    the_seq = add_readout_markers_and_gates(seq=the_seq, pat=pat)
    
    #
    the_seq.write_sequence(base_name='foo',
                           file_path=sw_setup.write_dir,
                           use_range_01=False,
                           num_offset=1,
                           write_binary=True)
    
    #
    pat.num_patterns = 2
    
    print("Patterns: {}".format(pat.num_patterns))
    key_in = input("Continue? (y/n)")
    
    if key_in=="n":
        return
    else:
        #
        write_folder_to_awg(sw_setup=sw_setup, pat=pat)
        wx_programs.wx_set_and_amplitude_and_offset()
    
    #END
    
def nopi_1pi2_pi(): # PMH 
    sw_setup = setup_seq_writer()
    pat = get_pattern_parameters()
    expt_cal = get_expt_cal()

    #
    pat.num_patterns = 3
    
    #
    end_time = pat.final_pulse_end
    
    #
    the_seq = gen.Sequence(pat.pat_length, pat.num_patterns)
    
    # pi ge
    p = gen.Pulse(start=end_time,
                  duration=expt_cal.pi_time.ge,
                  amplitude=0.,
                  ssm_freq=expt_cal.ssm.ge,
                  phase=0)
    the_seq = add_iq_pulse_sweep(seq=the_seq,
                                 pulse=p,
                                 sweep_name='amplitude',
                                 start=0,
                                 stop=expt_cal.pi_amp.ge)
    
    ##
    do_final_programs(sw_setup=sw_setup, pat=pat, seq=the_seq)
    
    #END
    
def nopi_pi(): # PMH 
    sw_setup = setup_seq_writer()
    pat = get_pattern_parameters()
    expt_cal = get_expt_cal()

    #
    pat.num_patterns = 2
    
    #
    end_time = pat.final_pulse_end
    
    #
    the_seq = gen.Sequence(pat.pat_length, pat.num_patterns)
    
    # pi ge
    p = gen.Pulse(start=end_time,
                  duration=expt_cal.pi_time.ge,
                  amplitude=0.,
                  ssm_freq=expt_cal.ssm.ge,
                  phase=0)
    the_seq = add_iq_pulse_sweep(seq=the_seq,
                                 pulse=p,
                                 sweep_name='amplitude',
                                 start=0,
                                 stop=expt_cal.pi_amp.ge)
    
    ##
    do_final_programs(sw_setup=sw_setup, pat=pat, seq=the_seq)
    
    #END
    
def test_alazar(): # PMH 
    sw_setup = setup_seq_writer()
    pat = get_pattern_parameters()
    pat.num_patterns = 11
    expt_cal = get_expt_cal()
    the_seq = gen.Sequence(pat.pat_length, pat.num_patterns)
    
    #
    p = gen.Pulse(start=7500,
                  duration=-1000,
                  amplitude=0.25)
    the_seq.add_sweep(channel=1, sweep_name='amplitude', start=0.25, stop=1.0, initial_pulse=p)
    the_seq.add_sweep(channel=2, sweep_name='amplitude', start=0.25, stop=1.0, initial_pulse=p)
    
    #
    do_final_programs(sw_setup=sw_setup, pat=pat, seq=the_seq)
    
    #END

def rabi_spectroscopy_ge_driving_ef(rabi_delta_ssb=0.): # PMH 
    sw_setup = setup_seq_writer()
    pat = get_pattern_parameters()
    expt_cal = get_expt_cal()
    
    #
    pat.num_patterns = 201
    
    ## 
    rabi_amp = 0.025
    rabi_freq = expt_cal.ssm.ef + rabi_delta_ssb
    rabi_spec_amp = 0.005

    #
    end_time = pat.final_pulse_end
    pulse_duration = pat.final_pulse_end
    ssm_cntr = expt_cal.ssm.ge
    ssm_width = 0.015
    ssm_start = ssm_cntr-ssm_width/2
    ssm_end = ssm_cntr+ssm_width/2

    # rabi spec on ge
    the_seq = gen.Sequence(pat.pat_length, pat.num_patterns)
    p = gen.Pulse(start=end_time,
                  duration=-pulse_duration,
                  amplitude=rabi_spec_amp,
                  ssm_freq=0.,
                  phase=0)
    the_seq = add_iq_pulse_sweep(seq=the_seq,
                                 pulse=p,
                                 sweep_name='ssm_freq',
                                 start=ssm_start,
                                 stop=ssm_end)
    
    # rabi on ef
    p = gen.Pulse(start=end_time,
                  duration=-pulse_duration,
                  amplitude=rabi_amp,
                  ssm_freq=rabi_freq,
                  phase=0)
    the_seq = add_iq_pulse_sweep(seq=the_seq,
                                 pulse=p,
                                 sweep_name='none')
    

    do_final_programs(sw_setup=sw_setup, pat=pat, seq=the_seq)
    
    #END

def rabi_spectroscopy_probe_ge_sweep_ef(): # PMH 
    sw_setup = setup_seq_writer()
    pat = get_pattern_parameters()
    expt_cal = get_expt_cal()
    
    #
    pat.num_patterns = 101
    
    ## 
    rabi_amp = 0.1
    rabi_spec_amp = 0.01

    #
    ssm_cntr = expt_cal.ssm.ef
    ssm_width = 0.020
    ssm_start = ssm_cntr-ssm_width/2
    ssm_end = ssm_cntr+ssm_width/2
    
    #
    end_time = pat.final_pulse_end
    pulse_duration = pat.final_pulse_end

    # rabi spec on ge
    the_seq = gen.Sequence(pat.pat_length, pat.num_patterns)
    p = gen.Pulse(start=end_time,
                  duration=-pulse_duration,
                  amplitude=rabi_spec_amp,
                  ssm_freq=expt_cal.ssm.ge,
                  phase=0)
    the_seq = add_iq_pulse_sweep(seq=the_seq,
                                 pulse=p,
                                 sweep_name='none')
    
    # rabi on ef
    p = gen.Pulse(start=end_time,
                  duration=-pulse_duration,
                  amplitude=rabi_amp,
                  ssm_freq=-1.,
                  phase=0)
    the_seq = add_iq_pulse_sweep(seq=the_seq,
                                 pulse=p,
                                 sweep_name='ssm_freq',
                                 start=ssm_start,
                                 stop=-ssm_end)

    do_final_programs(sw_setup=sw_setup, pat=pat, seq=the_seq)
    
    #END
    
def g_e_f(): # PMH 
    sw_setup = setup_seq_writer()
    pat = get_pattern_parameters()
    
    expt_cal = get_expt_cal()

    #
    end_time = pat.final_pulse_end
    
    # no pulse
    pat.num_patterns = 1
    the_seq = gen.Sequence(pat.pat_length, pat.num_patterns)
    p = gen.Pulse(start=end_time,
                  duration=-10,
                  amplitude=0)
    the_seq = add_iq_pulse_sweep(seq=the_seq,
                                 pulse=p,
                                 sweep_name='none')
    
    # add readout pulses, triggers, and marker gates
    the_seq = add_readout_markers_and_gates(seq=the_seq, pat=pat)
    
    #
    the_seq.write_sequence(base_name='foo',
                           file_path=sw_setup.write_dir,
                           use_range_01=False,
                           num_offset=0,
                           write_binary=True)
    
    # pi-ge
    pat.num_patterns = 1
    the_seq = gen.Sequence(pat.pat_length, pat.num_patterns)
    p = gen.Pulse(start=end_time,
                  duration=-expt_cal.pi_time.ge,
                  amplitude=expt_cal.pi_amp.ge,
                  ssm_freq=expt_cal.ssm.ge,
                  phase=0)
    the_seq = add_iq_pulse_sweep(seq=the_seq,
                                 pulse=p,
                                 sweep_name='none')
    
    # add readout pulses, triggers, and marker gates
    the_seq = add_readout_markers_and_gates(seq=the_seq, pat=pat)
    
    #
    the_seq.write_sequence(base_name='foo',
                           file_path=sw_setup.write_dir,
                           use_range_01=False,
                           num_offset=1,
                           write_binary=True)
    
    # pi-ge, pi-ef
    pat.num_patterns = 1
    the_seq = gen.Sequence(pat.pat_length, pat.num_patterns)
    p = gen.Pulse(start=end_time-expt_cal.pi_time.ef,
                  duration=-expt_cal.pi_time.ge,
                  amplitude=expt_cal.pi_amp.ge,
                  ssm_freq=expt_cal.ssm.ge,
                  phase=0)
    the_seq = add_iq_pulse_sweep(seq=the_seq,
                                 pulse=p,
                                 sweep_name='none')
    p = gen.Pulse(start=end_time,
                  duration=-expt_cal.pi_time.ef,
                  amplitude=expt_cal.pi_amp.ef,
                  ssm_freq=expt_cal.ssm.ef,
                  phase=0)
    the_seq = add_iq_pulse_sweep(seq=the_seq,
                                 pulse=p,
                                 sweep_name='none')
    
    # add readout pulses, triggers, and marker gates
    the_seq = add_readout_markers_and_gates(seq=the_seq, pat=pat)
    
    #
    the_seq.write_sequence(base_name='foo',
                           file_path=sw_setup.write_dir,
                           use_range_01=False,
                           num_offset=2,
                           write_binary=True)
    
    #
    pat.num_patterns = 3
    write_folder_to_awg(sw_setup=sw_setup, pat=pat)
    print("Patterns: {}".format(pat.num_patterns))
    
    #END
    
def ramsey_ef(): # PMH 
    sw_setup = setup_seq_writer()
    pat = get_pattern_parameters()
    expt_cal = get_expt_cal()

    #
    pat.num_patterns = 101
    sweep_time = 500
    ssm_clock = expt_cal.ssm.ef + 0.010
    
    #
    end_time = pat.final_pulse_end
    
    #
    the_seq = gen.Sequence(pat.pat_length, pat.num_patterns)
    
    # pi ge
    p = gen.Pulse(start=end_time-expt_cal.pi_time.ef,
                  duration=-expt_cal.pi_time.ge,
                  amplitude=expt_cal.pi_amp.ge,
                  ssm_freq=expt_cal.ssm.ge,
                  phase=0)
    the_seq = add_iq_pulse_sweep(seq=the_seq,
                                 pulse=p,
                                 sweep_name='start',
                                 start=0,
                                 stop=-sweep_time)
    
    
    # pi/2 ef
    p = gen.Pulse(start=end_time-expt_cal.pi_time.ef/2,
                  duration=-expt_cal.pi_time.ef/2,
                  amplitude=expt_cal.pi_amp.ef,
                  ssm_freq=expt_cal.ssm.ef,
                  phase=0,
                  clock_freq=ssm_clock)
    the_seq = add_iq_pulse_sweep(seq=the_seq,
                                 pulse=p,
                                 sweep_name='start',
                                 start=0,
                                 stop=-sweep_time)
    
    # pi/2 ef
    p = gen.Pulse(start=end_time,
                  duration=-expt_cal.pi_time.ef/2,
                  amplitude=expt_cal.pi_amp.ef,
                  ssm_freq=expt_cal.ssm.ef,
                  clock_freq=ssm_clock)
    the_seq = add_iq_pulse_sweep(seq=the_seq,
                                 pulse=p,
                                 sweep_name='none')
    
    ##
    do_final_programs(sw_setup=sw_setup, pat=pat, seq=the_seq)
    
    #END
    
def t1_decay_ge(): # PMH 
    sw_setup = setup_seq_writer()
    pat = get_pattern_parameters()
    expt_cal = get_expt_cal()

    #
    pat.num_patterns = 101
    sweep_time = 1000
    ssm_clock = expt_cal.ssm.ef
    
    #
    end_time = pat.final_pulse_end
    
    #
    the_seq = gen.Sequence(pat.pat_length, pat.num_patterns)
    
    # pi ge
    p = gen.Pulse(start=end_time,
                  duration=-expt_cal.pi_time.ge,
                  amplitude=expt_cal.pi_amp.ge,
                  ssm_freq=expt_cal.ssm.ge,
                  phase=0)
    the_seq = add_iq_pulse_sweep(seq=the_seq,
                                 pulse=p,
                                 sweep_name='start',
                                 start=0,
                                 stop=-sweep_time)
    
    ##
    do_final_programs(sw_setup=sw_setup, pat=pat, seq=the_seq)
    
    #END
    
def ramsey_ge(): # PMH 
    sw_setup = setup_seq_writer()
    pat = get_pattern_parameters()
    expt_cal = get_expt_cal()

    #
    pat.num_patterns = 101
    sweep_time = 500
    ssm_clock = expt_cal.ssm.ge + 0.010
    
    #
    end_time = pat.final_pulse_end
    
    #
    the_seq = gen.Sequence(pat.pat_length, pat.num_patterns)

    
    # pi/2 ge
    p = gen.Pulse(start=end_time-expt_cal.pi_time.ge/2,
                  duration=-expt_cal.pi_time.ge/2,
                  amplitude=expt_cal.pi_amp.ge,
                  ssm_freq=expt_cal.ssm.ge,
                  phase=0,
                  clock_freq=ssm_clock)
    the_seq = add_iq_pulse_sweep(seq=the_seq,
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
    the_seq = add_iq_pulse_sweep(seq=the_seq,
                                 pulse=p,
                                 sweep_name='none')
    
    ##
    do_final_programs(sw_setup=sw_setup, pat=pat, seq=the_seq)
    
    #END
    
def rabi_spectroscopy_ge(): # PMH 
    print('x')
    sw_setup = setup_seq_writer()
    pat = get_pattern_parameters()
    expt_cal = get_expt_cal()
    
    ## 
    pat.num_patterns = 201
    ssm_cntr = expt_cal.ssm.ge
    ssm_width = 0.05
    
    #
    end_time = pat.final_pulse_end
    pulse_duration = pat.final_pulse_end
    ssm_start = ssm_cntr-ssm_width/2
    ssm_end = ssm_cntr+ssm_width/2
    ssm_amp = 0.05

    #
    the_seq = gen.Sequence(pat.pat_length, pat.num_patterns)
    p = gen.Pulse(start=end_time,
                  duration=-pulse_duration,
                  amplitude=ssm_amp,
                  ssm_freq=0.,
                  phase=0)
    the_seq = add_iq_pulse_sweep(seq=the_seq,
                                 pulse=p,
                                 sweep_name='ssm_freq',
                                 start=ssm_start,
                                 stop=ssm_end)

    ##
    do_final_programs(sw_setup=sw_setup, pat=pat, seq=the_seq)
    
    #END
    
def rabi_ge(): # PMH 
    sw_setup = setup_seq_writer()
    pat = get_pattern_parameters()
    expt_cal = get_expt_cal()

    #
    pat.num_patterns = 51
    sweep_time = 200
    ssm_clock = expt_cal.ssm.ef
    
    #
    end_time = pat.final_pulse_end
    
    #
    seq = gen.Sequence(pat.pat_length, pat.num_patterns)
    
    # pi ge
    p = gen.Pulse(start=end_time,
                  duration=0,
                  amplitude=expt_cal.pi_amp.ge,
                  ssm_freq=expt_cal.ssm.ge,
                  phase=0)
    seq = add_iq_pulse_sweep(seq=seq,
                                 pulse=p,
                                 sweep_name='width',
                                 start=0,
                                 stop=-sweep_time)
    
    #
    do_final_programs(sw_setup=sw_setup, pat=pat, seq=seq)

    #END
    
def rabi_ge_no_markers(): # PMH 
    sw_setup = setup_seq_writer()
    pat = get_pattern_parameters()
    expt_cal = get_expt_cal()

    #
    pat.num_patterns = 51
    sweep_time = 200
    ssm_clock = expt_cal.ssm.ef
    
    #
    end_time = pat.final_pulse_end
    
    #
    the_seq = gen.Sequence(pat.pat_length, pat.num_patterns)
    
    # pi ge
    p = gen.Pulse(start=end_time,
                  duration=0,
                  amplitude=expt_cal.pi_amp.ge,
                  ssm_freq=expt_cal.ssm.ge,
                  phase=0)
    the_seq = add_iq_pulse_sweep(seq=the_seq,
                                 pulse=p,
                                 sweep_name='width',
                                 start=0,
                                 stop=-sweep_time)
    # add readout pulses, triggers, and marker gates
    #seq = add_readout_markers_and_gates(seq=seq, pat=pat)

    # display output
    make_seq_plots(sw_setup=sw_setup, pat=pat, seq=the_seq)
    
    print("Patterns: {}".format(pat.num_patterns))
    
    the_seq.write_sequence(base_name='foo',
                       file_path=sw_setup.write_dir,
                       use_range_01=False,
                       num_offset=0,
                       write_binary=True)
        
    # write and load patterns
    #write_patterns_to_disk(sw_setup=sw_setup, seq=the_seq, num_offset=0)
    write_folder_to_awg(sw_setup=sw_setup, pat=pat)
    wx_programs.wx_set_and_amplitude_and_offset()
    
    #END
    
def t1_decay_ef(): # PMH 
    sw_setup = setup_seq_writer()
    pat = get_pattern_parameters()
    expt_cal = get_expt_cal()

    #
    pat.num_patterns = 51
    sweep_time = 5000
    
    #
    end_time = pat.final_pulse_end
    
    #
    the_seq = gen.Sequence(pat.pat_length, pat.num_patterns)
    
    # pi ge
    p = gen.Pulse(start=end_time-expt_cal.pi_time.ef,
                  duration=-expt_cal.pi_time.ge,
                  amplitude=expt_cal.pi_amp.ge,
                  ssm_freq=expt_cal.ssm.ge,
                  phase=0)
    the_seq = add_iq_pulse_sweep(seq=the_seq,
                                 pulse=p,
                                 sweep_name='start',
                                 start=0,
                                 stop=-sweep_time)
    
    # pi ef
    p = gen.Pulse(start=end_time,
                  duration=-expt_cal.pi_time.ef,
                  amplitude=expt_cal.pi_amp.ef,
                  ssm_freq=expt_cal.ssm.ef,
                  phase=0)
    the_seq = add_iq_pulse_sweep(seq=the_seq,
                                 pulse=p,
                                 sweep_name='start',
                                 start=0,
                                 stop=-sweep_time)
    
    ##
    do_final_programs(sw_setup=sw_setup, pat=pat, seq=the_seq)
    
    #END
    
def rabi_ef_prep_f(): # PMH 
    sw_setup = setup_seq_writer()
    pat = get_pattern_parameters()
    expt_cal = get_expt_cal()

    #
    pat.num_patterns = 101
    sweep_time = 2000
    rabi_amp = 0.065 #expt_cal.pi_amp.ef
    
    #
    end_time = pat.final_pulse_end
    
    #
    the_seq = gen.Sequence(pat.pat_length, pat.num_patterns)
    
    # pi ge
    p = gen.Pulse(start=end_time-expt_cal.pi_time.ef,
                  duration=-expt_cal.pi_time.ge,
                  amplitude=expt_cal.pi_amp.ge,
                  ssm_freq=expt_cal.ssm.ge,
                  phase=0)
    the_seq = add_iq_pulse_sweep(seq=the_seq,
                                 pulse=p,
                                 sweep_name='start',
                                 start=0,
                                 stop=-sweep_time)
    
    # pi ef
    p = gen.Pulse(start=end_time,
                  duration=-expt_cal.pi_time.ef,
                  amplitude=expt_cal.pi_amp.ef,
                  ssm_freq=expt_cal.ssm.ef,
                  phase=0)
    the_seq = add_iq_pulse_sweep(seq=the_seq,
                                 pulse=p,
                                 sweep_name='start',
                                 start=0,
                                 stop=-sweep_time)
    
    # rabi ef
    p = gen.Pulse(start=end_time,
                  duration=0,
                  amplitude=rabi_amp,
                  ssm_freq=expt_cal.ssm.ef,
                  phase=0)
    the_seq = add_iq_pulse_sweep(seq=the_seq,
                                 pulse=p,
                                 sweep_name='width',
                                 start=0,
                                 stop=-sweep_time)
    
    ##
    do_final_programs(sw_setup=sw_setup, pat=pat, seq=the_seq)
    
    #END
    
def rabi_ef_prep_f_fixed_time_sweep_J(): # PMH 
    sw_setup = setup_seq_writer()
    pat = get_pattern_parameters()
    expt_cal = get_expt_cal()

    #
    pat.num_patterns = 201
    rabi_duration = 425
    rabi_amp_start = 0.025
    rabi_amp_stop = 0.075
    
    #
    end_time = pat.final_pulse_end
    
    #
    the_seq = gen.Sequence(pat.pat_length, pat.num_patterns)
    
    # pi ge
    p = gen.Pulse(start=end_time-expt_cal.pi_time.ef-rabi_duration,
                  duration=-expt_cal.pi_time.ge,
                  amplitude=expt_cal.pi_amp.ge,
                  ssm_freq=expt_cal.ssm.ge,
                  phase=0)
    the_seq = add_iq_pulse_sweep(seq=the_seq,
                                 pulse=p,
                                 sweep_name='none')
    
    # pi ef
    p = gen.Pulse(start=end_time-rabi_duration,
                  duration=-expt_cal.pi_time.ef,
                  amplitude=expt_cal.pi_amp.ef,
                  ssm_freq=expt_cal.ssm.ef,
                  phase=0)
    the_seq = add_iq_pulse_sweep(seq=the_seq,
                                 pulse=p,
                                 sweep_name='none')
    
    # rabi ef
    p = gen.Pulse(start=end_time,
                  duration=-rabi_duration,
                  amplitude=0.,
                  ssm_freq=expt_cal.ssm.ef,
                  phase=0)
    the_seq = add_iq_pulse_sweep(seq=the_seq,
                                 pulse=p,
                                 sweep_name='amplitude',
                                 start=rabi_amp_start,
                                 stop=rabi_amp_stop)
    
    ##
    do_final_programs(sw_setup=sw_setup, pat=pat, seq=the_seq)
    
    #END
    
def prep_e_1pi2(): # PMH 
    sw_setup = setup_seq_writer()
    pat = get_pattern_parameters()
    expt_cal = get_expt_cal()

    #
    pat.num_patterns = 10
    
    #
    end_time = pat.final_pulse_end
    
    #
    the_seq = gen.Sequence(pat.pat_length, pat.num_patterns)
    
    # pi ge
    p = gen.Pulse(start=end_time-expt_cal.pi_time.ef/2,
                  duration=-expt_cal.pi_time.ge,
                  amplitude=expt_cal.pi_amp.ge,
                  ssm_freq=expt_cal.ssm.ge,
                  phase=0)
    the_seq = add_iq_pulse_sweep(seq=the_seq,
                                 pulse=p,
                                 sweep_name='none')
    
    # pi/2 ef
    p = gen.Pulse(start=end_time,
                  duration=-expt_cal.pi_time.ef/2,
                  amplitude=expt_cal.pi_amp.ef/2,
                  ssm_freq=expt_cal.ssm.ef,
                  phase=0)
    the_seq = add_iq_pulse_sweep(seq=the_seq,
                                 pulse=p,
                                 sweep_name='none')
    
    ##
    do_final_programs(sw_setup=sw_setup, pat=pat, seq=the_seq)
    
    #END
    
def rabi_ef_prep_f_with_pi_cal():
    #
    sw_setup = setup_seq_writer()
    pat = get_pattern_parameters()
    expt_cal = get_expt_cal()

    #
    num_pats_rabi = 101
    sweep_time = 2000
    rabi_amp = 0.10 #0.065
    
    ### rabi w/o pi
    num_offset_running_count = 0
    print(num_offset_running_count)
    pat.num_patterns = num_pats_rabi
    the_seq = gen.Sequence(pat.pat_length, pat.num_patterns)
    
    # no pi pulse at end
    end_time = pat.final_pulse_end
    
    ## prefare e then f
    # prepare e
    p = gen.Pulse(start=end_time-expt_cal.pi_time.ef,
                  duration=-expt_cal.pi_time.ge,
                  amplitude=expt_cal.pi_amp.ge,
                  ssm_freq=expt_cal.ssm.ge,
                  phase=0)
    the_seq = add_iq_pulse_sweep(seq=the_seq,
                                 pulse=p,
                                 sweep_name='start',
                                 start=0,
                                 stop=-sweep_time)
    
    # prepare f
    p = gen.Pulse(start=end_time,
                  duration=-expt_cal.pi_time.ef,
                  amplitude=expt_cal.pi_amp.ef,
                  ssm_freq=expt_cal.ssm.ef,
                  phase=0)
    the_seq = add_iq_pulse_sweep(seq=the_seq,
                                 pulse=p,
                                 sweep_name='start',
                                 start=0,
                                 stop=-sweep_time)
    
    # rabi
    p = gen.Pulse(start=end_time,
                  duration=0,
                  amplitude=rabi_amp,
                  ssm_freq=expt_cal.ssm.ef,
                  phase=0)
    the_seq = add_iq_pulse_sweep(seq=the_seq,
                                 pulse=p,
                                 sweep_name='width',
                                 start=0,
                                 stop=-sweep_time)
    the_seq = add_readout_markers_and_gates(seq=the_seq, pat=pat)
    write_patterns_to_disk(sw_setup=sw_setup, seq=the_seq, num_offset=num_offset_running_count)

    ### rabi w/ pi
    num_offset_running_count += pat.num_patterns
    pat.num_patterns = num_pats_rabi
    print(num_offset_running_count)
    the_seq = gen.Sequence(pat.pat_length, pat.num_patterns)
    end_time = pat.final_pulse_end - expt_cal.pi_time.ef

    ## prepare e then f    
    # prepare e
    p = gen.Pulse(start=end_time-expt_cal.pi_time.ef,
                  duration=-expt_cal.pi_time.ge,
                  amplitude=expt_cal.pi_amp.ge,
                  ssm_freq=expt_cal.ssm.ge,
                  phase=0)
    the_seq = add_iq_pulse_sweep(seq=the_seq,
                                 pulse=p,
                                 sweep_name='start',
                                 start=0,
                                 stop=-sweep_time)
    # prepare f
    p = gen.Pulse(start=end_time,
                  duration=-expt_cal.pi_time.ef,
                  amplitude=expt_cal.pi_amp.ef,
                  ssm_freq=expt_cal.ssm.ef,
                  phase=0)
    the_seq = add_iq_pulse_sweep(seq=the_seq,
                                 pulse=p,
                                 sweep_name='start',
                                 start=0,
                                 stop=-sweep_time)
    
    # rabi
    p = gen.Pulse(start=end_time,
                  duration=0,
                  amplitude=rabi_amp,
                  ssm_freq=expt_cal.ssm.ef,
                  phase=0)
    the_seq = add_iq_pulse_sweep(seq=the_seq,
                                 pulse=p,
                                 sweep_name='width',
                                 start=0,
                                 stop=-sweep_time)
    
    # pi ef    
    p = gen.Pulse(start=pat.final_pulse_end,
                  duration=-expt_cal.pi_time.ef,
                  amplitude=expt_cal.pi_amp.ef,
                  ssm_freq=expt_cal.ssm.ef,
                  phase=0)
    the_seq = add_iq_pulse_sweep(seq=the_seq,
                                 pulse=p,
                                 sweep_name='none',
                                 start=0,
                                 stop=-sweep_time)
    the_seq = add_readout_markers_and_gates(seq=the_seq, pat=pat)
    write_patterns_to_disk(sw_setup=sw_setup, seq=the_seq, num_offset=num_offset_running_count)
    
    ## create population readout calibration pulses
    end_time = pat.final_pulse_end
    
    # no pulse
    num_offset_running_count += pat.num_patterns
    pat.num_patterns = 1
    print(num_offset_running_count)
    the_seq = gen.Sequence(pat.pat_length, pat.num_patterns)
    p = gen.Pulse(start=end_time,
                  duration=-1,
                  amplitude=0)
    the_seq = add_iq_pulse_sweep(seq=the_seq,
                                 pulse=p,
                                 sweep_name='none')
    the_seq = add_readout_markers_and_gates(seq=the_seq, pat=pat)
    write_patterns_to_disk(sw_setup=sw_setup, seq=the_seq, num_offset=num_offset_running_count)
    
    # pi-ge
    num_offset_running_count += pat.num_patterns
    pat.num_patterns = 1
    print(num_offset_running_count)
    the_seq = gen.Sequence(pat.pat_length, pat.num_patterns)
    p = gen.Pulse(start=end_time,
                  duration=-expt_cal.pi_time.ge,
                  amplitude=expt_cal.pi_amp.ge,
                  ssm_freq=expt_cal.ssm.ge,
                  phase=0)
    the_seq = add_iq_pulse_sweep(seq=the_seq,
                                 pulse=p,
                                 sweep_name='none')
    the_seq = add_readout_markers_and_gates(seq=the_seq, pat=pat)
    write_patterns_to_disk(sw_setup=sw_setup, seq=the_seq, num_offset=num_offset_running_count)
    
    # pi-ge, pi-ef
    num_offset_running_count += pat.num_patterns
    pat.num_patterns = 1
    print(num_offset_running_count)
    the_seq = gen.Sequence(pat.pat_length, pat.num_patterns)
    p = gen.Pulse(start=end_time-expt_cal.pi_time.ef,
                  duration=-expt_cal.pi_time.ge,
                  amplitude=expt_cal.pi_amp.ge,
                  ssm_freq=expt_cal.ssm.ge,
                  phase=0)
    the_seq = add_iq_pulse_sweep(seq=the_seq,
                                 pulse=p,
                                 sweep_name='none')
    p = gen.Pulse(start=end_time,
                  duration=-expt_cal.pi_time.ef,
                  amplitude=expt_cal.pi_amp.ef,
                  ssm_freq=expt_cal.ssm.ef,
                  phase=0)
    the_seq = add_iq_pulse_sweep(seq=the_seq,
                                 pulse=p,
                                 sweep_name='none')
    the_seq = add_readout_markers_and_gates(seq=the_seq, pat=pat)
    write_patterns_to_disk(sw_setup=sw_setup, seq=the_seq, num_offset=num_offset_running_count)
    
    # load folder
    pat.num_patterns = num_offset_running_count + pat.num_patterns
    write_folder_to_awg(sw_setup=sw_setup, pat=pat)
    
    #END
    
def pi_cal_ge(): # PMH 
    sw_setup = setup_seq_writer()
    pat = get_pattern_parameters()
    expt_cal = get_expt_cal()
    
    #
    pat.num_patterns = 101
    
    ## 

    #
    end_time = pat.final_pulse_end

    #
    the_seq = gen.Sequence(pat.pat_length, pat.num_patterns)
    p = gen.Pulse(start=end_time,
                  duration=-2*expt_cal.pi_time.ge,
                  amplitude=0,
                  ssm_freq=expt_cal.ssm.ge,
                  phase=0)
    the_seq = add_iq_pulse_sweep(seq=the_seq,
                                 pulse=p,
                                 sweep_name='amplitude',
                                 start=0.,
                                 stop=1.)

    do_final_programs(sw_setup=sw_setup, pat=pat, seq=the_seq)
    
    #END
    
def pi_cal_ef(): # PMH 
    sw_setup = setup_seq_writer()
    pat = get_pattern_parameters()
    expt_cal = get_expt_cal()
    
    #
    pat.num_patterns = 101
    
    ## 

    #
    end_time = pat.final_pulse_end

    #
    the_seq = gen.Sequence(pat.pat_length, pat.num_patterns)
    p = gen.Pulse(start=end_time-2*expt_cal.pi_time.ef,
                  duration=-expt_cal.pi_time.ge,
                  amplitude=expt_cal.pi_amp.ge,
                  ssm_freq=expt_cal.ssm.ge,
                  phase=0)
    the_seq = add_iq_pulse_sweep(seq=the_seq,
                                 pulse=p,
                                 sweep_name='none')


    #
    p = gen.Pulse(start=end_time,
                  duration=-2*expt_cal.pi_time.ef,
                  amplitude=0.,
                  ssm_freq=expt_cal.ssm.ef,
                  phase=0)
    the_seq = add_iq_pulse_sweep(seq=the_seq,
                                 pulse=p,
                                 sweep_name='amplitude',
                                 start=0.,
                                 stop=1.0)
    
    do_final_programs(sw_setup=sw_setup, pat=pat, seq=the_seq)
    
    #END
    
def readout_only(): # PMH 
    sw_setup = setup_seq_writer()
    pat = get_pattern_parameters()
    expt_cal = get_expt_cal()
    
    ## 
    pat.readout_duration = 8000
    pat.readout_trig_start = 6000
    pat.num_patterns = 1
    
    # readout pulse
    main_pulse = gen.Pulse(start=0.,
                           duration=pat.pat_length,
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
    
    #
    write_patterns_to_disk(sw_setup=sw_setup, seq=seq, num_offset=0)
    write_folder_to_awg(sw_setup=sw_setup, pat=pat)
    
def calibrate_mixer_ch1ch2(mixer_orthog_deg=90.): # PMH 
    sw_setup = setup_seq_writer()
    pat = get_pattern_parameters()
    expt_cal = get_expt_cal()

    #
    pat.num_patterns = 3
    end_time = pat.pat_length
    
    #
    seq = gen.Sequence(pat.pat_length, pat.num_patterns)
    p = gen.Pulse(start=end_time,
                  duration=-pat.pat_length,
                  amplitude=0.5,
                  ssm_freq=0.125,
                  phase=0.)
    seq.add_sweep(channel=1,
                  sweep_name='none', initial_pulse=p)
    p.phase = mixer_orthog_deg
    seq.add_sweep(channel=2,
                  sweep_name='none', initial_pulse=p)
    
    ## markers
    readout_trigger = gen.Pulse(start=pat.readout_trig_start,
                               duration=pat.readout_trig_duration,
                               amplitude=1)
    seq.add_sweep(channel=3, 
                  marker=1, 
                  sweep_name='none', 
                  initial_pulse=readout_trigger)
    
    # create the gate for ch1 an ch2
#    seq.add_gate(source_1=1, source_2=2, destination_tuple=(1,1))
    
#    channel1_channel = seq.channel_list[0][0] # dim 0: channel 1; dim 1: [ch,m1,m2]
#    channel2_channel = seq.channel_list[1][0] # dim 0: channel 1; dim 1: [ch,m1,m2]
#    both_ch1_ch2 = channel1_channel**2 + channel2_channel**2
#    ch1ch2_gate = gen.create_gate(both_ch1_ch2)
#    seq.channel_list[0][1] = ch1ch2_gate
    
    #
    #make_seq_plots(sw_setup=sw_setup, pat=pat, seq=seq)
    
    #
    write_patterns_to_disk(sw_setup=sw_setup, seq=seq, num_offset=0)
    write_folder_to_awg(sw_setup=sw_setup, pat=pat)
    wx_programs.set_run_mode_continuous()
    
def rabi_ef_prep_e(): # PMH 
    sw_setup = setup_seq_writer()
    pat = get_pattern_parameters()
    expt_cal = get_expt_cal()

    #
    pat.num_patterns = 51
    sweep_time = 1000
    rabi_amp = expt_cal.pi_amp.ef
    
    #
    end_time = pat.final_pulse_end
    
    #
    the_seq = gen.Sequence(pat.pat_length, pat.num_patterns)
    
    # pi ge
    p = gen.Pulse(start=end_time,
                  duration=-expt_cal.pi_time.ge,
                  amplitude=expt_cal.pi_amp.ge,
                  ssm_freq=expt_cal.ssm.ge,
                  phase=0)
    the_seq = add_iq_pulse_sweep(seq=the_seq,
                                 pulse=p,
                                 sweep_name='start',
                                 start=0,
                                 stop=-sweep_time)
    
    # rabi ef
    p = gen.Pulse(start=end_time,
                  duration=0,
                  amplitude=expt_cal.ssm.ef,
                  ssm_freq=expt_cal.ssm.ef,
                  phase=0)
    the_seq = add_iq_pulse_sweep(seq=the_seq,
                                 pulse=p,
                                 sweep_name='width',
                                 start=0,
                                 stop=-sweep_time)
    
    ##
    do_final_programs(sw_setup=sw_setup, pat=pat, seq=the_seq)
    
    #END
    
def tom_cal_6pt(): # PMH 
    #
    sw_setup = setup_seq_writer()
    pat = get_pattern_parameters()
    expt_cal = get_expt_cal()

    #
    end_time = pat.final_pulse_end
    
    #
    pi_time = expt_cal.pi_time.ge
    pi_amp = expt_cal.pi_amp.ge
    pi_ssm_freq = expt_cal.ssm.ge
    
    # prep +x, x-tom
    num_offset = 0
    rotation_axis_prep = '+y'
    rotation_axis_tom = '+y'
    the_seq = gen.Sequence(pat.pat_length, num_steps=1)
    p = gen.Pulse(start=end_time-pi_time/2,
                  duration=-pi_time/2,
                  amplitude=pi_amp,
                  ssm_freq=pi_ssm_freq,
                  phase=0)
    the_seq = add_iq_pulse_sweep(seq=the_seq,
                                 pulse=p,
                                 sweep_name='none',
                                 rotation_axis=rotation_axis_prep)
    p = gen.Pulse(start=end_time-pi_time/2,
                  duration=-pi_time/2,
                  amplitude=pi_amp,
                  ssm_freq=pi_ssm_freq,
                  phase=0)
    the_seq = add_iq_pulse_sweep(seq=the_seq,
                                 pulse=p,
                                 sweep_name='none',
                                 rotation_axis=rotation_axis_tom)
    #
    the_seq = add_readout_markers_and_gates(seq=the_seq, pat=pat)
    the_seq.write_sequence(base_name='foo',
                           file_path=sw_setup.write_dir,
                           use_range_01=False,
                           num_offset=num_offset,
                           write_binary=True)
    
    # prep -x, x-tom
    num_offset += 1
    rotation_axis_prep = '-y'
    rotation_axis_tom = '+y'
    the_seq = gen.Sequence(pat.pat_length, num_steps=1)
    p = gen.Pulse(start=end_time-pi_time/2,
                  duration=-pi_time/2,
                  amplitude=pi_amp,
                  ssm_freq=pi_ssm_freq,
                  phase=0)
    the_seq = add_iq_pulse_sweep(seq=the_seq,
                                 pulse=p,
                                 sweep_name='none',
                                 rotation_axis=rotation_axis_prep)
    p = gen.Pulse(start=end_time-pi_time/2,
                  duration=-pi_time/2,
                  amplitude=pi_amp,
                  ssm_freq=pi_ssm_freq,
                  phase=0)
    the_seq = add_iq_pulse_sweep(seq=the_seq,
                                 pulse=p,
                                 sweep_name='none',
                                 rotation_axis=rotation_axis_tom)
    #
    the_seq = add_readout_markers_and_gates(seq=the_seq, pat=pat)
    the_seq.write_sequence(base_name='foo',
                           file_path=sw_setup.write_dir,
                           use_range_01=False,
                           num_offset=num_offset,
                           write_binary=True)
    
    # prep -y, y-tom
    num_offset += 1
    rotation_axis_prep = '+x'
    rotation_axis_tom = '-x'
    the_seq = gen.Sequence(pat.pat_length, num_steps=1)
    p = gen.Pulse(start=end_time-pi_time/2,
                  duration=-pi_time/2,
                  amplitude=pi_amp,
                  ssm_freq=pi_ssm_freq,
                  phase=0)
    the_seq = add_iq_pulse_sweep(seq=the_seq,
                                 pulse=p,
                                 sweep_name='none',
                                 rotation_axis=rotation_axis_prep)
    p = gen.Pulse(start=end_time,
                  duration=-pi_time/2,
                  amplitude=pi_amp,
                  ssm_freq=pi_ssm_freq,
                  phase=0)
    the_seq = add_iq_pulse_sweep(seq=the_seq,
                                 pulse=p,
                                 sweep_name='none',
                                 rotation_axis=rotation_axis_tom)
    #
    the_seq = add_readout_markers_and_gates(seq=the_seq, pat=pat)
    the_seq.write_sequence(base_name='foo',
                           file_path=sw_setup.write_dir,
                           use_range_01=False,
                           num_offset=num_offset,
                           write_binary=True)
    
    # prep +y, y-tom
    num_offset += 1
    rotation_axis_prep = '-x'
    rotation_axis_tom = '-x'
    the_seq = gen.Sequence(pat.pat_length, num_steps=1)
    p = gen.Pulse(start=end_time-pi_time/2,
                  duration=-pi_time/2,
                  amplitude=pi_amp,
                  ssm_freq=pi_ssm_freq,
                  phase=0)
    the_seq = add_iq_pulse_sweep(seq=the_seq,
                                 pulse=p,
                                 sweep_name='none',
                                 rotation_axis=rotation_axis_prep)
    p = gen.Pulse(start=end_time,
                  duration=-pi_time/2,
                  amplitude=pi_amp,
                  ssm_freq=pi_ssm_freq,
                  phase=0)
    the_seq = add_iq_pulse_sweep(seq=the_seq,
                                 pulse=p,
                                 sweep_name='none',
                                 rotation_axis=rotation_axis_tom)
    #
    the_seq = add_readout_markers_and_gates(seq=the_seq, pat=pat)
    the_seq.write_sequence(base_name='foo',
                           file_path=sw_setup.write_dir,
                           use_range_01=False,
                           num_offset=num_offset,
                           write_binary=True)
    
    # prep -z, z-tom
    num_offset += 1
    rotation_axis_prep = '-y'
    the_seq = gen.Sequence(pat.pat_length, num_steps=1)
    p = gen.Pulse(start=end_time-pi_time/2,
                  duration=-pi_time,
                  amplitude=pi_amp,
                  ssm_freq=pi_ssm_freq,
                  phase=0)
    the_seq = add_iq_pulse_sweep(seq=the_seq,
                                 pulse=p,
                                 sweep_name='none',
                                 rotation_axis=rotation_axis_prep)
    #
    the_seq = add_readout_markers_and_gates(seq=the_seq, pat=pat)
    the_seq.write_sequence(base_name='foo',
                           file_path=sw_setup.write_dir,
                           use_range_01=False,
                           num_offset=num_offset,
                           write_binary=True)
    
    # prep +z, z-tom
    num_offset += 1
    the_seq = gen.Sequence(pat.pat_length, num_steps=1)
    #
    the_seq = add_readout_markers_and_gates(seq=the_seq, pat=pat)
    the_seq.write_sequence(base_name='foo',
                           file_path=sw_setup.write_dir,
                           use_range_01=False,
                           num_offset=num_offset,
                           write_binary=True)
    
    # write and load patterns
    pat.num_patterns = num_offset + 1
    write_folder_to_awg(sw_setup=sw_setup, pat=pat)
    wx_programs.wx_set_and_amplitude_and_offset()
    #END
    
def tom_cal_6pt_ef(): # PMH 
    #
    sw_setup = setup_seq_writer()
    pat = get_pattern_parameters()
    expt_cal = get_expt_cal()

    #
    end_time = pat.final_pulse_end
    
    #
    pi_prep_time = expt_cal.pi_time.ge
    pi_prep_amp = expt_cal.pi_amp.ge
    pi_prep_ssm_freq = expt_cal.ssm.ge
  
    #
    pi_time = expt_cal.pi_time.ef
    pi_amp = expt_cal.pi_amp.ef
    pi_ssm_freq = expt_cal.ssm.ef
    
    # prep +x, x-tom
    num_offset = 0
    rotation_axis_prep = '+y'
    rotation_axis_tom = '+y'
    the_seq = gen.Sequence(pat.pat_length, num_steps=1)
    p = gen.Pulse(start=end_time-pi_time/2-pi_time/2,
                  duration=-pi_prep_time,
                  amplitude=pi_prep_amp,
                  ssm_freq=pi_prep_ssm_freq,
                  phase=0)
    the_seq = add_iq_pulse_sweep(seq=the_seq,
                                 pulse=p,
                                 sweep_name='none')
    p = gen.Pulse(start=end_time-pi_time/2,
                  duration=-pi_time/2,
                  amplitude=pi_amp,
                  ssm_freq=pi_ssm_freq,
                  phase=0)
    the_seq = add_iq_pulse_sweep(seq=the_seq,
                                 pulse=p,
                                 sweep_name='none',
                                 rotation_axis=rotation_axis_prep)
    p = gen.Pulse(start=end_time-pi_time/2,
                  duration=-pi_time/2,
                  amplitude=pi_amp,
                  ssm_freq=pi_ssm_freq,
                  phase=0)
    the_seq = add_iq_pulse_sweep(seq=the_seq,
                                 pulse=p,
                                 sweep_name='none',
                                 rotation_axis=rotation_axis_tom)
    #
    the_seq = add_readout_markers_and_gates(seq=the_seq, pat=pat)
    the_seq.write_sequence(base_name='foo',
                           file_path=sw_setup.write_dir,
                           use_range_01=False,
                           num_offset=num_offset,
                           write_binary=True)
    
    # prep -x, x-tom
    num_offset += 1
    rotation_axis_prep = '-y'
    rotation_axis_tom = '+y'
    the_seq = gen.Sequence(pat.pat_length, num_steps=1)
    p = gen.Pulse(start=end_time-pi_time/2-pi_time/2,
                  duration=-pi_prep_time,
                  amplitude=pi_prep_amp,
                  ssm_freq=pi_prep_ssm_freq,
                  phase=0)
    the_seq = add_iq_pulse_sweep(seq=the_seq,
                                 pulse=p,
                                 sweep_name='none')
    p = gen.Pulse(start=end_time-pi_time/2,
                  duration=-pi_time/2,
                  amplitude=pi_amp,
                  ssm_freq=pi_ssm_freq,
                  phase=0)
    the_seq = add_iq_pulse_sweep(seq=the_seq,
                                 pulse=p,
                                 sweep_name='none',
                                 rotation_axis=rotation_axis_prep)
    p = gen.Pulse(start=end_time-pi_time/2,
                  duration=-pi_time/2,
                  amplitude=pi_amp,
                  ssm_freq=pi_ssm_freq,
                  phase=0)
    the_seq = add_iq_pulse_sweep(seq=the_seq,
                                 pulse=p,
                                 sweep_name='none',
                                 rotation_axis=rotation_axis_tom)
    #
    the_seq = add_readout_markers_and_gates(seq=the_seq, pat=pat)
    the_seq.write_sequence(base_name='foo',
                           file_path=sw_setup.write_dir,
                           use_range_01=False,
                           num_offset=num_offset,
                           write_binary=True)
    
    # prep -y, y-tom
    num_offset += 1
    rotation_axis_prep = '+x'
    rotation_axis_tom = '-x'
    the_seq = gen.Sequence(pat.pat_length, num_steps=1)
    p = gen.Pulse(start=end_time-pi_time/2-pi_time/2,
                  duration=-pi_prep_time,
                  amplitude=pi_prep_amp,
                  ssm_freq=pi_prep_ssm_freq,
                  phase=0)
    the_seq = add_iq_pulse_sweep(seq=the_seq,
                                 pulse=p,
                                 sweep_name='none')
    p = gen.Pulse(start=end_time-pi_time/2,
                  duration=-pi_time/2,
                  amplitude=pi_amp,
                  ssm_freq=pi_ssm_freq,
                  phase=0)
    the_seq = add_iq_pulse_sweep(seq=the_seq,
                                 pulse=p,
                                 sweep_name='none',
                                 rotation_axis=rotation_axis_prep)
    p = gen.Pulse(start=end_time,
                  duration=-pi_time/2,
                  amplitude=pi_amp,
                  ssm_freq=pi_ssm_freq,
                  phase=0)
    the_seq = add_iq_pulse_sweep(seq=the_seq,
                                 pulse=p,
                                 sweep_name='none',
                                 rotation_axis=rotation_axis_tom)
    #
    the_seq = add_readout_markers_and_gates(seq=the_seq, pat=pat)
    the_seq.write_sequence(base_name='foo',
                           file_path=sw_setup.write_dir,
                           use_range_01=False,
                           num_offset=num_offset,
                           write_binary=True)
    
    # prep +y, y-tom
    num_offset += 1
    rotation_axis_prep = '-x'
    rotation_axis_tom = '-x'
    the_seq = gen.Sequence(pat.pat_length, num_steps=1)
    p = gen.Pulse(start=end_time-pi_time/2-pi_time/2,
                  duration=-pi_prep_time,
                  amplitude=pi_prep_amp,
                  ssm_freq=pi_prep_ssm_freq,
                  phase=0)
    the_seq = add_iq_pulse_sweep(seq=the_seq,
                                 pulse=p,
                                 sweep_name='none')
    p = gen.Pulse(start=end_time-pi_time/2,
                  duration=-pi_time/2,
                  amplitude=pi_amp,
                  ssm_freq=pi_ssm_freq,
                  phase=0)
    the_seq = add_iq_pulse_sweep(seq=the_seq,
                                 pulse=p,
                                 sweep_name='none',
                                 rotation_axis=rotation_axis_prep)
    p = gen.Pulse(start=end_time,
                  duration=-pi_time/2,
                  amplitude=pi_amp,
                  ssm_freq=pi_ssm_freq,
                  phase=0)
    the_seq = add_iq_pulse_sweep(seq=the_seq,
                                 pulse=p,
                                 sweep_name='none',
                                 rotation_axis=rotation_axis_tom)
    #
    the_seq = add_readout_markers_and_gates(seq=the_seq, pat=pat)
    the_seq.write_sequence(base_name='foo',
                           file_path=sw_setup.write_dir,
                           use_range_01=False,
                           num_offset=num_offset,
                           write_binary=True)
    
    # prep -z, z-tom
    num_offset += 1
    rotation_axis_prep = '-y'
    the_seq = gen.Sequence(pat.pat_length, num_steps=1)
    p = gen.Pulse(start=end_time-pi_time/2-pi_time/2,
                  duration=-pi_prep_time,
                  amplitude=pi_prep_amp,
                  ssm_freq=pi_prep_ssm_freq,
                  phase=0)
    the_seq = add_iq_pulse_sweep(seq=the_seq,
                                 pulse=p,
                                 sweep_name='none')
    p = gen.Pulse(start=end_time-pi_time/2,
                  duration=-pi_time,
                  amplitude=pi_amp,
                  ssm_freq=pi_ssm_freq,
                  phase=0)
    the_seq = add_iq_pulse_sweep(seq=the_seq,
                                 pulse=p,
                                 sweep_name='none',
                                 rotation_axis=rotation_axis_prep)
    #
    the_seq = add_readout_markers_and_gates(seq=the_seq, pat=pat)
    the_seq.write_sequence(base_name='foo',
                           file_path=sw_setup.write_dir,
                           use_range_01=False,
                           num_offset=num_offset,
                           write_binary=True)
    
    # prep +z, z-tom
    num_offset += 1
    the_seq = gen.Sequence(pat.pat_length, num_steps=1)
    p = gen.Pulse(start=end_time-pi_time/2-pi_time/2,
                  duration=-pi_prep_time,
                  amplitude=pi_prep_amp,
                  ssm_freq=pi_prep_ssm_freq,
                  phase=0)
    the_seq = add_iq_pulse_sweep(seq=the_seq,
                                 pulse=p,
                                 sweep_name='none')
    
    ###
    #
    the_seq = add_readout_markers_and_gates(seq=the_seq, pat=pat)
    the_seq.write_sequence(base_name='foo',
                           file_path=sw_setup.write_dir,
                           use_range_01=False,
                           num_offset=num_offset,
                           write_binary=True)
    
    # write and load patterns
    pat.num_patterns = num_offset + 1
    write_folder_to_awg(sw_setup=sw_setup, pat=pat)
    wx_programs.wx_set_and_amplitude_and_offset()
    #END
    
    
def tom_cal(ge_or_ef='ge'): # PMH 
    #
    sw_setup = setup_seq_writer()
    pat = get_pattern_parameters()
    expt_cal = get_expt_cal()

    # prep +x, x-tom
    num_offset = 0
    make_prep_and_tom_single_pattern(pat=pat,
                                     expt_cal=expt_cal,
                                     ge_or_ef=ge_or_ef,
                                     num_offset=num_offset,
                                     prep_state = '+x',
                                     tomography = 'x')
        
    # prep -x, x-tom
    num_offset = 0
    make_prep_and_tom_single_pattern(pat=pat,
                                     expt_cal=expt_cal,
                                     ge_or_ef=ge_or_ef,
                                     num_offset=num_offset,
                                     prep_state = '-x',
                                     tomography = 'x')
    
    # prep +y, y-tom
    num_offset = 0
    make_prep_and_tom_single_pattern(pat=pat,
                                     expt_cal=expt_cal,
                                     ge_or_ef=ge_or_ef,
                                     num_offset=num_offset,
                                     rotation_axis_prep = '+y',
                                     tomography = 'y')

    # prep -y, y-tom
    num_offset = 0
    make_prep_and_tom_single_pattern(pat=pat,
                                     expt_cal=expt_cal,
                                     ge_or_ef=ge_or_ef,
                                     num_offset=num_offset,
                                     prep_state = '-y',
                                     tomography = 'y')
    
    # prep +z, z-tom
    num_offset = 0
    make_prep_and_tom_single_pattern(pat=pat,
                                     expt_cal=expt_cal,
                                     ge_or_ef=ge_or_ef,
                                     num_offset=num_offset,
                                     prep_state = '+z',
                                     tomography = 'z')
    
    # prep -z, z-tom
    num_offset = 0
    make_prep_and_tom_single_pattern(pat=pat,
                                     expt_cal=expt_cal,
                                     ge_or_ef=ge_or_ef,
                                     num_offset=num_offset,
                                     prep_state = '-z',
                                     tomography = 'z')
    
    # write and load patterns
    pat.num_patterns = num_offset + 1
    write_folder_to_awg(sw_setup=sw_setup, pat=pat)
    wx_programs.wx_set_and_amplitude_and_offset()
    #END
    
   
def test_seq_add(): # PMH 
    sw_setup = setup_seq_writer()
    pat = get_pattern_parameters()
    expt_cal = get_expt_cal()

    #
    pat.num_patterns = 51
    sweep_time = 200
    ssm_clock = expt_cal.ssm.ef
    
    #
    end_time = pat.final_pulse_end
    
    #
    the_seq = gen.Sequence(pat.pat_length, pat.num_patterns)
    
    # pi ge
    p = gen.Pulse(start=end_time,
                  duration=0,
                  amplitude=expt_cal.pi_amp.ge,
                  ssm_freq=expt_cal.ssm.ge,
                  phase=0)
    the_seq = add_iq_pulse_sweep(seq=the_seq,
                                 pulse=p,
                                 sweep_name='width',
                                 start=0,
                                 stop=-sweep_time)
    
    seq_a = the_seq
    
    #
    the_seq = gen.Sequence(pat.pat_length, pat.num_patterns)
    
    # pi ge
    p = gen.Pulse(start=end_time,
                  duration=0,
                  amplitude=expt_cal.pi_amp.ge,
                  ssm_freq=expt_cal.ssm.ge,
                  phase=0)
    the_seq = add_iq_pulse_sweep(seq=the_seq,
                                 pulse=p,
                                 sweep_name='width',
                                 start=0,
                                 stop=-sweep_time)
    
    
    seq_b = the_seq
    seq_c = seq_a+seq_b
    print(seq_c.channel_list.shape)
    
    return seq_a, seq_b, seq_c
    #END
    
if __name__=="__main__":
    pass