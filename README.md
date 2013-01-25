SMELLIE
=======

Scattering Module for the Embedded LED Light Injection Entity

* File and function names are a work in progress
* Please update this readme when altering or adding to the code

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
-- set_laser_intensity(new_intensity,device_id): sets laser intensity, between 0 and 100
-- set_laser_frequency(new_frequency,device_id): sets laser frequency, integer between 0 and 8
-- get_laser_parameters(device_id): displays the intensity, frequency, pulse mode and head id 
-- get_laser_lock_status(device_id,slot_id): checks whether the laser is soft-locked
-- laser_soft_lock_on(device_id,slot_id): sets the laser soft-lock to "on"
-- laser_soft_lock_off(device_id,slot_id): sets the laser soft-lock to "off"


(code below still needs to be cleaned up)


- simple_smellie_run.py -- Contains a mock smellie "run" initialising the software, checking for errors, setting parameters before switching laser on. Laser is then locked and system closed down.
- tcpip_simple_smellie_run.py -- Contains a mock smellie "run" but with communication to ORCA via TCP/IP Protocol. 
			   This program recieves commands from ORCA (from commands in smellie_orca_control.py).
			   A run typically involves initialising the software, checking for errors, setting parameters before switching laser on. Laser is then locked and system closed down. 
- smellie_orca_control.py -- Contains the commands to control a SMELLIE RUN from the ORCA Terminal. 
			   This communicates with SMELLIE via the tcpip_simple_smellie_run.py script 
