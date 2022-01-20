# -*- coding: utf-8 -*-
"""
Created on Sat Jan 25 11:50:58 2020

@author: P. M. Harrington
"""

import numpy as np
import matplotlib.pyplot as plt

import expt_parameters
from daq_alazar import *
from daq_processing import *
import wx_programs
from Nop_class import Nop

def get_daq_parameters(num_patterns=None, num_records_per_pattern=None):
    daq_params = expt_parameters.get_daq_parameters()
    
    # number of patterns
    if num_patterns is None:
        daq_params.num_patterns = 51
    else:
        daq_params.num_patterns = num_patterns
        
    # number of repetitions for each pattern
    if num_records_per_pattern is None:
        daq_params.num_records_per_pattern = 50
    else:
        daq_params.num_records_per_pattern = num_records_per_pattern
    
    return daq_params

def run_daq(num_patterns=None, num_records_per_pattern=None):
    # get parameters: number of patterns, etc.
    daq_params = get_daq_parameters(num_patterns=num_patterns, 
                                    num_records_per_pattern=num_records_per_pattern)
    alazar_params = get_alazar_parameters(daq_params=daq_params)
    
    print("\nSetup Alazar configuration")
    board = ats.Board(systemId = 1, boardId = 1)
    configure_board(alazar_params, board)
    
    # setup wx to start at first pattern
    print("Initialize WX")
    wx_programs.wx_initialize()
    
    #
    print("Acquire data\n")
    (rec_avg_all, rec_readout) = acquire_data(daq_params, alazar_params, board)
    
    # reshape the records
    rec_readout_vs_pats = record_vs_patterns(daq_params, rec_readout)
    
    # average all repetitions for each pattern
    rec_avg_vs_pats_ch_a, rec_avg_vs_pats_ch_b = record_avg_vs_patterns(daq_params, rec_readout_vs_pats)
    
    # threshold the readout signal for every record (channel a)
    n_readout = threshold_record_averages(daq_params, signal_in=rec_readout[0])
    n_vs_pats, p_vs_pats = readout_vs_patterns(daq_params, n_readout)

    #
    bins, counts = make_iq_plot(rec_readout)

    #
    make_readout_vs_patterns_plot(p_vs_pats)
    
    return daq_params, rec_readout_vs_pats, p_vs_pats

def run_iq_vs_patterns(num_patterns=None, num_records_per_pattern=None):
    # get parameters: number of patterns, etc.
    daq_params = get_daq_parameters(num_patterns=num_patterns, 
                                    num_records_per_pattern=num_records_per_pattern)
    alazar_params = get_alazar_parameters(daq_params=daq_params)
    
    print("\nSetup Alazar configuration")
    board = ats.Board(systemId = 1, boardId = 1)
    configure_board(alazar_params, board)
    
    # setup wx to start at first pattern
    print("Initialize WX")
    wx_programs.wx_initialize()
    
    #
    print("Acquire data\n")
    (rec_avg_all, rec_readout) = acquire_data(daq_params, alazar_params, board)
    
    # reshape the records
    rec_readout_vs_pats = record_vs_patterns(daq_params, rec_readout)
        
    # make IQ plot for each pattern
    bins_cntr, counts = make_n_state_iq_plot(rec_readout_vs_pats)
#    fit_readout_histogram(rec_readout[0], bins_cntr[0], counts[0], num_gaussians=3)
    
    # average all repetitions for each pattern
    #rec_avg_vs_pats_ch_a, rec_avg_vs_pats_ch_b = record_avg_vs_patterns(daq_params, rec_readout_vs_pats)
    
    # threshold the readout signal for every record (channel a)
    n_readout = threshold_record_averages(daq_params, signal_in=rec_readout[0])
    n_vs_pats, p_vs_pats = readout_vs_patterns(daq_params, n_readout)
    make_readout_vs_patterns_plot(p_vs_pats)

    return daq_params, rec_readout_vs_pats, n_vs_pats, p_vs_pats, bins_cntr, counts

if __name__ == "__main__":
    pass
    