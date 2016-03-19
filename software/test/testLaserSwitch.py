# This script is designed to test the SMELLIE laser switch. Currently this is the test given in
# the "installing the SMELLIE Off-Detector" Hardware document and is the specific test for
# subsection 2 of the "testing the full hardware" section of this document.
# Press F5 to run this script

# Created by Christopher Jones on 6 March 2014


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

def laserSwitchCheckTest():
    iDevIdx,iModuleType,iSlotID = sepiaUser.initialise()
    set_to_safe_state(iDevIdx, iSlotID)
    set_laser_switch_channel(0)
    set_laser_switch_channel(1)
    set_laser_switch_channel(2)
    set_laser_switch_channel(3)
    set_laser_switch_channel(4)
    set_to_safe_state(iDevIdx, iSlotID)
    sepiaUser.laser_soft_lock_on(iDevIdx, iSlotID)
    sepiaUser.close(iDevIdx)

#laserSwitchCheckTest()
iDevIdx,iModuleType,iSlotID = sepiaUser.initialise()
rs.SetSelectedChannel(4)
sepiaUser.close(iDevIdx)
rs.Execute()
    
