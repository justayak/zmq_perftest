import datetime
import zmq
import numpy

def perf_start():
    return datetime.datetime.now()

def perf_end(perf_start):
    end = datetime.datetime.now()
    diff = end - perf_start
    return (diff.seconds, diff.microseconds)

def zmq_pair(server=True):
    port = "5556"
    context = zmq.Context()
    socket = context.socket(zmq.PAIR)
    if server:
        socket.bind("tcp://*:%s" % port)
    else:
        socket.connect("tcp://localhost:%s" % port)
    return socket

def ping(socket):
    socket.send_string("ping")

def await_ping(socket):
    socket.recv_string()

def send_array(socket, A, flags=0, copy=True, track=False):
    md = dict(
        dtype = str(A.dtype),
        shape = A.shape,
    )
    socket.send_json(md, flags|zmq.SNDMORE)
    socket.send(A, flags, copy=copy, track=track)

def recv_array(socket, flags=0, copy=True, track=False):
    md = socket.recv_json(flags=flags)
    msg = socket.recv(flags=flags, copy=copy, track=track)
    buf = memoryview(msg)
    print("h")
    A = numpy.frombuffer(buf, dtype=md['dtype'])
    return A.reshape(md['shape'])
