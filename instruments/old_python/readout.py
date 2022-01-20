# -*- coding: utf-8 -*-
"""
Created on Tue Mar 10 14:14:04 2020

@author: crow104
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
import black_nonHermitian

from Nop_class import Nop

import wx_programs
import keithley2401

if __name__ == '__main__':
    expt = expt_parameters.expt_parameters()
    seq = Nop("seq")
    msmt = Nop("measurement")

#    seq.comment = "ramsey_ge calibration"
#    seq.num_patterns = 51
#    seq.sweep_time = 1000
#    seq.num_records_per_pattern = 500
#    seq.rabi_amp = 0.05
#    seq.times = np.linspace(0., seq.sweep_time, seq.num_patterns)*1e-3
#    steps=13
#    
#    sweep = Nop("sweep")
#    sweep.comment = "rabi ssb freq near EP"
#    sweep.vals = np.linspace(-3, 3, steps)*1e-3 + 0.092 # ge ramsey
##    sweep.vals = np.linspace(-0.5, 0.5, 3)*1e-3 + expt_cal.ssm.ef
#    pop_3state = []
#    fpop=[]
#
#    for idx, ssm_ef in enumerate(sweep.vals):
#        print(idx)
#        
#        black_nonHermitian.ramsey_ef(ssm_ef)
#        wx_programs.wx_set_and_amplitude_and_offset()
#
##        seq_experiments.rabi_ef_prep_f(seq.num_patterns, seq.sweep_time, seq.rabi_amp, rabi_ssb_freq)
#        daq_params, rec_readout_vs_pats, p_readout = daq_programs.run_daq(
#                num_patterns=seq.num_patterns, num_records_per_pattern=seq.num_records_per_pattern)
#        p_post = analysis.p_readout_postselected(p_readout)
#        pop_3state.append(p_readout)
##        msmt.popt, msmt.perr, _, _ = analysis.fit_sine_decay(x, y, guess_vals=None)
#        x = seq.times
#        y = p_post[1]
##        analysis.fit_sine_decay(x,y,)
#        fpop.append(p_post[1])
##        save_by_pickle((expt, seq, daq, msmt))
#        plt.plot(seq.times, p_post[1])
#        plt.ylim([0,4])
#        plt.show()
##    pop_3state = np.stack(pop_3state)
#    popdstack=np.dstack(pop_3state)
#
#    pop3state_f=popdstack.reshape(seq.num_patterns*3,steps)
#    np.savetxt('popdstack', pop3state_f)
#    np.savetxt('fpop', fpop)
#    fig = plt.figure()
#    plt.imshow(fpop)
##    plt.imshow(pop_3state[:,1,:])
#    plt.show
    
    seq.comment = "t1 ge"
    seq.num_patterns = 51
    seq.sweep_time = 1000
    seq.num_records_per_pattern = 1000
 
    seq.times = np.linspace(0., seq.sweep_time, seq.num_patterns)*1e-3
    black_nonHermitian.ramsey_ef()
    wx_programs.wx_set_and_amplitude_and_offset()
    daq, msmt.rec_readout_vs_pats, msmt.p_readout = daq_programs.run_daq(
            num_patterns=seq.num_patterns, num_records_per_pattern=seq.num_records_per_pattern)
#    msmt.p_post = analysis.p_readout_postselected(msmt.p_readout)
    msmt.p_post = analysis.p_readout_postselected(msmt.p_readout)
    #
    x = seq.times
    y = msmt.p_post[1]
    plt.plot(x, y)
    plt.ylim([0, 1])
#    msmt.popt, msmt.perr, _, _ =  analysis.fit_exp_decay(x, y, guess_vals=None)
    msmt.popt, msmt.perr, _, _ =  analysis.fit_sine_decay(x, y, guess_vals=None)
#    save_by_pickle((expt, seq, daq, msmt))