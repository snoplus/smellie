# User functions for controlling and monitoring the Sepia II Laser Driver Unit
# These functions have been modified from those in pysepia.py by adding additional safety checks and monitoring output 
# Written by Christopher Jones 11/01/2013
# Additional changes by Krish Majumdar (25/01/2013)

import time, sys
from pysepia import *	# Import all functions present in pysepia.py


# Initialise the laser so that it is ready for commands
# This function must be performed before sending any commands to the laser
def initialise():
	iDevIdx = SEPIA2_USB_OpenDevice()	# open the USB device  
	SEPIA2_FWR_GetModuleMap(iDevIdx)	# retrieve the module map 
	iSlotID = 000			
	iModuleType = SEPIA2_COM_GetModuleType(iDevIdx,200,1)	# the value 200 is the slot section for the Sepia II Unit 
	SEPIA2_COM_DecodeModuleType(iModuleType)	# decode the module map
	return iDevIdx,iModuleType,iSlotID


# Close the laser
# This function must be performed every time the laser is used
def close(iDevIdx):
	SEPIA2_FWR_FreeModuleMap(iDevIdx)	# free the module map
	SEPIA2_USB_CloseDevice(iDevIdx)		# close the device


# Check that the laser is in "Pulse Mode"!  If it is not, i.e. it is in "Continuous Mode", the laser may be damaged
def check_pulse_mode(pulse_mode):
	if (pulse_mode == 1):	# Pulse_mode = 1 means that the laser is in Pulse Mode
		pass
	else:
		sys.exit("The laser is NOT in Pulse Mode!  Check to make sure Pulse Mode is enabled")


# Set the intensity of the laser (input intensity is a % between 0 and 100)
def set_laser_intensity(new_intensity,iDevIdx):
	if (new_intensity < 0) or (new_intensity > 100):
		# NOTE: I may need to change this call when integrating with an ORCA-like system 
		sys.exit("Input intensity is not valid - it must be between 0 and 100 (%)")
	else:
		pass

	intensity,frequency,pulse_mode,head_id = SEPIA2_SLM_GetParameters(iDevIdx, 200)		# get the current laser parameters
	check_pulse_mode(pulse_mode)														# check that the laser is in "Pulse Mode"
	SEPIA2_SLM_SetParameters(iDevIdx,200,frequency,new_intensity)						# set the new intensity as the laser parameter
	SEPIA2_SLM_GetParameters(iDevIdx, 200)


# Set the frequency mode of the laser
def set_laser_frequency(new_frequency,iDevIdx):
	if (new_frequency >= 0) and (new_frequency < 8):
		pass
	else:
		# NOTE: I may need to change this call when integrating with an ORCA-like system 
		sys.exit("Input frequency mode is not valid - possible values are: 0 (80MHz), 1 (40MHz), 2 (20MHz), 3 (10MHz), 4 (5MHz), 5 (2.5MHz), 6 (external rising edge), 7 (external falling edge)")  

	intensity,frequency,pulse_mode,head_id = SEPIA2_SLM_GetParameters(iDevIdx, 200)		# get the current laser parameters
	check_pulse_mode(pulse_mode)														# check that the laser is in "Pulse Mode"	
	SEPIA2_SLM_SetParameters(iDevIdx,200,new_frequency,intensity)						# set the new frequency as the laser parameter
        SEPIA2_SLM_GetParameters(iDevIdx, 200)


def get_laser_parameters(iDevIdx):
	new_intensity,new_frequency,new_pulse_mode,new_head_id = SEPIA2_SLM_GetParameters(iDevIdx, 200)
	return new_intensity,new_frequency,new_pulse_mode,new_head_id


def get_laser_lock_status(iDevIdx,iSlotID):
	value = SEPIA2_SCM_GetLaserSoftLock(iDevIdx,iSlotID) 
	return value


# Turn on the laser's soft-lock
def laser_soft_lock_on(iDevIdx,iSlotID):
	SEPIA2_SCM_SetLaserSoftLock(iDevIdx,iSlotID,1)		# value of 1 means that the laser is soft-locked
	return 1


# Turn off the laser's soft-lock
def laser_soft_lock_off(iDevIdx,iSlotID):
	SEPIA2_SCM_SetLaserSoftLock(iDevIdx,iSlotID,0)		# value of 0 means that the laser is not soft-locked
 	return 0 
