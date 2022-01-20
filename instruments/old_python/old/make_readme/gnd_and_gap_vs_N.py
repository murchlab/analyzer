#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Dec 14 14:24:43 2019

@author: P. M. Harrington
"""

from defs import *
import time
import csv

class Nop():
    pass

def make_plot(name, p, x_, y_, label_x, label_y, ylim_btm_zero):
    path_fig = p.path0  + "/" + name + ".pdf"
    path_table = p.path0 + "/" + name + ".txt"
    
    fig, ax = plt.subplots(figsize=(10,6))
    ax.plot(x_, y_, 'k.')
#    plt.xlim([0, *])
    plt.gca().set_xlim(left=0)
    if ylim_btm_zero:
        plt.gca().set_ylim(bottom=0)
    plt.xlabel(label_x)
    plt.ylabel(label_y)
    
    fig.savefig(path_fig)
    np.savetxt(path_table, list(zip(x_, y_)), fmt="%5.4f, %5.4f")
    
def plot_evals_vs_N(p, energy_gap):
    N_list = p.N
    
    fig, ax = plt.subplots(figsize=(10,6))
    ax.plot(1/N_list, energy_gap, 'k.')
    plt.xlim([0, 0.6])
    plt.ylim([0, 1.5])
    plt.xlabel("1/N")
    plt.ylabel("Energy gap")
    
    fig.savefig(p.path0 + "/" + "gap_vs_invN" + ".pdf")
    
def plot_gndOverN_vs_invNsqr(p, vals_vs_list):
    list_ = p.N
    
    fig, ax = plt.subplots(figsize=(10,6))
    ax.plot(1/list_**2, vals_vs_list/list_, 'k.')
    plt.xlim([0, 0.3])
#    plt.ylim([0, 1.5])
    plt.xlabel("1/N^2")
    plt.ylabel("Ground state energy / N")
    fig.savefig(p.path0 + "/" + "gnd_vs_invNsqr" + ".pdf")

def plot_string_order_vs_N(p, vals_vs_list):
    list_ = p.N
    
    fig, ax = plt.subplots(figsize=(10,6))
    ax.plot(1/list_, vals_vs_list, 'k.')
    plt.xlim([0, 0.6])
#    plt.ylim([0, 1.5])
    plt.xlabel("1/N")
    plt.ylabel("String order parameter")
    
    fig.savefig(p.path0 + "/" + "string_order_vs_invN" + ".pdf")

def save_csv(p, name, N_list, e_gnd, e_gap):
    path1 = p.path0 + "/" + name + ".txt"
    
    header = ("N_list", "e_gnd", "e_gap")
    table = list(zip(N_list, e_gnd, e_gap))
    
    table.insert(0, header)
    
#    fmt_ = "%5.4f, "*len(table[0])
#    fmt_ = fmt_[:-2]

#    file = open(, "w")
#    file.write("\n{}".format(header))
#    for line in table:
#        file.write("\n%s" % str(line))
#    file.close()
    f = open(path1, "w", newline="")
    writer = csv.writer(f)
    writer.writerows(table)
    
    
def main():
    evals_vs_N = []
    ekets_vs_N = []
    
    p = Nop()
    p.path0 = "gnd_and_gap_vs_N"
    
    #
    p.N = np.array(range(3, 8+1, 2))
    p.J = 1.0 #2*np.pi
    p.alpha = 0.0
    
    string_order = []
    
    #
    tic = time.time()
    for N in p.N:
        print("N: {}".format(N))
        
        #
        parameters = get_parameters(J = p.J, alpha = p.alpha, N = N)
        op, ops = get_operators(N = N)
        parameters.paths = make_dir_and_readme(parameters)
        make_readme(parameters)

        hamiltonian = get_hamiltonian(parameters, ops)
#        evals = hamiltonian.eigenenergies()
        evals, ekets = get_eigenstates(hamiltonian)
        
        string_order.append(expect(op.string_order, ekets[0]))
        
        evals_vs_N.append(evals)
        ekets_vs_N.append(ekets)
        
        toc = time.time()
        print("Elapsed time: {}".format(toc-tic))

    # ground state energy
    e_gnd = []
    for evals in evals_vs_N:
        e_gnd.append(evals[0])
        
    make_plot("gndOverN_vs_invNsqr", p, 
              1/p.N**2, -1.0*(e_gnd/p.N), 
              "1/N^2", " - Ground state energy / N", True)
    
    # energy_gap
    e_gap = []
    for evals in evals_vs_N:
        e_gap.append(evals[1] - evals[0])
    
    plot_evals_vs_N(p, e_gap)
    make_plot("gap_vs_invN", p, 
              1/p.N, e_gap, 
              "1/N", "Energy gap", True)
    
    make_plot("gapOverN_vs_invN", p, 
              1/p.N, e_gap/p.N, 
              "1/N", "Energy gap / N", True)
    
    make_plot("gapOverN_vs_invNsqr", p, 
              1/p.N**2, e_gap/p.N, 
              "1/N^2", "Energy gap / N", True)
    
    # string order parameter
    make_plot("string_order_vs_invN", p, 
              1/p.N, string_order, 
              "1/N", "String order parameter", True)
    
    # save data to table
    save_csv(p, "table", p.N, e_gnd, e_gap)
    
    return (p, evals_vs_N, ekets_vs_N)

if __name__ == "__main__":
    list_, e, h = main()