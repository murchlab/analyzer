# -*- coding: utf-8 -*-
"""
Created on Sat Feb  1 15:14:44 2020

@author: P. M. Harrington
"""

import numpy as np
import pyvisa
import matplotlib.pyplot as plt 

address = "GPIB0::18::INSTR"

def get_trace():
    inst = pyvisa.ResourceManager().open_resource(address)
    
    #print(inst.query(':INST?'))
    inst.write(':INIT;')
    freq_str = inst.query(':FREQ:STAR?;:FREQ:STOP?')
    sa_vals = inst.query_binary_values(':FORM REAL,64;:TRAC? TRACE1;', datatype='d', is_big_endian=True)
    #print(inst.query(':SYST:ERR?'))
    inst.close()
    
    #
    freq = [float(freq_str[0:19]), float(freq_str[20:-1])]
    #print('Frequency range (GHz):\n{},{}'.format(1e-9*freq[0], 1e-9*freq[1]))
    
    sa_freq = np.linspace(freq[0], freq[1], len(sa_vals))
    
    return sa_freq, sa_vals
if __name__=="__main__":
    pass