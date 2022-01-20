# -*- coding: utf-8 -*-
"""
Created on Sat Jan 25 14:33:26 2020

@author: P. M. Harrington, 25 January 2020
"""

import tewx

def wx_initialize():
    instr_addr = '128.252.134.119'
    
    # Initializing the instrument
    inst = tewx.TEWXAwg(instr_addr, paranoia_level=1)
    inst.send_cmd('*CLS') # Clear errors
    #inst.send_cmd('*RST') # Reset the device
    inst.send_cmd(":FREQ:RAST 1000000001.000000", paranoia_level=1)
    inst.send_cmd(":FREQ:RAST 1000000000.000000", paranoia_level=1)
    inst.close()