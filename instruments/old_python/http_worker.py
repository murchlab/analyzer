from http.server import BaseHTTPRequestHandler, HTTPServer
import numpy as np
import multiprocessing
import threading


def send_data(a):

    hostname = "localhost"
    hostport = 31416

    a_shape = np.array2string(np.asarray(a.shape), separator=';', max_line_width=np.NaN)
    a = np.transpose(a, np.flip(range(len(a.shape))))
    a_shape = a_shape[1:-1]
    a_flat = a.flatten()
    # a_string = np.array2string(a_flat, separator=';', max_line_width=np.NaN, floatmode='maxprec', threshold=sys.maxsize)
    a_string = ';'.join([np.format_float_scientific(num) for num in a_flat])
    print(123)
    # a_string = a_string[1:-1]
    bytedata = (a_shape + ',' + a_string).encode("utf-8")

    class MyServer(BaseHTTPRequestHandler):

        def do_GET(self):
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            self.wfile.write(bytedata)

    myserver = HTTPServer((hostname, hostport), MyServer)

    # myserver.handle_request()
    class HTTPThread(threading.Thread):
        def run(self):
            print("Starting ")
            myserver.serve_forever()
            myserver.server_close()
            print("Exiting ")

    # def http_process():
    #     print("Starting ")
    #     myserver.serve_forever()
    #     myserver.server_close()
    #     print("Exiting ")

    thread1 = HTTPThread()
    thread1.start()
    # p = multiprocessing.Process(target=http_process)
    # p.start()


a = np.random.rand(100, 1000)
send_data(a)
exit()
