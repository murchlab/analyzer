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
    path0 = "C:\\Data\\2020\\ep_metrology\\data\\data_200303"
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
    seq.comment = "rabi_ge, sweep wx amps"
    seq.num_patterns = 101
    seq.num_records_per_pattern = 200
    seq.sweep_time = 1000
    seq.times = np.linspace(0., seq.sweep_time, seq.num_patterns)*1e-3
    #seq_experiments.rabi_ge(seq.num_patterns, seq.sweep_time)
    
    #
    sweep = Nop("sweep")
    sweep.comment = "wx amps, ch1ch2"
    sweep.vals = np.linspace(0.1, 1.1, 21)
    sweep.num_steps = sweep.vals.size
    
    #
    daq = Nop("daq")
    sweep.p = []
    for step_num, v in enumerate(sweep.vals):
        #
        print("\nstep_num: {}".format(step_num))
        
        #
        amp = [v*1.5, v*1.77, 1.5, 1.5]
        wx_programs.wx_set_and_amplitude_and_offset(amp=amp)
    
        #
        daq.daq_params, daq.rec_readout_vs_pats, daq.p_readout = daq_programs.run_daq(
                num_patterns=seq.num_patterns, num_records_per_pattern=seq.num_records_per_pattern)
        sweep.p.append(daq.p_readout)
        
    wx_programs.wx_set_and_amplitude_and_offset()
    
    sweep.p = np.array(sweep.p)
    
    #
    sweep.fit = []
    for k in range(sweep.num_steps):
        #.
        popt, perr, _, _ = analysis.fit_sine_decay(seq.times, sweep.p[k][0])
        sweep.fit.append(popt)

    #
    sweep.fit = np.array(sweep.fit)
    sweep.rabi_freq = sweep.fit.T[0]
    sweep.rabi_gamma = sweep.fit.T[1]

    #
    plt.figure()
    plt.plot(sweep.vals, sweep.rabi_freq)
    plt.ylabel("Rabi freq (MHz)")
    #
    plt.figure()
    plt.plot(sweep.vals, sweep.rabi_gamma)
    plt.ylabel("Rabi decay, 1/T_Rabi (1/us)")

#
    popt, perr, _, _ = analysis.fit_line(sweep.vals, sweep.rabi_freq)
    
    #
    plt.show()
    
#    times = np.linspace(0., seq.sweep_time, seq.num_patterns)*1e-3
#    plt.plot(times, p_readout[0])
#    popt, perr, _, _ = analysis.fit_sine_decay(times, p_readout[0])
#    #
#    print("pi_time from fit (ns): {}".format(1e3*0.5/popt[0]))
#    expt_cal = seq_programs.get_expt_cal()
#    print("pi_time is expt_cal (ns): {}".format(expt_cal.pi_time.ge))
    
    wx_programs.wx_set_and_amplitude_and_offset()
    save_by_pickle((seq, daq, sweep))


