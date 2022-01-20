# -*- coding: utf-8 -*-
"""
Created on Tue Jun 23 16:01:40 2020

@author: J. Monroe
"""

import pyvisa, time, sys
rm = pyvisa.ResourceManager()
dir_path = r"C:\Users\Crow108\Documents\Python\instr\analyzer"
if dir_path not in sys.path: sys.path.append(dir_path)
import vna_analysis
import bnc


def continuous_wave_spectroscopy(sweep_f_min, sweep_f_max, bnc_power_dBm=-30):
    '''
    INPUT:
    OUTPUT: cavity response (complex) as a function of CW probe frequency
    REQUIREMENTS: BNC + VNA are connected
    '''
    
    ## constants
    bnc_address = 'USB0::0x03EB::0xAFFF::421-4385A0002-0619::INSTR'
    vna_address = "GPIB0::20::INSTR"

    bnc_power_dBm = -10
    bnc_start_GHz = 4.5
    bnc_stop_GHz = 5.3
    num_freqs = 401
    vna_power_dBm = -25
    vna_freq_GHz = 5.82
    dwell_time = 0.05
    
    # setup sessions with insruments
    #vna_handle = rm.open_resource(vna_address)
    #bnc_handle= rm.open_resource(bnc_address)
    #try
    if True:
        # prep each instrument
        #vna_handle.write(':MMEM:STOR "recent_state.sta"')
        vna_analysis.prepare_for_cw_spec(vna_freq_GHz=vna_freq_GHz,\
                                         vna_power_dBm=vna_power_dBm,\
                                         dwell_sec=dwell_time,\
                                         num_freq=num_freqs,\
                                         vna_gpib=vna_address)
        bnc.configure_for_sweep(start_freq_GHz=bnc_start_GHz,\
                                stop_freq_GHz=bnc_stop_GHz,\
                                power_dBm=bnc_power_dBm,\
                                dwell_sec=dwell_time,\
                                num_freq_points=num_freqs,\
                                bnc_addr=bnc_address)
        
        # wait for sweep to finish
        time_to_complete = num_freqs *dwell_time
        print(f"Sweeping for {time_to_complete}")
        time.sleep(2*time_to_complete) # time in ms
        
        # grab data
        smith_data = vna_analysis.get_smith_data(vna_address)        
        
        # clean up
#        vna_handle.write(':MMEM:LOAD "recent_state.sta"')
    
#    finally:
#        vna_handle.close()
#        bnc_handle.close()
        
    return smith_data
##END CW_spectroscopy    


#def bnc_setup(bnc_handle, freq_start_ghz, freq_stop_ghz, power_dbm):
#    '''
#    DESC: This function prepares the BNC continuous-wave generator to sweep
#        through a frequency range, triggering the VNA as it goes.
#        This script is a direct translation of the labview VI "setup_BNC_for_trigger.VI"
#        See https://www.berkeleynucleonics.com/sites/default/files/BNC%20Model%20845%20PM%2011-30-17.pdf
#        for detailed parameter definitions
#    INPUT: 
#        bnc_handle: a visa session with the CW generator
#    
#    '''
#    pass
#    ## 1. Initialize generator
#    # visa handle takes care of this.
#       
#    ## 2. Configure RF output
#    #freq_ghz = 5.831 
#    dwell_time_sec = 0.1
#    num_freq_steps = 201
#    bnc_handle.write( f":FREQ {freq_start_ghz} GHZ" )
#    bnc_handle.write( f":POW {power_dbm}")
#    bnc_handle.write(":FREQ:MODE FIX")
#    
#    ## 3. Configure Sweep
#    bnc_handle.write(":SWE:DEL 0")
#    bnc_handle.write(f":SWE:DWEL {dwell_time_sec}")
#    bnc_handle.write(":SWE:DIR UP") # increase or decrease (DOWN) frequency.
#    bnc_handle.write(":SWE:SPAC LIN") # linear or log (LOG) steps
#    bnc_handle.write(f":SWE:POIN {num_freq_steps}")
#    bnc_handle.write(":SWE:COUNT 1") # number of times to repeat the sweep
#    # the default value for the above command is INF
#    
#    ## 4. Configre Trigger
#    bnc_handle.write(":TRIG:TYPE NORM") # normal (vs gated or pointed) trigger
#    bnc_handle.write(":TRIG:SLOP POS") # use positive slope
#    bnc_handle.write(":TRIG:SOUR IMM") # immediately trigger upon freq. set
#    bnc_handle.write(":TRIG:DEL 0") # delay between freq. set and trigger
#    bnc_handle.write(":TRIG:ECO 1")
#    
#    ## 5. Configure Trigger output
#    # now that trigger params are set, we need to program the actual output
#    #   Not sure how/why they're different
#    bnc_handle.write(":TRIG:OUTP:MODE POIN")
#    bnc_handle.write(":TRIG:OUTP:POL NORM")
#    
#    # 6. Enable Low Frequency
#    # low frequency port contains the trigger
#    # make a 1 V square pulse based on trigger (0 Hz)
#    bnc_handle.write(":LFO:STAT ON")
#    bnc_handle.write(":LFO:SOUR TRIG") # source is trigger
#    # I think the below commands don't take effect because SOURce not set to LFGenerator
#    bnc_handle.write(":LFO:SHAP SQU") 
#    bnc_handle.write(":LFO:FREQ 0") # 10 Hz is lowest value.
#    #bnc_handle.write(":LFO:AMPL 1") when not set to    sine or triangle, this 
#    #   defaults to 2.5 V
#    
#    ## 7. Enable output
#    bnc_handle.write(":OUTP ON")
#    
#    ## 8. Run sweep
#    bnc_handle.write(":INIT:CONT OFF") # do not rearm the trigger after the sweep finshes
#    bnc_handle.write(":FREQ:MODE FIX") # cease any previous sweep
#    bnc_handle.write(f":FREQ:STAR {freq_start_ghz} GHZ")
#    bnc_handle.write(f":FREQ:STOP {freq_stop_ghz} GHZ")
#    bnc_handle.write(":FREQ:MODE SWE") # start this sweep
#    
#    # a hack to start the sweep
#    bnc_handle.write(":INIT:CONT ON; :INIT:CONT OFF")
####END bnc_setup
    
    
def bnc_setup2(bnc_handle):
    ## direct copy of labview commands
    bnc_handle.write("*CLS;")
    print("1, ", bnc_handle.query(":SYST:ERR?") )
    bnc_handle.write(":FREQ 4.000000 GHZ;:POW -15.000000;")
    print("2, ", bnc_handle.query(":SYST:ERR?") )
    bnc_handle.write(":SWE:DEL  0.000000;:SWE:DWEL 0.050000;:SWE:DIR UP;:SWE:SPAC LIN;:SWE:POIN 251.000000;:SWE:COUN 1.000000")
    print("3, ", bnc_handle.query(":SYST:ERR?") )
    bnc_handle.write(":TRIG:TYPE NORM;:TRIG:SLOP POS;:TRIG:SOUR IMM;:TRIG:DEL 0.000000;:TRIG:ECO 1.000000")
    print("4, ", bnc_handle.query(":SYST:ERR?") )
    bnc_handle.write(":TRIG:OUTP:MODE POIN;:TRIG:OUTP:POL NORM;")
    print("5, ", bnc_handle.query(":SYST:ERR?") )
    bnc_handle.write(":LFO:STAT ON;:LFO:SOUR TRIG;:LFO:SHAP SQU;:LFO:FREQ 0.000000;:LFO:AMPL 1.000000")
    print("6, ", bnc_handle.query(":SYST:ERR?") )
    bnc_handle.write(":OUTP ON;")
    print("7, ", bnc_handle.query(":SYST:ERR?") )
    bnc_handle.write("INIT:CONT OFF;:FREQ:MODE FIX;:FREQ:STAR 4.000000 GHZ;:FREQ:STOP 4.500000 GHZ;:FREQ:MODE SWE")
    print("8, ", bnc_handle.query(":SYST:ERR?") )
    bnc_handle.write("INIT:CONT OFF;:INIT")
    print("9, ", bnc_handle.query(":SYST:ERR?") )



