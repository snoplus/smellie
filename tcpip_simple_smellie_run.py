## Written by Christopher Jones 18/02/2013
## This is a simple SMELLIE run
## SmellieRS = relay switch on smellie, fs = fibre switch on smellie, safepysepia are safe functions for the sepia 2 laser box

# Import all the functions in these python modules

import sys,time
import safepysepia as sepia
import pysepia
import SmellieRS as rs
import fs
import socket as conn                     # get socket constructor and constants
import sm_analogue as smni

## TODO: Need to fix the frequencies in safepysepia and also need to check the numbers for internal and external triggers.

# this function incorporates a timeout on the socket. If data isn't received before the timeout then SMELLIE will restart.
def SMELLIE_while_loop_with_timeout(connection,timeout_sec):
        connection.settimeout(timeout_sec)
        while 1:
                try:
                        item_set = connection.recv(1024)
                except conn.timeout:
                        connection.send(timeout_flag)
                        main()
                if item_set : break

        connection.settimeout(None)
        return item_set


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

#this function waits until it sees a command from ORCA and checks to see what RS channel is set
def set_relay_switch_from_ORCA(connection,iDevIdx):

        rs_channel_set = SMELLIE_while_loop_with_timeout(connection,10)  #get rs_channel_value with a 5 second timeout

        connection.send(continue_flag)          #continue and get frequency
        print "ORCA: Relay Switch set to :" + rs_channel_set
        rs.SetRSChannel(int(rs_channel_set))
        sepia.close(iDevIdx)
        rs.Execute()
        connection.send(continue_flag)

#this function sets the intensity and frequency
def set_parameters_from_ORCA(connection):

        intensity_seen = SMELLIE_while_loop_with_timeout(connection,10)

        connection.send(continue_flag)          #continue and get frequency

        frequency_seen = SMELLIE_while_loop_with_timeout(connection,10)

        connection.send(continue_flag)          #continue

        print "ORCA: Set to this intensity :" + intensity_seen +"%"
        if (frequency_seen == '6') :
                print "ORCA: Set to this frequency : External Rising"
        else:
                connection.send(sepia_wrong_pulse_mode_flag)
                main()


def complete_self_test(connection,iDevIdx,iSlotID):
        print "Starting Self-test"

        read_signal = smni.AquireAnalogue()
        number_of_measurements = 10
        voltage_signal = read_signal.start(number_of_measurements)
        read_signal.stop()
        print voltage_signal
        #TO DO Self-Test is to performed here!!!
        ## NEED TO CHANGE THE LINE BELOW ONCE SELF-TEST HAS BEEN IMPLEMENTED
        ## Set the fibre switch to the desired channel
        self_test_status = 1 ##Assuming the self-test has been passed!
        ## NEED TO CHANGE THE LINE ABOVE ONCE SELF-TEST HAS BEEN IMPLEMENTED
        if (self_test_status == 1):
                print "Self-test Sucessful"
                connection.send(continue_flag)
        else:
                print "Self-test Failure"
                connection.send(self_test_fail)
                main()


def set_fs_channel(connection):

        fs_channel_seen = SMELLIE_while_loop_with_timeout(connection,10)

        try:
                fs.SetFSChannel(fs_channel_seen)	  ##sets the fibre switch channel (channel 29 is labelled channel 1)
                connection.send(continue_flag)
        except:
                connection.send(fs_channel_broken)
                main()

def get_pulses(connection):

        pulse_number = SMELLIE_while_loop_with_timeout(connection,10)

        if (int(pulse_number) <= 100000):
                connection.send(continue_flag)
                print "ORCA: Generate " + str(int(pulse_number)) + " pulses"
                return int(pulse_number)
        else:
                connection.send(pulse_number_too_high)
                main()

def get_trigger_frequency(connection):
        try:
                trigger_frequency = SMELLIE_while_loop_with_timeout(connection,10)
                connection.send(continue_flag)
                print "ORCA: Pulse Frequency: " + str(int(trigger_frequency)) + " Hz"
                return int(trigger_frequency)
        except:
                connection.send(trigger_frequency_flag)
                main()

def perform_run(connection,number_of_pulses,trigger_frequency,iDevIdx,iSlotID):
        try:
                sepia.laser_soft_lock_off(iDevIdx,iSlotID)
                digi_trig = smni.GenerateDigitalTrigger(trigger_frequency,number_of_pulses)
                digi_trig.start()
                digi_trig.stop()
                sepia.laser_soft_lock_on(iDevIdx,iSlotID)
                sepia.close(iDevIdx)
                connection.send(continue_flag)
        except:
                sepia.laser_soft_lock_on(iDevIdx,iSlotID)
                connection.send(run_failure_flag)
                main()


## START OF THE PROGRAM #################################################################################################

# question: with the continue flag does TCP/IP hold values between the system ?
# this could be a problem with checking if the sepia box or relay switch bow are working
continue_flag = '5189'                          # this is the flag to continue to the next stage of a run
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
self_test_fail = '77'                           # this flag indicates that a self-test has failed
relay_switch_set_wrong ='79'                    # this flag indicates that the relay switch is set incorrectly
fs_channel_broken = '84'                        # this flag indicates that the fs channel is broken
pulse_number_too_high = '87'                    # this flag indicates the number of pulses sent is too high
run_failure_flag = '102'                        # this flag indicates that the run has failed
trigger_frequency_flag = '132'                  # this flag indicates that the trigger frequency isn't properly set
timeout_flag = '123456'                         # this is the timeout flag for all while loops

## whenever there is an error, the program will revert back here and wait for more commands from ORCA
def main():
        print "\n"
        print "Starting SMELLIE..."
        myHost = ''                             # server machine, '' means local host
        myPort = 50007                          # listen on a non-reserved port number

        conn.sockobj = conn.socket(conn.AF_INET, conn.SOCK_STREAM)       # make a TCP socket object
        conn.sockobj.settimeout(None)                                            # No timeout on the socket
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
        connection.settimeout(5)                                        ##set a timeout for recieving data
        try:
                while 1:
                        start_init_data = connection.recv(1024)
                        if (start_init_data == start_initialise_flag):          #check to see if initialisation command has been given
                                print "ORCA: Start initialisation stage of SMELLIE run"
                                break
        except conn.timeout:
                connection.send(timeout_flag)
                main()

        connection.settimeout(None)                                     ##remove timeout for recieving data

        ##Initialisation stage
        iDevIdx,iModuleType,iSlotID = sepia.initialise()                #Initialise the Sepia 2 box
        check_sepia_box_connection(iModuleType,connection)              #Check the Sepia 2 box is working as expected
        check_relay_switch(connection)
        set_safe_states(iDevIdx,iSlotID)	                        ##sets all the laser components to their safe states print here
        iDevIdx,iModuleType,iSlotID = sepia.initialise()                ##Need to reinitialise the Sepia Box after turning off during the relay switching
        check_safe_states(iDevIdx,iSlotID,connection)		        ##checks all devices are in their safe states

        print "Looking for confirmation from ORCA to start SMELLIE run"
        
        connection.settimeout(5)                                        ##set a timeout for recieving data
        try:
                while 1:
                        start_run = connection.recv(1024)
                        if (start_init_data == start_initialise_flag):          #check to see if initialisation command has been given
                                print "ORCA: Ready to start sending run parameters"
                                break
        except conn.timeout:
                ## not sure if this is good TCPIP usage
                connection.send(timeout_flag)
                main()
                
        connection.settimeout(None)                                     ##remove timeout for recieving data
        
        print "Waiting for run parameters from ORCA"
        set_relay_switch_from_ORCA(connection,iDevIdx)
        iDevIdx,iModuleType,iSlotID = sepia.initialise()                ##Need to restart sepia box as the Relay switch is changed
        set_parameters_from_ORCA(connection)
        complete_self_test(connection,iDevIdx,iSlotID)
        sepia.laser_soft_lock_on(iDevIdx,iSlotID)
        set_fs_channel(connection)
        number_of_pulses = get_pulses(connection)                      ##this gets number of pulses
        trigger_frequency = get_trigger_frequency(connection)          ##this gets the trigger frequency
        perform_run(connection,number_of_pulses,trigger_frequency,iDevIdx,iSlotID)        ##this actually completes the SMELLIE run


        sys.exit("good exit")
## try the main function and if anything goes wrong then go back to the main function 
try:
        main()
except conn.error:
        print "\n Connection error: SMELLIE is restarting... \n"
        main()
except conn.timeout:
        print "\n Connection timeout: SMELLIE is restarting... \n"
        main()

sys.exit("bad exit")








