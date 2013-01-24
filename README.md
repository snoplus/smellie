smellie
=======

a scattering module in the embedded led light injection entity

* file and function names are a work in progress but should be changed to be more self-explanatory,
  e.g. laserSwitch.py instead of SmellieRS.py
       pysepiaUser.py instead of safepysepia.py

* please update when altering or adding to code

Contains:
- fibreSwitch.py -- Contains the commands for controlling the fibre switch
                 -- SetFSChannel(x) changes the fibre switch channel via serial port to the channel "x", between 1 and 70
                 -- SetIOChannels(i, o) changes the fibre switch channel via serial port to the input channel "i", between 1 and 5, and output channel "o", between 1 and 14
                        * The calculation of the overall channel number "x" from the input and output channels is done automatically by the function

- SmellieRS.py -- Contains the commands for the laser switch
               -- ChannelUp() change selected channel up one number (0-5)
               -- Execute() switches to selected channel and waits 30s to allow laser driver to reset
               -- GetDisplayChannel() returns selected channel
               -- GetLastChannel() returns currently active channel
               -- SetRSChannel(x) changes selected channel to "x"
               -- CheckExe() checks if Execute() command is in progress (hardware freezes user out while laser switch is happening so software needs to be aware of this)

- pysepia.py -- Contains the basic commands of the laser driver box
             -- These are just the default C++ functions in python wrappers.
             -- More details in Sepia2 users manual

- safepysepia.py -- Contains commands for the user for the laser driver box
                 -- The basic pysepia commands arranged into useful forms
                 -- initialise() opens USB communication, gets module map, device id, module type, etc...
                 -- close() free module map and close USB communication
                 -- check_pulse_mode(pulse_mode) check laser is set to pulse mode rather than continuous
                 -- set_laser_intensity(new_intensity,device_id) sets laser intensity (if sensible) 
                 -- set_laser_frequency(new_frequency,device_id) sets laser frequency (if sensible)
                 -- get_laser_states(device_id) gets intensity, frequency, pulse mode, head id 
                 -- get_laser_lock_status(device_id,slot_id) checks whether laser is locked
                 -- laser_soft_lock_on(device_id,slot_id) sets soft lock on
                 -- laser_soft_lock_off(device_id,slot_id) sets soft lock off

- simple_smellie_run.py -- Contains a mock smellie "run" initialising the software, checking for errors, setting parameters before switching laser on. Laser is then locked and system closed down.
- tcpip_simple_smellie_run.py -- Contains a mock smellie "run" but with communication to ORCA via TCP/IP Protocol. 
			   This program recieves commands from ORCA (from commands in smellie_orca_control.py).
			   A run typically involves initialising the software, checking for errors, setting parameters before switching laser on. Laser is then locked and system closed down. 
- smellie_orca_control.py -- Contains the commands to control a SMELLIE RUN from the ORCA Terminal. 
			   This communicates with SMELLIE via the tcpip_simple_smellie_run.py script 
