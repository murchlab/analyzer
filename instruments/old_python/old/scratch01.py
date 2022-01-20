# -*- coding: utf-8 -*-
"""
Created on Wed Jan 29 17:31:28 2020

@author: crow104
"""

for _ in p_readout_all:
    plt.plot(_)
    
fig = plt.figure(figsize=(8,8))
plt.imshow(np.vstack(p_readout_all).T, extent=[-6, +6, -10, 10])