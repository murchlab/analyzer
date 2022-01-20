# -*- coding: utf-8 -*-
"""
Created on Sat Nov 14 16:42:05 2020

@author: DVK
"""
#A program to return VNA Smith chart in Wisbey's vi format

import numpy as np
from datetime import datetime
import os
import pyvisa

rm = pyvisa.ResourceManager()
vna_gpib='GPIB20::20::INSTR'
vna = rm.open_resource(vna_gpib)

#data_dir = "C:\\Data\\20210112_CPW_Res\\DVK_068_05\\TempSweep"

def wisform(smith):
    outarray = np.column_stack((smith.freqs,smith.log_mag,smith.phase_rad,smith.real,smith.imag))
    return outarray

#
power_list=[-20]
del_time = [1]
span = [61, 90, 405] #in KHz
center_freq = [6.582951264, 6.746680516, 7.156077464] # in GHz

#
#power_list = np.linspace(0,-80,41)
#del_time = np.zeros((np.size(power_list)))
#del_time[0:20] = 60; del_time[20::] = 120  
#power_list = np.linspace(0,-80,41)
#del_time=np.zeros(np.size(power_list))
#del_time[0:20]=5; del_time[20:25]=10; del_time[25:29]=60; del_time[29:34]=90; del_time[34:41]=120

for j in range (len(center_freq)):
    data_dir = "C:\\Data\\20210112_CPW_Res\\DVK_068_05\\TempSweep\\"+str(center_freq[j])
    
    for i,power in enumerate(power_list):
        vna.write(f"SOUR:POW {power}")
        vna.write(":AVER 0")
        vna.write(":AVER 1")
        
        vna.write(f":SENSE:FREQ:CENT {center_freq[j]*1E9}")
        vna.write(f":SENSE:FREQ:SPAN {span[j]*1E3}")
        
        print(f"Averaging for {del_time[i]} minutes")
        time.sleep(60*del_time[i])
        vs=get_smith_data(vna_gpib)
        outarray = wisform(vs)
        file_name = f"vna_{np.min(vs.freqs)/1E9:0.6f},{np.max(vs.freqs)/1E9:0.6f}_power{power}dBm.txt"
        os.makedirs(data_dir+'\\'+datetime.now().strftime('%Y%m%d'),exist_ok=True)
        np.savetxt(data_dir+'\\'+datetime.now().strftime('%Y%m%d')+"/"+datetime.now().strftime('%H%M%S')+file_name,outarray, delimiter='\t')
    