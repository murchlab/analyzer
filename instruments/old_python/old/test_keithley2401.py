# -*- coding: utf-8 -*-
"""
Created on Tue Mar  3 11:02:02 2020

@author: crow104
"""

import numpy as np
import matplotlib.pyplot as plt
import time

import seq_experiments as seq
import seq_programs
import daq_programs
import analysis

import wx_programs
import keithley2401

class Nop():
    pass

if __name__ == '__main__':
    pass

    keithley_current = Nop()
    keithley_current.num_steps = 21
    keithley_current.setpoint_mA = np.linspace(7.35, 7.40, keithley_current.num_steps)
    dum = np.full(keithley_current.num_steps, np.nan)
    keithley_current.msmt_mA_start = dum
    keithley_current.msmt_mA_end = dum

    
    for k, bias_val in enumerate(keithley_current.setpoint_mA):
        mA_start, mA_end = keithley2401.set_current(bias_val)
        print("\n step")
        keithley_current.msmt_mA_start[k] = mA_start
        keithley_current.msmt_mA_end[k] = mA_end

    #
    keithley_current.msmt_mA_end = np.array(keithley_current.msmt_mA_end)

    #
    plt.figure()
    plt.plot(keithley_current.setpoint_mA, keithley_current.msmt_mA_start,'.')
    plt.figure()
    plt.plot(keithley_current.setpoint_mA, keithley_current.msmt_mA_end,'.')
    plt.show()