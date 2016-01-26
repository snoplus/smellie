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
	#sepiaUser.laser_soft_lock_on(iDevIdx, iSlotID)   # turn the laser soft-lock on
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
#def ORCA_set_laser_parameters(connection):
#	intensity_set = timeout(connection, 10)   # get the laser intensity, with a 10 second timeout
#	connection.send(continue_flag)            # continue
#	frequency_set = timeout(connection,10)    # get the laser frequency mode, with a 10 second timeout
#	connection.send(continue_flag)            # continue
#	print "Simple TCP/IP Run (ORCA Set Laser Parameters) - Laser is set to intensity:" + intensity_set + "%"

#	if (frequency_set == '6'):
#		print "Simple TCP/IP Run (ORCA Set Laser Parameters) - Laser is set to frequency mode: 6 (External Rising-Edge)"
#	else:
#                print "Simple TCP/IP Run (ORCA Set Laser Parameters) - Laser is NOT set to frequency mode 6 (External Rising-Edge)"
#                connection.send(sepia_wrong_pulse_mode_flag)
#		main()


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
#def ORCA_ni_get_pulses(connection):
#	pulse_number_set = timeout(connection, 10)    # get the number of pulses to be generated by the NI box, with a 10 second timeout
#	if (int(pulse_number_set) <= 100000):
#		connection.send(continue_flag)
#		print "Simple TCP/IP Run (ORCA Set NI No. of Pulses) - Generate " + str(int(pulse_number_set)) + " pulses"
#		return int(pulse_number_set)
#	else:
#    		print "Simple TCP/IP Run (ORCA Set NI No. of Pulses) - The number of pulses you want is too high"
#		connection.send(pulse_number_too_high)
#		main()

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


def extractMasterModeFromCode(masterModeValues):
        separateIndex = masterModeValues.index('s')
        masterModeFrequency = masterModeValues[0:separateIndex]
        masterModeNumPulses = masterModeValues[separateIndex+1:-1]
        print masterModeFrequency, masterModeNumPulses
        return masterModeFrequency, masterModeNumPulses

def extractLaserFibreValues(masterModeValues):
        separateIndex = masterModeValues.index('s')
        masterModeFrequency = masterModeValues[0:separateIndex]
        masterModeNumPulses = masterModeValues[separateIndex+1:]
        print masterModeFrequency, masterModeNumPulses
        return masterModeFrequency, masterModeNumPulses

##### START OF THE MAIN PROGRAM ####################################################################################################

timeout_flag = str(500)

# CONTROL FLAGS
check_connection_flag = 10
set_laser_switch_flag = 2050
set_safe_states_flag = 30
set_fibre_switch_channel_flag = 40
set_laser_intensity_flag = 50
set_laser_soft_lock_on_flag = 60
set_laser_soft_lock_off_flag = 70
master_mode_flag = 80 #this has two arguments separated by an s in the string
set_laser_testing_frequency_mode = 90 #be very careful with this mode (do not use this during normal running)

# Whenever there is an error, the program will revert back to this point and wait for more commands via TCP/IP (from ORCA)
def main():	

        myHost = ''                                                     # initialise the server machine ('' means: local host)
        myPort = 50009                                                  # listen on a non-reserved port number

        conn.sockobj = conn.socket(conn.AF_INET, conn.SOCK_STREAM)       # make a TCP/IP socket object
        conn.sockobj.settimeout(None)                                    # No timeout on the socket
        conn.sockobj.setsockopt(conn.SOL_SOCKET,conn.SO_REUSEADDR,1)
        conn.sockobj.bind((myHost, myPort))                              # bind the socket object to the specified server and port number 
        conn.sockobj.listen(5)                                           # begin listening, and allow 5 pending connects

        # Check for connection confimation from ORCA
        print "Simple TCP/IP Run (Main) - Checking for connection confimation from ORCA ... "	
        while 1:                                                        # listen until process killed
                connection, address = conn.sockobj.accept()             # wait for next client connection
                print 'Connection made to:' + str(address)              # connection is a new socket
                if address : break		
        connection.send(str(check_connection_flag))                          # send signal to ORCA  to check connection

        controlFlag = '0'
        controlArgument = '0'
        master_mode_trigger_frequency = '0'
        master_mode_number_of_pulses = '0'

        # Get the control flag
        connection.settimeout(5) 
        try:
                while 1:
                        controlFlag = connection.recv(1024)
                        #print "ControlFlag = " + str(controlFlag)
                        break
                
        except conn.timeout:
                connection.send(timeout_flag)
                main()

        connection.send(str(check_connection_flag))         

        # Get the control argument
        connection.settimeout(5) 
        try:
                while 1:
                        controlArgument = connection.recv(1024)
                        break
                
        except conn.timeout:
                connection.send(timeout_flag)
                main()
                
        connection.send(str(check_connection_flag)) 
        #connection.send(str(check_connection_flag)) #send this to signify that this is finished
        #main()

        #print "ControlFlag = " + str(controlFlag)
        #controlFlag = 60
        
        try:
                #print 'controlFlag: ' + str(controlFlag)
                #print 'laser intensity flag' + str(set_laser_intensity_flag)
                # set the laser switch channel 
                if (int(controlFlag) == int(set_laser_switch_flag)):      
                        print "Set the Laser switch to state" + str(controlArgument)
                        iDevIdx,iModuleType,iSlotID = sepiaUser.initialise()
                        rs.SetSelectedChannel(int(controlArgument))
                        sepiaUser.close(iDevIdx)
                        rs.Execute() 
                
                # set safe sates
                elif (int(controlFlag) == int(set_safe_states_flag)):
                        print "Setting to safe states"
                        iDevIdx,iModuleType,iSlotID = sepiaUser.initialise()
                        set_safe_states(iDevIdx, iSlotID)
                        
                # set fibre switch channel 
                elif (int(controlFlag) == int(set_fibre_switch_channel_flag)):
                        print(controlArgument)
                        input_channel,output_channel = extractLaserFibreValues(controlArgument)
                        print "Set the Fibre Switch to input Channel:" + str(input_channel) +" and output channel:" + str(output_channel)
                        fs.SetIOChannels(int(input_channel), int(output_channel))
                        # fs.SetFSChannel(controlArgument)

                # set laser intensity 
                elif (int(controlFlag) == int(set_laser_intensity_flag)):
                        print "Set Laser Intensity to " + str(controlArgument) + "%"
                        iDevIdx,iModuleType,iSlotID = sepiaUser.initialise()
                        time.sleep(1.0)
                        sepiaUser.set_laser_intensity(int(controlArgument), iDevIdx)
                        time.sleep(1.0)
                        sepiaUser.close(iDevIdx)

                # set soft lock on
                elif (int(controlFlag) == int(set_laser_soft_lock_on_flag)):
                        print "Set laser soft lock on"
                        iDevIdx,iModuleType,iSlotID = sepiaUser.initialiseSCMModule()
                        time.sleep(1.0)
                        sepiaUser.laser_soft_lock_on(iDevIdx, iSlotID)
                        time.sleep(1.0)
                        sepiaUser.close(iDevIdx)

                # start master mode run 
                elif (int(controlFlag) == int(master_mode_flag)):
                        master_mode_trigger_frequency,master_mode_number_of_pulses = extractMasterModeFromCode(controlArgument)
                        print "Starting a Master mode sub run with trig frequency: " + str(master_mode_trigger_frequency) + "Hz and num_of_pulses:" + str(master_mode_number_of_pulses)
                        #iDevIdx,iModuleType,iSlotID = sepiaUser.initialise()
                        #time.sleep(1.0)
                        #iDevIdx2,iModuleType2,iSlotID2 = sepiaUser.initialiseSCMModule()
                        #sepiaUser.laser_soft_lock_off(iDevIdx, iSlotID2)
                        #time.sleep(1.0)
                        digi_trig = ni.GenerateDigitalTrigger(int(master_mode_trigger_frequency), int(master_mode_number_of_pulses))
                        digi_trig.start()
                        digi_trig.stop()
                        #sepiaUser.laser_soft_lock_on(iDevIdx, iSlotID2)
                        #time.sleep(1.0)
                        #sepiaUser.close(iDevIdx)
                        #sepiaUser.close(iDevIdx2)

                # set soft lock off
                elif (int(controlFlag) == int(set_laser_soft_lock_off_flag)):
                        print "Set laser soft lock off"
                        iDevIdx,iModuleType,iSlotID = sepiaUser.initialiseSCMModule()
                        time.sleep(1.0)
                        print sepiaUser.laser_soft_lock_off(iDevIdx, iSlotID)
                        time.sleep(1.0)
                        sepiaUser.close(iDevIdx)
                # set the laser frequency to high enough to see visually 
                elif (int(controlFlag) == int(set_laser_testing_frequency_mode)):
                        print "Setting laser to 20MHz testing Mode"
                        iDevIdx,iModuleType,iSlotID = sepiaUser.initialise()
                        sepiaUser.set_laser_frequency(2, iDevIdx)        # set the laser frequency to 20Mhz
                        sepiaUser.close(iDevIdx)
                        
                else:
                        print "No command value recieved"
                        # put all the possible options in here

                        
        except:
                connection.send(timeout_flag)
                main()

        connection.send(str(check_connection_flag)) #send this to signify that this is finished

        print "Return to listening on the port"
        main()                                # return to listening on the port 

# try the main function, and if anything goes wrong then return to the start of the main function 
try:	
        main()
except conn.error:
        print "Simple TCP/IP Run (Main Try/Catch) - Connection error: SMELLIE is restarting ... "
        main()
except conn.timeout:
        print "Simple TCP/IP Run (Main Try/Catch) - Connection timeout: SMELLIE is restarting ... "
        main()


