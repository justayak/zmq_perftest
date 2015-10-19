import shared
import threading

def do_stuff():
    print("b")

    socket = shared.zmq_pair(server=False)

    while True:
        print("waiting for send..")
        A = shared.recv_array(socket)
        shared.ping(socket)

def run():
    t = threading.Thread(target=do_stuff)
    t.start()
