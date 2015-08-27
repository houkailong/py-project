__author__ = 'user'
import zmq
import time
import os,sys

try:
    pid = os.fork()
    if pid > 0:
        sys.exit(0)
except OSError,e:
    sys.exit(1)
os.chdir('/')
os.umask(0)
os.setsid()

try:
    pid = os.fork()
    if pid > 0:
        sys.exit(0)
except OSError,e:
    sys.exit(1)

context = zmq.Context(1)
socket = context.socket(zmq.REP)
socket.bind('tcp://127.0.0.1:8888')
while True:
    message = socket.recv_json()
    print 'received request:',message
    time.sleep(1)
    socket.send_json('world')
