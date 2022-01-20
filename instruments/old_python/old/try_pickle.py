# -*- coding: utf-8 -*-
"""
Created on Tue Mar  3 11:26:14 2020

@author: crow104
"""

import pickle

if __name__ == '__main__':
    def __init__(self):
        self.name = self

    path0 = "C:\\Data\\2020\\ep_metrology\\data\\data_200303"
    fname = path0 + "\\20200304_080823.pickle"
    
#    with open(fname, "wb") as open_file:
#        pickle.dump((ramsey, t1decay), open_file)

    with open(fname, "rb") as open_file:    
        x = pickle.load(open_file)
        print(x)