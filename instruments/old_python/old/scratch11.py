# -*- coding: utf-8 -*-
"""
Created on Tue Feb 18 22:14:25 2020

@author: crow104
"""

import hp_E4405B

x, y = hp_E4405B.get_trace()

plt.plot(x,y)