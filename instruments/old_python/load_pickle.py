# -*- coding: utf-8 -*-
"""
Created on Tue Mar  3 17:24:13 2020

@author: P. M. Harrington, 03 March 2020
"""

import pickle
import daq_programs

fname = "C:\\Data\\2020\\ep_metrology\\data\\data_200303\\20200304_080823.pickle"
with open(fname, "rb") as open_file:    
    x = pickle.load(open_file)
    print(x)
    
    plt.figure()
    for idx, y in enumerate(x[2].p_post):
        if idx>50:
            plt.plot(y[2])
            plt.ylim([0,1])
        
    plt.show()
    
    y = []
    for p in x[2].p_post:
        y.append(p[2])
    y = np.array(y)
    #
    plt.figure()
    plt.imshow(y, aspect='auto')

    y = []
    for p in x[2].p:
        y.append(p[0])
    y = np.array(y)
    #
    plt.figure()
    plt.imshow(y, aspect='auto')
    