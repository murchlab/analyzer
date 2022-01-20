# -*- coding: utf-8 -*-
"""
Created on Sat Feb  1 16:03:32 2020

@author: crow104
"""

# -*- coding: utf-8 -*-
"""
Created on Mon Jan 27 20:04:05 2020

@author: P. M. Harrington
"""

import numpy as np
import matplotlib.pyplot as plt
import time

import seq_experiments as seq
#import daq_programs
import daq_processing

import wx_programs
import hp_E4405B

# index +75 for a 400 MHz span with 401 points
idx_lo = 200-80
idx_hi = 200+80

def mixer_orthogonality():
    # mixer orthogonality
    # 103.
    angle_sweep = np.linspace(90., 92., 6)
    
    #
    sa_dbm = []
    for k, ang in enumerate(angle_sweep):
        print(k)
        seq.calibrate_mixer_ch1ch2(ang)
        time.sleep(1.)
        x, y = hp_E4405B.get_trace()
        sa = [y[idx_lo], y[idx_hi]]
        sa_dbm.append(sa)
        
        plt.plot(x, y)
        plt.show()
        print("{}, {}, {}".format(ang, sa[0], sa[1]))
        
    plt.plot(angle_sweep, np.vstack(sa_dbm).T[0])
    plt.show()
    plt.plot(angle_sweep, np.vstack(sa_dbm).T[1])
    plt.show()
    
def ch2_amp(mixer_orthog_deg = 90.):
    
    #
#    seq.calibrate_mixer_ch1ch2(mixer_orthog_deg)

    #
    amp_sweep = np.linspace(1.2, 1.8, 21)

    #
    sa_dbm = []
    for amp in amp_sweep:
        #
        wx_programs.wx_set_and_amplitude_and_offset(amp=[1.5, amp, 1.5, 1.5])
        time.sleep(0.25)
        
        #
        x, y = hp_E4405B.get_trace()
        sa = [y[idx_lo], y[idx_hi]]
        sa_dbm.append(sa)
        
        #
        plt.plot(x, y)
        plt.show()
        print("{}, {}, {}".format(amp, sa[0], sa[1]))
        
    plt.plot(amp_sweep, np.vstack(sa_dbm).T[0])
    plt.show()
    plt.plot(amp_sweep, np.vstack(sa_dbm).T[1])
    plt.show()
    
def null_carrier_leakage(mixer_orthog_deg=90., channel=3):
    
    #
    #seq.calibrate_mixer_ch1ch2(mixer_orthog_deg)

    #
    if channel==3:
        amp_sweep = np.linspace(0.010, 0.020, 11)
    elif channel==4:
        amp_sweep = np.linspace(-0.073, -0.069, 11)
        
    amp_a = 0.019
    amp_b = -0.0722
    
    #
    sa_dbm = []
    for amp in amp_sweep:
        #
        #[0., 0., +0.046, -0.049]
        if channel==3:
            wx_programs.wx_set_and_amplitude_and_offset(offset=[0., 0., amp, amp_b])
        elif channel==4:
            wx_programs.wx_set_and_amplitude_and_offset(offset=[0., 0., amp_a, amp])
            
        time.sleep(0.1)
        
        #
        x, y = hp_E4405B.get_trace()
        sa = y[200]
        sa_dbm.append(sa)
        
        #
#        plt.plot(x, y)
#        plt.show()
        print("{} V, {} dBm".format(amp, sa))
        
    plt.plot(amp_sweep, sa_dbm)
    plt.show()
    
    fit, _ = daq_processing.fit_parabola(amp_sweep, sa_dbm)
    print("min (val): {}".format(amp_sweep[sa_dbm.index(min(sa_dbm))]))
    print("min (fit): {}".format(-fit[0][1]/(2*fit[0][0])))
    
    return amp_sweep, sa_dbm
    
if __name__ == '__main__':
    pass