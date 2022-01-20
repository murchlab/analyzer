# -*- coding: utf-8 -*-
"""
Created on Tue Feb 18 22:06:11 2020

@author: crow104
"""

expt_cal = seq_programs.get_expt_cal()
expt_cal.ssm.ge
ssm_ge = 0.3875
ssm_ef = 0.0925
freq_ef = 5.32+ssm_ef
freq_ge = 5.32+expt_cal.ssm.ge
new_ssm_ge = 0.200
freq_c = freq_ge - new_ssm_ge
new_ssm_ef = freq_ef - freq_c
freq_gf = 0.5*(freq_ge + freq_ef)
freq_gf_freq_c_diff = freq_gf - freq_c