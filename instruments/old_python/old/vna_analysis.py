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
        self.imag = np.array( vna_smith_data[1::2] )
        num_points = self.real.size

        self.complex = self.real + 1j*self.imag        
        self.lin_mag = np.sqrt(self.real**2 + self.imag**2)
        self.log_mag = 20*np.log10( self.lin_mag)
        # arctan2 chooses the quadrant based on the sign of each step
        self.wrapped_phase = np.arctan2(self.imag, self.real)
        
        ## unwrap the phase
        unwrapped = np.unwrap(self.wrapped_phase)
        # a quick linear fit to subtract off electrical delay. 
        # calculating physical ED requires frequency information. I'll instead
        #   allow frequency to remain unspecified
        # The linear fit is better when we do not include the resonance itself. 
        #   So we'll only look at the first quarter of the trace
        xs = np.arange(num_points//4)
        ys = unwrapped[:num_points//4]
        # solve y = mx +b as  y = A.f where A is Nx2 with x as first  column and 
        # ones as second column f is 2x1 of coefficients m and b.
        # fit by minimizing (ys-A.f)^2
        A_mat = np.array([xs, np.ones(xs.shape)]).T
        m, b = np.linalg.lstsq(A_mat, ys, rcond=None)[0]
        
        full_range = np.arange(num_points) 
        self.phase_rad = unwrapped - (m*full_range + b)
        # 
        #self.phase_rad += np.pi
        self.phase_deg = self.phase_rad/np.pi*180
              
        if f_min and f_max:
            self.freqs = np.linspace(f_min, f_max, num_points)
        else:
            self.freqs = None                
    ##END __init__
    
    def rotate_rad(self, angle_rads):
        self.complex *= np.exp(1j*angle_rads)
        self.real = np.real(self.complex)
        self.imag = np.imag(self.complex)
        self.phase_rad = np.angle(self.complex)
        self.phase_deg = self.phase_rad/np.pi*180
        
    def copy(self):
        smith_format = np.zeros(2*self.real.size)
        smith_format[0::2] = self.real
        smith_format[1::2] = self.imag
        
        try:
            return Smith_data(smith_format, f_min=min(self.freqs), f_max=max(self.freqs))
        except TypeError: # freqs = None
            return Smith_data(smith_format)
##END Smith_data
        

def pull_smith_data(vna_handle, restart_average=False):
    '''
    DESCRIPTION: Talk to VNA instrument to extract smith data
    INPUT: active visa session handle for VNA
    OUTPUT: Smith_data object
    '''
    ## on N5230A VNAs user must select the current measurement
    measurements_list = vna_handle.query("calc:par:cat?")
    # name is of form '"CH1_S12_1,S12"' (ie includes double quote)
    measurement_name = measurements_list[1:measurements_list.index(',')]
    #vna_handle.write("calc:par:sel '{}'".format(measurement_name))
    
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
    # note that "fdata" returns the same as sdata, but the even-index values are 
    #   whatever is displayed on screen and odd-index values are 0
    string_data = vna_handle.query("calc:data? SDATA")
    numerical_data = np.array(string_data.split(','), dtype='float')

    ## get frequency range
    freq_start = float(vna_handle.query('sense:freq:start?'))
    freq_stop = float(vna_handle.query('sense:freq:stop?'))
    
    ## parse data
    smith_data = Smith_data(numerical_data, f_min=freq_start, f_max=freq_stop)
    return smith_data
###END get_smith_data