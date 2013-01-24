# Written by Christopher Jones 9/01/2013 email:christopher.jones@physics.ox.ac.uk
# This requires the LabJackPython Software that has been adapted to work for a Windows 7 64-bit machine
# Please Check the u12SMELLIE.py script for more details  

import u12SMELLIE,time
 
d = u12SMELLIE.U12()

# Pulses the channel up bit on the LabJack
def ChannelUp():    
    #Raises D1
    d.eDigitalOut(1,1)
    #Lowers D1
    d.eDigitalOut(1,0)
    #Raises D1
    d.eDigitalOut(1,1)

# Pulses the execute bit on the LabJack
def Execute():    
    #Raises D0
    d.eDigitalOut(0,1)
    #Lowers D0
    d.eDigitalOut(0,0)
    #Raises D0
    d.eDigitalOut(0,1)
    time.sleep(30)      ##time for sepia to power up 


#gets the channel displayed on the Fibre Switch 
def GetDisplayChannel():
    
    def invert(bit):
        if (bit == 0):
            bit = 1
            return bit
        elif(bit == 1):
            bit = 0
            return bit 
        else:
            return "Invalid input"
		    
    channel = invert(d.eDigitalIn(2)) + 2.0*float(invert(d.eDigitalIn(3))) + 4.0*float(invert(d.eDigitalIn(4)))
    return int(channel)

#gets the last execute channel on the Fibre Switch 
def GetLastChannel():
    
    def invert(bit):
        if (bit == 0):
            bit = 1
            return bit
        elif(bit == 1):
            bit = 0
            return bit 
        else:
            return "Invalid input"
		    
    channel = invert(d.eDigitalIn(5)) + 2.0*float(invert(d.eDigitalIn(6))) + 4.0*float(invert(d.eDigitalIn(7)))
    return int(channel)

# this function can be changed if necessary
def SetRSChannel(picked_channel):
    if (picked_channel >= 6 or picked_channel < 0):
        print "Fail: Pick a Valid Channel between 0-5 inclusive"
        return 0 
    else:
        current_display_channel = GetDisplayChannel()
        while (picked_channel != current_display_channel):
            ChannelUp()
            current_display_channel = GetDisplayChannel()
        return

# this checks to see if the laser channel switch execution is in progress (or not)
def CheckExe():
    manual_execution_flag = d.eDigitalIn(8)
    #Note: If the argument UpdateDigital=True then new values are sent 
    if (manual_execution_flag == 1):
	    print "Execution in Progress"
	    return  
    else:
	    print "No execution in Progress"
	    return  

def help():
	print "SmellieRS Commands include:\n -	SetChannel(0-5)\n -	GetLastChannel()\n -	Execute()\n -	GetDisplayChannel()\n -	ChannelUp()\n -	help()\n -	CheckExe()\n Please see the LabJackPython module for more information https://github.com/labjack/LabJackPython"            





        
