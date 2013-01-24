## Written by Christopher Jones 22/01/2013
## This is a simple SMELLIE run 
## SmellieRS = relay switch on smellie, fs = fibre switch on smellie, safepysepia are safe functions for the sepia 2 laser box 

# Import all the functions in these python modules

import sys,time
import safepysepia as sepia
import pysepia
import SmellieRS as rs
import fs
import socket as conn                     # get socket constructor and constants


##TO NOTE: sys.exit() commands are only in place for the moment in reality these would abort the run and send a message to ORCA 

## TODO: Need to fix the frequencies in safepysepia and also need to check the numbers for internal and external triggers. 


def set_safe_states(iDevIdx,iSlotID):
	sepia.laser_soft_lock_on(iDevIdx,iSlotID)	## turns the laser soft lock on 
	sepia.set_laser_intensity(0,iDevIdx)          #sets the intensity to 0%
	## TODO: Need to fix the frequencies in safepysepia and also need to check the numbers for internal and external triggers. 
	sepia.set_laser_frequency(6,iDevIdx) 		##sets the frequency to external trigger need to check this
	rs.SetRSChannel(0)			        ##sets the relay box to channel 0 (default channel)
	sepia.close(iDevIdx)
	rs.Execute()                                    ##executes the relay switch channel
	
	


def check_safe_states(iDevIdx,iSlotID,connection):
	intensity,frequency_number,pulse_mode,head_id = sepia.get_laser_states(iDevIdx)
        #print intensity,frequency_number,pulse_mode,head_id

	if (intensity != 0 or frequency_number != 6 or pulse_mode != 1):
                print 'Intensity not correctly set'
                sepia.set_laser_intensity(0,iDevIdx)
                connection.send(sepia_wrong_set_intensity_flag)
                main() ##Cancel run and only continue if a new ORCA command is sent

        if (frequency_number != 6):
                print 'Frequency_number or pulse_mode not correctly set'
                sepia.set_laser_frequency(6)
                connection.send(sepia_wrong_freq_flag)
                main() ##Cancel run and only continue if a new ORCA command is sent

        if (pulse_mode != 1):
                print 'Pulse_mode not correctly set'
                connection.send(sepia_wrong_pulse_mode_flag)
                main() ##Cancel run and only continue if a new ORCA command is sent    

	relay_switch_default_channel = rs.GetDisplayChannel() ##Check relay switch channel status 	
	if (relay_switch_default_channel != 0):
                print "Relay Switch box not set to correct default channel"
                rs.SetRSChannel(0)
                rs.Execute()
                connection.send(relay_switch_wrong_default_flag)
                main()
        else:
                print "Safe states correctly set"
                connection.send(continue_flag)
	return 	

def check_set_states(iDevIdx,iSlotID,input_intensity,input_frequency):
	intensity2,frequency_number2,pulse_mode2,head_id2 = sepia.get_laser_states(iDevIdx)
	if (intensity2 != input_intensity or frequency_number2 != input_frequency):
		##TODO: Send command to ORCA to cancel the run 		
		sys.exit('States have not been correctly set! Aborting run!')
	return 	

# this function checks the connection of the Sepia 2 Laser box and its power supply 
def check_sepia_box_connection(iModuleType,connection):
        if (iModuleType == 0):
                print "Sepia laser Box is not connected properly or has no power"
                print "Will restart the SMELLIE program from beginning"
                connection.send(sepia_box_no_connection_flag)
                main()
        else:
                print "Sepia is connected and powered up"
                connection.send(continue_flag)

def check_relay_switch(connection):
        check_relay_switch = rs.GetDisplayChannel()
        if (check_relay_switch == 7):
                print "Relay Switch Box not connected properly to power and/or SNODROP DAQ"
                connection.send(relay_switch_no_connection_flag)
                main()
        else:
                print "Relay Switch Box is connected and powered up"
                connection.send(continue_flag)

#this function waits until it sees a command from ORCA
def get_parameters_from_ORCA(connection):
        while 1:                                                
                intensity_seen = connection.recv(1024)
                if intensity_seen : break
        connection.send(continue_flag)          #continue and get other parameters
        print "ORCA: Set to this intensity :" + intensity_seen +"%"

        
## START OF THE PROGRAM #################################################################################################	

# question: with the continue flag does TCP/IP hold values between the system ?
# this could be a problem with checking if the sepia box or relay switch bow are working
continue_flag = '5'                             # this is the flag to continue to the next stage of a run 
check_connection_flag = '10'                    # this is the number to check the connection is present
start_initialise_flag = '20'                    # this starts the initialisation stage of a SMELLIE run
sepia_box_no_connection_flag = '30'             # this flag is raised if the Sepia box is not powered or connected properly
relay_switch_no_connection_flag = '40'          # this flag is raised if the relay switch is not powered or connected properly to SNODROP
# SAFE STATE ERROR CODES 
sepia_wrong_set_intensity_flag= '50'            # this flag is raised if the wrong default intensity is set on the Sepia 2 
sepia_wrong_freq_flag = '55'                    # this flag is raised if the wrong default frequency is set on the Sepia 2      
sepia_wrong_pulse_mode_flag = '60'              # this flag is raised if the wrong default pulse mode is set on the Sepia 2 
relay_switch_wrong_default_flag = '65'          # this flag is raised if the wrong default relay switch channel is set
setup_new_run = '70'                            # this flag is to setup the parameters for a smellie run 

## whenever there is an error, the program will revert back here and wait for more commands from ORCA
def main():
        print "\n"
        print "Starting SMELLIE..."
        myHost = ''                             # server machine, '' means local host
        myPort = 50007                          # listen on a non-reserved port number

        conn.sockobj = conn.socket(conn.AF_INET, conn.SOCK_STREAM)       # make a TCP socket object
        conn.sockobj.bind((myHost, myPort))                              # bind it to server port number 
        conn.sockobj.listen(5)                                           # listen, allow 5 pending connects

        ## Looking for connection confimation from ORCA
        print "Looking for connection confimation from ORCA"
        while 1:                                                        # listen until process killed
                connection, address = conn.sockobj.accept()             # wait for next client connect
                print 'Connection made to :' + str(address)             # connection is a new socket
                if address : break

        connection.send(check_connection_flag)                          # Send signal to ORCA checking connection

        ## Looking for ORCA initialisation commmand
        print "Looking for ORCA initialisation commmand"
        while 1:
                start_init_data = connection.recv(1024)
                if (start_init_data == start_initialise_flag):          #check to see if initialisation command has been given
                        print "ORCA: Start initialisation stage of SMELLIE run"
                        break 

        ##Initialisation stage
        iDevIdx,iModuleType,iSlotID = sepia.initialise()                #Initialise the Sepia 2 box 
        check_sepia_box_connection(iModuleType,connection)              #Check the Sepia 2 box is working as expected
        check_relay_switch(connection)
        set_safe_states(iDevIdx,iSlotID)	                        ##sets all the laser components to their safe states print here
        iDevIdx,iModuleType,iSlotID = sepia.initialise()                ##Need to reinitialise the Sepia Box after turning off during the relay switching
        check_safe_states(iDevIdx,iSlotID,connection)		        ##checks all devices are in their safe states

        print "Looking for confirmation from ORCA to start SMELLIE run"
        while 1:
                start_run = connection.recv(1024)
                if (start_init_data == start_initialise_flag):          #check to see if initialisation command has been given
                        print "ORCA: Ready to start sending run parameters"
                        break
        print "Waiting for run parameters from ORCA"
        get_parameters_from_ORCA(connection)                
        
        
        sys.exit("good exit")
main()
sys.exit("bad exit")
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







