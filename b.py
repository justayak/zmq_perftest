import shared
print("b")

socket = shared.zmq_pair(server=False)

while True:
    print("waiting for send..")
    A = shared.recv_array(socket)
    shared.ping(socket)
