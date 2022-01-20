#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Dec 14 12:28:07 2019

@author: P. M. Harrington
"""

import numpy as np
from qutip import *
import matplotlib.pyplot as plt
import os
from datetime import datetime
    
class Nop:
    pass

def get_parameters(J = 2*np.pi, alpha = 0., N = 4):
    parameters = Nop()
    parameters.N = N
    parameters.J = J
    parameters.J_nnn = alpha*J
    parameters.boundary = "periodic" #"open"
    parameters.save_files = False
    parameters.label = "axx_nnn0p5"
    parameters.time_start = datetime.now()
    
    return parameters
    
def make_dir_and_readme(parameters):
    paths = Nop()
    
    paths.cwd = os.getcwd()
    paths.parent = (paths.cwd + "/" + parameters.label +
                       "_" + parameters.boundary)
    
    paths.figs = paths.parent + "/" + "figs"
    paths.tables = paths.parent + "/" + "tables"
    
    if (not os.path.isdir(paths.parent)):
        os.mkdir(paths.parent)
        
    for p in [paths.figs, paths.tables]:
        if (not os.path.isdir(p)):
            os.mkdir(p)
    
    return paths
    
def make_readme(parameters):
    paths = parameters.paths
    
    paths.readme = paths.parent + "/" + "readme.txt"
    if (not os.path.exists(paths.readme)):
        file = open(paths.readme, "w") 
    else:
        file = open(paths.readme, "a")
        file.write("\n\n")
    
    p = parameters        
    file.write("# " + p.label + "\n")
    file.write(p.time_start.strftime("%Y%m%d_%H%M%S"))
    file.write("\nboundary, {}".format(p.boundary))
    file.write("\nN, {}".format(p.N))
    file.write("\nJ, {}".format(p.J))
    file.close()
    
def get_basic_operators(N = 4):
    ops = Nop()
    
    Szero = qzero(3)
    Seye = qeye(3)
    Sm = (spin_Jx(1)+1j*spin_Jy(1))/2
    Sz = spin_Jz(1)
    Sx = spin_Jx(1)
    Sy = spin_Jy(1)
    
    """
    Szero = qzero(2)
    Seye = qeye(2)
    Sm = destroy(2)
    Sz = sigmaz()
    Sx = sigmax()
    Sy = sigmay()
    """
    
    ops.Szero = []
    ops.Seye = []
    ops.Sm = []
    ops.Sz = []
    ops.Sx = []
    ops.Sy = []
   
    ops.Szero = []
    ops.Seye = []
    for n in range(N):
        op_list = []
        for m in range(N):
            op_list.append(Szero)

        op_list[n] = Szero
        ops.Szero.append(tensor(op_list))
        
        op_list[n] = Seye
        ops.Seye.append(tensor(op_list))
        
    for n in range(N):
        op_list = []
        for m in range(N):
            op_list.append(Seye)

        op_list[n] = Seye
        ops.Seye.append(tensor(op_list))
        
        op_list[n] = Sm
        ops.Sm.append(tensor(op_list))
    
        op_list[n] = Sz
        ops.Sz.append(tensor(op_list))
        
        op_list[n] = Sx
        ops.Sx.append(tensor(op_list))
        
        op_list[n] = Sy
        ops.Sy.append(tensor(op_list))
        
    return ops
     
def get_operators(N = 4):
    ops = get_basic_operators(N)
    op = Nop()
    
    # create the string operator
    op.string_order = ops.Sz[0]
    for k in range(N-1):
        op.string_order = op.string_order*(1j*np.pi*ops.Sz[k+1]).expm()    
    op.string_order = op.string_order*ops.Sz[N-1]
    
    # total spin operator for each site
    ops.Ssqr = []
    for n in range(N):
        ops.Ssqr.append(
                ops.Sx[n]*ops.Sx[n] + 
                ops.Sy[n]*ops.Sy[n] +
                ops.Sz[n]*ops.Sz[n])
        
    # spin-spin operators for each bond (nearest neighbor))
    ops.SdotS = []
    ops.Sxy = []
    for n in range(N):
        if (n==(N-1)):
            i = n
            j = 0
        else:
            i = n
            j = n+1
            
        ops.SdotS.append(
            ops.Sx[i]*ops.Sx[j] + 
            ops.Sy[i]*ops.Sy[j] +
            ops.Sz[i]*ops.Sz[j])
        
        ops.Sxy.append(
            0.5*(ops.Sm[i]*ops.Sm[j].dag() + ops.Sm[i].dag()*ops.Sm[j]))
        
    # spin-spin operators for each bond (next nearest neighbor))
    ops.SdotS = []
    ops.Sxy_nnn = []
    for n in range(N):
        if (n==(N-2)):
            m = 0
        elif (n==(N-1)):
            m = 1
        else:
            m = n+2
        
        ops.Sxy_nnn.append(
            ops.Sm[n]*ops.Sm[m].dag() + ops.Sm[n].dag()*ops.Sm[m])
    
    return (op, ops)

def get_hamiltonian(parameters, ops):
    J = parameters.J
    J_nnn = parameters.J_nnn
    
    if parameters.boundary == "open":
        num_terms = parameters.N - 1
    elif parameters.boundary == "periodic":
        num_terms = parameters.N

    # construct the hamiltonian
    hamiltonian = 0
    
    for n in range(num_terms):
        hamiltonian += J*ops.Sxy[n] + J_nnn*ops.Sxy_nnn[n]
    
    return hamiltonian

def get_eigenstates(hamiltonian):
    evals, ekets = hamiltonian.eigenstates()

    return (evals, ekets)

def get_expectation_values(parameters, op, ops, evals, ekets):
    N = parameters.N
    vals = Nop()
    
    vals.string_order = []
    vals.Sz = []
    vals.mutual_info = []
    vals.entropy_vn = []
    for ket in ekets:
        #
        vals.string_order.append(expect(op.string_order, ket))
        
        #
        vals.Sz.append(expect(ops.Sz, ket))
        
        #
        v = entropy_mutual(
                ket2dm(ket), range(0, N//2), range(N//2, N))
        vals.mutual_info.append(v)
        
        #
        v = entropy_vn(ket.ptrace(
                [k for k in range(N) if (k is not N//2)]))
        vals.entropy_vn.append(v)
        
    return vals

def make_plot_evals(evals):
    # energy levels
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.plot(evals, '.')
    plt.ylabel('Energy eigenvalues')
    
def make_plots(parameters, vals, evals, ekets):
    path_figs = parameters.paths.figs
    N = parameters.N

    # Sz
    fig, ax = plt.subplots(figsize=(10, 6))
    legend_str = []
    for k in range(4):
        ax.plot(vals.Sz[k])
        legend_str.append("{}, {:+f}".format(k, evals[k]))
    plt.ylim((-1, +1))
    plt.ylabel(['Sz'])
    plt.legend(legend_str)

    if parameters.save_files:
        fig.savefig(path_figs + "/fig_" + "sz" + ".pdf")

    # string order parameter
    fig, ax = plt.subplots(figsize=(10,6))
    ax.plot(vals.string_order)
    plt.ylim((-1, +1))
    plt.ylabel('string order parameter')
    
    if parameters.save_files:
        fig.savefig(path_figs + "/fig_" + "str" + ".pdf")
        
    # mutual information, chain ends
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.plot(vals.mutual_info)
    plt.ylabel('Mutual information, chain ends')

    if parameters.save_files:
        fig.savefig(path_figs + "/fig_" + "mi" + ".pdf")
        
    # entropy, reduced density matrix at N//2
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.plot(vals.entropy_vn)
    plt.ylabel('von Neumann entropy, N//2')

    if parameters.save_files:
        fig.savefig(path_figs + "/fig_" + "mi" + ".pdf")
      
    # energy levels
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.plot(evals, '.')
    plt.ylabel('Energy eigenvalues')
    
    # qubism plot
    if ((-1)**N == 1):
        fig, ax = plt.subplots(2, 2, figsize=(8,8))
        ax = ax.flat
            
        for k in range(4):
            plot_qubism(ekets[k], ax=ax[k])
            ax[k].title.set_text("{}, {:+f}".format(k, evals[k]))
        
        plt.savefig(path_figs + "/fig_" + "states" + ".png") 