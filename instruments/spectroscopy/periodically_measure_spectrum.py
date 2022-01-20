# -*- coding: utf-8 -*-
"""
Created on Tue Oct 20 10:42:53 2020

@author: J. Monroe

DESCRIPTION: This script periodically measures spectra from both the 
    VNA (vector network analyzer) and SA (spectrum analyzer)
    intended to compare to fridge temperatures
"""

## IMPORTS
import numpy as np
import matplotlib.pyplot as plt
import time, pyvisa 
rm = pyvisa.ResourceManager()

    
    
def get_SA_spectrum(sa_address):
    ##INPUT: a string address to the SA (eg 'GPIB0::18::INSTR')
    sa_handle = rm.open_resource(sa_address)
    
    try:
        # get spectrum
        spectrum_str = sa_handle.query(":TRAC? TRACE1")
        spectrum = np.array( spectrum_str.split(','), dtype='float' )
        
        # get frequency range
        range_str = sa_handle.query(":FREQ:STAR?;:FREQ:STOP?")
        f_min,f_max = [ float(x) for x in range_str.split(';') ]        
        num_points = spectrum.size
        fs = np.linspace(f_min, f_max, num_points)
        
        return fs, spectrum
    finally:
        sa_handle.close()
##END get_SA_spectrum
        

def spectrum_vs_time():
    ## settings
    data_dir = r"C:\Data\20201102_HEMT_noise_rise\during_warmup"
    sa_address = 'GPIB0::18::INSTR'
    stop_time_hour = 23
    
    ## configure SA
    
    summary = []
    while( time.localtime().tm_hour < stop_time_hour):
    
        ## get current time
        current_time = time.localtime()
        hour = str(current_time.tm_hour).zfill(2)
        minute = str(current_time.tm_min).zfill(2)
        second = str(current_time.tm_sec).zfill(2)
        time_str = f"{hour}{minute}{second}"
    
        ## take SA spectrum    
        fs_sa, spectrum_sa = get_SA_spectrum(sa_address)
        fs_sa_GHz = fs_sa/1E9
        peak = np.max(spectrum_sa)
        print(f"{peak} dBm at {time_str}")
    
        file_name = f"power_{np.min(fs_sa_GHz)},{np.max(fs_sa_GHz)}GHZ_time_{time_str}.txt" 
        np.savetxt( data_dir + "/" + file_name, spectrum_sa)
        
        summary.append( [int(time_str), peak] )
        summary_file_name = "_peaks_time_HHMMSS_power.txt"
        np.savetxt( data_dir + "/" + summary_file_name, summary)
        
        time.sleep(30)
        
    ## output
#    plt.plot(fs_vna_GHz, spectrum_vna)
#    plt.show()
    plt.plot(fs_sa_GHz, spectrum_sa)
    plt.show()
    
##END spectrum_vs_time

    



