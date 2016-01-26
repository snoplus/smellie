# This script contains functions to test if the SMELLIE software has been correctly installed on a computer
# Written by Christopher Jones (19/01/2013)
# Additional changes by Krish Majumdar (01/03/2013, 05/03/2013)

# This script is designed to test the SMELLIE system. Currently this is the test given in
# the "installing the SMELLIE Off-Detector" Hardware document and is the specific test for
# subsection 6)c. of the "testing the full hardware" section of this document.

# Import all functions found in the following python modules:
import sys, time, os
import pysepiaUser as sepiaUser
import pysepia
import laserSwitch as rs
import fibreSwitch as fs
import niADC as ni


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


def test_run(ls_channel, fs_input_channel, iDevIdx, iModuleType, iSlotID):
    
    print "Installation Testing (Test Run) - Testing Laser Switch Channel: " + str(ls_channel)
    set_laser_switch_channel(ls_channel)
    sepiaUser.set_laser_intensity(100, iDevIdx) # set the intensity to 100%
    sepiaUser.set_laser_frequency(2, iDevIdx) # this is the internal 5MHz trigger frequency ... use to check if Sepia is working properly
    
    for fs_output_channel in range(1, 15):

        channel_number = ((fs_input_channel - 1) * 14) + fs_output_channel
        fs.SetFSChannel(channel_number) # set the fibreSwitch channel
        sepiaUser.laser_soft_lock_off(iDevIdx, iSlotID) # unlock the laser
        time.sleep(10) 
        sepiaUser.laser_soft_lock_on(iDevIdx, iSlotID)


def fibreSwitchTesting():
    iDevIdx,iModuleType,iSlotID = sepiaUser.initialise() 
    set_to_safe_state(iDevIdx, iSlotID)                       # set all the laser parameters to safe values 	
    
    #timestamp = str(time.time())
    #timestamp = timestamp[0:10]

    
    # initiate test run across ALL laserSwitch channels and ALL fibreSwitch input/output channel combinations
    test_run(1, 1, iDevIdx, iModuleType, iSlotID)
    test_run(2, 2, iDevIdx, iModuleType, iSlotID)
    test_run(2, 3, iDevIdx, iModuleType, iSlotID)
    test_run(4, 4, iDevIdx, iModuleType, iSlotID)
    test_run(5, 5, iDevIdx, iModuleType, iSlotID)
    
    iDevIdx,iModuleType,iSlotID = sepiaUser.initialise()          # re-initialise Sepia
    sepiaUser.laser_soft_lock_on(iDevIdx, iSlotID)
    sepiaUser.close(iDevIdx)
    
    time.sleep(1)

def setLaserAndFibreSwitch(ls_channel,fs_input_channel,fs_output_channel,time_in_minutes,operation_mode,intensity):
    
    iDevIdx,iModuleType,iSlotID = sepiaUser.initialise() 
    set_to_safe_state(iDevIdx, iSlotID)                                     # set all the laser parameters to safe values

    set_laser_switch_channel(ls_channel)
    sepiaUser.set_laser_intensity(intensity, iDevIdx) # set the intensity to 100%
    sepiaUser.set_laser_frequency(operation_mode, iDevIdx) 


    channel_number = ((fs_input_channel - 1) * 14) + fs_output_channel      # pick the correct channel number
    print(channel_number)
    fs.SetFSChannel(channel_number)                                         # set the fibreSwitch channel
    laserTime = time_in_minutes*60.0                                        # time for program to wait before locking the laser (i.e. laser operating time)
    sepiaUser.laser_soft_lock_off(iDevIdx, iSlotID)                         # unlock the laser
    time.sleep(laserTime)                                                   # make Python sleep while laser is working 

    iDevIdx,iModuleType,iSlotID = sepiaUser.initialise()                    # re-initialise Sepia 
    sepiaUser.laser_soft_lock_on(iDevIdx, iSlotID)                          # soft lock on
    sepiaUser.close(iDevIdx)                                                # close the Sepia box down...
    
    time.sleep(1)
    
    
#USE THIS FOR TESTING AND CONTROLLING THE LASEER
#Testing and controling the different outputs from the fibre switch
#OPERATION MODE: 0 (80MHz), 1 (40MHz), 2 (20MHz), 3 (10MHz), 4 (5MHz), 5 (2.5MHz), 6 (external rising edge), 7 (external falling edge)

def mainRun():
    laser_switch_channel = 2                #choose the laser
    fibre_switch_input_channel = 3
    fibre_switch_ouput_channel = 10
    laser_operating_time_in_minutes = 0.5
    operation_mode = 6                      #DO NOT USE 0 OR 1 !!!!!!!!!!!!!!!
    intensity = 0                         #this is in percentage of the intensity 
    setLaserAndFibreSwitchVersion2(laser_switch_channel,fibre_switch_input_channel,fibre_switch_ouput_channel,laser_operating_time_in_minutes,operation_mode,intensity)


def setLaserAndFibreSwitchVersion2(ls_channel,fs_input_channel,fs_output_channel,time_in_minutes,operation_mode,intensity):
    
    iDevIdx,iModuleType,iSlotID = sepiaUser.initialise() 
    set_to_safe_state(iDevIdx, iSlotID)                                     # set all the laser parameters to safe values

    iDevIdx,iModuleType,iSlotID = sepiaUser.initialise() 
    sepiaUser.set_laser_intensity(intensity, iDevIdx) # set the intensity to 100%
    sepiaUser.set_laser_frequency(operation_mode, iDevIdx)
    sepiaUser.close(iDevIdx)

    set_laser_switch_channel(ls_channel)
    
    channel_number = ((fs_input_channel - 1) * 14) + fs_output_channel      # pick the correct channel number
    print(channel_number)
    fs.SetFSChannel(channel_number)                                         # set the fibreSwitch channel
    laserTime = 0.5#time_in_minutes*60.0                                        # time for program to wait before locking the laser (i.e. laser operating time)
    sepiaUser.laser_soft_lock_off(iDevIdx, iSlotID)                         # unlock the laser
    time.sleep(laserTime)                                                   # make Python sleep while laser is working 

    iDevIdx,iModuleType,iSlotID = sepiaUser.initialise()                    # re-initialise Sepia 
    sepiaUser.laser_soft_lock_on(iDevIdx, iSlotID)                          # soft lock on
    sepiaUser.close(iDevIdx)                                                # close the Sepia box down...
    
    time.sleep(1)

#mainRun()
def safeFibreSwitch():
    fs_input_channel = 5
    fs_output_channel = 1

    channel_number = ((fs_input_channel - 1) * 14) + fs_output_channel      # pick the correct channel number
    print(channel_number)
    fs.SetFSChannel(channel_number)

def setFibreSwitch(fs_input_channel,fs_output_channel):
    channel_number = ((fs_input_channel - 1) * 14) + fs_output_channel      # pick the correct channel number
    print(channel_number)
    fs.SetFSChannel(channel_number)


#safeFibreSwitch()
#This will set the fibre switch to a different laser channel
#40 percent intensity seems to work fine
setFibreSwitch(5,14)
#setFibreSwitch(3,11)
#mainRun()




