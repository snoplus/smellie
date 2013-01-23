#Written by Christopher Jones 11/01/2013
#Used to control fibre switch

import serial

def SetFSChannel(channel_number):
    # greater than 70 will not be accepted
    # think about valid channels
    ser = serial.Serial(0,57600)  # open first serial port, 57600 is the baud rate
    print ser.portstr       # check which port was really used
    ser.write("ch"+str(channel_number))      # write to channel number
    ser.write("\r\n")      # executes the previously written number
    ser.close()             # close port
    return

