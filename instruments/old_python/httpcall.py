import os
import sys
import threading
import subprocess
from subprocess import Popen
import zmq
import json
import time
import win32gui, win32con
from urllib.parse import unquote


def http_call_pyhost(module, function):
    zmq_port = 27183

    try:
        process = Popen(['python', r'C:\Users\crow104\Documents\Python Scripts\python_interface\python\pyhost.py'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    except:
        pass

    #  Socket to talk to the pyhost.py
    context = zmq.Context()
    socket = context.socket(zmq.REQ)
    socket.connect("tcp://localhost:" + str(zmq_port))

    # host_init()
    method = 'HTTP'
    call_dict = {'method': method, 'module': module, 'function': function}
    call_json = json.dumps(call_dict)

    socket.send(call_json.encode('utf-8'))

    #  Get the reply.
    message = socket.recv()
    print(message)
    exit()


if __name__ == "__main__":
#    Minimize = win32gui.GetForegroundWindow()
#    win32gui.ShowWindow(Minimize, win32con.SW_MINIMIZE)
    if len(sys.argv) == 3:
       module = unquote(sys.argv[1])
       function = unquote(sys.argv[2])
       print(module)
       print(function)
    else:
        module = r"C:\Users\crow104\Documents\Python Scripts\python_interface\python\test_module.py"
        function = r"rand(200, 300)"
    http_call_pyhost(module, function)
