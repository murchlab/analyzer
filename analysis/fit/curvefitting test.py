# -*- coding: utf-8 -*-
"""
Created on Fri Feb 12 15:29:18 2021

@author: Crow108
"""

import sys
import numpy as np
import daq_programs
import time
from scipy.optimize import curve_fit

def objective(x, a, b, c, d):
	return a + (b*np.sin(2*np.pi*c*x+d))

def fit(y,time = 151):
    x_data = np.linspace(0,time,51)
    y_data = y
    initial  = [116,2,0.025,1]
    popt, _ = curve_fit(objective, x_data, y_data, p0 = initial)
    a, b , c, d= popt
    plt.plot(x_data,objective(x_data,a,b,c,d))
    plt.plot(x_data,y_data)
    plt.show()
    return 1.0/(2.0*c)

    