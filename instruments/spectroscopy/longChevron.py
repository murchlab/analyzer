# -*- coding: utf-8 -*-
"""
Created on Wed Jan  6 18:20:30 2021

@author: CGDVK
"""

import chevron
import dg535_control


clocks = [1000, 2000, 5000, 10000]

for i, clock in enumerate(clocks):
    dg535_control.set_rep_rate(clock)
    
    for j in range (11):
        try:
           _ = chevron.sweep_bnc_freq(3.75+(j*0.020),3.77+(j*0.020),21)
        except Exception as e:
           if "ApiPllNotLocked" in str(e) : 
               _ = chevron.sweep_bnc_freq(3.75+(j*0.020),3.77+(j*0.020),21)
        plt.show()
    print(clock)
    
