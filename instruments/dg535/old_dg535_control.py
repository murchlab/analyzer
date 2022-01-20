# -*- coding: utf-8 -*-
"""
Created on Fri Jul  3 14:04:16 2020

@author: J. Monroe
"""
import numpy as np
# manual: https://www.thinksrs.com/downloads/pdfs/manuals/DG535m.pdf

## constants
# see table in manual p13, RHS column.
# 0 corresponds to trigger input
T0 = 1
A  = 2
B  = 3
AB = 4 # also !AB ??
# !AB = 4
C  = 5
D  = 6
CD = 7


def initialize_dg535(dg_handle):
    ## trigger one at a time.
    dg_handle.write("TM 0") # trigger mode to internal (0)
    dg_handle.write("TR 0, 10e3") # 10 kHz trigger rate
    
    ## prep all outputs for variable signaling
    #  allows variable amplitudes.
    dg_handle.write(f"OM {T0}, 3")
    dg_handle.write(f"OM {A}, 3") # 3 is VARiable mode
    dg_handle.write(f"OM {B}, 3")
    dg_handle.write(f"OM {AB}, 3")
    dg_handle.write(f"OM {C}, 3")
    dg_handle.write(f"OM {D}, 3") 
    dg_handle.write(f"OM {CD}, 3") 
    
    ## set channel impedences to 50 Ohms
    dg_handle.write(f"TZ {AB}, 0") # 0 is 50 Ohms, 1 is 'high Z'.
    dg_handle.write(f"TZ {CD}, 0")
    dg_handle.write(f"TZ {T0}, 1") # to avoid confusion, prepare T0 for 'scope display
#    
#    ## turn output off while setting commands
    dg_handle.write(f"OO {T0}, -0.1") # start with Output Offset set to -0.1 V.
    dg_handle.write(f"OA {T0}, 0.1") # Output Amplitude to 0.1 V.
    
    ## channel offsets
    # ensures these are set to zero (tuned by hand)
    dg_handle.write(f"OO {CD}, 0") # cavity
    dg_handle.write(f"OO {AB}, 0") # qubit
    
    return dg_handle.query("ES")
##END initialize_dg535


def start_dg535(dg_handle):
    dg_handle.write(f"OA {T0}, 1.0")
##END start_dg535
    
def always_on_seq(dg_handle):
    seq_len_s = 100E-6 # 10 kHz rep rate --> 100 us.
    
    # amplitudes
    ## NOTE: 0.1 is minimum value; returns error "4" =0B0100 = bit 2 = value outside range
    ## NOTE: 0.01 is increment.
    cavity_amp_V = 1 # units: volts
    qubit_amp_V  = 1 # units: volts
    
    # cavity on
    dg_handle.write(f"DT {C}, {T0}, {0.1}E-6")
    dg_handle.write(f"DT {D}, {C}, {seq_len_s-2E-6}")
    dg_handle.write(f"OA {CD}, {cavity_amp_V}") 
    
    ## qubit pulse
    dg_handle.write(f"DT {A}, {T0}, {0.1}E-6")
    dg_handle.write(f"DT {B}, {A}, {seq_len_s-2E-6}")
    dg_handle.write(f"OA {AB}, {qubit_amp_V}")
    
    # check for errors
    return dg_handle.query("ES")
##END always_on


def rabi_seq(dg_handle, step_num, total_steps=51):
    rabi_time_us = 0.200  
    
    ## cavity pulse
    cavity_pulse_dur_us = 1
    cavity_pulse_start_us = 2
    dg_handle.write(f"DT {C}, {T0}, {cavity_pulse_start_us}E-6")
    dg_handle.write(f"DT {D}, {C}, {cavity_pulse_dur_us}E-6")
    dg_handle.write(f"OA {CD}, 1") # amplitude set to 1 V.
    
    ## qubit pulse
    pulse_length_us = np.round( step_num/total_steps* rabi_time_us, 3)
    pulse_start_us = cavity_pulse_start_us - pulse_length_us  - 10E-3
    dg_handle.write(f"DT {A}, {T0}, {pulse_start_us}E-6")  # T0 to A delay is 1 us.
    dg_handle.write(f"DT {B}, {A}, {pulse_length_us}E-6" ) # A to B delay is 0.5 us.
    
    dg_handle.write(f"OA {AB}, 1") # amplitude set to 1 V
    
    ## beginnning of seqeunce: turn from -0.1 V to +1V.
    ## enable output on A, B
    
    return dg_handle.query("ES")
##END rabi_seq

## Alazar card triggered with T0

## cavity readout on C and D

## qubit pulses on A and B



##NOTES
# error status 4 implies bad command (eg forgot comma)

