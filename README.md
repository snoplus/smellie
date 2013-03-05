SMELLIE
=======

Scattering Module for the Embedded LED Light Injection Entity  

* File and function names are a work in progress  
* Please update this README when altering or adding to the code  

-------------------------


Contains:

* fibreSwitch.py - contains the commands for controlling the fibre switch  
-- SetFSChannel(x): changes the fibre switch channel via serial port to the channel "x", between 1 and 70  
-- SetIOChannels(i, o): changes the fibre switch channel via serial port to the input channel "i", between 1 and 5, and output channel "o", between 1 and 14  

* laserSwitch.py - contains the commands for controlling the laser switch  
-- ChannelUp(): changes the selected channel up by 1  
-- Execute(): switches the active channel to the selected channel, and then waits 30 seconds to allow the SEPIA Unit to reset  
-- GetSelectedChannel(): returns the selected channel as shown on the Laser Switch's front panel 8-segment display  
-- GetActiveChannel(): returns the currently active channel as shown on the Laser Switch's front panel LEDs  
-- SetSelectedChannel(x): changes the selected channel to "x", between 0 and 5 inclusive  
-- CheckExecution(): checks if the Execute() command is currently in progress (the hardware locks out user-control while switching between lasers, so the software needs to be aware of this)  

* pysepia.py  - contains the basic commands for controlling the SEPIA II Laser Driver unit  
-- These are just the default C++ functions in python wrappers  
-- More details can be found in the Sepia II Users Manual  
-- THIS SCRIPT SHOULD NOT BE ALTERED  

* pysepiaUser.py - contains the commands for Users to control the SEPIA II Laser Driver unit  
-- All pysepia.py commands are available here, but now arranged into more user-friendly forms  
-- initialise(): opens USB communication, gets module map, device id, module type, etc ...  
-- close(): frees module map and closes USB communication  
-- check_pulse_mode(pulse_mode): checks that the laser is set to "Pulse" mode rather than "Continuous"  
-- set_laser_intensity(new_intensity, device_id): sets laser intensity, between 0 and 100  
-- set_laser_frequency(new_frequency, device_id): sets laser frequency, integer between 0 and 8  
-- get_laser_parameters(device_id): displays the intensity, frequency, pulse mode and head id  
-- get_laser_lock_status(device_id, slot_id): checks whether the laser is soft-locked  
-- laser_soft_lock_on(device_id, slot_id): sets the laser soft-lock to "on"  
-- laser_soft_lock_off(device_id, slot_id): sets the laser soft-lock to "off"  

* DAQmx scripts (CallBack, Config, Constants, Functions, Types)  
-- These are control scripts for the National Instruments (NI) ADC box  
-- THESE SCRIPTS SHOULD NOT BE ALTERED  

* tcpip.py - contains very basic code for testing the ability to communicate over a TCP/IP connection  

* orcaControl.py - contains the commands to control a SMELLIE run from a separate terminal over a TCP/IP connection (analogous to using ORCA)  
-- initialise_socket(ip_address): creates a TCP/IP socket to the server with the specified ip-address, and check that the communication is available  
-- close_socket(socket): safely closes the communication socket  
-- check_connection(socket): checks that the TCP/IP connection from the terminal to SNOdrop is working correctly  
-- initialise(socket): sends a command to SNOdrop to begin the SMELLIE run  
-- check_laserSwitch(socket): checks the status of the laserSwitch  
-- set_ls_channel(x, socket): sets the laserSwitch channel to "x", between 0 and 5 inclusive  
-- check_sepia_connection(socket): checks that the communication to SEPIA is working correctly  
-- set_laser_parameters(intensity, frequency, socket): sets the laser intensity and frequency to the user-desired values  
-- set_fs_channel(x, socket): sets the fibreSwitch channel to the user-desired value  
-- set_ni_pulse_number(x, socket): sets the NI box to give "x" number of pulses  
-- set_ni_trigger_frequency(x, socket): sets the NI box to give pulses at a frequency of "x"  
-- check_safe_states(socket): checks that the hardware safe-states have been correctly set  
-- run_completion(socket): checks the completion status of the SMELLIE run  
-- main(): run the full TCP/IP Control Tests using THIS over-arching function  

* installationTesting - a full program for testing if the SMELLIE software has been correctly and successfully installed onto any given computer  
-- set_to_safe_state(device_id, slot_id): sets all parameters (laser intensity, laser frequency, laserSwitch channel) to their "safe" values  
-- set_laser_switch_channel(x): sets the laserSwitch to a given channel "x", between 0 and 5 inclusive  
-- test_run(laserSwitch Channel, fibreSwitch Channel, name of logfile, device_id, mode, slot_id): performs a full test run of all hardware (laserSwitch, Sepia and fibreSwitch)  
[THIS NEEDS TO BE CHECKED]  
-- main(): run the installation test using THIS over-arching function  

-------------------------


* simpleRun.py - contains a complete script for simulating a full run of the SMELLIE hardware  
-- this script is designed for running on SNOdrop itself - it does not simulate communication from or with ORCA via TCP/IP  
-- it uses functions from laserSwitch.py, fibreSwitch.py, pysepia.py and pysepiaUser.py above  
[THIS IS STILL A WORK-IN-PROGRESS]  

* simpleRun_withTCPIP.py - contains a complete script for simulating a full run of the SMELLIE hardware  
-- this script is to be run from an external terminal (i.e. ORCA) - it uses communication from or with ORCA via TCP/IP using functions from the various TCP/IP scripts detailed above  
-- it also uses functions from laserSwitch.py, fibreSwitch.py, pysepia.py and pysepiaUser.py above  

