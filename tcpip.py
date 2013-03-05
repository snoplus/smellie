# Commands to Control the TCP/IP Communication
# Written by Christopher Jones (23/01/2013)
# Additional changes by Krish Majumdar (01/03/2013, 05/03/2013)

import time, sys
import laserSwitch as rs
from socket import *        # get socket constructor and constants
myHost = ''                 # initialise the server machine ('' means: local host)
myPort = 50007              # listen on a non-reserved port number


sockobj = socket(AF_INET, SOCK_STREAM)    # make a TCP socket object
sockobj.bind(myHost, myPort)              # bind the socket object to the specified server and port number 
sockobj.listen(5)                         # begin listening, and allow 5 pending connects

while 1:                                                  # listen until process killed
    connection, address = sockobj.accept()                # wait for next client connection
    print 'TCP/IP () - Server connected by' + address     # connection is a new socket
    
	while 1:
        data = connection.recv(1024)                 # read the next line on client socket
        print 'TCP/IP () - Data: ' + data 
        rs.SetSelectedChannel(int(data))
        if not data: break                           # send a reply line to the client
        connection.send('different' + str(data))     # keep sending until reach the end of file

        if data: break
    
	connection.close()                               # once the end of file is reached, the socket is closed
    sys.exit()
