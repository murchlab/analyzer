# -*- coding: utf-8 -*-
"""
Created on Sat Jan 25 11:50:58 2020

@author: P. M. Harrington
"""


import daq_alazar 
import daq_processing
import atsapi as ats 
import dg535_control
import numpy as np

class Nop():
    def __init__(self):
        self.name = None
        pass

def get_daq_parameters(num_patterns=None, num_records_per_pattern=None):
    daq_params = Nop()
    daq_params.iq_angle_deg = 0 # WARNING: nonzeros values significantly slow acquisition rate.
    daq_params.threshold = [130.5, 999]
    # note: daq_alazar sets the clock to 1000 MS/s
    daq_params.readout_start =  1000
    daq_params.readout_duration = 3500 #2000

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
    alazar_params = daq_alazar.get_alazar_parameters(daq_params=daq_params)
    
    print("\nSetup Alazar configuration")
    board = ats.Board(systemId = 1, boardId = 1)
    daq_alazar.configure_board(alazar_params, board)
    
    # setup wx to start at first pattern
    print("Initialize DG535")
    dg535_control.initialize_dg535()
    
    # 
    print("Acquire data\n")
    (rec_avg_all, rec_readout) = daq_alazar.acquire_data(daq_params, alazar_params, board)
    
    # reshape the records
    rec_readout_vs_pats = daq_processing.record_vs_patterns(daq_params, rec_readout)
    
    # average all repetitions for each pattern
    rec_avg_vs_pats_ch_a, rec_avg_vs_pats_ch_b = daq_processing.record_avg_vs_patterns(daq_params, rec_readout_vs_pats)
    
    # threshold the readout signal for every record (channel a)
    n_readout = daq_processing.threshold_record_averages(daq_params, signal_in=rec_readout[0])
    n_vs_pats, prob_vs_pats = daq_processing.readout_vs_patterns(daq_params, n_readout)

    #
    bins, counts = daq_processing.make_iq_plot(rec_readout)

    #
    daq_processing.make_readout_vs_patterns_plot(prob_vs_pats)
    
    #return daq_params, rec_readout_vs_pats, prob_vs_pats
    return prob_vs_pats

def run_iq_vs_patterns(num_patterns=None, num_records_per_pattern=None):
    # get parameters: number of patterns, etc.
    daq_params = get_daq_parameters(num_patterns=num_patterns, 
                                    num_records_per_pattern=num_records_per_pattern)
    alazar_params = daq_alazar.get_alazar_parameters(daq_params=daq_params)
    
    print("\nSetup Alazar configuration")
    board = ats.Board(systemId = 1, boardId = 1)
    daq_alazar.configure_board(alazar_params, board)
    
    # setup wx to start at first pattern
    print("Initialize DG535")
    dg535_control.initialize_dg535()
    
    #
    print("Acquire data\n")
    (rec_avg_all, rec_readout) = daq_alazar.acquire_data(daq_params, alazar_params, board)
    
    # reshape the records
    rec_readout_vs_pats = daq_processing.record_vs_patterns(daq_params, rec_readout)
        
    # make IQ plot for each pattern
    bins_cntr, counts = daq_processing.make_n_state_iq_plot(rec_readout_vs_pats)
#    fit_readout_histogram(rec_readout[0], bins_cntr[0], counts[0], num_gaussians=3)
    
    # average all repetitions for each pattern
    rec_avg_vs_pats_ch_a, rec_avg_vs_pats_ch_b = daq_processing.record_avg_vs_patterns(daq_params, rec_readout_vs_pats)
    
    # threshold the readout signal for every record (channel a)
    n_readout = daq_processing.threshold_record_averages(daq_params, signal_in=rec_readout[0])
    n_vs_pats, p_vs_pats = daq_processing.readout_vs_patterns(daq_params, n_readout)
    #daq_processing.make_readout_vs_patterns_plot(p_vs_pats)

    #return daq_params, rec_readout_vs_pats, n_vs_pats, p_vs_pats, bins_cntr, counts
    return rec_readout_vs_pats
##END run_daq
    

def run_daq2(num_patterns=None, num_records_per_pattern=None, verbose=True):
    # get parameters: number of patterns, etc.
    daq_params = get_daq_parameters(num_patterns=num_patterns, 
                                    num_records_per_pattern=num_records_per_pattern)
    alazar_params = daq_alazar.get_alazar_parameters(daq_params=daq_params, verbose=False)
    
    
    #print("\nTroubleshoot stuck at this step 1")
    board = ats.Board(systemId = 1, boardId = 1)
    #print("\nTroubleshoot stuck at this step 2")
    daq_alazar.configure_board(alazar_params, board)
    #print("\nTroubleshoot stuck at this step 3")
    (rec_avg_all, rec_readout) = daq_alazar.acquire_data(daq_params, alazar_params, board, verbose=False)
    #print("\nTroubleshoot stuck at this step 4")
    # reshape the records
    rec_readout_vs_pats = daq_processing.record_vs_patterns(daq_params, rec_readout)
    #print("\nTroubleshoot stuck at this step 5")
    # average all repetitions for each pattIern
    rec_avg_vs_pats_ch_a, rec_avg_vs_pats_ch_b = daq_processing.record_avg_vs_patterns(daq_params, rec_readout_vs_pats)
    #print("\nTroubleshoot stuck at this step 6")
    rec_avg_vs_pats = [ rec_avg_vs_pats_ch_a, rec_avg_vs_pats_ch_b]
    
    if verbose:
        pass
        bins, counts = daq_processing.make_iq_plot(rec_readout)
            
    return rec_avg_all, rec_readout, rec_avg_vs_pats
##END run_daq2


def run_daq3(num_patterns=None, num_records_per_pattern=None, verbose=True):
    # get parameters: number of patterns, etc.
    daq_params = get_daq_parameters(num_patterns=num_patterns, 
                                    num_records_per_pattern=num_records_per_pattern)
    alazar_params = daq_alazar.get_alazar_parameters(daq_params=daq_params,verbose=False)
    if verbose:
        print("\nSetup Alazar configuration")
    board = ats.Board(systemId = 1, boardId = 1)
    daq_alazar.configure_board(alazar_params, board)
    
   
    # setup wx to start at first pattern
    if verbose:
        print(" DO NOT Initialize DG535")
    #dg535_control.initialize_dg535()
    #dg535_control.set_state(0)
    
    # 
    if verbose:
        print("Acquire data\n")
    
#    dg535_control.always_on_seq(1)
#    dg535_control.single_pulse(0, verbose) ## turn qubit drive on.
    (rec_avg_all, rec_readout, temp) = daq_alazar.acquire_data2(daq_params, alazar_params, board, verbose=False)
    
#    dg535_control.single_pulse(0)
        
    return rec_avg_all, rec_readout, temp

if __name__ == "__main__":
    pass
    