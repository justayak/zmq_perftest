import datetime
import zmq
import numpy
import math

COPY = True
context = zmq.Context()

def convert_size(size):
    size_name = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
    i = int(math.floor(math.log(size,1024)))
    p = math.pow(1024,i)
    s = round(size/p,2)
    if (s > 0):
        return '%s %s' % (s,size_name[i])
    else:
        return '0B'


def perf_start():
    return datetime.datetime.now()

def perf_end(perf_start):
    end = datetime.datetime.now()
    diff = end - perf_start
    return (diff.seconds, diff.microseconds)

def zmq_pair(server=True):
    port = "5556"
    socket = context.socket(zmq.PAIR)
    if server:
        socket.bind("inproc://#1")
        #socket.bind("inproc://127.0.0.1")
        #socket.bind("tcp://*:%s" % port)
    else:
        socket.connect("inproc://#1")
        #socket.connect("inproc://127.0.0.1")
        #socket.connect("tcp://localhost:%s" % port)
    return socket

def ping(socket):
    socket.send_string("ping")

def await_ping(socket):
    socket.recv_string()

def send_array(socket, A, flags=0, copy=COPY, track=False):
    md = dict(
        dtype = str(A.dtype),
        shape = A.shape,
    )
    socket.send_json(md, flags|zmq.SNDMORE)
    socket.send(A, flags, copy=copy, track=track)

def recv_array(socket, flags=0, copy=COPY, track=False):
    md = socket.recv_json(flags=flags)
    msg = socket.recv(flags=flags, copy=copy, track=track)
    buf = memoryview(msg)
    print("h")
    A = numpy.frombuffer(buf, dtype=md['dtype'])
    return A.reshape(md['shape'])
