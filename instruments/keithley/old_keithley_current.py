# -*- coding: utf-8 -*-
"""
Created on Wed Feb 12 11:50:10 2020

@author: J. Monroe
"""

'''
Set source output level
Set continuous measurement mode

'''
import numpy as np
import time

def set_level(current_source_handle, target_current_A, current_step_A=1e-6):
    ## ramps to a target current by small steps
    ## small steps are required to avoid trapping flux in 
    current_source_handle.write("sour:curr?")
    current_level_A = float( current_source_handle.read() )
    num_steps = abs(target_current_A - current_level_A)/current_step_A;
    
    step_list = np.linspace(current_level_A, target_current_A, num_steps+1)
    for level in step_list:
        current_source_handle.write("sour:curr {}".format(level))
        time.sleep(0.1) # wait 100 ms for current to stabilize
##END set_level