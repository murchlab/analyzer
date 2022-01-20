# -*- coding: utf-8 -*-
"""
Created on Wed Sep  2 09:40:21 2020

@author: J. Monroe
"""
import numpy as np
import time
from IPython.display import  clear_output
import sys
file_path = r"C:\Users\Crow108\Documents\Python\instr\analyzer"
if file_path not in sys.path: sys.path.append(file_path)
import keithley
import bnc
file_path = r"C:\Users\Crow108\Documents\Python\controller"
if file_path not in sys.path: sys.path.append(file_path)
import set_amplitudes
file_path = r"C:\Users\Crow108\Documents\Python\instr\python_interface\python_without_WX2184C"
if file_path not in sys.path: sys.path.append(file_path)
import daq_programs
import matplotlib.pyplot as plt
        

def current_to_qubit_freq(current_mA):
    # based on 20/09/09 fit of DVKJTM.200205.C5D23
#    stark_shift = -0.0035 # based on Ramsey tuning.
    x = current_mA
    sqrt = np.sqrt
    cos = np.cos
    pi = np.pi
    fq = 5.2044*sqrt( cos(pi*(x-0.7)/48.3))
    return fq 

#def current_to_drive_amp(current_mA):
#    # based on 20/09/10 cavity-attenuation of DVKJTM.200205.C5D23
#    return 1+0.006*current_mA + 0.007*current_mA**2
#
##    # based on fit to fixed-amp sweep
##    x = current_mA
##    y = 0.9871*x**0+0.018268*x**1+0.10576*x**2+-0.12156*x**3+0.047133*x**4+-0.0073716*x**5+0.00041356*x**6
##    return y

def sweep_amp():
    amp_min = 0.01
    amp_max = 0.81
    num_amp_steps = 21
    num_seq_steps = 51
    num_averages = 2000
    rabi_time = 800 # ns
    cavity_amp = 0.4
    
    sweep_result_I = np.zeros( (num_amp_steps, num_seq_steps) )
    sweep_result_Q = np.zeros( (num_amp_steps, num_seq_steps) )
    
    print("") # clear space for indicator
    for i,amp in enumerate(np.linspace( amp_min, amp_max, num_amp_steps)):
        ## status indicator
        N = num_amp_steps
        indicator_str = "!"*(int(np.ceil( i/N *10))) + "."*( 10- int(np.ceil( i/N *10)) )
        clear_output(wait=True)
        print(indicator_str, end='\r', flush=True)
        
        ## set amplitude
        set_amplitudes.set_proteus_amplitude([amp,amp, 1, cavity_amp])
        
        ## acquire data
        # assumes the sequence is already loaded
        try:
            _, _, (rec_avg_vs_pats_I,rec_avg_vs_pats_Q) = daq_programs.run_daq2(num_seq_steps, num_averages, verbose=False)
        except Exception as e:
            if "ApiPllNotLocked" in e.args[0]:
                print("PLL error occured. Restarting DAQ")
                time.sleep(1)
                _, _, (rec_avg_vs_pats_I,rec_avg_vs_pats_Q) = daq_programs.run_daq2(num_seq_steps, num_averages, verbose=False)
            else:
                raise(e)
                
        # organize data
        sweep_result_I[i, :] = rec_avg_vs_pats_I
        sweep_result_Q[i, :] = rec_avg_vs_pats_Q
    ## end loop through currents
    
    ## display results
    plt.imshow( sweep_result_I, extent=[0,rabi_time,amp_max,amp_min], aspect='auto' )
    plt.xlabel("Seq Time [ns]")
    plt.ylabel("Rabi amp [V]")
    plt.show()
    
    return sweep_result_I, sweep_result_Q
##END sweep_amp
    

def sweep_bnc_freq():
    freq_span_GHz = 0.005    
    num_freq_steps = 51
    num_seq_steps = 51
    num_averages = 1000
    seq_duration = 100 # ns
    
    sweep_result_I = np.zeros( (num_freq_steps, num_seq_steps) )
    sweep_result_Q = np.zeros( (num_freq_steps, num_seq_steps) )
    
    # cavity BNC:
    target_bnc = 'USB0::0x03EB::0xAFFF::471-43A6D0000-1458::INSTR'
    
    current_freq = bnc.get_bnc_freq_GHz(bnc_addr=target_bnc)
    print(f"BNC Freq. Sweeping around center: {current_freq}")
    freq_min = current_freq - freq_span_GHz/2
    freq_max = current_freq + freq_span_GHz/2
    
    try:
        print("") # blank line for indicator
        for i,freq in enumerate(np.linspace( freq_min, freq_max, num_freq_steps)):
            ## status indicator
            N = num_freq_steps
            indicator_str = "!"*(int(np.ceil( i/N *10))) + "."*( 10- int(np.ceil( i/N *10)) )
            clear_output(wait=True)
            print(indicator_str, end='\r', flush=True)
            
            ## set BNC qubit drive
            bnc.set_bnc_output(freq, power_dBm=13, bnc_addr=target_bnc)
            
            ## set proteus board amplitude
            #set_amplitudes.set_proteus_amplitude([0.5,0.5,1,cavity_drive_amp]);
            
            ## acquire data
            # assumes the sequence is already loaded
            try:
                _, _, (rec_avg_vs_pats_I,rec_avg_vs_pats_Q) = daq_programs.run_daq2(num_seq_steps, num_averages, verbose=False)
    #           pf, pe, pg = daq_programs.run_daq(num_seq_steps, num_averages)
            except Exception as e:
                if "ApiPllNotLocked" in e.args[0]:
                    print("PLL error occured. Restarting DAQ")
                    time.sleep(1)
                    _, _, (rec_avg_vs_pats_I,rec_avg_vs_pats_Q) = daq_programs.run_daq2(num_seq_steps, num_averages, verbose=False)
    #                pf, pe, pg = daq_programs.run_daq(num_seq_steps, num_averages)
                else:
                    raise(e)
                    
            # organize data
            sweep_result_I[i, :] = rec_avg_vs_pats_I
            sweep_result_Q[i, :] = rec_avg_vs_pats_Q
        ## end loop through currents
    finally:
        ## put toys back where you found them
        bnc.set_bnc_output( current_freq, bnc_addr=target_bnc )    
    
    ## display results
    plt.imshow( sweep_result_I, extent=[0, seq_duration, freq_span_GHz/2*1000, -freq_span_GHz/2*1000], aspect='auto' )
    plt.xlabel("Seq Time [ns]")
    plt.ylabel("Detuning [MHz]")
    plt.show()

    ## output
    return sweep_result_I, sweep_result_Q
##END sweep_bnc_freq
    

def sweep_keithley():
    curr_min_mA =0
    curr_max_mA = -0.72
    num_curr_steps = 2
    num_seq_steps = 51
    num_averages = 200
    rabi_time = 50 # ns
#    qubit_amp_base = 0.4
    
    sweep_result = np.zeros( (num_curr_steps, num_seq_steps) )
    sweep_result2 = np.zeros( (num_curr_steps, num_seq_steps) )
    
    print( "" )
    for i,curr_mA in enumerate(np.linspace( curr_min_mA, curr_max_mA, num_curr_steps)):
        ## status indicator
        N = num_curr_steps
        indicator_str = "!"*(int(np.ceil( i/N *10))) + "."*( 10- int(np.ceil( i/N *10)) )
        clear_output(wait=True)
        print(indicator_str, end='\r', flush=True)
        
        ## set keithley current source
        keithley.ramp_from_prev_value( curr_mA)
        
        ## set BNC qubit drive
        qubit_drive_freq = current_to_qubit_freq(curr_mA) - 0.100
        qubit_drive_freq = np.round(qubit_drive_freq, 4) # round to 100 kHz level.
        bnc.set_bnc_output(qubit_drive_freq, power_dBm=13)
        
        ## set proteus board amplitude
#        qubit_drive_amp = qubit_amp_base*current_to_drive_amp(curr_mA)
#        qubit_drive_amp = np.round( qubit_drive_amp, 3) # mV precision
#        qubit_drive_amp = np.min([ 1.3, qubit_drive_amp]) # don't exceed the max
        #print( f"Set drive to {qubit_drive_amp} V")
        #set_amplitudes.set_proteus_amplitude([qubit_drive_amp,qubit_drive_amp,1,cavity_drive_amp])
        
        ## acquire data
        # assumes the sequence is already loaded
        try:
            _, _, (rec_avg_vs_pats_I,rec_avg_vs_pats_Q) = daq_programs.run_daq2(num_seq_steps, num_averages, verbose=False)
        except Exception as e:
            if "ApiPllNotLocked" in e.args[0]:
                print("PLL error occured. Restarting DAQ")
                time.sleep(1)
                _, _, (rec_avg_vs_pats_I,rec_avg_vs_pats_Q) = daq_programs.run_daq2(num_seq_steps, num_averages, verbose=False)
            else:
                raise(e)
                
        # organize data
        sweep_result[i, :] = rec_avg_vs_pats_I
        sweep_result2[i,:] = rec_avg_vs_pats_Q
    ## end loop through currents
    
    ## display results
    plt.imshow( sweep_result, extent=[0,rabi_time,curr_max_mA,curr_min_mA], aspect='auto' )
    plt.xlabel("Seq Time [ns]")
    plt.ylabel("Current [mA]")
    plt.show()

    ## output
    return sweep_result, sweep_result2
##END sweep_keithley
    
if __name__ == '__main__':
#      x = sweep_amp()
#    y = sweep_keithley()
    pass