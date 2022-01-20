# -*- coding: utf-8 -*-
"""
Created on Tue Mar  3 13:00:04 2020

@author: P. M. Harrington
"""

import numpy as np
import matplotlib.pyplot as plt
import pickle
import datetime

import seq_experiments
import seq_programs
import daq_programs
import analysis

import wx_programs
import keithley2401
#import hp_E4405B

class Nop():
    def __init__(self, name):
        self.name = name

def get_save_path():
    path0 = "C:\\Data\\2020\\ep_metrology\\data\\data_200303"
    time_str = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    save_path = path0 + time_str
    return save_path

def save_by_pickle(data_in):
    save_path = get_save_path()
    fname = save_path + ".pickle"
    print(fname)
    
    with open(fname, "wb") as open_file:
        pickle.dump(data_in, open_file)
    
if __name__ == '__main__':
    pass

    #
    seq = Nop("seq")
    seq.comment = "t1decay_ge"
    seq.num_patterns_each = 101
    seq.num_records_per_pattern = 500
    seq.sweep_time = 5000
    #seq_experiments.t1decay_ge(seq.num_patterns, seq.sweep_time)
    
    #
    keithley_current = Nop("keithley_current")
    keithley_current.num_steps = 41
    keithley_current.setpoint_mA = np.linspace(7.25, 7.35, keithley_current.num_steps)
    dum = np.full(keithley_current.num_steps, np.nan)
    keithley_current.msmt_mA_start = dum
    keithley_current.msmt_mA_end = dum
    
    t1decay = Nop("t1decay")
    t1decay.times = np.linspace(0.,seq.sweep_time, seq.num_patterns_each)*1e-3
    t1decay.freq = dum.copy()
    t1decay.gamma = dum.copy()
    t1decay.p = []
    
    #
    daq = Nop("daq")
    for k, bias_val in enumerate(keithley_current.setpoint_mA):
        mA_start, mA_end = keithley2401.set_current(bias_val)
        keithley_current.msmt_mA_start[k] = mA_start
        keithley_current.msmt_mA_end[k] = mA_end
        
        daq.daq_params, daq.rec_readout_vs_pats, daq.p_readout = (
                daq_programs.run_daq(num_patterns=seq.num_patterns_each, num_records_per_pattern=seq.num_records_per_pattern))
        t1decay.p.append(daq.p_readout[0])
        
    #
    keithley_current.msmt_mA_end = np.array(keithley_current.msmt_mA_end)
    t1decay.p = np.array(t1decay.p)
    
    #
    t1decay.fit = []
    for k in range(keithley_current.num_steps):
        #.
        popt, perr, _, _ = analysis.fit_exp_decay(t1decay.times, t1decay.p[k])
        t1decay.fit.append(popt)

    #
    t1decay.fit = np.array(t1decay.fit)
    t1decay.gamma = t1decay.fit.T[1]

    #
    plt.figure()
    plt.plot(keithley_current.msmt_mA_end, t1decay.gamma)
    plt.ylabel("T1 decay, 1/T1 (1/us)")
    #
    plt.figure()
    t1 = t1decay.gamma
    plt.plot(keithley_current.msmt_mA_end, t1)

    #
    plt.show()
    
    #
    save_by_pickle((seq, daq, keithley_current, t1decay))