# -*- coding: utf-8 -*-
"""
Created on Wed Aug 26 10:20:06 2020

@author: Crow108
"""
import sys
controller_path = r"C:\Users\crow108\Documents\Python\controller"
if controller_path not in sys.path: sys.path.append(controller_path)
import proteusapi

def set_proteus_amplitude(amps=[1, 1, 1, 1], offsets=[0, 0, 0, 0]):
    for ch_index in range(4):
        pass
        proteusapi.SendScpi(f":INST:CHAN {ch_index+1}")
        proteusapi.SendScpi(f":VOLT {amps[ch_index]}")
        proteusapi.SendScpi(f":VOLT:OFFS {offsets[ch_index]}")
