# -*- coding: utf-8 -*-
"""
Created on Tue Mar  3 14:31:52 2020

@author: crow104
"""

# -*- coding: utf-8 -*-
"""
Created on Mon Jan 27 20:04:05 2020

@author: P. M. Harrington
"""

import numpy as np
import matplotlib.pyplot as plt
from Nop_class import Nop
import pickle
import datetime

import seq_experiments
import seq_programs
import daq_programs
import analysis

import wx_programs
import keithley2401
#import hp_E4405B

def get_save_path():
    path0 = "C:\\Data\\2020\\ep_metrology\\data\\data_200304"
    time_str = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    save_path = path0 + "\\" + time_str
    return save_path

def save_by_pickle(data_in):
    save_path = get_save_path()
    fname = save_path + ".pickle"
    print(fname)
    
    with open(fname, "wb") as open_file:
        pickle.dump(data_in, open_file)

if __name__ == '__main__':
    seq = Nop("seq")
    expt_cal = seq_programs.get_expt_cal()
    
    #
    seq.comment = "rabi_ef, sweep wx amps"
    seq.num_patterns = 101
    seq.num_records_per_pattern = 200
    seq.num_avgs = 1
    seq.sweep_time = 2000
    seq.rabi_amp = 0.5
    seq.times = np.linspace(0., seq.sweep_time, seq.num_patterns)*1e-3
    #seq_experiments.rabi_ef_prep_f(seq.num_patterns, seq.sweep_time, seq.rabi_amp)
    
    #
    sweep = Nop("sweep")
    sweep.comment = "wx amps, ch1ch2"
    sweep.vals = np.linspace(0.1, 0.3, 2)
    sweep.num_steps = sweep.vals.size
    
    #
    sweep.p = []
    sweep.p_post = []
    for step_num, v in enumerate(sweep.vals):
        #
        print("\nstep_num: {}, sweep.val: {}".format(step_num, v))
        
        #
        amp = [v*1.5, v*1.77, 1.5, 1.5]
        wx_programs.wx_set_and_amplitude_and_offset(amp=amp)
    
        for k in range(seq.num_avgs):
            #
            daq_params, _, p = daq_programs.run_daq(
                num_patterns=seq.num_patterns, num_records_per_pattern=seq.num_records_per_pattern)
            if k is 0:
                p_readout = p
            else:
                p_readout += p
            
        p_readout = p_readout/seq.num_avgs
        p_post = analysis.p_readout_postselected(p_readout)
        sweep.p.append(p_readout)
        sweep.p_post.append(p_post)
        
    daq = Nop("daq")
    daq.daq_params = daq_params
    wx_programs.wx_set_and_amplitude_and_offset()
    
    sweep.p = np.array(sweep.p)
    sweep.p_post = np.array(sweep.p_post)
    
    #
    for p in sweep.p:
        daq_programs.make_readout_vs_patterns_plot(p)
        
    #
    sweep.fit = []
    for k in range(sweep.num_steps):
        #
        x = seq.times
        y = sweep.p_post[k][-1]
        plt.plot(x,y)
        plt.show()
        popt, perr, _, _ = analysis.fit_sine_decay(x, y, [0.5, 1, 0.5, 0, 0.5])            
        sweep.fit.append(popt)
        
    #
    sweep.fit = np.array(sweep.fit)
    sweep.rabi_freq = sweep.fit.T[0]
    sweep.rabi_gamma = sweep.fit.T[1]

    #
    plt.figure()
    plt.plot(sweep.vals, sweep.rabi_freq, 'k.')
    plt.ylabel("Rabi freq (MHz)")
    #
    plt.figure()
    plt.plot(sweep.vals, sweep.rabi_gamma, 'k.')
    plt.ylabel("Rabi decay, 1/T_Rabi (1/us)")
    
    #
    plt.show()
    
    #
#    save_by_pickle((seq, daq, sweep))


