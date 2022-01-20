# -*- coding: utf-8 -*-
"""
Created on Wed Feb 12 15:12:56 2020

@author: J. Monroe
"""
import numpy as np
import os
import pyvisa
import keithley_current
import vna_analysis
#import instrument_setup
import matplotlib.pyplot as plt


min_current = 200e-6
max_current = 600e-6
N_steps = 31; 

## setup instruments for measurement
rm = pyvisa.ResourceManager()
vna_handle = rm.open_resource('USB0::0x2A8D::0x5D01::MY54503364::INSTR')
curr_source = rm.open_resource('GPIB0::18::INSTR')


## sweep through currents
current_list = np.linspace(min_current, max_current, N_steps)
output_list = [None for i in range(N_steps)]

for i,bias_current in enumerate(current_list):
    keithley_current.set_level(curr_source, bias_current,10e-6)
    smith_data = vna_analysis.get_smith_data(vna_handle, restart_average=True)
    output_list[i] = smith_data
freq_min_GHz = min(smith_data.freqs)/1e9
freq_max_GHz = max(smith_data.freqs)/1e9
#
### process data
num_freqs = len(smith_data.real)
flux_map = np.zeros((N_steps, num_freqs))
for i,smith in enumerate(output_list):
    flux_map[i, :] = smith.phase_deg

## save data
save_dir = r"C:\Users\Axion-Workstation\Documents\jmonroe\data\20200212\jpa_dut2"
file_name = "flux_sweep_vna_0dBm"
file_name += f"_{freq_min_GHz}_{freq_max_GHz}GHz_bias_{min_current*1e3}_{max_current*1e3}mA"
file_name += ".dat"
print("creating file {}".format(file_name))
np.savetxt(os.path.join(save_dir, file_name), flux_map)


## make figures
f = plt.figure()
plt.imshow(flux_map, extent=[freq_min_GHz, freq_max_GHz, min_current*1e3,max_current*1e3],aspect='auto')
plt.xlabel("VNA Freq [GHz]")
plt.ylabel("Current Bias [mA]")
plt.show()
    
