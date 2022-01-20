#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on 14 December 2019

@author: P. M. Harrington
"""

from defs import *

def main():
    parameters = []
    vals = []
    evals = []
    ekets = []
    
    #
    parameters = get_parameters(J = 2*np.pi, alpha = 0.0, N = 4)
    parameters.paths = make_dir_and_readme(parameters)
    make_readme(parameters)
    
    #
    op, ops = get_operators(N = parameters.N)
    hamiltonian = get_hamiltonian(parameters, ops)
    evals, ekets = get_eigenstates(hamiltonian)
    
    make_plot_evals(evals)
    
    
#    vals = get_expectation_values(parameters, op, ops, evals, ekets)
#    make_plots(parameters, vals, evals, ekets)
    
    return (parameters, vals, evals, ekets)

if __name__ == "__main__":
    main()