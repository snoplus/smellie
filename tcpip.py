import time,sys
import SmellieRS as rs
from socket import *                    # get socket constructor and constants
myHost = ''                             # server machine, '' means local host
myPort = 50007                          # listen on a non-reserved port number

sockobj = socket(AF_INET, SOCK_STREAM)       # make a TCP socket object
sockobj.bind((myHost, myPort))               # bind it to server port number 
sockobj.listen(5)                            # listen, allow 5 pending connects

while 1:                                     # listen until process killed
    connection, address = sockobj.accept()   # wait for next client connect
    print 'Server connected by', address     # connection is a new socket
    while 1:
        data = connection.recv(1024)         # read next line on client socket
        print data 
        rs.SetRSChannel(int(data))
        if not data: break                   # send a reply line to the client
        connection.send('different' + str(data))     # until eof when socket closed
        print "here"
        if data: break
    connection.close()
    sys.exit()



        
