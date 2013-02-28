## Written by Christopher Jones 19/01/2013
## This is designed as a quick run to test if SMELLIE has been installed properly after being moved 
## SmellieRS = relay switch on smellie, fs = fibre switch on smellie, safepysepia are safe functions for the sepia 2 laser box 

# Import all the functions in these python modules

import sys,time,os
import safepysepia as sepia
import pysepia
import SmellieRS as rs
import fs
import sm_analogue as smni


def set_safe_states(iDevIdx,iSlotID):
    sepia.laser_soft_lock_on(iDevIdx,iSlotID)	## turns the laser soft lock on 
    sepia.set_laser_intensity(0,iDevIdx)          #sets the intensity to 0%
    sepia.set_laser_frequency(6,iDevIdx) 		##sets the frequency to external trigger need to check this
    rs.SetRSChannel(0)			        ##sets the relay box to channel 0 (default channel)
    sepia.close(iDevIdx)
    rs.Execute()                                    ##executes the relay switch channel

def set_laser_switch(laser_switch_number):
    iDevIdx,iModuleType,iSlotID = sepia.initialise() 
    rs.SetRSChannel(laser_switch_number)
    sepia.close(iDevIdx)
    rs.Execute()                                    
    iDevIdx,iModuleType,iSlotID = sepia.initialise() 
    sepia.laser_soft_lock_on(iDevIdx,iSlotID)	


def smellie_test_run(laser_switch_number,fibre_switch_start_number,file_to_write,iDevIdx,iModuleType,iSlotID):
    print "Testing laser switch number : " + str(laser_switch_number)
    set_laser_switch(laser_switch_number)
    input_intensity = 100
    input_frequency = 4	                                        ## this number determines if the sepia is working properly	                
    sepia.set_laser_intensity(input_intensity,iDevIdx)	        ##sets the intensity to 100%
    sepia.set_laser_frequency(input_frequency,iDevIdx)		##sets the frequency
    
    for fibre_switch_number in range(1,15):
        
        fibre_switch_number =  fibre_switch_start_number + fibre_switch_number 
        fs.SetFSChannel(fibre_switch_number)		        ##sets the fibre switch channel 
        sepia.laser_soft_lock_off(iDevIdx,iSlotID)		## this function unlocks the laser 
        time.sleep(1)						

        ## this part of the code includes generating a pulse and reading the PMT value  ##############
        ############# ############ ############ ############ ############## ############## ##########
        #trigger_frequency = 10000
        #number_of_pulses = 100000
        #digi_trig = smni.GenerateDigitalTrigger(trigger_frequency,number_of_pulses)
        #read_signal = smni.AquireAnalogue()
        #number_of_measurements = 1  
        #voltage_signal = str(read_signal.start(number_of_measurements))
        #digi_trig.start()
        #digi_trig.stop()
        #read_signal = smni.AquireAnalogue()
        #a = raw_input("Generating pulse train. Press Enter to interrupt\n")
        #read_signal.stop()
        #print voltage_signal                                    ## Need to decide how we would like this data
        #file_to_write.write(str(laser_switch_number) + '\t'+ str(fibre_switch_number) + '\t' + voltage_signal[1:-1] + '\n')
        ####################    ####################    ################### ##############  ############
        sepia.laser_soft_lock_on(iDevIdx,iSlotID)


def main():
    iDevIdx,iModuleType,iSlotID = sepia.initialise() 
    #set_safe_states(iDevIdx,iSlotID)                            ##sets all the laser components to their safe states 	
    
    timestamp = str(time.time())
    timestamp = timestamp[0:10]

    filename = 'smellie_test_at_20MHz_' + timestamp + '.txt' 

    f = open(filename,'w')
    
    ##run is completed here
    #smellie_test_run(3,0,f,iDevIdx,iModuleType,iSlotID)
    smellie_test_run(3,56,f,iDevIdx,iModuleType,iSlotID)
    #smellie_test_run(2,14,f,iDevIdx,iModuleType,iSlotID)
    #smellie_test_run(3,28,f,iDevIdx,iModuleType,iSlotID)
    #smellie_test_run(4,42,f,iDevIdx,iModuleType,iSlotID)
    #smellie_test_run(5,56,f,iDevIdx,iModuleType,iSlotID)
    
    iDevIdx,iModuleType,iSlotID = sepia.initialise() #Initialise the Sepia 2 box
    sepia.laser_soft_lock_on(iDevIdx,iSlotID)
    sepia.close(iDevIdx)
    f.close()
    time.sleep(1)
    folder_path = "C:\Users\LocalAdmin\Desktop\smellie_install_tests"    

main()






