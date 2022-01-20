# -*- coding: utf-8 -*-
"""
Created on Tue Jan 28 14:46:15 2020

@author: P. M. Harrington
"""

import numpy as np
import matplotlib.pyplot as plt
from daq_alazar import *
from daq_processing import *
import wx_programs

class Nop():
    pass

def get_daq_parameters():
    daq_params = Nop()

    #
    daq_params.save_name = "readout"
    
    #
    daq_params.num_patterns = 3 #2*51+3
    daq_params.num_records_per_pattern = 3000
    
    daq_params.iq_angle_deg = -53.13 + 180
    daq_params.threshold = [-155, np.inf]

    # note: daq_alazar sets the clock to 250 MS/s
    daq_params.readout_start = 348 #1100
    daq_params.readout_duration = 120 #1000
    
    return daq_params

if __name__ == "__main__":
    # get parameters: number of patterns, etc.
    daq_params = get_daq_parameters()
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
    
    record_avg_channel_a = rec_readout[0]
    record_avg_channel_b = rec_readout[1]
    all_rec_avg_ch_a = rec_avg_all[0]
    all_rec_avg_ch_b = rec_avg_all[1]
    
    # reshape the records
    rec_readout_vs_pats = record_vs_patterns(daq_params, rec_readout)
    rec_vs_pats_ch_a = rec_readout_vs_pats[0]
    rec_vs_pats_ch_b = rec_readout_vs_pats[1]
    
    # average all repetitions for each pattern
    rec_avg_vs_pats_ch_a, rec_avg_vs_pats_ch_b = record_avg_vs_patterns(daq_params, rec_vs_pats_ch_a, rec_vs_pats_ch_b)
    
    # threshold the readout signal for every record
    n_readout = threshold_record_averages(daq_params, signal_in=record_avg_channel_a)
    p_readout = p_readout_vs_patterns(daq_params, n_readout)
    p_readout_post = p_readout_post_vs_patterns(p_readout)
    
    #
    make_all_record_average_plots(all_rec_avg_ch_a, all_rec_avg_ch_b)
    
    #
    make_avg_record_vs_patterns_plot(rec_avg_vs_pats_ch_a, rec_avg_vs_pats_ch_b)
    
    #
    make_readout_vs_patterns_plot(p_readout)
    save_csv(daq_params.save_name+"_p_readout", p_readout)
    
    # create readout histograms
    bins_cntr, counts = make_readout_histogram_for_each_pattern(rec_vs_pats=rec_vs_pats_ch_a)
    
    
    