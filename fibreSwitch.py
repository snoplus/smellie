# Commands to Control the Fibre Switch
# Written by Christopher Jones (11/01/2013)
# Additional changes by Ian Coulter (23/01/2013) and Krish Majumdar (24/01/2013)

import serial


def SetFSChannel(channel_number):
    # invalid channel_number values will not be accepted
    if (channel_number < 1) or (channel_number > 70):
        print "The channel number is not valid - it must between 1 and 70 inclusive."

    ser = serial.Serial(0,57600)				# open first serial port, 57600 is the baud rate
    print ser.portstr							# check which port was really used
    ser.write("ch" + str(channel_number))		# write the command to change channel number
    ser.write("\r\n")							# executes the previously written command
    ser.close()									# close serial port
    return


def SetIOChannels(input_channel, output_channel):
    # invalid input_channel values will not be accepted
    if (input_channel < 1) or (input_channel > 5):
        print "The input channel is not valid - it must be between 1 and 5 inclusive."

    # invalid output_channel values will not be accepted
    if (output_channel < 1) or (output_channel > 14):
        print "The output channel is not valid - it must be between 1 and 14 inclusive."

    # calculate the correct channel number from the given input and output channels
    channel_number = ((input_channel - 1) * 14) + output_channel

    ser = serial.Serial(0,57600)				# open first serial port, 57600 is the baud rate
    print ser.portstr							# check which port was really used
    ser.write("ch" + str(channel_number))		# write the command to change channel number
    ser.write("\r\n")							# executes the previously written command
    ser.close()									# close serial port
    return
