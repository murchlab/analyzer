# -*- coding: utf-8 -*-
"""
Created on Mon May  3 14:56:33 2021

@author: Kaiwen Zheng
"""

import numpy as np
#import daq_programs
import matplotlib.pyplot as plt
import time

from scipy.optimize import curve_fit

def objective_T2(x, a, b, c, d):
	return a + (b*np.exp(-x/c))*sin(d*x)

def fit_T2(y,t = 300):
    x_data = np.linspace(0,t,51)
    y_data = y
    initial  = [118,2,5,2]
    popt, _ = curve_fit(objective_T1, x_data, y_data, p0 = initial)
    a, b , c= popt
    plt.plot(x_data,objective_T1(x_data,a,b,c))
    plt.plot(x_data,y_data)
    plt.show()
    return c

def T1_loop(hrs = 1.0, t = 300 , avg = 800):
    s = 600 # sleep time in s
    runs =  (hrs*60*60)//s; runs = int(runs)
    T1_list = np.zeros((runs)) 
    
    for i in range (runs):
        try:
            rec_avg_all, rec_readout, rec_avg_vs_pats = daq_programs.run_daq2(51, avg, verbose=0)
        except Exception as e:
            if "ApiPllNotLocked" in str(e) : 
                rec_avg_all, rec_readout, rec_avg_vs_pats = daq_programs.run_daq2(51, avg, verbose=0)
        T1_list[i] = fit(rec_avg_vs_pats[1],t)
        time.sleep(s)
        
    plt.plot(np.linspace(0,hrs,runs),T1_list)
    return T1_list
         

