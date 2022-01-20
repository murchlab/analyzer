# -*- coding: utf-8 -*-
"""
Created on Fri Jan 31 11:23:50 2020

@author: P. M. Harrington
"""

import numpy as np
import pyvisa
import matplotlib.pyplot as plt
import time

address = "GPIB0::24::INSTR"
rm = pyvisa.ResourceManager()
inst = pyvisa.ResourceManager().open_resource(address)

#inst.write(":SYST:BEEP:STAT OFF")

def set_current(set_value_mA, step_size_mA=0.001):
    value_stop = 1e-3*set_value_mA
    value_start = measure_current() #np.round(measure_current(), 3+2)
    num_steps = int(np.ceil(abs((value_stop-value_start)/(1e-3*step_size_mA))))
    value_sweep = np.linspace(value_start, value_stop, num_steps)
    
    #
    for v in value_sweep:
        str_cmd = "SOUR:FUNC CURR;:SOUR:CURR "+"{}".format(v)+";:VOLT:PROT 0.100000;"
        inst.write(str_cmd)
        
    mA_start = 1e3*value_start
    mA_end = 1e3*measure_current()
    
    return mA_start, mA_end
        
def measure_current():
    inst.write(':SENS:FUNC "CURR"')
    vals = inst.query_ascii_values(":READ?")

    value = vals[1]
    print("Keithley current: {:.5f} mA".format(1e3*value))
    
    return value
    
if __name__=="__main__":
    pass