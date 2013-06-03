# This is a Simple SMELLIE Run that uses the TCP/IP Networking to Communicate between SNOdrop and another computer (simulating the use of ORCA)
# Written by Christopher Jones (18/02/2013)
# Additional changes by Krish Majumdar (04/03/2013, 05/03/2013, 15/03/2013)

# Import all the functions in the following python modules:
import sys, time
import pysepiaUser as sepiaUser
import pysepia
import laserSwitch as rs
import fibreSwitch as fs
import socket as conn                # socket constructor and constants
import niADC as ni


# Incorporate a timeout on the socket
# If data isn't received before the timeout, the SMELLIE software will restart
def timeout(connection, timeout_sec):
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


def set_safe_states(iDevIdx, iSlotID):
	sepiaUser.laser_soft_lock_on(iDevIdx, iSlotID)   # turn the laser soft-lock on
	sepiaUser.set_laser_intensity(0, iDevIdx)        # set the laser intensity to 0%
	sepiaUser.set_laser_frequency(6, iDevIdx)        # set the laser frequency to external rising-edge trigger
	rs.SetSelectedChannel(0)			 # set the laserSwitch to channel 0 (default)
	sepiaUser.close(iDevIdx)
	rs.Execute()                                     # execute the laserSwitch channel change from above


def check_safe_states(iDevIdx, iSlotID, connection):
	intensity,frequency_number,pulse_mode,head_id = sepiaUser.get_laser_parameters(iDevIdx)
	ls_channel = rs.GetActiveChannel()    # Check the active channel on the laserSwitch

	if (intensity != 0):
		print 'Simple TCP/IP Run (Check Safe States) - The laser Intensity is not at SAFE value (0%)'
		sepiaUser.set_laser_intensity(0, iDevIdx)
		connection.send(sepia_wrong_set_intensity_flag)
		main()    # Cancel the run, and only continue if a new TCP/IP (ORCA) command is sent
	if (frequency_number != 6):
		print 'Simple TCP/IP Run (Check Safe States) - The laser Frequency is not at SAFE value (6 - external rising edge)'
		sepiaUser.set_laser_frequency(6, iDevIdx)
		connection.send(sepia_wrong_freq_flag)
		main()    # Cancel the run, and only continue if a new TCP/IP (ORCA) command is sent
	if (pulse_mode != 1):
		print 'Simple TCP/IP Run (Check Safe States) - The laser Pulse Mode is not set correctly (1 - pulse mode, NOT continuous)'
		connection.send(sepia_wrong_pulse_mode_flag)
		main()    # Cancel the run, and only continue if a new TCP/IP (ORCA) command is sent
	if (ls_channel != 0):
		print "Simple TCP/IP Run (Check Safe States) - The Laser Switch channel is not set to SAFE value (0)"
		rs.SetSelectedChannel(0)
		rs.Execute()
		connection.send(relay_switch_wrong_default_flag)
		main()
	else:
		print "Simple TCP/IP Run (Check Safe States) - All Safe States are Correctly Set"
		connection.send(continue_flag)

	return


def check_current_states(iDevIdx, iSlotID, input_intensity, input_frequency):
	intensity,frequency_number,pulse_mode,head_id = sepiaUser.get_laser_parameters(iDevIdx)

	if (intensity != input_intensity or frequency_number != input_frequency):
		## TODO: Send command to ORCA to cancel the run
		sys.exit('Simple TCP/IP Run (Check Current States) - Laser States have not been correctly set to your specified values ... aborting run!')

	return


# Check the connection to the Sepia 2 Laser Driver, and also if it is powered on
def check_sepia_connection(iModuleType, connection):
	if (iModuleType == 0):
		print "Simple TCP/IP Run (Check Sepia Connection) - The SEPIA Laser Driver is not connected correctly, or has no power"
		print "Simple TCP/IP Run (Check Sepia Connection) - This SMELLIE run will restart from the beginning"
		connection.send(sepia_box_no_connection_flag)
		main()
	else:
		print "Simple TCP/IP Run (Check Sepia Connection) - The SEPIA Laser Driver is connected and powered up correctly"
		connection.send(continue_flag)


# Check the connection to the Laser Switch, and also if it is powered on
def check_ls_connection(connection):
	ls_channel = rs.GetActiveChannel()

	if (ls_channel > 5):
    		print "Simple TCP/IP Run (Check laserSwitch Connection) - The Laser Switch is not connected correctly to mains power and/or the SNOdrop PC"
    		connection.send(relay_switch_no_connection_flag)
    		main()
	else:
    		print "Simple TCP/IP Run (Check laserSwitch Connection) - The Laser Switch is connected and powered up correctly"
    		connection.send(continue_flag)


# Wait for a TCP/IP command (from ORCA), and then check and set the Selected Laser Switch Channel
def ORCA_set_ls_channel(connection, iDevIdx):
	ls_channel_set = timeout(connection, 10)    # get the laserSwitch channel, with a 10 second timeout
	connection.send(continue_flag)
	print "Simple TCP/IP Run (ORCA Set laserSwitch Channel) - Laser Switch channel is set to:" + ls_channel_set
	rs.SetSelectedChannel(int(ls_channel_set))
	sepiaUser.close(iDevIdx)
	rs.Execute()
	connection.send(continue_flag)


# Wait for a TCP/IP command (from ORCA), and then check and set the Laser Intensity and Frequency
def ORCA_set_laser_parameters(connection):
	intensity_set = timeout(connection, 10)   # get the laser intensity, with a 10 second timeout
	connection.send(continue_flag)            # continue
	frequency_set = timeout(connection,10)    # get the laser frequency mode, with a 10 second timeout
	connection.send(continue_flag)            # continue
	print "Simple TCP/IP Run (ORCA Set Laser Parameters) - Laser is set to intensity:" + intensity_set + "%"

	if (frequency_set == '6'):
		print "Simple TCP/IP Run (ORCA Set Laser Parameters) - Laser is set to frequency mode: 6 (External Rising-Edge)"
	else:
    		print "Simple TCP/IP Run (ORCA Set Laser Parameters) - Laser is NOT set to frequency mode 6 (External Rising-Edge)"
		connection.send(sepia_wrong_pulse_mode_flag)
		main()


def complete_self_test(connection, iDevIdx, iSlotID):
	print "Simple TCP/IP Run (Complete Self Test) - Beginning complete Self-Test ... "
	## TODO Self-Test is to performed here!!!
	## NEED TO CHANGE THE LINE BELOW ONCE SELF-TEST HAS BEEN IMPLEMENTED
	self_test_status = 1
	## NEED TO CHANGE THE LINE ABOVE ONCE SELF-TEST HAS BEEN IMPLEMENTED
	if (self_test_status == 1):
		print "Simple TCP/IP Run (Complete Self Test) - Self-Test was Successful"
		connection.send(continue_flag)
	else:
		print "Simple TCP/IP Run (Complete Self Test) - Self-Test Failed"
		connection.send(self_test_fail)
		main()


# Wait for a TCP/IP command (from ORCA), and then check and set the Selected Fibre Switch Channel
def ORCA_set_fs_channel(connection):
	fs_channel_set = timeout(connection, 10)    # get the fibreSwitch channel, with a 10 second timeout
	try:
		fs.SetFSChannel(fs_channel_set)	        # set the fibreSwitch channel
		connection.send(continue_flag)
	except:
		connection.send(fs_channel_broken)
		main()


# Wait for a TCP/IP command (from ORCA), and then check and set the NI Box's Pulse Number
def ORCA_ni_get_pulses(connection):
	pulse_number_set = timeout(connection, 10)    # get the number of pulses to be generated by the NI box, with a 10 second timeout
	if (int(pulse_number_set) <= 100000):
		connection.send(continue_flag)
		print "Simple TCP/IP Run (ORCA Set NI No. of Pulses) - Generate " + str(int(pulse_number_set)) + " pulses"
		return int(pulse_number_set)
	else:
    		print "Simple TCP/IP Run (ORCA Set NI No. of Pulses) - The number of pulses you want is too high"
		connection.send(pulse_number_too_high)
		main()

# Wait for a TCP/IP command (from ORCA), and then check and set the NI Box's Trigger Frequency
def ORCA_ni_get_trigger_frequency(connection):
	try:
		trigger_frequency = timeout(connection, 10)
		connection.send(continue_flag)
		print "Simple TCP/IP Run (ORCA Set NI Trigger Frequency) - Trigger Frequency: " + str(int(trigger_frequency)) + "Hz"
		return int(trigger_frequency)
	except:
		connection.send(trigger_frequency_flag)
		main()


def perform_run(connection, number_of_pulses, trigger_frequency, iDevIdx, iSlotID):
# try/except statement didn't work here during testing with SNO+. Need to know why? 
	
	sepiaUser.laser_soft_lock_off(iDevIdx, iSlotID)
	digi_trig = ni.GenerateDigitalTrigger(trigger_frequency, number_of_pulses)
	digi_trig.start()
	digi_trig.stop()
	sepiaUser.laser_soft_lock_on(iDevIdx, iSlotID)
	sepiaUser.close(iDevIdx)
	connection.send(continue_flag)
	#except:
	#	sepiaUser.laser_soft_lock_on(iDevIdx, iSlotID)
	#	connection.send(run_failure_flag)
	#	main()


##### START OF THE MAIN PROGRAM ####################################################################################################

# Question: when using the continue flag, does TCP/IP hold values between the system?
# this could be a problem when checking if the Sepia or LaserSwitch boxes are working

continue_flag = '5189'                          # this is the flag to continue to the next stage of a run
check_connection_flag = '10'                    # this checks if the connection is present
start_initialise_flag = '20'                    # this starts the initialisation stage of a SMELLIE run
sepia_box_no_connection_flag = '30'             # this flag is raised if Sepia is not powered or connected correctly
relay_switch_no_connection_flag = '40'          # this flag is raised if the Laser Switch is not powered or connected to SNOdrop correctly

# SAFE-STATE ERROR CODES
sepia_wrong_set_intensity_flag = '50'           # this flag is raised if the wrong default intensity is set on Sepia
sepia_wrong_freq_flag = '55'                    # this flag is raised if the wrong default frequency is set on Sepia
sepia_wrong_pulse_mode_flag = '60'              # this flag is raised if the wrong default pulse mode is set on Sepia
relay_switch_wrong_default_flag = '65'          # this flag is raised if the wrong default channel on the Laser Switch is set
setup_new_run = '70'                            # this flag is to setup the parameters for a SMELLIE run
self_test_fail = '77'                           # this flag indicates that the self-test has failed
relay_switch_set_wrong = '79'                   # this flag indicates that the Laser Switch is set incorrectly
fs_channel_broken = '84'                        # this flag indicates that the Fibre Switch channel is broken or incorrectly set
pulse_number_too_high = '87'                    # this flag indicates the number of pulses sent from the NI box is too high
run_failure_flag = '102'                        # this flag indicates that the run has failed
trigger_frequency_flag = '132'                  # this flag indicates that the trigger frequency for the NI box is incorrectly set
timeout_flag = '123456'                         # this is the timeout flag for all calls to the timeout function

# Whenever there is an error, the program will revert back to this point and wait for more commands via TCP/IP (from ORCA)
def main():
	print "\n"
	print "Simple TCP/IP Run (Main) - Starting SMELLIE RUN..."
	
        #Perform a clean open and close of the Sepia Laser Driver before talking to ORCA. 
        iDevIdx,iModuleType,iSlotID = sepiaUser.initialise()
        sepiaUser.laser_soft_lock_on(iDevIdx, iSlotID)
	rs.SetSelectedChannel(0)
	sepiaUser.close(iDevIdx)
        
	myHost = ''                          # initialise the server machine ('' means: local host)
	myPort = 50007                       # listen on a non-reserved port number

	conn.sockobj = conn.socket(conn.AF_INET, conn.SOCK_STREAM)       # make a TCP/IP socket object
	conn.sockobj.settimeout(None)                                    # No timeout on the socket
	conn.sockobj.bind((myHost, myPort))                              # bind the socket object to the specified server and port number 
	conn.sockobj.listen(5)                                           # begin listening, and allow 5 pending connects

	# Check for connection confimation from ORCA
	print "Simple TCP/IP Run (Main) - Checking for connection confimation from ORCA ... "	
	while 1:                                                        # listen until process killed
		connection, address = conn.sockobj.accept()             # wait for next client connection
		print 'Connection made to:' + str(address)              # connection is a new socket
		if address : break		
	connection.send(check_connection_flag)                          # send signal to ORCA  to check connection

	# Check for SMELLIE initialisation commmand from ORCA
	print "Simple TCP/IP Run (Main) - Looking for SMELLIE initialisation commmand from ORCA ... "
	connection.settimeout(5)                                    # set a timeout of 5 seconds for receiving data
	try:
		while 1:
    			start_init_data = connection.recv(1024)
    			if (start_init_data == start_initialise_flag):      # check if initialisation command has been given
        			print "Simple TCP/IP Run (Main) - Start initialisation stage of the SMELLIE run"
        			break
	except conn.timeout:
		connection.send(timeout_flag)
		main()

	connection.settimeout(None)                                 # remove timeout for receiving data

	# Initialisation stage
	iDevIdx,iModuleType,iSlotID = sepiaUser.initialise()        # initialise Sepia
	check_sepia_connection(iModuleType, connection)             # check that Sepia is working as expected
	check_ls_connection(connection)                             # check that the laserSwitch is working as expected
	set_safe_states(iDevIdx, iSlotID)	                    # sets all the Sepia parameters to their safe state values
	iDevIdx,iModuleType,iSlotID = sepiaUser.initialise()        # need to reinitialise Sepia after turning off during the changing of the laserSwitch channel (part of set_safe_states)
	check_safe_states(iDevIdx, iSlotID, connection)		    # check that all devices are in their safe-states

	print "Simple TCP/IP Run (Main) - Looking for a Confirmation from ORCA to start the SMELLIE run ... "
	connection.settimeout(5)                                    # set a timeout for receiving data
	try:
		while 1:
    			start_run = connection.recv(1024)
    			if (start_init_data == start_initialise_flag):      # check if initialisation command has been given
        			print "Simple TCP/IP Run (Main) - Ready to start sending run parameters"
        			break
	except conn.timeout:
		connection.send(timeout_flag)
		main()
        
	connection.settimeout(None)                                 # remove timeout for receiving data

	print "Simple TCP/IP Run (Main) - Waiting for run parameters from ORCA ... "
	ORCA_set_ls_channel(connection, iDevIdx)
	iDevIdx,iModuleType,iSlotID = sepiaUser.initialise()        # need to reinitialise Sepia after turning off during the changing of the laserSwitch channel (part of ORCA_set_ls_channel)
	ORCA_set_laser_parameters(connection)
	complete_self_test(connection, iDevIdx, iSlotID)
	sepiaUser.laser_soft_lock_on(iDevIdx, iSlotID)
	ORCA_set_fs_channel(connection)
	number_of_pulses = ORCA_ni_get_pulses(connection)                                 # get the number of pulses from the NI box
	trigger_frequency = ORCA_ni_get_trigger_frequency(connection)                     # get the trigger frequency of the NI box
	perform_run(connection, number_of_pulses, trigger_frequency, iDevIdx, iSlotID)    # complete the SMELLIE run

	sys.exit("Simple TCP/IP Run (Main) - good exit")


# try the main function, and if anything goes wrong then return to the start of the main function 
try:
	main()
except conn.error:
	print "Simple TCP/IP Run (Main Try/Catch) - Connection error: SMELLIE is restarting ... "
	main()
except conn.timeout:
	print "Simple TCP/IP Run (Main Try/Catch) - Connection timeout: SMELLIE is restarting ... "
	main()

sys.exit("Simple TCP/IP Run (Main Try/Catch) - bad exit")


