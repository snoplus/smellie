## Written by Christopher Jones 11/01/2013
## This is a simple SMELLIE run 
## SmellieRS = relay switch on smellie, fibreSwitch = fibre switch on smellie, safepysepia are safe functions for the sepia 2 laser box 

# Import all the functions in these python modules

import sys,time
import safepysepia as sepia
import pysepia
import SmellieRS as rs
import fibreSwitch as fs 

##TO NOTE: sys.exit() commands are only in place for the moment in reality these would abort the run and send a message to ORCA 


def set_safe_states(iDevIdx,iSlotID):
	sepia.laser_soft_lock_on(iDevIdx,iSlotID)	## turns the laser soft lock on 
	sepia.set_laser_intensity(0,iDevIdx)          #sets the intensity to 0%
	## TODO: Need to fix the frequencies in safepysepia and also need to check the numbers for internal and external triggers. 
	sepia.set_laser_frequency(6,iDevIdx) 		##sets the frequency to external trigger need to check this
	rs.SetRSChannel(0)			        ##sets the relay box to channel 0 (default channel)
	sepia.close(iDevIdx)
	rs.Execute()                                    ##executes the relay switch channel
        #sepia.initialise()
	#fs.SetFSChannel(1)			        ##sets the fibre switch to channel 0 (default channel)
	
	


def check_safe_states(iDevIdx,iSlotID):
	intensity,frequency_number,pulse_mode,head_id = sepia.get_laser_states(iDevIdx)
        print intensity,frequency_number,pulse_mode,head_id
	if (intensity != 0 or frequency_number != 6 or pulse_mode != 1):
		##TODO: Send command to ORCA to cancel the run
        	sepia.set_laser_intensity(0,iDevIdx)
		sys.exit('Safe states are not correctly set! Aborting run! (1)')
	##Check relay switch channel status 	
	relay_switch_default_channel = rs.GetDisplayChannel()
	if (relay_switch_default_channel != 0):
		##TODO: Send command to ORCA to cancel the run
                print "Stuff going wrong"
                #sepia.close(iDevIdx)
		#sys.exit('Safe states are not correctly set! Aborting run! (2)')
	##Check the laser soft lock status 	
	#laser_lock_on_check = sepia.get_laser_lock_status(iDevIdx,iSlotID)
	#print laser_lock_on_check 
	#if (laser_lock_on_check != 1):
		##TODO: Send command to ORCA to cancel the run
        #	sepia.laser_soft_lock_on(iDevIdx,iSlotID)
        #	print sepia.get_laser_lock_status(iDevIdx,iSlotID)
 	#	sys.exit('Safe states are not correctly set! Aborting run! (3)')
	return 	

def check_set_states(iDevIdx,iSlotID,input_intensity,input_frequency):
	intensity2,frequency_number2,pulse_mode2,head_id2 = sepia.get_laser_states(iDevIdx)
	if (intensity2 != input_intensity or frequency_number2 != input_frequency):
		##TODO: Send command to ORCA to cancel the run 		
		sys.exit('States have not been correctly set! Aborting run!')
	return 	



## START OF THE PROGRAM #################################################################################################	

## TODO: Need a while loop looking for communication from ORCA

##Initialisation steps
iDevIdx,iModuleType,iSlotID = sepia.initialise() #Initialise the Sepia 2 box
## TODO: Need to check the relay switch here

## TODO: Need to check connections and error status and send to ORCA

set_safe_states(iDevIdx,iSlotID)	        ##sets all the laser components to their safe states print here
iDevIdx,iModuleType,iSlotID = sepia.initialise() #Initialise the Sepia 2 box
sepia.laser_soft_lock_on(iDevIdx,iSlotID)
print "here"
check_safe_states(iDevIdx,iSlotID)		##checks all devices are in their safe states 
print "here check safe states"

#setting up the relay box

rs.SetRSChannel(3)				##sets the relay channel to 1
sepia.close(iDevIdx)
rs.Execute()                                    ##executes the relay switch channel
iDevIdx,iModuleType,iSlotID = sepia.initialise() #Initialise the Sepia 2 box
sepia.laser_soft_lock_on(iDevIdx,iSlotID)


##set parameters stage
## these numbers need to integers 
input_intensity = 100
input_frequency = 4		                ##I think this corresponds to 5Hz
#input_rs_channel = 1
#input_fs_channel = 1  
sepia.set_laser_intensity(input_intensity,iDevIdx)	##sets the intensity to 100%
print "here1"
sepia.set_laser_frequency(input_frequency,iDevIdx)		##sets the frequency
print "here2"
#sepia.close(iDevIdx)
#sys.exit("forced exit here")

fs.SetFSChannel(29)				##sets the fibre switch channel to 1 
check_set_states(iDevIdx,iSlotID,input_intensity,input_frequency)

##TODO: Dry test using only the PMT's (this section needs to be put in ) 

##TODO: Send ORCA Parameters 

sepia.laser_soft_lock_off(iDevIdx,iSlotID)		## this function unlocks the laser 
time.sleep(30)						## pulse laser for 10 seconds
sepia.laser_soft_lock_on(iDevIdx,iSlotID)
set_safe_states(iDevIdx,iSlotID)	##sets all the laser components to their safe states 
##TODO: Check that the states have been set properly 


##TODO: Send to ORCA that the run has been completed

iDevIdx,iModuleType,iSlotID = sepia.initialise() #Initialise the Sepia 2 box
sepia.laser_soft_lock_on(iDevIdx,iSlotID)
sepia.close(iDevIdx)







