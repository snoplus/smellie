#!/usr/bin/env python
import xmlrpclib,sys
s = xmlrpclib.ServerProxy('http://snodrop:5020')

#Commands
check_connection_flag = 10
set_laser_switch_flag = 2050
set_safe_states_flag = 30
set_fibre_switch_channel_flag = 40
set_laser_intensity_flag = 50
set_laser_soft_lock_on_flag = 60
set_laser_soft_lock_off_flag = 70
master_mode_flag = 80 #this has two arguments separated by an s in the string
set_laser_testing_frequency_mode = 90 #be very careful with this mode (do not use this during normal running)
kill_external_software_flag = 110 #this kills the sepia and ni software hosted locally on the snotdaq machine.
set_gain_control_flag = 22110 #sets the gain control flag
controlFlag = sys.argv[1]
controlArgument = sys.argv[2]
print "Connected to server: " + str(s)

def extractLaserFibreValues(masterModeValues):
    separateIndex = masterModeValues.index('s')
    masterModeFrequency = masterModeValues[0:separateIndex]
    masterModeNumPulses = masterModeValues[separateIndex+1:]
    print masterModeFrequency, masterModeNumPulses
    return masterModeFrequency, masterModeNumPulses
    
def extractMasterModeFromCode(masterModeValues):
    separateIndex = masterModeValues.index('s')
    masterModeFrequency = masterModeValues[0:separateIndex]
    masterModeNumPulses = masterModeValues[separateIndex+1:]
    print masterModeFrequency, masterModeNumPulses
    return masterModeFrequency, masterModeNumPulses

def main():

    try:
        # set laser switch channel
        if (int(controlFlag) == int(set_laser_switch_flag)):
            print "Setting Laser Switch to Channel" + str(controlArgument)
            print s.set_laser_switch(controlArgument)
    
        # set safe sates
        elif (int(controlFlag) == int(set_safe_states_flag)):
            print controlFlag
            print "Setting to Safe States"
            print s.set_safe_states()
                
        # set fibre switch channel 
        elif (int(controlFlag) == int(set_fibre_switch_channel_flag)):
            input_channel,output_channel = extractLaserFibreValues(controlArgument)
            print "Set the Fibre Switch to input Channel:" + str(input_channel) +" and output channel:" + str(output_channel)
            s.set_fibre_switch(input_channel,output_channel)
    
        # set laser intensity 
        elif (int(controlFlag) == int(set_laser_intensity_flag)):
            print "Set Laser Intensity to " + str(controlArgument) + "%"
            s.set_laser_intensity(controlArgument)
    
        # set soft lock on
        elif (int(controlFlag) == int(set_laser_soft_lock_on_flag)):
            print "Set laser soft lock on"
            s.set_soft_lock_on()
    
        elif(int(controlFlag) == int(kill_external_software_flag)):
            print "killing external sepia and ni software processes on snodrop"
            s.kill_sepia_and_nimax()
    
        # start master mode run 
        elif (int(controlFlag) == int(master_mode_flag)):
            master_mode_trigger_frequency,master_mode_number_of_pulses = extractMasterModeFromCode(controlArgument)
            print "Starting a Master mode sub run with trig frequency: " + str(master_mode_trigger_frequency) + "Hz and num_of_pulses:" + str(master_mode_number_of_pulses)
            s.pulse_master_mode(master_mode_trigger_frequency,master_mode_number_of_pulses)
    
        # set soft lock off
        elif (int(controlFlag) == int(set_laser_soft_lock_off_flag)):
            print "Set laser soft lock off"
            s.set_soft_lock_off()
                
        # set the laser frequency to high enough to see visually 
        elif (int(controlFlag) == int(set_laser_testing_frequency_mode)):
            print "Removed Setting laser to 20MHz testing Mode"
    
        elif (int(controlFlag) == int(set_gain_control_flag)):
            print "Setting Gain Control to " + str(controlArgument) + " mV"
            s.set_gain_control(controlArgument)
                
        else:
            print "No command value recieved"
            # put all the possible options in here
    
                            
    except ValueError, Argument:
        print "Error: " + str(ValueError) + "  " + str(Argument)

main()
