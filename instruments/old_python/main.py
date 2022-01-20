# -*- coding: utf-8 -*-
"""
Created on Mon Jan 27 20:04:05 2020

@author: P. M. Harrington
"""

import numpy as np
import matplotlib.pyplot as plt
import pickle
import datetime

import expt_parameters
import seq_experiments
import seq_programs
import daq_programs
import analysis
from Nop_class import Nop

import wx_programs
import keithley2401
#import hp_E4405B

def get_save_path():
    path0 = r"C:\Data\2020\200309_nonHermitian\data\\"
    time_str = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    save_path = path0 + time_str
    return save_path, path0

def save_by_pickle(data_in):
    save_path, _ = get_save_path()
    fname = save_path + ".pickle"
    print(fname)
    
    with open(fname, "wb") as open_file:
        pickle.dump(data_in, open_file)
        
def load_pickle():
    _, path0 = get_save_path()
    fname = path0 + "20200309_152452.pickle"
    
    with open(fname, "rb") as open_file:    
        x = pickle.load(open_file)
        
    return x

if __name__ == '__main__':
    expt = expt_parameters.expt_parameters()
    seq = Nop("seq")
    msmt = Nop("measurement")
#
    seq.comment = "rabi_ef_prep_f, sweep rabi detuning"
    seq.num_patterns = 101
    seq.sweep_time = 2000
    seq.num_records_per_pattern = 200
    seq.rabi_amp = 0.05
    seq.times = np.linspace(0., seq.sweep_time, seq.num_patterns)*1e-3
    
    sweep = Nop("sweep")
    sweep.comment = "rabi ssb freq near EP"
    sweep.vals = np.linspace(-0.5, 0.5, 2)*1e-3 + 0.092
#    sweep.vals = np.linspace(-0.5, 0.5, 3)*1e-3 + expt_cal.ssm.ef
    pop_3state = []
    for idx, rabi_ssb_freq in enumerate(sweep.vals):
        print(idx)
        seq_experiments.rabi_ef_prep_f(seq.num_patterns, seq.sweep_time, seq.rabi_amp, rabi_ssb_freq)
        daq_params, rec_readout_vs_pats, p_readout = daq_programs.run_daq(
                num_patterns=seq.num_patterns, num_records_per_pattern=seq.num_records_per_pattern)
        p_post = analysis.p_readout_postselected(p_readout)
        pop_3state.append(p_readout)
#        save_by_pickle((expt, seq, daq, msmt))
        plt.plot(seq.times, p_readout[0])
        plt.ylim([0, 1])
        plt.show()
#
#    seq.comment = "new exp t1_test"
#    seq.num_patterns = 51
#    seq.sweep_time = 100
#    seq.num_records_per_pattern = 200
# 
#    seq.times = np.linspace(0., seq.sweep_time, seq.num_patterns)*1e-3
#    seq_experiments.rabi_ge(seq.num_patterns, seq.sweep_time)
#    daq, msmt.rec_readout_vs_pats, msmt.p_readout = daq_programs.run_daq(
#            num_patterns=seq.num_patterns, num_records_per_pattern=seq.num_records_per_pattern)
#    msmt.p_post = analysis.p_readout_postselected(msmt.p_readout)
#    #
#    x = seq.times
#    y = msmt.p_readout[0]
#    plt.plot(x, y)
#    plt.ylim([0, 1])
#    msmt.popt, msmt.perr, _, _ = analysis.fit_exp_decay(x, y, [-1, 7, 1])
#    save_by_pickle((expt, seq, daq, msmt))
    #
#    seq.comment = "rabi_ef_prep_f, f & not f readout"
#    seq.num_patterns = 51
#    seq.sweep_time = 200
#    seq.num_records_per_pattern = 200
#    seq.rabi_amp = 0.5
#    seq.times = np.linspace(0., seq.sweep_time, seq.num_patterns)*1e-3
#    seq_experiments.rabi_ef_prep_f_fnotf(seq.num_patterns, seq.sweep_time, seq.rabi_amp)
#    daq, msmt.rec_readout_vs_pats, msmt.p_readout = daq_programs.run_daq(
#            num_patterns=2*seq.num_patterns, num_records_per_pattern=seq.num_records_per_pattern)
#    msmt.p_readout_fnotf, msmt.p_post_fnotf = analysis.readout_fnotf(msmt.p_readout)
#    plt.plot(msmt.p_post_fnotf.T)
#    plt.ylim([0,1])
#    plt.show()
#    save_by_pickle((expt, seq, daq, msmt))
    
#    #
#    seq.comment = "g_e_f readout"
#    seq.num_patterns = 6
#    seq.num_records_per_pattern = 1000
#    #seq_experiments.g_e_f()
#    for _ in range(1):
#        print(_)
#        daq, msmt.rec_readout_vs_pats, msmt.n_vs_pats, msmt.p_vs_pats, msmt.bins_cntr, msmt.counts = (
#            daq_programs.run_iq_vs_patterns(
#                    num_patterns=seq.num_patterns, num_records_per_pattern=seq.num_records_per_pattern))
#    
#    fit = []
#    for k in range(seq.num_patterns):    
#        r = msmt.rec_readout_vs_pats[0].T[k]
#        _ = analysis.fit_gaussian(r, msmt.bins_cntr[0], msmt.counts[0][k])
#        fit.append(_)        
#    t0_a, t0_b = analysis.get_threshold_value_from_gaussians(fit[0][0][0], fit[1][0][0]);
#    t1_a, t1_b = analysis.get_threshold_value_from_gaussians(fit[1][0][0], fit[2][0][0]);
#    print(t0_a)
#    print(t1_a)
#    save_by_pickle((expt, seq, daq, msmt))
    
#    #
#    seq.comment = "pi_ge, calibration"
#    seq.num_patterns = 101
#    seq.num_records_per_pattern = 1000
#    seq.sweep_start_stop = [0.1, 0.9]
#    seq_experiments.pi_ge_cal_amp(num_patterns=seq.num_patterns, sweep_start_stop=seq.sweep_start_stop)
#    daq, msmt.rec_readout_vs_pats, msmt.p_readout = daq_programs.run_daq(
#            num_patterns=seq.num_patterns, num_records_per_pattern=seq.num_records_per_pattern)
#    seq.vals = np.linspace(seq.sweep_start_stop[0], seq.sweep_start_stop[1], seq.num_patterns)
#    plt.plot(msmt.p_readout[0])
#    idx = [60, 100]
#    x = seq.vals[idx[0]:idx[1]]
#    y = msmt.p_readout[0][idx[0]:idx[1]]
#    msmt.popt, msmt.perr = analysis.fit_parabola(x, y)
#    save_by_pickle((expt, seq, daq, msmt))
    
#    #
#    seq.comment = "pi_ef, calibration"
#    seq.num_patterns = 101
#    seq.num_records_per_pattern = 1000
#    seq.sweep_start_stop = [0, 1]
#    seq.vals = np.linspace(seq.sweep_start_stop[0], seq.sweep_start_stop[1], seq.num_patterns)
#    seq_experiments.pi_ef_cal_amp(num_patterns=seq.num_patterns, sweep_start_stop=seq.sweep_start_stop)
#    daq, msmt.rec_readout_vs_pats, msmt.p_readout = daq_programs.run_daq(num_patterns=seq.num_patterns, num_records_per_pattern=seq.num_records_per_pattern)
#    msmt.p_post = analysis.p_readout_postselected(msmt.p_readout)
#    #
#    plt.plot(msmt.p_post[1])
#    idx = [40,80]
#    x = seq.vals[idx[0]:idx[1]]
#    y = msmt.p_post[1][idx[0]:idx[1]]
#    msmt.popt, msmt.perr = analysis.fit_parabola(x, y)
#    save_by_pickle((expt, seq, daq, msmt))
#    
#    #
#    seq.comment = "ramsey_ef_prep_e"
#    seq.num_patterns = 51
#    seq.sweep_time = 500
#    seq.num_records_per_pattern = 200
#    seq.times = np.linspace(0., seq.sweep_time, seq.num_patterns)*1e-3
#    seq_experiments.ramsey_ef_prep_e(seq.num_patterns, seq.sweep_time)
#    daq, msmt.rec_readout_vs_pats, msmt.p_readout = daq_programs.run_daq(
#            num_patterns=seq.num_patterns, num_records_per_pattern=seq.num_records_per_pattern)
#    msmt.p_post = analysis.p_readout_postselected(msmt.p_readout)
#    plt.plot(seq.times, msmt.p_post[-1])
#    msmt.popt, msmt.perr, _, _ = analysis.fit_sine_decay(seq.times, msmt.p_post[-1])
#    save_by_pickle((expt, seq, daq, msmt))
    
    
###############################################################################
    
    
#    #
#    plt.plot(seq.times, p_post[-1])
#    plt.ylim([0, 1])
#    popt, perr, _, _ = analysis.fit_sine_decay(seq.times, p_post[-1])
    #
#    print("pi_time from fit (ns): {}".format(1e3*0.5/popt[0]))
#    expt_cal = seq_programs.get_expt_cal()
#    print("pi_time is expt_cal (ns): {}".format(expt_cal.pi_time.ef))
        
#    #
#    seq.comment = "rabi_ef_prep_f, sweep rabi detuning"
#    seq.num_patterns = 101
#    seq.sweep_time = 2000
#    seq.num_records_per_pattern = 200
#    seq.rabi_amp = 0.05
#    seq.times = np.linspace(0., seq.sweep_time, seq.num_patterns)*1e-3
#    
#    sweep = Nop("sweep")
#    sweep.comment = "rabi ssb freq near EP"
#    sweep.vals = np.linspace(-0.5, 0.5, 3)*1e-3 + 0.092
##    sweep.vals = np.linspace(-0.5, 0.5, 3)*1e-3 + expt_cal.ssm.ef
#    
#    for idx, rabi_ssb_freq in enumerate(sweep.vals):
#        print(idx)
#        seq_experiments.rabi_ef_prep_f(seq.num_patterns, seq.sweep_time, seq.rabi_amp, rabi_ssb_freq)
#        daq_params, rec_readout_vs_pats, p_readout = daq_programs.run_daq(
#                num_patterns=seq.num_patterns, num_records_per_pattern=seq.num_records_per_pattern)
#        p_post = analysis.p_readout_postselected(p_readout)
#        
#        save_by_pickle((expt, seq, daq, msmt))
#        plt.plot(seq.times, p_post[-1])
#        plt.ylim([0, 1])
#        plt.show()
        
    
#    #
#    seq.comment = "g_e_f readout"
#    seq.num_patterns = 3
#    seq.num_records_per_pattern = 1000
#    #seq_experiments.g_e_f()
#    for _ in range(1):
#        print(_)
#        daq_params, rec_readout_vs_pats, n_vs_pats, p_vs_pats, bins_cntr, counts = (
#            daq_programs.run_iq_vs_patterns(
#                    num_patterns=seq.num_patterns, num_records_per_pattern=seq.num_records_per_pattern))
#    
#    fit = []
#    for k in range(seq.num_patterns):    
#        r = rec_readout_vs_pats[0].T[k]
#        _ = analysis.fit_gaussian(r, bins_cntr[0], counts[0][k])
#        fit.append(_)        
#    t0_a, t0_b = analysis.get_threshold_value_from_gaussians(fit[0][0][0], fit[1][0][0]);
#    t1_a, t1_b = analysis.get_threshold_value_from_gaussians(fit[1][0][0], fit[2][0][0]);
#    print(t0_a)
#    print(t1_a)

#    #    
#    seq.comment = "rabi_ge"
#    seq.num_patterns = 51
#    seq.num_records_per_pattern = 500
#    seq.sweep_time = 200
#    seq_experiments.rabi_ge(seq.num_patterns, seq.sweep_time)
#    daq_params, rec_readout_vs_pats, p_readout = daq_programs.run_daq(
#            num_patterns=seq.num_patterns, num_records_per_pattern=seq.num_records_per_pattern)
#    #
#    times = np.linspace(0., seq.sweep_time, seq.num_patterns)*1e-3
#    plt.plot(times, p_readout[0])
#    popt, perr, _, _ = analysis.fit_sine_decay(times, p_readout[0])
#    #
#    print("pi_time from fit (ns): {}".format(1e3*0.5/popt[0]))
#    expt_cal = seq_programs.get_expt_cal()
#    print("pi_time is expt_cal (ns): {}".format(expt_cal.pi_time.ge))
    
#    #
#    seq.comment = "t1decay_ef"
#    seq.num_patterns = 101
#    seq.num_records_per_pattern = 500
#    seq.sweep_time = 5000
#    seq.times = np.linspace(0, seq.sweep_time, seq. num_patterns)*1e-3
#    #seq_experiments.t1decay_ef(seq.num_patterns, seq.sweep_time)
#    #
#    daq_params, rec_readout_vs_pats, p_readout = daq_programs.run_daq(
#            num_patterns=seq.num_patterns, num_records_per_pattern=seq.num_records_per_pattern)
#    p_post = analysis.p_readout_postselected(p_readout)
#    #
#    x = seq.times
#    y = p_readout[2]
#    plt.plot(x, y)
#    plt.ylim([0, 1])
#    popt, perr, _, _ = analysis.fit_exp_decay(x, y, [-1, 7, 1])
    
#    #
#    seq.comment = "t1decay_ge"
#    seq.num_patterns = 101
#    seq.num_records_per_pattern = 500
#    seq.sweep_time = 5000
#    seq.times = np.linspace(0, seq.sweep_time, seq. num_patterns)*1e-3
#    seq_experiments.t1decay_ge(seq.num_patterns, seq.sweep_time)
#    #
#    daq_params, rec_readout_vs_pats, p_readout = daq_programs.run_daq(
#            num_patterns=seq.num_patterns, num_records_per_pattern=seq.num_records_per_pattern)
#    p_post = analysis.p_readout_postselected(p_readout)
#    #
#    x = seq.times
#    y = p_readout[0]
#    plt.plot(x, y)
#    plt.ylim([0, 1])
#    popt, perr, _, _ = analysis.fit_exp_decay(x, y, [-1, 7, 1])

##    #
#    seq.comment = "rabi_ef_prep_f"
#    seq.num_patterns = 51
#    seq.sweep_time = 200
#    seq.num_records_per_pattern = 200
#    seq.rabi_amp = 0.5
#    seq.times = np.linspace(0., seq.sweep_time, seq.num_patterns)*1e-3
#    #seq_experiments.rabi_ef_prep_f(seq.num_patterns, seq.sweep_time, seq.rabi_amp)
#    daq_params, rec_readout_vs_pats, p_readout = daq_programs.run_daq(
#            num_patterns=seq.num_patterns, num_records_per_pattern=seq.num_records_per_pattern)
#    p_post = analysis.p_readout_postselected(p_readout)
#    #
#    plt.plot(seq.times, p_post[-1])
#    plt.ylim([0, 1])
#    popt, perr, _, _ = analysis.fit_sine_decay(seq.times, p_post[-1])
#    #
#    print("pi_time from fit (ns): {}".format(1e3*0.5/popt[0]))
#    expt_cal = seq_programs.get_expt_cal()
#    print("pi_time is expt_cal (ns): {}".format(expt_cal.pi_time.ef))
    
#    #
#    seq.comment = "rabi_ef_prep_f"
#    seq.num_patterns = 51
#    seq.sweep_time = 200
#    seq.num_records_per_pattern = 200
#    seq.rabi_amp = 0.5
#    seq.times = np.linspace(0., seq.sweep_time, seq.num_patterns)*1e-3
#    #
#    #seq_experiments.rabi_ef_prep_f(seq.num_patterns, seq.sweep_time, seq.rabi_amp)
#    daq_params, rec_readout_vs_pats, p_readout = daq_programs.run_daq(
#            num_patterns=seq.num_patterns, num_records_per_pattern=seq.num_records_per_pattern)
#    p_post = analysis.p_readout_postselected(p_readout)
#    #
#    plt.plot(seq.times, p_post[-1])
#    plt.ylim([0, 1])
#    popt, perr, _, _ = analysis.fit_sine_decay(seq.times, p_post[-1])
#    #
#    print("pi_time from fit (ns): {}".format(1e3*0.5/popt[0]))
#    expt_cal = seq_programs.get_expt_cal()
#    print("pi_time is expt_cal (ns): {}".format(expt_cal.pi_time.ef))

#    #
#    seq.comment = "ramsey_ge"
#    seq.num_patterns = 101
#    seq.num_records_per_pattern = 200
#    seq.sweep_time = 500
#    #seq_experiments.ramsey_ge(num_patterns=seq.num_patterns, sweep_time=seq.sweep_time)
#    daq_params, rec_readout_vs_pats, p_readout = daq_programs.run_daq(num_patterns=seq.num_patterns, num_records_per_pattern=seq.num_records_per_pattern)
#    #
#    times = np.linspace(0., seq.sweep_time, seq.num_patterns)*1e-3
#    plt.plot(times, p_readout[0])
#    popt, perr, _, _ = analysis.fit_sine_decay(times, p_readout[0])
    
    
    ###########################################################################
    
#    #
#    seq = Nop("seq")
#    seq.comment = "t1decay_ge"
#    seq.num_patterns = 101
#    seq.num_records_per_pattern = 50
#    seq.sweep_time = 5000
#    #seq_experiments.t1decay_ge(seq.num_patterns, seq.sweep_time)
#    daq_params, rec_readout_vs_pats, p_readout = daq_programs.run_daq(
#            num_patterns=seq.num_patterns, num_records_per_pattern=seq.num_records_per_pattern)
#    times = np.linspace(0., seq.sweep_time, seq.num_patterns)*1e-3
#    plt.plot(times, p_readout[0])
#    popt, perr, _, _ = analysis.fit_exp_decay(times, p_readout[0], guess_vals=[-1, 5, 1.])
    
    

#    times_ramsey = np.linspace(0.,sweep_time_ramsey, num_patterns_each)*1e-3
#    times_t1decay = np.linspace(0.,sweep_time_t1decay, num_patterns_each)*1e-3
#    daq_params, rec_readout_vs_pats, p_readout = daq_programs.run_daq(num_patterns=2*num_patterns_each, num_records_per_pattern=500)
#    p_ramsey = p_readout[0][:num_patterns_each]
#    p_t1decay = p_readout[0][num_patterns_each:]    
#    popt_ramsey, _, _, _ = analysis.fit_sine_decay(times_ramsey, p_ramsey)
#    fit_t1decay, _ = analysis.fit_exp_decay(times_t1decay, p_t1decay)
#    print("\nT2*: {}".format(1/popt_ramsey[0][1]))
    
#    
#    plt.plot(times, p_readout[0])
#    fit, _ = analysis.fit_sine_decay(times, p_readout[0])

##    # sweep flux, ramsey
#    num_patterns = 101
#    sweep_time = 500
###    seq.ramsey_ge(num_patterns, sweep_time)
##    keithley_current_mA = np.linspace(7.25, 7.30, 5)
##    freq_array = []
##    gamma_array = []
##    for bias_val in keithley_current_mA:
##        keithley2401.set_current(bias_val)
##        
##        daq_params, rec_readout_vs_pats, p_readout = daq_programs.run_daq(num_patterns=num_patterns, num_records_per_pattern=100)
##        times = np.linspace(0.,sweep_time, num_patterns)*1e-3
##        plt.plot(times, p_readout[0])
##        fit, _ = analysis.fit_sine_decay(times, p_readout[0])
##        freq_array.append(fit[0][0])
##        gamma_array.append(fit[0][1])
##        
##    freq_array = np.array(freq_array)
##    gamma_array = np.array(gamma_array)
##    
##    plt.figure()
##    plt.plot(keithley_current_mA, abs(freq_array))
##    plt.plot(keithley_current_mA, gamma_array)
#    
#    num_loops = 1
#    dum = np.full(num_loops, np.nan)
#    freq_array = dum.copy()
#    gamma_array = dum.copy()
#    for k in range(num_loops):
#        daq_params, rec_readout_vs_pats, p_readout = daq_programs.run_daq(num_patterns=num_patterns, num_records_per_pattern=200)
#        times = np.linspace(0., sweep_time, num_patterns)*1e-3
#        plt.plot(times, p_readout[0])
#        try:
#            fit, _ = analysis.fit_sine_decay(times, p_readout[0])
#            freq_array[k] = fit[0][0]
#            gamma_array[k] = fit[0][1]
#        except RuntimeError:
#            print("RuntimeError")
#            
#    
#    plt.figure()
#    plt.plot(abs(freq_array))
#    plt.show()
#    plt.figure()
#    plt.plot(gamma_array)
#    plt.show()
        
#    num_patterns = 101
#    sweep_time = 500
##    seq.ramsey_ge(num_patterns, sweep_time)
#    daq_params, rec_readout_vs_pats, p_readout = daq_programs.run_daq(num_patterns=num_patterns, num_records_per_pattern=200)
#    times = np.linspace(0., sweep_time, num_patterns)*1e-3
#    plt.plot(times, p_readout[0])
#    analysis.fit_sine_decay(times, p_readout[0])
    
#    # rabi_ge
#    num_patterns = 51
#    sweep_time = 200
#    seq.rabi_ge(num_patterns=num_patterns, sweep_time=sweep_time)
#    daq_params, rec_readout_vs_pats, p_readout = daq_programs.run_daq(num_patterns=num_patterns, num_records_per_pattern=200)
#    x = np.linspace(0., sweep_time, num_patterns)*1e-3
#    y = p_readout[0]
#    plt.plot(x, y)
#    fit, _ = analysis.fit_sine_decay(x, y, guess_vals = [15, 5., 0.25, 90., 0.5])
#    print("pi_time from fit (ns): {}".format(1e3*0.5/fit[0][0]))
#    expt_cal = seq_programs.get_expt_cal()
#    print("pi_time is expt_cal (ns): {}".format(expt_cal.pi_time.ge))
    
#    seq.rabi_spectroscopy_ge()
#    expt_cal = seq_programs.get_expt_cal();
#    freq = 5.584 + expt_cal.ssm.ge + np.linspace(-0.025, 0.025, 201)
#    plt.plot(freq, p_readout[0])

#    # measurement of Omega vs J
#    seq.rabi_ge_prep_e(0.1)
#    rabi_freq = []
#    #rabi_amp_array = np.linspace(0.05, 0.5, 10)
#    rabi_amp_array = np.linspace(0.05, 0.5, 10)
#    for rabi_amp in rabi_amp_array:
#        wx_programs.wx_set_and_amplitude_and_offset(amp=[rabi_amp, rabi_amp, 1.5, 1.5])
#        daq_params, rec_readout_vs_pats, p_readout = daq_programs.run_daq(num_patterns=101, num_records_per_pattern=2000)
#        times = np.linspace(0., 1.0, 101)
#        plt.plot(times, p_readout[1])
#        fit, _ = daq_processing.fit_sine_decay(times, p_readout[1])
#        rabi_freq.append(fit[0][0])
#    
#    gamma = 6.6
#    J_theory = 3.2886755678047384*np.pi/1.5*rabi_amp_array
#    Omega_theory = 0.25*np.sqrt(64*J_theory**2-gamma**2)/(2*np.pi)
#    
#    
#    rabi_freq = np.array(rabi_freq)
#    plt.plot(rabi_amp_array, rabi_freq,'.')
#    
#    plt.figure()
#    plt.plot(J_theory, rabi_freq,'.')
#    plt.plot(J_theory, Omega_theory, 'r.')
#    plt.ylim(0,2)
    
#    seq.t1_decay_ge()
#    daq_params, rec_readout_vs_pats, p_readout = daq_programs.run_daq(num_patterns=101, num_records_per_pattern=200)
#    times = np.linspace(0., 1.0, 101)
#    plt.plot(times, p_readout[0])
#    daq_processing.fit_exp_decay(times, p_readout[0], guess_vals=[-1, 5, 1.])
    
#    seq.nopi_1pi2_pi()
#    daq_params, rec_readout_vs_pats = daq_programs.run_iq_vs_patterns(num_patterns=3, num_records_per_pattern=1000)

#    seq.rabi_ef_prep_e()
#    daq_params, rec_readout_vs_pats, p_readout = daq_programs.run_daq(num_patterns=51, num_records_per_pattern=200)
#    p_readout_post = p_readout_post_vs_patterns(p_readout)
#    make_readout_vs_patterns_plot(p_readout_post)
#    
#    times = np.linspace(0., 1., 51)
#    plt.plot(times, p_readout_post[1])
#    daq_processing.fit_sine_decay(times, p_readout[1])
    
#    rabi_spectroscopy_probe_ge_sweep_ef()
#    daq_params, rec_readout_vs_pats, p_readout = daq_programs.run_daq(num_patterns=101, num_records_per_pattern=200)
#    expt_cal = seq_programs.get_expt_cal();
#    freq = 5.6082+expt_cal.ssm.ef + np.linspace(-0.010, 0.010, 101)
#    plt.plot(freq, p_readout[0])
    
#    seq.pi_cal_ge()
#    daq_params, rec_readout_vs_pats, p_readout = daq_programs.run_daq(num_patterns=101, num_records_per_pattern=200)
#    fit_idx = [25, 70]
#    sweep_vals = np.linspace(0,1, 101)
#    x = sweep_vals[fit_idx[0]:fit_idx[1]]
#    y = p_readout[0][fit_idx[0]:fit_idx[1]]
#    fit, _ = daq_processing.fit_parabola(x, y)
    
#    # aulter-townes, rabi spectroscopy ge while sweep ef drive
#    num_patterns = 201
#    ssm_width = 0.060
#    #seq.rabi_spectroscopy_probe_ge_sweep_ef(num_patterns=num_patterns, ssm_width=ssm_width)
#    daq_params, rec_readout_vs_pats, p_readout = daq_programs.run_daq(num_patterns=num_patterns, num_records_per_pattern=200)
#    expt_cal = seq_programs.get_expt_cal()
#    x = expt_cal.freq.carrier + expt_cal.ssm.ef + np.linspace(-ssm_width/2, +ssm_width/2, num_patterns)
#    plt.figure()
#    plt.plot(x, p_readout[2])
#    plt.ylim(0, 1)
#    plt.xlabel("Frequency (GHz)")
#    plt.show()
    
#    # rabi_ef
#    num_patterns = 51
#    sweep_time = 200
#    num_reps = 200
#    seq.rabi_ef_prep_e(num_patterns=num_patterns, sweep_time=sweep_time, rabi_amp=0.5)
#    daq_params, rec_readout_vs_pats, p_vs_pats, p_vs_pats_post = daq_programs.run_daq_with_post_selection(num_patterns=num_patterns, num_records_per_pattern=num_reps)
#    x = np.linspace(0., sweep_time, num_patterns)*1e-3
#    y = p_vs_pats_post[2]
#    plt.figure()
#    plt.plot(x, y)
#    fit, _ = daq_processing.fit_sine_decay(x, y)
#    print("pi_time from fit (ns): {}".format(1e3*0.5/fit[0][0]))
#    expt_cal = seq_programs.get_expt_cal()
#    print("pi_time is expt_cal (ns): {}".format(expt_cal.pi_time.ef))
    
#    num_patterns = 101
#    sweep_time = 500
#    #seq.ramsey_ef(num_patterns=num_patterns, sweep_time=sweep_time)
#    daq_params, rec_readout_vs_pats, p_vs_pats, p_vs_pats_post = daq_programs.run_daq_with_post_selection(num_patterns=num_patterns, num_records_per_pattern=1000)
#    x = np.linspace(0., sweep_time, num_patterns)*1e-3
#    y = p_vs_pats_post[2]
#    plt.plot(x, y)
#    daq_processing.fit_sine_decay(x, y, guess_vals = [40, 5., 0.25, 90., 0.5])
    
#    for _ in range(1):
#        daq_programs.run_iq_vs_patterns(num_patterns=3, num_records_per_pattern=1000);