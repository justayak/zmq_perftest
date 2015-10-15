import shared
import numpy as np

print ("start {a}")


socket = shared.zmq_pair()

# create a "video"-stream
stream = []
for i in range(0, 1000):
    stream.append(np.random.rand(1024, 768))

print("send images:")

# measure the transform and sending
perf = []

for image in stream:
    start = shared.perf_start()
    shared.send_array(socket, image)
    shared.await_ping(socket)
    perf.append(shared.perf_end(start))
    

total_micro = 0
for p in perf:
    if (p[0] > 0):
        raise "Nope"
    else:
        total_micro = total_micro + p[1]

print ("a finished: sec:" + str(total_micro / len(perf)))
