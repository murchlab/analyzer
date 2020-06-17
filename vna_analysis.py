# -*- coding: utf-8 -*-
"""
Created on Wed Feb 12 10:47:41 2020

@author: J. Monroe
@date: Feb 12, 2020
"""
import numpy as np
import time

class Smith_data():
    
    def __init__(self, vna_smith_data, f_min=None, f_max=None):
        self.real = np.array( vna_smith_data[0::2] )
        num_points = self.real.size
        self.imag = np.array( vna_smith_data[1::2] )
        self.lin_mag = np.sqrt(self.real**2 + self.imag**2)
        self.log_mag = 20*np.log10( self.lin_mag)
        # arctan2 chooses the quadrant based on the sign of each step
        self.wrapped_phase = np.arctan2(self.imag, self.real)
        
        ## unwrap the phase
        unwrapped = np.unwrap(self.wrapped_phase)
        # a quick linear fit to subtract off electrical delay. 
        # calculating physical ED requires frequency information. I'll instead
        #   keep this function robust.    
        xs = np.arange(num_points)
        # solve y = mx +b as  y = A.f where A is Nx2 with x as first  column and 
        # ones as second column f is 2x1 of coefficients m and b.
        # fit by minimizing (data-A.f)^2
        A_mat = np.array([xs, np.ones(xs.shape)]).T
        m, b = np.linalg.lstsq(A_mat, unwrapped, rcond=None)[0]
        
        self.phase_rad = unwrapped - (m*xs + b)
        self.phase_deg = self.phase_rad/np.pi*180
              
        if f_min and f_max:
            self.freqs = np.linspace(f_min, f_max, num_points)
        else:
            self.freqs = None    
        
    ##END __init__
##END Smith_data
        

def get_smith_data(vna_handle, restart_average=False):
    '''
    DESCRIPTION: Talk to VNA instrument to extract smith data
    INPUT: active visa session handle for VNA
    OUTPUT: Smith_data object
    '''
    # note that "fdata" returns the same as sdata, but the even-index values are 
    #   whatever is displayed on screen and odd-index values are 0
    
    if restart_average:
        # start averaging by toggling the "Avg Trigger" setting. Upon next trigger
        # (assume internal), the average will restart
        vna_handle.write("sens:aver 0"); 
        vna_handle.write("sens:aver 1")
        ##TODO: wait for collection to end?
        num_avgs = float( vna_handle.query("sens1:aver:coun?") )
        sweep_time = float(vna_handle.query("sense1:swe:time?") )
        delay_time = sweep_time*num_avgs
        print("VNA waiting {:.2f} seconds".format(delay_time)) 
        time.sleep(delay_time)
        
    
    ## offload data
    vna_handle.write('calc1:trac1:data:sdat?')
    string_data = vna_handle.read()
    numerical_data = np.array(string_data.split(','), dtype='float')

    ## get frequency range
    vna_handle.write('SENS1:FREQ:DATA?')
    freq_list_str = vna_handle.read() 
    freq_list = np.array( freq_list_str.split(','), dtype='float')
    f_start = min(freq_list)
    f_stop = max(freq_list)
    
    ## parse data
    smith_data = Smith_data(numerical_data, f_min=f_start, f_max=f_stop)
    return smith_data
##END get_smith_data