## Written by Christopher Jones 11/01/2013
## This is a simple SMELLIE run 
## SmellieRS = relay switch on smellie, fs = fibre switch on smellie, safepysepia are safe functions for the sepia 2 laser box 

# Import all the functions in these python modules 
import safepysepia as sepia
import SmellieRS as rs
import fs 

##TO NOTE: sys.exit() commands are only in place for the moment in reality these would abort the run and send a message to ORCA 


def set_safe_states(iDevIdx,iSlotID):
	laser_soft_lock_on(iDevIdx,iSlotID)	## turns the laser soft lock on 
	sepia.set_laser_intensity(0.0,iDevIdx)  #sets the intensity to 0.0%
	## TODO: Need to fix the frequencies in safepysepia and also need to check the numbers for internal and external triggers. 
	sepia.set_laser_frequency(5) 		##sets the frequency to external trigger need to check this 
	rs.SetRSChannel(0)			##sets the relay box to channel 0 (default channel)
	fs.SetFSChannel(0)			##sets the fibre switch to channel 0 (default channel)


def check_safe_states(iDevIdx,iSlotID):
	intensity,frequency_number,pulse_mode,head_id = sepia.get_laser_states(iDevIdx)
	if (intensity != 0.0 or frequency_number != 0 or pulse_mode !=1):
		##TODO: Send command to ORCA to cancel the run 		
		sys.exit('Safe states are not correctly set! Aborting run!')
	##Check fibre switch channel status 	
	fibre_switch_default_channel = rs.GetDisplayChannel()
	if (fibre_switch_default_channel != 0):
		##TODO: Send command to ORCA to cancel the run 
		sys.exit('Safe states are not correctly set! Aborting run!')
	##Check the laser soft lock status 	
	laser_lock_on_check = get_laser_lock_status(iDevIdx,iSlotID)
	if (fibre_switch_default_channel != 1):
		##TODO: Send command to ORCA to cancel the run 
		sys.exit('Safe states are not correctly set! Aborting run!')
	return 	

def check_set_states(iDevIdx,iSlotID,input_intensity,input_frequency):
	intensity,frequency_number,pulse_mode,head_id = sepia.get_laser_states(iDevIdx)
	if (intensity != input_intensity or frequency_number != input_frequency or pulse_mode !=1):
		##TODO: Send command to ORCA to cancel the run 		
		sys.exit('States have not been correctly set! Aborting run!')
	return 	



## START OF THE PROGRAM #################################################################################################	

## TODO: Need a while loop looking for communication from ORCA

##Initialisation steps 
iDevIdx,iModuleType,iSlotID = sepia.initialise() #Initialise the Sepia 2 box
## TODO: Need to check the relay switch here

## TODO: Need to check connections and error status and send to ORCA

set_safe_states(iDevIdx,iModuleType,iSlotID)	##sets all the laser components to their safe states 
check_safe_states(iDevIdx)			##checks all devices are in their safe states 

##set parameters stage
input_intensity = 50.0
input_frequency = 5.0				##I think this corresponds to external triggering
input_rs_channel = 1
input_fs_channel = 1  
sepia.set_laser_intensity(100.0,iDevIdx)	##sets the intensity to 100%
sepia.set_laser_frequency(5.0,iDevIdx)		##sets the frequency
rs.SetRSChannel(1)				##sets the relay channel to 1
fs.SetFSChannel(1)				##sets the fibre switch channel to 1 
check_set_states(iDevIdx,iSlotID,input_intensity,input_frequency)

##TODO: Dry test using only the PMT's (this section needs to be put in ) 

##TODO: Send ORCA Parameters 

sepia.laser_soft_lock_off(iDevIdx,iSlotID)		## this function unlocks the laser 
time.sleep(10)						## pulse laser for 10 seconds
sepia.laser_soft_lock_on(iDevIdx,iSlotID)
set_safe_states(iDevIdx,iModuleType,iSlotID)	##sets all the laser components to their safe states 
##TODO: Check that the states have been set properly 


##TODO: Send to ORCA that the run has been completed 








