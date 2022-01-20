# -*- coding: utf-8 -*-
"""
Created on Fri Jul  3 18:35:46 2020

@author: J. Monroe
"""
import numpy as np
import pyvisa
import dg535_control as dg_control

## prep insturments
rm = pyvisa.ResourceManager()
dg_535 = rm.open_resource('GPIB0::15::INSTR')

num_steps = 51
thresh = 120

decomp_seq = np.zeros(num_steps)

for step_num in range(num_steps):
    
    dg_control.rabi_seq(dg_535, step_num)
    dg_control.start_dg535(dg_535)
    alazar.get_buffers(300)
       
    dg_control.initialize_dg535(dg_535) ## turn off once we're done.
    
    ## process signal
    
    exp_z = np.sum( np.sign(alazar.data.I - thresh) )
    prob_gnd = 0.5*exp_z + 0.5 ## z=1 corresponds to gnd state
    
## Start dg535

## tell Alazar to get some buffers

