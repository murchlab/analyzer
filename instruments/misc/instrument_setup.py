# -*- coding: utf-8 -*-
"""
Created on Wed Feb 12 10:29:31 2020

@author: J. Monroe
@date: Feb 12, 2020
"""


import datetime as dt
import time
import pyvisa
import matplotlib.pyplot as plt
import numpy as np

def setup_vna(vna_handle):
    ## see programming guide:44
    ## default configuration for VNA
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
    
#
## get visa resources
#rm = pyvisa.ResourceManager()
#print(rm.list_resources(), '\n')
#vna = rm.open_resource('GPIB0::16::INSTR')
#print(vna.query('*IDN?'))
## the following are not currently connected.
##sig_gen = rm.open_resource('GPIB::2::INSTR')
##print(sig_gen.query('*IDN?'))
##cur_source = rm.open_resource('GPIB0::18::INSTR')
##print(cur_source.query('*IDN?'))
#
#
### start data processing
#setup_vna(vna)
