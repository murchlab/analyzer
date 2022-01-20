# -*- coding: utf-8 -*-
"""
Created on Thu Jan 30 15:15:30 2020

@author: crow104
"""
#
#while not KeyboardInterrupt:
#    print("...")
    
try:
    for k in range(10):
        print("...{}".format(input()))
        time.sleep(0.2)
except KeyboardInterrupt:
    print('interrupted!')