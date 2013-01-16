#Written by Christopher Jones to control a Fibre Switch using an RS323 Serial Port

import serial

def SetFSChannel(channel_number):
    # greater than 70 will no be accepted
    # think about valid channels
    ser = serial.Serial(0,57600)  # open first serial port, 57600 is the baud rate
    print ser.portstr       # check which port was really used
    ser.write("ch"+str(channel_number))      # write to channel number
    ser.write("\r\n")      # executes the previously written number
    ser.close()             # close port
    return

