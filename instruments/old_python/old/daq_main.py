# -*- coding: utf-8 -*-
"""
Created on Fri Jan 31 11:22:12 2020

@author: P. M. Harrington
"""

import numpy as np
import daq_programs
import daq_processing
import keithley2401
import matplotlib.pyplot as plt

if __name__ == "__main__":
#    freq_sweep = []
#    gamma_sweep = []
#    current_sweep = np.linspace(7.20, 7.25, 6)
#    
#    for val_mA in current_sweep:
#        keithley2401.set_current(val_mA)
#        daq_params, rec_readout_vs_pats, p_readout = daq_programs.run_daq();
#        times = np.linspace(0, 0.5, daq_params.num_patterns)
#        fit, y_vals = daq_processing.fit_sine_decay(times, p_readout[1])
#        freq_sweep.append(fit[0][0])
#        gamma_sweep.append(fit[0][1])
    
#    plt.figure(figsize=(6,4))
#    plt.plot(current_sweep, freq_sweep)
#    plt.show()
#    
#    plt.figure(figsize=(6,4))
#    plt.plot(current_sweep, gamma_sweep)
#    plt.show()
#    
    
    daq_params, rec_readout_vs_pats, p_readout = daq_programs.run_daq();
    times = np.linspace(0, 1.0, daq_params.num_patterns)
    fit, y_vals = daq_processing.fit_sine_decay(times, p_readout[2])