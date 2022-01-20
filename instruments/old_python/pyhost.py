from http.server import BaseHTTPRequestHandler, HTTPServer
import numpy as np
import threading
import time
import zmq
import json
import ntpath
import importlib.util

zmq_port = 27183
http_port = 31416
timeout = 120000     # Timeout in ms
http_timeout = 120     # Timeout in s


context = zmq.Context()
socket = context.socket(zmq.REP)
socket.RCVTIMEO = timeout
socket.bind("tcp://*:" + str(zmq_port))


def send_data(a):

    a_shape = np.array2string(np.asarray(a.shape), separator=';', max_line_width=np.NaN)
    a = np.transpose(a, np.flip(range(len(a.shape))))
    a_shape = a_shape[1:-1]
    a_flat = a.flatten()
    a_string = ';'.join([np.format_float_scientific(num) for num in a_flat])
    bytedata = (a_shape + ',' + a_string).encode("utf-8")

    class MyServer(BaseHTTPRequestHandler):
        def do_GET(self):
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            self.wfile.write(bytedata)

    myserver = HTTPServer(("localhost", http_port), MyServer)
    myserver.timeout = http_timeout

    class HTTPThread(threading.Thread):
        def run(self):
            print("Starting ")
            myserver.handle_request()
            # myserver.serve_forever()
            myserver.server_close()
            print("Exiting ")

    thread1 = HTTPThread()
    thread1.start()
    socket.send('Finished'.encode("utf-8"))
    return thread1


while True:
    try:
        message = socket.recv()
        print(message)
        if message == 'status'.encode('utf-8'):
            print("status: idle")
            socket.send('idle'.encode('utf-8'))
        else:
            call_json = message.decode('utf-8')
            call_dict = json.loads(call_json)
            module_path = call_dict['module']
            _, module_name = ntpath.split(module_path)
            module_name = module_name.rstrip('.py')
            spec = importlib.util.spec_from_file_location(module_name, module_path)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            eval_str = 'module.' + call_dict['function']
            result = eval(eval_str)
            thread1 = send_data(result)
            thread1.join()
    except zmq.error.Again:
        print("Timeout")
        socket.close()
        break
