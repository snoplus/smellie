# This script contains functions to test if the SMELLIE software has been correctly installed on a computer
# Written by Christopher Jones (19/01/2013)
# Additional changes by Krish Majumdar (01/03/2013, 05/03/2013)

# Import all functions found in the following python modules:
import sys, time, os
import pysepiaUser as sepiaUser
import pysepia
import laserSwitch as rs
import fibreSwitch as fs
import sm_analogue as ni


def set_to_safe_state(iDevIdx, iSlotID):
    sepiaUser.laser_soft_lock_on(iDevIdx, iSlotID)	# turn the laser soft-lock on 
    sepiaUser.set_laser_intensity(0, iDevIdx)       # set the laser intensity to 0%
    sepiaUser.set_laser_frequency(6, iDevIdx) 		# set the laser to trigger on the rising edge of an external pulse
    rs.SetSelectedChannel(0)			            # set the laserSwitch to channel 0 (default channel)
    sepiaUser.close(iDevIdx)
    rs.Execute()                                    # execute the laserSwitch channel change


def set_laser_switch_channel(channel):
    iDevIdx,iModuleType,iSlotID = sepiaUser.initialise() 
    rs.SetSelectedChannel(channel)
    sepiaUser.close(iDevIdx)
    rs.Execute()                                    
    iDevIdx,iModuleType,iSlotID = sepiaUser.initialise() 
    sepiaUser.laser_soft_lock_on(iDevIdx, iSlotID)	


def test_run(ls_channel, fs_input_channel, logfile, iDevIdx, iModuleType, iSlotID):
    print "Installation Testing (Test Run) - Testing Laser Switch Channel: " + str(ls_channel)
    set_laser_switch_channel(ls_channel)
    sepiaUser.set_laser_intensity(100, iDevIdx)	    # set the intensity to 100%
    sepiaUser.set_laser_frequency(4, iDevIdx)		# this is the internal 5MHz trigger frequency ... use to check if Sepia is working properly
    
    for fs_output_channel in range(1, 15):
        
		channel_number = ((fs_input_channel - 1) * 14) + fs_output_channel
        fs.SetFSChannel(channel_number)                          # set the fibreSwitch channel 
        sepiaUser.laser_soft_lock_off(iDevIdx, iSlotID)		     # unlock the laser 
        time.sleep(1)						

        # this section of code is for generating a pulse via the NI Box, and reading the PMT value #
        ##### ##### ##### ##### ##### ##### ##### ##### ##### ##### ##### ##### ##### ##### ##### ##
        #trigger_frequency = 10000
        #number_of_pulses = 100000
        #digi_trig = ni.GenerateDigitalTrigger(trigger_frequency,number_of_pulses)
        #read_signal = ni.AcquireAnalogue()
        #number_of_measurements = 1  
        #voltage_signal = str(read_signal.start(number_of_measurements))
        #digi_trig.start()
        #digi_trig.stop()
        #read_signal = ni.AcquireAnalogue()
        #a = raw_input("Generating pulse train. Press Enter to interrupt ...\n")
        #read_signal.stop()
        #print voltage_signal                      # we need to decide how we would like this data to be outputted
        #logfile.write(str(ls_channel) + '\t' + str(channel_number) + '\t' + voltage_signal[1:-1] + '\n')
        ##### ##### ##### ##### ##### ##### ##### ##### ##### ##### ##### ##### ##### ##### ##### ##
        
		sepiaUser.laser_soft_lock_on(iDevIdx, iSlotID)


def main():
    iDevIdx,iModuleType,iSlotID = sepiaUser.initialise() 
    set_to_safe_state(iDevIdx, iSlotID)                       # set all the laser parameters to safe values 	
    
    timestamp = str(time.time())
    timestamp = timestamp[0:10]

    filename = 'Testing_SMELLIE_at_5MHz_' + timestamp + '.txt' 
    f = open(filename, 'w')
    
    # initiate test run across ALL laserSwitch channels and ALL fibreSwitch input/output channel combinations
    test_run(1, 1, f, iDevIdx, iModuleType, iSlotID)
    test_run(2, 2, f, iDevIdx, iModuleType, iSlotID)
    test_run(3, 3, f, iDevIdx, iModuleType, iSlotID)
    test_run(4, 4, f, iDevIdx, iModuleType, iSlotID)
    test_run(5, 5, f, iDevIdx, iModuleType, iSlotID)
    
    iDevIdx,iModuleType,iSlotID = sepia.initialise()          # re-initialise Sepia
    sepiaUser.laser_soft_lock_on(iDevIdx, iSlotID)
    sepiaUser.close(iDevIdx)
    
	f.close()
    time.sleep(1)
    folder_path = "C:\Users\LocalAdmin\Desktop\smellie_install_tests"    

main()






