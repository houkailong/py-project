__author__ = 'user'
import zmq
context = zmq.Context()
print 'connecting to hello worlld server.........'
socket = context.socket(zmq.REQ)
socket.connect('tcp://127.0.0.1:8888')
for request in range(1,10):
    print 'sending request',request,'...........'
    a={3:['a','b'],4:('a','b')}
    socket.send_json(a)
    message = socket.recv_json()
    print 'recvived reply',request,'[',message,']'
