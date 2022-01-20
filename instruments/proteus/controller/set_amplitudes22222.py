# -*- coding: utf-8 -*-
"""
Created on Wed Aug 26 10:20:06 2020

@author: Crow108
"""


def set_proteus_ampltiude(amps=[1, 1, 1, 1], offset=[0, 0, 0, 0]):
    # Initializing the instrument
        admin = instFunction.loadDLL()
        slotId = instFunction.getSlotId(admin)
    
        try:
            if not slotId:
                raise Exception("Invalid slot choice!")
            inst = admin.OpenInstrument(slotId) 
            if not inst:
                raise Expection("Failed to Open instrument with slot-Id {0}".format(slotId))
            instId = inst.InstrId
                ###########  CALL THE SCPI ###########
                ScpiCommands(inst) #     <<<-------   #
                ######################################
            for ch_index, _ in enumerate(self.channel_list):
                # Setting up amplitudes and offsets
                instFunction.SendScpi(inst, ":INST:CHAN {}".format(ch_index+1))
                instFunction.SendScpi(inst, ":VOLT {}".format(amp[ch_index]))
                instFunction.SendScpi(inst, ":VOLT:OFFS {}".format(offset[ch_index]))
                instFunction.SendScpi(inst, ":SOUR:FUNC:MODE TASK")
    #                instFunction.SendScpi(inst, ":SOUR:FUNC:MODE ARB")
                
                # connect ouput
                instFunction.SendScpi(inst, ":OUTP ON")
                
    #                 enble markers
                instFunction.SendScpi(inst, ":MARK:MASK 65535")
                instFunction.SendScpi(inst, ":MARK:SEL 1")
                instFunction.SendScpi(inst, ":MARK:STAT ON")
                instFunction.SendScpi(inst, ":MARK:SEL 2")
                instFunction.SendScpi(inst, ":MARK:STAT ON")
            ##END SCPI commands
        
            rc = admin.CloseInstrument(instId)
            instFunction.Validate(rc,__name__,instFunction.inspect.currentframe().f_back.f_lineno)   
        finally:
            rc = admin.Close()
            instFunction.Validate(rc,__name__,instFunction.inspect.currentframe().f_back.f_lineno)