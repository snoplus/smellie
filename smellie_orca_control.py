import sys,time
from socket import *              # portable socket interface plus constants

continue_flag = '5189'	      #this is the flag to continue with any run 
check_connection_flag = '10'  #this has to correspond the the check_connection_flag on SNODROP
start_initialise_flag = '20'  #this has to correspond the the start_initialise_flag on SNODROP 
sepia_box_no_connection_flag = '30'	#there is a problem with the sepia box or it is not connected properly
relay_switch_no_connection_flag  = '40'	#there is a probelm with the relay switch bow or it is not connected properly

# SAFE STATE ERROR CODES - These flags are raised if the wrong safe state settings are in place
sepia_wrong_set_intensity_flag = '50'	
sepia_wrong_freq_flag ='55'
sepia_wrong_pulse_mode_flag = '60'
relay_switch_wrong_default_flag = '65'
setup_run_flag = '70' 		##this flag is to confirm ORCA is happy to send parameters for the laser
self_test_fail = '77'		##this flag indicates a SMELLIE self-test has failed 
relay_switch_set_wrong = '79'	##this flag indicates that the relay_switch has been set wrong 
fs_channel_broken = '84'	##this flag indicates that the fs_channel is broken 
pulse_number_too_high = '87'
run_failure_flag = '102'
trigger_frequency_flag = '132'
timeout_flag = '123456'

# Initialise the TCP/IP socket with an IP address 
def initialise_socket(ip_address):	
	serverPort = 50007
	sockobj = socket(AF_INET, SOCK_STREAM)     # make a TCP/IP socket object
	sockobj.connect((ip_address, serverPort))  # connect to server machine and port
 	sockobj.send("")			   #send a blank message to SMELLIE to see response
	return sockobj	 	


#check that SMELLIE/SNODROP is working and responding to TCP/IP connection
def check_connection(sockobj):		  
	data = sockobj.recv(1024)
	if(data == check_connection_flag):
		print "\nSucessful connection to SMELLIE"
	else:
		print "Signal received :" + str(data)
		print "Signal recieved should be: " + check_connection_flag 
		sys.exit("No connection made to SMELLIE")	 

# command sent to SMELLIE to begin its initialisation 
def start_initialise_command(sockobj):
	sockobj.send(start_initialise_flag) 
	print "Command to start SMELLIE initialisation sent..."

# this function closes the socket and the TCP/IP connection 
def close_socket(sockobj):
	sockobj.close()

# this function checks the connection status of the sepia 2 box 
def check_sepia_connection(sockobj):
	data = sockobj.recv(1024)
	if(data == continue_flag):
		print "SMELLIE:Sepia 2 Laser Box working correctly"
	else:
		sys.exit("\nProgram Exit: Sepia 2 Laser Box either not connected properly or not powered up\n\n Re-run this program when this issue is resolved\n")

def check_relay_switch_box(sockobj):
	data = sockobj.recv(1024)
	if(data == continue_flag):
		print "SMELLIE:Relay Switch Box is working correctly"
	else:
		sys.exit("\nProgram Exit: Relay Switch Box either not connected properly or not powered up.\n\nRe-run this program when this issue is resolved\n")

def check_safe_states(sockobj):
	data = sockobj.recv(1024)
	if(data == continue_flag):
		print "SMELLIE:Safe states are correctly set"
		sockobj.send(setup_run_flag) 
	elif(data == sepia_wrong_set_intensity_flag):
		sys.exit("\nProgram Exit: Safe states intensity is incorrect.\n\nRe-run this program when this issue is resolved\n")
	elif(data == sepia_wrong_freq_flag):
		sys.exit("\nProgram Exit: Safe states frequency is incorrect.\n\nRe-run this program when this issue is resolved\n")
	elif(data == sepia_wrong_pulse_mode_flag):
		sys.exit("\nProgram Exit: Safe states pulse mode is incorrect. This needs to be set to 1!\n\nRe-run this program when this issue is resolved\n")
	elif(data == relay_switch_wrong_default_flag):
		sys.exit("\nProgram Exit: Relay Switch box safe state is incorrect\n\nRe-run this program when this issue is resolved\n")	
	else:
		sys.exit("\nProgram Exit: Unknown error. Please re-start SMELLIE and check SMELLIE DAQ\n\nRe-run this program when this issue is resolved\n")

def set_rs_channel(rs_channel,sockobj):	
	sockobj.send(rs_channel)
	data = sockobj.recv(1024)
	if(data == continue_flag):
		print "SMELLIE:Relay Channel Setting sent"
	elif(data == timeout_flag):
		sys.exit("\nProgram Exit: SMELLIE has timed out\n")
	else:
		sys.exit("\nProgram Exit: Unknown error. Please re-start SMELLIE and check SMELLIE DAQ\n\nRe-run this program when this issue is resolved\n")
		
	#wait for confirmation that the Sepia has rebooted
	while 1:
		data = sockobj.recv(1024)
		if data : break
	if(data == continue_flag):
		print "SMELLIE:Relay Channel set to : " + rs_channel
	elif(data == timeout_flag):
		sys.exit("\nProgram Exit: SMELLIE has timed out\n")
	else:
		sys.exit("\nProgram Exit: Relay Channel not set correctly\n")		


def send_parameters_cmd(intensity,frequency_mode,sockobj):
	sockobj.send(intensity)
	data = sockobj.recv(1024)
	if(data == continue_flag):
		print "SMELLIE:Intensity set to : " + intensity +"%" 
		sockobj.send(frequency_mode)
	elif(data == timeout_flag):
		sys.exit("\nProgram Exit: SMELLIE has timed out\n")
	else:
		sys.exit("\nProgram Exit: Intensity value not seen by ORCA\n")		
	##Do not change this order and this sets and this checks the frequency has been set correctly	
	data = sockobj.recv(1024)	
	if(data == continue_flag):
		print "SMELLIE:Frequency set to : External Rising" #external rising = 6 on Sepia Laser box		
		return 
	elif(data == timeout_flag):
		sys.exit("\nProgram Exit: SMELLIE has timed out\n")	
	else:
		sys.exit("\nProgram Exit: Frequency value not seen by ORCA\n")
# checks the self_test for SMELLIE
def check_self_test(sockobj):
	data = sockobj.recv(1024)
	if(data == continue_flag):
		print "SMELLIE:Self-test passed"
	elif(data == self_test_fail):
		sys.exit("\nProgram Exit: SMELLIE Self-test failed\n")
	elif(data == timeout_flag):
		sys.exit("\nProgram Exit: SMELLIE has timed out\n")
	else:
		sys.exit("\nProgram Exit: Unknown error. Please re-start SMELLIE and check SMELLIE DAQ\n\nRe-run this program when this issue is resolved\n")

def send_fs_channel(fs_channel,sockobj):
	sockobj.send(fs_channel)
	data = sockobj.recv(1024)
	if(data == continue_flag):
		print "SMELLIE:Fibre Switch Channel Set to : " + fs_channel
	elif(data == fs_channel_broken):
		sys.exit("\nProgram Exit: SMELLIE Fibre Switch Channel not correctly set\n")
	elif(data == timeout_flag):
		sys.exit("\nProgram Exit: SMELLIE has timed out\n")
	else:
		sys.exit("\nProgram Exit: Unknown error. Please re-start SMELLIE and check SMELLIE DAQ\n\nRe-run this program when this issue is resolved\n")

def send_pulse_number(number_of_pulses,sockobj):
	sockobj.send(number_of_pulses)
	data = sockobj.recv(1024)
	if(data == continue_flag):
		print "SMELLIE:Number of Pulses to be sent : " + number_of_pulses
	elif(data == pulse_number_too_high):
		sys.exit("\nProgram Exit: The number of pulses is greater than 100,000 pulses\n")
	elif(data == timeout_flag):
		sys.exit("\nProgram Exit: SMELLIE has timed out\n")
	else:
		sys.exit("\nProgram Exit: Unknown error. Please re-start SMELLIE and check SMELLIE DAQ\n\nRe-run this program when this issue is resolved\n")

def send_trigger_frequency(trigger_frequency,sockobj):
	sockobj.send(trigger_frequency)
	data = sockobj.recv(1024)
	if(data == continue_flag):
		print "SMELLIE:Trigger Frequency : " + trigger_frequency + " Hz"
	elif(data == trigger_frequency_flag):
		print data 
		sys.exit("\nProgram Exit: Trigger frequency is not correctly set\n")
	elif(data == timeout_flag):
		sys.exit("\nProgram Exit: SMELLIE has timed out\n")
	else:
		print data
		sys.exit("\nProgram Exit: Unknown error. Please re-start SMELLIE and check SMELLIE DAQ\n\nRe-run this program when this issue is resolved\n")

def run_completion(sockobj):
	data = sockobj.recv(1024)
	if(data == continue_flag):
		print "SMELLIE:Run Complete!"
	elif(data == run_failure_flag):
		sys.exit("\nProgram Exit: SMELLIE run failed\n")
	elif(data == timeout_flag):
		sys.exit("\nProgram Exit: SMELLIE has timed out\n")
	else:
		sys.exit("\nProgram Exit: Unknown error. Please re-start SMELLIE and check SMELLIE DAQ\n\nRe-run this program when this issue is resolved\n")

def main():		
	ip_address = "192.168.0.1" 
	sockobj = initialise_socket(ip_address)
	check_connection(sockobj)			
	start_initialise_command(sockobj)
	check_sepia_connection(sockobj)
	check_relay_switch_box(sockobj)
	check_safe_states(sockobj)
	set_intensity = '100'
	set_frequency_mode = '6'
	rs_channel = '3'
	fs_channel = '29'
	number_of_pulses = '100000'
	trigger_frequency = '10000'
	set_rs_channel(rs_channel,sockobj)
	send_parameters_cmd(set_intensity,set_frequency_mode,sockobj)
	check_self_test(sockobj)
	send_fs_channel(fs_channel,sockobj)
	send_pulse_number(number_of_pulses,sockobj)
	send_trigger_frequency(trigger_frequency,sockobj)
	run_completion(sockobj)
main()

