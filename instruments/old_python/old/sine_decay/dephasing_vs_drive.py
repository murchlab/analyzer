#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jun  6 19:18:04 2019

@author: P. M. Harrington
"""

import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import curve_fit
#import pylab as plt
from qutip import *


def sine_decay(time, freq, gamma, amplitude, phase, offset):
    return amplitude*np.exp(-gamma*time)*np.sin(time*freq + phase) + offset

Delta = -0.0025*2*np.pi
chi = -0.0005*2*np.pi
kappa = 0.015*2*np.pi
N = 25
nbar_list = np.linspace(0.05,0.505,21)
times = np.linspace(0,500,201)

#
Gamma_d_vs_nbar_ideal = 1e3*8*chi**2*nbar_list/kappa
freq_vs_nbar_ideal = 1e3*(chi*nbar_list + Delta)/(2*np.pi)

# intial state
xp = (basis(2,0)+basis(2,1))/np.sqrt(2)
psi0_qubit = ket2dm(xp)
psi0_cavity = ket2dm(basis(N,0))
psi0 = tensor(psi0_cavity, psi0_qubit)

# operators
a  = tensor(destroy(N), qeye(2))
sm = tensor(qeye(N), destroy(2))
sz = tensor(qeye(N), sigmaz())
sx = tensor(qeye(N), sigmax())
sy = tensor(qeye(N), sigmay())

# Hamiltonian
H0 = Delta*sz + chi*sz*(a.dag()*a - 0.5)

c_op_list = []
c_op_list.append(np.sqrt(kappa)*a)

op_list = []
op_list.append(sz)
op_list.append(sx)
op_list.append(sy)

guess_freq = 0.01
guess_gamma = 0.001
guess_amplitude = 1.0
guess_phase = np.pi/2
guess_offset = 0
guess_vals = [guess_freq, guess_gamma, guess_amplitude, guess_phase, guess_offset]

#
freq_vs_nbar = []
Gamma_d_vs_nbar = []
for nbar_step in range(len(nbar_list)):
    nbar = nbar_list[nbar_step]
    epsilon = np.sqrt(nbar*(kappa**2/4 + chi**2))
    #epsilon = np.sqrt(nbar*(kappa**2/4))
    H = H0 + epsilon*a + np.conj(epsilon)*a.dag()
    
    #
    output = mesolve(H, psi0, times, c_op_list, op_list)
    
    #
    x_vs_times = output.expect[1]
    
    #
    fit = curve_fit(sine_decay, times, x_vs_times, p0=guess_vals)
    guess_vals = fit[0]
    #data_first_guess = sine_decay(times, *p0)
    x_vs_times_fit = sine_decay(times, *fit[0])
    
    #
    freq_vs_nbar.append(1e3*fit[0][0]/(2*np.pi))
    Gamma_d_vs_nbar.append(1e3*fit[0][1])
    
    print([nbar, epsilon, 1e3*fit[0][1], Gamma_d_vs_nbar_ideal[nbar_step]])
    
    #"""
    #
    fig, ax = plt.subplots(figsize=(8,5))
    ax.plot(times, output.expect[0], label="z")
    ax.plot(times, output.expect[1], label="x")
    ax.plot(times, output.expect[2], label="y")
    ax.plot(times, x_vs_times_fit, label="x_fit")
    
    ax.legend()
    ax.set_xlabel('Time')
    ax.set_ylabel('Expectation value')
    
    plt.show()
    #"""

#
fig, ax = plt.subplots(figsize=(8,5))
ax.plot(nbar_list, freq_vs_nbar,
        linestyle='None', marker='+', label="Freq")
#ax.plot(nbar_list, freq_vs_nbar_ideal, label="chi*nbar+Delta")
ax.legend()
ax.set_xlabel('nbar')
ax.set_ylabel('Frequency (MHz)')

plt.show()

#
fig, ax = plt.subplots(figsize=(8,5))
ax.plot(nbar_list, Gamma_d_vs_nbar,
        linestyle='None', marker='+', label="Gamma_d")
ax.plot(nbar_list, Gamma_d_vs_nbar_ideal, label="8 chi^2 nbar/kappa")
ax.legend()
ax.set_xlabel('nbar')
ax.set_ylabel('Gamma_d (1/us)')

plt.show()


"""
fig, ax = plt.subplots(figsize=(8,5))
ax.plot(tlist, output.expect[0], label="Cavity")
ax.plot(tlist, output.expect[1], label="Atom excited state")
ax.legend()
ax.set_xlabel('Time')
ax.set_ylabel('Occupation probability')
ax.set_title('Vacuum Rabi oscillations');
"""