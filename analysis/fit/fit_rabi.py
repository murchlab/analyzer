# -*- coding: utf-8 -*-
"""
Created on Fri Feb 12 15:29:18 2021

@author: Crow108
"""

import numpy as np
#import daq_programs
import matplotlib.pyplot as plt

from scipy.optimize import curve_fit

def objective_rabi(x, a, b, c, d):
	return a + (b*np.sin(2*np.pi*c*x+d))

def fit_rabi(y,t = 301):
    x_data = np.linspace(0,t,51)
    y_data = y
    initial  = [121.4,0.2,0.002,1.57]
    popt, _ = curve_fit(objective_rabi, x_data, y_data, p0 = initial)
    a, b , c, d= popt
    plt.plot(x_data,objective_rabi(x_data,a,b,c,d))
    plt.plot(x_data,y_data)
    plt.show()
    return 1.0/(2.0*c)

    