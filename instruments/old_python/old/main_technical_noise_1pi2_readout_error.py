# -*- coding: utf-8 -*-
"""
Created on Mon Jan 27 20:04:05 2020

@author: P. M. Harrington
"""

import numpy as np
import matplotlib.pyplot as plt
import time

import seq_experiments as seq
import seq_programs
import daq_programs
import daq_processing

if __name__ == '__main__':
    
    #seq.nopi_1pi2_pi_ge()
    #daq_params, rec_readout_vs_pats, n_readout = daq_programs.run_iq_vs_patterns(num_patterns=1, num_records_per_pattern=100000)
    
    num_chuncks = 20
    rec_idx = 0

    p_avg_vs_num_samples = []
    p_std_vs_num_samples = []
    num_samples_array = np.arange(100, 5001, 500)
    n_prev = 0
    for num_reps in num_samples_array:
        print("num_samples: {}".format(n))
        print("num_chuncks: {}".format(num_chuncks))
        print("num_reps: {}".format(num_chuncks*n))
        
        daq_params, rec_readout_vs_pats, n_readout, p_readout = daq_programs.run_iq_vs_patterns(num_patterns=1, num_records_per_pattern=num_chuncks*num_reps)
        rec_vs_pats = rec_readout_vs_pats[0].T
        cnts_vs_pats = n_readout.T

#        plt.figure()
#        for r in rec_vs_pats:
#            plt.plot(r)
#        plt.show()
        
        rec = rec_vs_pats[rec_idx]
        
        cnt_g = n_readout.T[rec_idx].T[0]
        cnt_e = n_readout.T[rec_idx].T[1]
        cnt_f = n_readout.T[rec_idx].T[2]
        
        rec_chuncks = rec.reshape((num_reps, num_chuncks))
        cnt_chuncks_g = cnt_g.reshape((num_chuncks, num_reps))
        cnt_chuncks_e = cnt_e.reshape((num_chuncks, num_reps))
        cnt_chuncks_f = cnt_f.reshape((num_chuncks, num_reps))
        
        p_avg_chunck = []
        for cnt in cnt_chuncks_g:
            p_avg_chunck.append(np.mean(cnt))
            #p_std_chunck.append(np.std(cnt)/np.sqrt(cnt.size))

        p_avg_chunck = np.array(p_avg_chunck)
        p_avg_vs_num_samples.append(p_avg_chunck)
    
    p_avg_vs_num_samples = np.array(p_avg_vs_num_samples)
    
    plt.plot(num_samples_array,p_avg_vs_num_samples)
    
    p = np.mean(p_avg_vs_num_samples[-1])
    p_std_vs_num_samples_theory = np.sqrt(p*(1-p)/num_samples_array)
    
    p_std_vs_num_samples = []
    for p in p_avg_vs_num_samples:
        p_std_vs_num_samples.append(np.std(p))
        
    p_std_vs_num_samples = np.array(p_std_vs_num_samples)
    
    plt.figure()
    plt.plot(num_samples_array, p_std_vs_num_samples)
    plt.plot(num_samples_array, p_std_vs_num_samples_theory)
    
#    np.random.shuffle(cnt_e)
#    
#    p_avg_vs_num_samples = []
#    p_std_vs_num_samples = []
#    num_samples_array = np.arange(10,cnt_g.size,200)
#    for k in num_samples_array:
#        cnt = cnt_g[:k]
#        p_avg_vs_num_samples.append(np.mean(cnt))
#        p_std_vs_num_samples.append(np.std(cnt)/np.sqrt(cnt.size))
#    p_avg_vs_num_samples = np.array(p_avg_vs_num_samples)
#    p_std_vs_num_samples = np.array(p_std_vs_num_samples)
#    
#    p = p_avg_vs_num_samples[-1]
#    std_err_theory = np.sqrt(p*(1-p)/num_samples_array)
#    
#    #
#    plt.figure()
#    plt.plot(num_samples_array, p_avg_vs_num_samples)
#    plt.ylim(0, 1)

#    #
#    plt.figure()
#    plt.plot(num_samples_array, p_std_vs_num_samples)
#    plt.plot(num_samples_array,std_err_theory)
    
#    #
#    plt.figure()
#    plt.plot(num_samples_array, p_std_vs_num_samples,'k.')
#    plt.plot(num_samples_array,std_err_theory)
#    plt.yscale('log')
#    
#    #
#    plt.figure()
#    plt.plot(num_samples_array, p_std_vs_num_samples/std_err_theory-1)
#    plt.yscale('log')
    
    
#    # calc theoretical avg probability given the std dev
##    p_theory_from_std = 0.5 + np.sqrt(1-4*np.sqrt(num_samples_array)*p_std_vs_num_samples)
#    plt.figure()
#    plt.plot(4*np.sqrt(num_samples_array)*p_std_vs_num_samples)
    
#    chunck_size = 50
#    rec_chuncks = rec.reshape((chunck_size,rec.size//chunck_size))
#    cnt_chuncks_g = cnt_g.reshape((chunck_size,rec.size//chunck_size))
#    cnt_chuncks_e = cnt_e.reshape((chunck_size,rec.size//chunck_size))
#    cnt_chuncks_f = cnt_f.reshape((chunck_size,rec.size//chunck_size))
#    
#    for cnt in cnt_chuncks_g:
#        p_avg = np.mean(cnt)
#        p_std = np.std(cnt)
#        
        
#    np.mean(cnt_chuncks_g, axis=0)
    
#    cnt_gnd = 0
#    cnt_exc = 0
#    for cnt in cnts_vs_pats[rec_idx]:
#        if cnt[2]==1:
#            continue
#        elif cnt[1]==1:
#            cnt_exc += 1
#        elif cnt[0]==1:
#            cnt_gnd += 1
    
#    plt.figure()
#    power_spectrum = abs(np.fft.fft(rec[rec_idx]))**2
#    plt.plot(power_spectrum,'.')
#    plt.yscale('log')
#    
#    plt.figure()
#    power_spectrum = abs(np.fft.fft(n_readout[rec_idx]))**2
#    plt.plot(power_spectrum,'.')
#    plt.yscale('log')
#
#    z = np.zeros((1,rec_chuncks.shape[1]))
#    r_chunck_fft_avg = z + 1j*z
#    for r in rec_chuncks:
#        r_chunck_fft_avg += np.fft.fft(r)/rec_chuncks.shape[0]
#        
#    r_chunck_power_spectrum = abs(r_chunck_fft_avg.T)**2
#    plt.plot(r_chunck_power_spectrum,'.')
#    plt.yscale('log')