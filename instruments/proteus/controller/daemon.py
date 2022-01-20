# NOTE, this will continuously run an asynchronous server session.
#   stop with command: daemon.request('stop')
    
import time
import zmq
import datetime
import numpy as np
import sys
import os
import subprocess
import pathlib
import ctypes
import win32process
import pickle
import json
#import threading

self_path = str(pathlib.Path(__file__).parent.absolute())
if self_path not in sys.path:
    sys.path.append(self_path)

import configtools

config = configtools.read_config()
PORT = config["PORT"]
TIMEOUT = config["TIMEOUT"]
HIDE_CLI_WINDOW = config["HIDE_CLI_WINDOW"]
verbose = config["VERBOSE"]


socket = None
in_cmd = True
proteus = None
kill_signal = False
restart_signal = False

def logger(msg):
    if verbose:
        print('[' + str(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')) + '] ' + str(msg))
    
def hide_cli_window():
    global in_cmd
    hwnd = ctypes.windll.kernel32.GetConsoleWindow()      
    if hwnd != 0:      
        ctypes.windll.user32.ShowWindow(hwnd, 0)
        ctypes.windll.kernel32.CloseHandle(hwnd)
        if in_cmd:
            _, pid = win32process.GetWindowThreadProcessId(hwnd)
            os.system('taskkill /PID ' + str(pid) + ' /f')
            in_cmd = False


def show_cli_window():
    hwnd = ctypes.windll.kernel32.GetConsoleWindow()      
    if hwnd != 0:      
        ctypes.windll.user32.ShowWindow(hwnd,10)      
        ctypes.windll.kernel32.CloseHandle(hwnd)
    
    
def run_python_file(python_file):
    # Make sure there's no blanckspace in the path
    run_with_conda_env_bat = "run_with_conda_env.bat"
    dirname = pathlib.Path(__file__).parent.absolute()
    run_with_conda_env_bat = str(dirname.joinpath(run_with_conda_env_bat))
    command = "start cmd /C " + '""'+ run_with_conda_env_bat + '" '
    command += "python "
    file = python_file.split()[0]
    args = python_file.lstrip(file)
    if os.path.isabs(file):
        command += '"' + file + '"' + args
    else:
        command += '"' + str(dirname.joinpath(file)) + '"'+ args
    command += '"'
    subprocess.Popen(command, shell=True)


def request(msg):
    if not is_running():
        start_daemon()
    is_str = isinstance(msg, str)
    if is_str:
        msg = msg.encode('utf-8')
    client_context = zmq.Context()
    client_socket = client_context.socket(zmq.REQ)
    client_socket.RCVTIMEO = TIMEOUT
    client_socket.connect(f"tcp://localhost:{PORT}")
    client_socket.send(msg)
    rep = None
    try:
        rep = client_socket.recv()
        if is_str:
            rep = rep.decode('utf-8')
    except:
        rep = b'timeout'
        if is_str:
            rep = "timeout"
    return rep


def is_running():
    try:
        context = zmq.Context()
        socket = context.socket(zmq.REP)
        socket.bind(f"tcp://127.0.0.1:{PORT}")
        socket.close()
        return False
    except zmq.error.ZMQError:
        return True


def reply(message):
    socket.send(message, zmq.NOBLOCK)
    

def parser(message):
    message = message.lstrip(b' ')
    space_start = 0
    space = b' '[0]
    for byte in message:
        if byte == space:
            break
        else:
            space_start += 1
    return message[:space_start], message[space_start:].lstrip(b' ')


def data_pack(data, method='pickle'):
    if method == 'pickle':
        data_pickle = pickle.dumps(data)
        return b'pickle=' + data_pickle
    elif method == 'json':
        data_json = json.dumps(data).encode('utf-8')
        return b'json=' + data_json
    else:
        return b''
    
    
def data_unpack(message):
    if message[:7] == b'pickle=':
        message = message.lstrip(b'pickle=')
        return pickle.loads(message)
    elif message[:5] == b'json=':
        message = message.lstrip(b'json=')
        return json.loads(message.decode('utf-8'))
    else:
        return {}


def handler(message):
    
    def start_fun():
        reply(b"Daemon is already running.")
        logger("Daemon is already running.")
    
    def stop_fun():
        global kill_signal
        reply(b"Stopping...")
        logger("Stopping...")
        kill_signal = True
        
    def restart_fun():
        global kill_signal
        global restart_signal
        reply(b"Restarting...")
        logger("Restarting...")
        kill_signal = True
        restart_signal = True
        
    def cli_fun(arg):
        global verbose
        if arg == b'show':
            show_cli_window()
            reply(b"no error")
        elif arg == b'hide':
            hide_cli_window()
            reply(b"no error")
        elif arg == b'verbose on':
            verbose = True
            reply(b"no error")
        elif arg == b'verbose off':
            verbose = False
            reply(b"no error")
        else:
            reply(b"missing argument")
            
    def proteus_fun(arg):
#        try:
#            thread = threading.Thread(target=proteus.handler, args=(data_unpack(arg),))
#        except Exception as e:
#            print(e)
        try:
            rep = proteus.handler(data_unpack(arg))
            reply(rep.encode('utf-8'))
        except Exception as e:
            print(e)
#        reply("no error.".encode('utf-8'))
        
    fun_dict = {
        b'start': start_fun,
        b'stop': stop_fun,
        b'restart': restart_fun,
        b'cli': lambda: cli_fun(arg),
        b'proteus': lambda: proteus_fun(arg)
    }
    
    kw, arg = parser(message)
    
    try:
        fun_dict[kw]()
    except Exception as err:
        reply(str(err).encode('utf-8'))
        logger(str(err))
        

def mainloop():
    while not kill_signal:
        #  Wait for next request from client
        message = socket.recv()
        logger(f"Received request: {message[:40]}")
        handler(message)
        
    
    socket.close()
    proteus.close()
    if restart_signal:
        start_daemon(delay=1)
        

# Initializing the zmq interface
def start_daemon(daemonized=True, delay=0):
    global socket
    global in_cmd
    global proteus
    if delay:
        time.sleep(delay)
    if daemonized:
        run_python_file("daemon.py start")
    else:
        in_cmd = False
        
        try:
            from proteusapi import Proteus
            proteus = Proteus()
        except Exception as err:
            logger(str(err))
        
        try:
            context = zmq.Context()
            socket = context.socket(zmq.REP)
            socket.bind(f"tcp://127.0.0.1:{PORT}")
            logger("Daemon started.")
            if HIDE_CLI_WINDOW:
                hide_cli_window()
            mainloop()
            socket.close()
        except zmq.error.ZMQError:
            logger("Daemon is already running.")


if __name__ == "__main__":
    if len(sys.argv) == 1:
        if is_running():
            logger("Daemon is already running.")
        else:
            start_daemon()
    elif sys.argv[1] == "start":
        start_daemon(daemonized=False)
    else:
        request(' '.join(sys.argv[1:]))

