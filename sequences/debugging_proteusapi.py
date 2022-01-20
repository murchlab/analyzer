# -*- coding: utf-8 -*-
"""
Created on Fri Aug 28 14:06:17 2020

@author: Crow108
"""

import os
import sys
import numpy as np
import matplotlib.pyplot as plt
import time
import tewx
sys.path.append(r"C:\Users\Crow108\Documents\Python\controller")

import proteusapi

num_steps = 21
#proteusapi.loadTaskTable(21)
for ch_index in range(4):
    proteusapi.SendScpi(":INST:CHAN {}".format(ch_index+1))
    
    proteusapi.SendScpi(":TASK:SEL {}".format(1))
    proteusapi.SendScpi(":TASK:DEF:NEXT1 {}".format(2))
#    proteusapi.SendScpi(":TASK:SEL {}".format(1))
#    proteusapi.SendScpi(":TASK:DEF:NEXT1 {}".format(2))