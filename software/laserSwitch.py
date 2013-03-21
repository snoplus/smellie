# Commands to Control the Laser Switch
# Written by Christopher Jones (09/01/2013)
# Additional changes by Krish Majumdar (24/01/2013, 05/03/2013)
# This requires the LabJackPython Software that has been adapted to work on a Windows 7 64-bit machine: https://github.com/labjack/LabJackPython
# Please check the u12SMELLIE.py script for more details

import u12SMELLIE, time
d = u12SMELLIE.U12()


# Increment the selected channel by 1 ... pulse the channel-up bit on the LabJack
def ChannelUp():    
    d.eDigitalOut(1,1)	# Raises D1
    d.eDigitalOut(1,0)	# Lowers D1
    d.eDigitalOut(1,1)	# Raises D1


# Execute and switch the active channel to the selected one ... pulse the execute-bit on the LabJack
def Execute():    
    d.eDigitalOut(0,1)	# Raises D0
    d.eDigitalOut(0,0)	# Lowers D0
    d.eDigitalOut(0,1)	# Raises D0
    time.sleep(30)      # The SEPIA Unit needs a short amount of time to fully power up 


# Return the channel as shown on the Laser Switch front panel's 8-segment display
def GetSelectedChannel():
    def invert(bit):
        if (bit == 0):
            bit = 1
            return bit
        elif(bit == 1):
            bit = 0
            return bit 
        else:
            return "Laser Switch (Get Selected Channel) - Invalid input ... check connections to and from the Laser Switch."
		    
    channel = invert(d.eDigitalIn(2)) + (2.0 * float(invert(d.eDigitalIn(3)))) + (4.0 * float(invert(d.eDigitalIn(4))))
    return int(channel)


# Return the currently active channel as shown on the Laser Switch front panel's LEDs
def GetActiveChannel():
    def invert(bit):
        if (bit == 0):
            bit = 1
            return bit
        elif(bit == 1):
            bit = 0
            return bit 
        else:
            return "Laser Switch (Get Active Channel) - Invalid input ... check connections to and from the Laser Switch."
		    
    channel = invert(d.eDigitalIn(5)) + (2.0 * float(invert(d.eDigitalIn(6)))) + (4.0 * float(invert(d.eDigitalIn(7))))
    return int(channel)


# Set the channel that will be shown on the Laser Switch front panel's 8-segment display
def SetSelectedChannel(picked_channel):
    if (picked_channel >= 6) or (picked_channel < 0):
        print "Laser Switch (Set Selected Channel) - The channel number is not valid ... it must be between 0 and 5 inclusive."
        return 0 
    else:
        current_display_channel = GetSelectedChannel()
        while (picked_channel != current_display_channel):
            ChannelUp()
            current_display_channel = GetSelectedChannel()
        return


# Check if the channel switching is in progress or not
def CheckExecution():
    manual_execution_flag = d.eDigitalIn(8)
    # Note: If the argument UpdateDigital is "True", then new values are sent 
    if (manual_execution_flag == 1):
	    print "Laser Switch (Check Execution) - Execution in Progress"
	    return  
    else:
	    print "Laser Switch (Check Execution) - Execution not in Progress"
	    return  
