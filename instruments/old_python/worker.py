#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Nov 16 19:41:39 2019

@author: crow104

This script exists to 
"""
import sys, time, os
import numpy as np
import matplotlib.pyplot as plt
import fileinput
import json
import importlib.util
import ntpath
import base64


def main(json_data=None):

    def call_python(dict_data):
        module_path = dict_data['module']
        _, module_name = ntpath.split(module_path)
        module_name = module_name.rstrip('.py')
        spec = importlib.util.spec_from_file_location(module_name, module_path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        eval_str = 'module.' + dict_data['function'] + '('
        first_arg = True
        for argument in dict_data['arguments']:
            arg = argument['0']
            val = argument['1']
            # print((arg, val))
            if not first_arg:
                eval_str += ', '
            else:
                first_arg = False
            if arg:
                eval_str += arg + '='
            eval_str += str(val)
        eval_str += ')'
        result = eval(eval_str)
        json_result = json.dumps({'result': result.tolist()})
        print(json_result)

    if json_data:
        data = json.loads(json_data)
        call_python(data)
        return

    if len(sys.argv) == 2:
        json_data = sys.argv[1]
        base64_bytes = json_data.encode('utf-8')
        json_data_bytes = base64.b64decode(base64_bytes)
        json_data = json_data_bytes.decode('utf-8')
        data = json.loads(json_data)
        call_python(data)
        return

    for line in fileinput.input():
        data = json.loads(line)
        call_python(data)
    
##END main
    
if __name__ == '__main__':
    main()

