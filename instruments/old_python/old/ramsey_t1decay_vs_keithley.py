# -*- coding: utf-8 -*-
"""
Created on Tue Mar  3 22:15:16 2020

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

#def make_readme(parameters):
#    paths = parameters.paths
#    
#    paths.readme = paths.parent + "/" + "readme.txt"
#    if (not os.path.exists(paths.readme)):
#        file = open(paths.readme, "w") 
#    else:
#        file = open(paths.readme, "a")
#        file.write("\n\n")
#    
#    p = parameters        
#    file.write("# " + p.label + "\n")
#    file.write(p.time_start.strftime("%Y%m%d_%H%M%S"))
#    file.write("\nboundary, {}".format(p.boundary))
#    file.write("\nN, {}".format(p.N))
#    file.write("\nJ, {}".format(p.J))
#    file.close()
    
    
if __name__ == '__main__':
    pass

#    # ramsey & t1decay, ge
#    num_patterns_each = 51
#    sweep_time_ramsey = 2500
#    sweep_time_t1decay = 5000
#    seq.ramsey_ge_t1decay_ge(num_patterns_each, sweep_time_ramsey, sweep_time_t1decay)
#    times_ramsey = np.linspace(0.,sweep_time_ramsey, num_patterns_each)*1e-3
#    times_t1decay = np.linspace(0.,sweep_time_t1decay, num_patterns_each)*1e-3
#    daq_params, rec_readout_vs_pats, p_readout = daq_programs.run_daq(num_patterns=2*num_patterns_each, num_records_per_pattern=500)
#    p_ramsey = p_readout[0][:num_patterns_each]
#    p_t1decay = p_readout[0][num_patterns_each:]    
#    popt, _ = analysis.fit_sine_decay(times_ramsey, p_ramsey)
#    fit_t1decay, _ = analysis.fit_exp_decay(times_t1decay, p_t1decay)
#    print("\nT2*: {}".format(1/popt[0][1]))
#    print("T1: {}".format(1/fit_t1decay[0][1]))
    
    # ramsey & t1decay, ge
    seq = Nop("seq")
    seq.comment = "ramsey & t1decay, ge"
    seq.num_patterns_each = 101
    seq.sweep_time_ramsey = 1000
    seq.sweep_time_t1decay = 5000
    seq.num_records_per_pattern = 200
    
    keithley_current = Nop("keithley_current")
    keithley_current.num_steps = 25
    keithley_current.setpoint_mA = np.linspace(7.29, 7.35, keithley_current.num_steps)
    dum = np.full(keithley_current.num_steps, np.nan)
    keithley_current.msmt_mA_start = dum
    keithley_current.msmt_mA_end = dum
    #seq.ramsey_ge_t1decay_ge(num_patterns_each, sweep_time_ramsey, sweep_time_t1decay)
    
    #
    ramsey = Nop("ramsey")
    ramsey.times = np.linspace(0.,seq.sweep_time_ramsey, seq.num_patterns_each)*1e-3
    ramsey.freq = dum.copy()
    ramsey.gamma = dum.copy()
    ramsey.p = []
    
    t1decay = Nop("t1decay")
    t1decay.times = np.linspace(0.,seq.sweep_time_t1decay, seq.num_patterns_each)*1e-3
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
                daq_programs.run_daq(num_patterns=2*seq.num_patterns_each, num_records_per_pattern=seq.num_records_per_pattern))
        ramsey.p.append(daq.p_readout[0][:seq.num_patterns_each])
        t1decay.p.append(daq.p_readout[0][seq.num_patterns_each:])
        
    #
    keithley_current.msmt_mA_end = np.array(keithley_current.msmt_mA_end)
    ramsey.p = np.array(ramsey.p)
    t1decay.p = np.array(t1decay.p)
    
    #
    ramsey.fit= []
    t1decay.fit = []
    for k in range(keithley_current.num_steps):
        #
        popt, perr, _, _ = analysis.fit_sine_decay(ramsey.times, ramsey.p[k])
        ramsey.fit.append(popt)
        #.
        popt, perr, _, _ = analysis.fit_exp_decay(t1decay.times, t1decay.p[k])
        t1decay.fit.append(popt)
        
    #
    ramsey.fit = np.array(ramsey.fit)
    ramsey.freq = ramsey.fit.T[0]
    ramsey.gamma = ramsey.fit.T[1]
    #
    t1decay.fit = np.array(t1decay.fit)
    t1decay.gamma = t1decay.fit.T[1]
    
#    keithley_current.msmt_mA_end = keithley_current.setpoint_mA
    
    plt.figure()
    plt.plot(keithley_current.msmt_mA_end, ramsey.gamma)
    plt.ylabel("Ramsey, 1/T2* (1/us)")
    #
    plt.figure()
    plt.plot(keithley_current.msmt_mA_end, ramsey.freq)
    plt.ylabel("Ramsey, frequency (MHz)")
    #
    plt.figure()
    plt.plot(keithley_current.msmt_mA_end, t1decay.gamma)
    plt.ylabel("T1 decay, 1/T1 (1/us)")
    #
    plt.figure()
    t2s = ramsey.gamma
    t1 = t1decay.gamma
    plt.plot(keithley_current.msmt_mA_end, t2s/(2*t1))
    plt.ylabel("t2*/(2t1)")
    #
    plt.figure()
    t2_pure = 1/(ramsey.gamma - 0.5*t1decay.gamma)
    plt.plot(keithley_current.msmt_mA_end, t2_pure)
    plt.ylabel("t2 pure dephasing")
    
    #
    plt.show()
    
    #
    save_by_pickle((seq, daq, keithley_current, ramsey, t1decay))
    
#    with open(fname, "rb") as open_file:    
#        x = pickle.load(open_file)
#        print(x)