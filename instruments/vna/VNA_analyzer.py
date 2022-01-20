# -*- coding: utf-8 -*-
"""
Created on Thu Jun 18 15:55:16 2020

@author: Crow108
"""

# -*- coding: utf-8 -*-

"""

Created on Wed Feb 12 10:47:41 2020



@author: J. Monroe

@date: Feb 12, 2020

"""

import numpy as np

import time

import datetime as dt

import time

import pyvisa

import matplotlib.pyplot as plt

import numpy as np


def setup_vna(vna_handle):

    ## see programming guide: http://ena.support.keysight.com/e5063a/manuals/webhelp/eng/

    ## efault configuration for VNA

    start_freq_Hz = 4e9;

    stop_freq_Hz = 5e9;

    vna_handle.write('sens:band 100') # set bandwith to 100 Hz

    vna_handle.write('calc:par:def S21')

    vna_handle.write('calc:form phase') # format options include 'mlog', 'phase', etc

    vna_handle.write('sour:pow -10.0')

    vna_handle.write('sens:aver:coun 100')

    #vna_handle.write('sens:aver on')

    #vna_handle.write('sens:aver:cle')

    vna_handle.write('sens:freq:start {}'.format(start_freq_Hz))

    vna_handle.write('sens:freq:stop {}'.format(stop_freq_Hz))

    vna_handle.write('outp on')

    #vna_handle.write('mmem:stor:fdat "run1/test.csv"')

##END setup_vna

    

def setup_sig_gen(sig_gen):

    sig_gen.write('sour:pow:lev:imm:ampl -10 dBm')

    sig_gen.write('sour:pow:lev:imm:ampl:step:incr 0.1 dBm')

    sig_gen.write('sour:freq:cw 1.88 GHz') # set frequency

    sig_gen.write('sour:freq:step 1 MHz') # set frequency step size to 1 MHz

    sig_gen.write('outp:stat on') # turn on

    #sig_gen.write(':SOUR:FREQ DOWN')

## setup_sig_gend

    

def setup_cur_source(cur_source):

    ## this is a PHYSICALLY DANGEROUS function. If the current source is 

    ##  currently generating output, this will cut it off. Possibly trapping

    ##  flux in device.

    cur_A = 0

    cur_source.write('sour:func:mode curr')

    cur_source.write('sour:curr:vlimit 2')

    cur_source.write('sour:curr {}'.format(cur_A) )

    cur_source.write('sens:func "curr"')

    cur_source.write('outp on')

##END setup_cur_source
    
# get visa resources

rm = pyvisa.ResourceManager()

print(rm.list_resources(), '\n')

vna = pyvisa.ResourceManager().open_resource('USB0::0x2A8D::0x5D01::MY54503364::INSTR')

print(vna.query('*IDN?'))

sig_gen = pyvisa.ResourceManager().open_resource('GPIB::2::INSTR')

print(sig_gen.query('*IDN?'))

cur_source = pyvisa.ResourceManager().open_resource('GPIB0::18::INSTR')

print(cur_source.query('*IDN?'))





## start data processing

setup_vna(vna)

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