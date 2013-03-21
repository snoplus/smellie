# This is a Simple SMELLIE Run for use on a single machine (i.e. no TCP/IP simulation)
# Written by Christopher Jones (11/01/2013)
# Additional changes by Krish Majumdar (24/01/2013, 25/01/2013, 04/03/2013, 05/03/2013)

# Import all the functions in the following python modules:
import sys, time
import pysepiaUser as sepiaUser   # User commands and functions for the SEPIA II Laser Driver Unit
import pysepia
import laserSwitch as rs		  # commands for the Laser Switch
import fibreSwitch as fs		  # commands for the Fibre Switch


def set_safe_states(iDevIdx, iSlotID):
	sepiaUser.laser_soft_lock_on(iDevIdx, iSlotID)   # turn the laser soft-lock on
	sepiaUser.set_laser_intensity(0, iDevIdx)        # set the laser intensity to 0%
	sepiaUser.set_laser_frequency(6, iDevIdx) 		 # set the laser frequency to external rising-edge trigger
	rs.SetSelectedChannel(0)			             # set the laserSwitch to channel 0 (default)
	sepiaUser.close(iDevIdx)
	rs.Execute()                                     # execute the laserSwitch channel change from above
    
	
def check_safe_states(iDevIdx, iSlotID):
	# Get the current states of Sepia and the LaserSwitch
	intensity,frequency_number,pulse_mode,head_id = sepiaUser.get_laser_parameters(iDevIdx)
	ls_channel = rs.GetActiveChannel()
	if (intensity != 0):
		sepiaUser.set_laser_intensity(0, iDevIdx)
		sys.exit('Simple Run (Check Safe States) - The laser Intensity is not at SAFE value (0%)')
	if (frequency_number != 6):
		sepiaUser.set_laser_frequency(6, iDevIdx)
		sys.exit('Simple Run (Check Safe States) - The laser Frequency is not at SAFE value (6 - external rising edge)')
	if (pulse_mode != 1):
		sys.exit('Simple Run (Check Safe States) - The laser Pulse Mode is not set correctly (1 - pulse mode, NOT continuous)')
	if (ls_channel != 0):
		rs.SetSelectedChannel(0)
		rs.Execute()
		sepiaUser.close(iDevIdx)
		sys.exit('Simple Run (Check Safe States) - The Laser Switch safe-state is not correctly set ... aborting run!')
		# Check the laser soft-lock status 	
		lock_check = sepiaUser.get_laser_lock_status(iDevIdx, iSlotID)
		if (laser_lock_on_check != 1):
			sepiaUser.laser_soft_lock_on(iDevIdx, iSlotID)
			sys.exit('Simple Run (Check Safe States) - Laser Soft-lock is not enabled ... aborting run!')
	return 	


def check_current_states(iDevIdx, iSlotID, input_intensity, input_frequency):
	intensity,frequency_number,pulse_mode,head_id = sepiaUser.get_laser_parameters(iDevIdx)	
	if (intensity != input_intensity or frequency_number != input_frequency):
		sys.exit('Simple Run (Check Current States) - Laser States have not been correctly set to your specified values ... aborting run!')
	return 	



##### START OF THE MAIN PROGRAM ####################################################################################################

# Initialisation stage
iDevIdx,iModuleType,iSlotID = sepiaUser.initialise()    # initialise Sepia
set_safe_states(iDevIdx, iSlotID)	                        # sets all the Sepia parameters to their safe state values
iDevIdx,iModuleType,iSlotID = sepiaUser.initialise()        # need to reinitialise Sepia after turning off during the changing of the laserSwitch channel (part of set_safe_states)
sepiaUser.laser_soft_lock_on(iDevIdx, iSlotID)
check_safe_states(iDevIdx, iSlotID, connection)		        # check that all devices are in their safe-states

rs.SetSelectedChannel(0)				              # set the laserSwitch channel to 1
sepiaUser.close(iDevIdx)
rs.Execute()                                          # execute the laserSwitch channel change
iDevIdx,iModuleType,iSlotID = sepiaUser.initialise()  # need to reinitialise Sepia after turning off during the changing of the laserSwitch channel (part of SetSelectedChannel)
sepiaUser.laser_soft_lock_on(iDevIdx, iSlotID)

# Set all Parameters (all must be INTEGERS)
input_intensity = 100
input_frequency = 4
input_rs_channel = 1
input_fs_channel = 1  
sepiaUser.set_laser_intensity(input_intensity, iDevIdx)	  # set the laser intensity to 100%
sepiaUser.set_laser_frequency(input_frequency, iDevIdx)   # set the laser frequency to Internal 5MHz
sepiaUser.close(iDevIdx)
fs.SetFSChannel(input_fs_channel)				          # set the fibreSwitch channel to 1 
#sys.exit("Simple Run (Main) - Forced Exit after Set Parameters stage")

check_current_states(iDevIdx, iSlotID, input_intensity, input_frequency)

sepiaUser.laser_soft_lock_off(iDevIdx, iSlotID)		     # unlock the laser 
time.sleep(30)						                     # pulse the laser for 30 seconds
sepiaUser.laser_soft_lock_on(iDevIdx, iSlotID)           # lock the laser again after pulsing is complete
set_safe_states(iDevIdx, iSlotID)	                     # set all laser parameter to their safe-state values 
iDevIdx,iModuleType,iSlotID = sepiaUser.initialise()     # need to reinitialise Sepia after turning off during the changing of the laserSwitch channel (part of set_safe_states)
sepiaUser.laser_soft_lock_on(iDevIdx, iSlotID)

check_safe_states(iDevIdx, iSlotID, connection)		     # check that all devices are in their safe-states

iDevIdx,iModuleType,iSlotID = sepiaUser.initialise()     # re-initialise Sepia
sepiaUser.laser_soft_lock_on(iDevIdx, iSlotID)
sepiaUser.close(iDevIdx)
