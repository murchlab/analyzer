# -*- coding: utf-8 -*-
"""
Created on Wed Aug 26 10:20:06 2020

@author: J. Monroe
"""
import sys, os
import numpy as np
mod_path = r"C:\Users\crow108\Documents\Python\controller"
if mod_path not in sys.path: sys.path.append(mod_path)
import proteusapi, instFunction
import generator

def set_proteus_amplitude(amps=[1, 1, 1, 1], offsets=[0, 0, 0, 0]):
    for ch_index in range(4):
        proteusapi.SendScpi(f":INST:CHAN {ch_index+1}")
        proteusapi.SendScpi(f":VOLT {amps[ch_index]}")
        proteusapi.SendScpi(f":VOLT:OFFS {offsets[ch_index]}")


#def new_set_proteus_amplitude(amps=[1, 1, 1, 1], offsets=[0, 0, 0, 0]):
#    winpath = os.environ['WINDIR'] + "\\System32\\"
#    clr.AddReference(winpath + R'TEPAdmin.dll')
#
#    ## open session
#    try:
#        admin = CProteusAdmin()
#        print( "return code: ", admin.Open() )
#        slotId = np.uint32(3)
#        inst = admin.OpenInstrument(slotId)
#        print("set amp: ", inst)
#        
#        if not inst:
#            errStr = "admin.OpenInstrument(slotId={0}) failed".format(slotId)
#            print(errStr)
#            raise RuntimeError(errStr)
#            
#        query_syst_err = True
#        verbose = True
#        print("ready to send")
#        instFunction.SendScpi(inst, ":INST:CHAN 1", query_syst_err, verbose=verbose) 
#        print("first has sent")
#        for ch_index in range(4):
#            # Setting up amplitudes and offsets
#            instFunction.SendScpi(inst, f":INST:CHAN {ch_index+1}", query_syst_err, verbose=verbose)             
#            instFunction.SendScpi(inst, f":VOLT {amps[ch_index]}", query_syst_err, verbose=verbose)
#            instFunction.SendScpi(inst, f":VOLT:OFFS {offsets[ch_index]}", query_syst_err, verbose=verbose)
#            instFunction.SendScpi(inst, ":SOUR:FUNC:MODE TASK", query_syst_err, verbose=verbose)
#    finally:          
#        admin.Close()
#    

def new_set_proteus_amplitude( amps=[1, 1, 1, 1], offsets=[0, 0, 0, 0],\
                      slotId = np.uint32(3), verbose=False):
        
        sclk = 1e9 
        query_syst_err = True
            
        try:
            ## initialize session with correct board
            generator.proteus_init()
            inst = generator.insts[slotId]
            
            for ch_index in range(4):
                instFunction.SendScpi(inst, f":INST:CHAN {ch_index+1}", query_syst_err, verbose=verbose)
                
                ## set amplitudes
                instFunction.SendScpi(inst, f":VOLT {amps[ch_index]}", query_syst_err, verbose=verbose)
                instFunction.SendScpi(inst, f":VOLT:OFFS {offsets[ch_index]}", query_syst_err, verbose=verbose)
                instFunction.SendScpi(inst, ":SOUR:FUNC:MODE TASK", query_syst_err, verbose=verbose)
                
                ## ensure output is on
                instFunction.SendScpi(inst, ":TRIG:STAT ON", query_syst_err, verbose=verbose) # Enable trigger state (CH specific)
                instFunction.SendScpi(inst, ":OUTP ON", query_syst_err, verbose=verbose)
                
            
            ## Ensure correct channel sychronization
            for ch_index in range(4):
                instFunction.SendScpi(inst, f":INST:CHAN {ch_index+1}", query_syst_err, verbose=verbose)
                instFunction.SendScpi(inst, f":FREQ:RAST {sclk}", query_syst_err, verbose=verbose)
                instFunction.SendScpi(inst, f":TASK:SEL 1", query_syst_err, verbose=verbose)
                instFunction.SendScpi(inst, f":TASK:DEF:NEXT1 2", query_syst_err, verbose=verbose)
        
        finally:
            generator.proteus_close()
    ##END load_sequence