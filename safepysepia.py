# Written by Christopher Jones 11/01/2013
# These are more logical functions for the Sepia 2 box which have had safety features added which are relevant to the SMELLIE Calibration System 

import time,sys
from pysepia import * # Imports all the functions created in Pysepia 

#This initialises the laser for commands and needs to be placed before any commands to the laser
def initialise():
	iDevIdx = SEPIA2_USB_OpenDevice() #Opens the Device  
	SEPIA2_FWR_GetModuleMap(iDevIdx)  ## this function is very important!! This retrieves the module map 
	iSlotID = 000			
	iModuleType = SEPIA2_COM_GetModuleType(iDevIdx,200,1) #200 is the slot section for our Sepia 2 Box 
	SEPIA2_COM_DecodeModuleType(iModuleType) # decodes the module map
	return iDevIdx,iModuleType,iSlotID

# This closes the laser and needs to be initiated everytime the laser is used .
def close(iDevIdx):
	SEPIA2_FWR_FreeModuleMap(iDevIdx)	# frees the module map
	SEPIA2_USB_CloseDevice(iDevIdx)		# closes the device down


# this function is required to check the laser is in pulse mode! This is important otherwise the laser could break
def check_pulse_mode(pulse_mode):
	if (pulse_mode == 1):	# Pulse_mode = 1 is that pulses are enabled
		pass
	else:
		sys.exit("Pulse mode is not enabled! Check to make sure Pulse mode is enabled")

# this function sets the intensity of the laser (Intensity is a % between 0 and 100)
def set_laser_intensity(new_intensity,iDevIdx):
	
	if (new_intensity < 0 or new_intensity > 100):
		## NOTE: I may need to change this call when integrating with an ORCA-like system 
		sys.exit("Need to set a valid Intensity! Intensity is given as a value between 0-100 (%)")
	else:
		pass

	intensity,frequency,pulse_mode,head_id = SEPIA2_SLM_GetParameters(iDevIdx, 200) ##gets the Parameters of the laser
	check_pulse_mode(pulse_mode)							##checks the laser is in pulsed mode			
	SEPIA2_SLM_SetParameters(iDevIdx,200,frequency,new_intensity) 			##sets the Parameters on the laser			
        SEPIA2_SLM_GetParameters(iDevIdx, 200)

# this function sets the frequency of the laser (Options are 80,40,20,10,external,internal)
def set_laser_frequency(new_frequency,iDevIdx):

	if (new_frequency >= 0 and new_frequency < 8):
		pass
	else:
		## NOTE: I may need to change this call when integrating with an ORCA-like system 
		sys.exit("Need to set a valid frequency! The options are 80,40,20,10,external,internal")  


	intensity,frequency,pulse_mode,head_id = SEPIA2_SLM_GetParameters(iDevIdx, 200) ##gets the Parameters of the laser
	check_pulse_mode(pulse_mode)							##checks the laser is in pulsed mode			
	SEPIA2_SLM_SetParameters(iDevIdx,200,new_frequency,intensity) 			##sets the Parameters on the laser
        SEPIA2_SLM_GetParameters(iDevIdx, 200)


def get_laser_states(iDevIdx):
	new_intensity,new_frequency,new_pulse_mode,new_head_id = SEPIA2_SLM_GetParameters(iDevIdx, 200)
	return new_intensity,new_frequency,new_pulse_mode,new_head_id

def get_laser_lock_status(iDevIdx,iSlotID):
	value = SEPIA2_SCM_GetLaserSoftLock(iDevIdx,iSlotID) 
	return value

# Function that turnes on the laser soft lock 
def laser_soft_lock_on(iDevIdx,iSlotID):
	SEPIA2_SCM_SetLaserSoftLock(iDevIdx,iSlotID,1) ##1 is laser-locked and checks the soft lock is actually on 
	return 1

def laser_soft_lock_off(iDevIdx,iSlotID):
	SEPIA2_SCM_SetLaserSoftLock(iDevIdx,iSlotID,0) ##0 is laser-unlocked
 	return 0 



