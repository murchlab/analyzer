# -*- coding: utf-8 -*-
"""
Created on Tue Jan  5 13:15:36 2021

@author: Crow108
"""

import sys
import numpy as np
import matplotlib.pyplot as plt

instrument_path = r"C:\Users\Crow108\Documents\Python\instr\analyzer"
if instrument_path not in sys.path: sys.path.append(instrument_path )
import bnc

analyzer_path = r"C:\Users\Crow108\Documents\Python\instr\python_interface\python_without_WX2184C"
if analyzer_path not in sys.path: sys.path.append(analyzer_path )
import daq_programs

target_bnc_address =  'USB0::0x03EB::0xAFFF::421-4385A0002-0784::INSTR'

def sweep_bnc_freq(start_freq, stop_freq, num_points):
    freq_list = np.linspace(start_freq, stop_freq, num_points)
    steps_in_seq = 51
    num_averages =500# 10000
    
    out_I, out_Q = np.zeros( (2, num_points, steps_in_seq))
    for i,freq in enumerate(freq_list):
        bnc.set_bnc_output(freq, bnc_addr=target_bnc_address)
    
        rec_avg_all, rec_readout, rec_avg_vs_pats = daq_programs.run_daq2(steps_in_seq, num_averages, verbose=0)
                
        out_I[i] = rec_avg_vs_pats[0]
        out_Q[i] = rec_avg_vs_pats[1]
        #time.sleep(4)
        
    # make plots
    plt.imshow(out_Q, extent=[0,steps_in_seq,stop_freq,start_freq],aspect='auto' )
        
    return out_Q
##END sweep_bnc_freq