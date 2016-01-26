# This script is written to test the 405nm Laser

# Import all functions found in the following python modules:
import sys, time, os
import pysepiaUser as sepiaUser
import pysepia
import laserSwitch as rs
import fibreSwitch as fs
import niADC as ni


def set_to_safe_state(iDevIdx, iSlotID):
    sepiaUser.laser_soft_lock_on(iDevIdx, iSlotID)	# turn the laser soft-lock on 
    sepiaUser.set_laser_intensity(0, iDevIdx)       # set the laser intensity to 0%
    sepiaUser.set_laser_frequency(6, iDevIdx) 		# set the laser to trigger on the rising edge of an external pulse
    rs.SetSelectedChannel(0)			            # set the laserSwitch to channel 0 (default channel)
    sepiaUser.close(iDevIdx)
    rs.Execute()                                    # execute the laserSwitch channel change


def set_laser_switch_channel(channel):
    iDevIdx,iModuleType,iSlotID = sepiaUser.initialise() 
    rs.SetSelectedChannel(channel)
    sepiaUser.close(iDevIdx)
    rs.Execute()                                    
    iDevIdx,iModuleType,iSlotID = sepiaUser.initialise() 
    sepiaUser.laser_soft_lock_on(iDevIdx, iSlotID)

def initialSetLaser(ls_channel,operation_mode,intensity):

    iDevIdx,iModuleType,iSlotID = sepiaUser.initialise() 
    set_laser_switch_channel(ls_channel)
    sepiaUser.set_laser_intensity(intensity, iDevIdx) # set the intensity to 100%
    sepiaUser.set_laser_frequency(operation_mode, iDevIdx)
    sepiaUser.close(iDevIdx) 

    #fs_input_channel = 5
    #fs_output_channel = 1

    #channel_number = ((fs_input_channel - 1) * 14) + fs_output_channel      # pick the correct channel number
    #print(channel_number)
    #fs.SetFSChannel(channel_number)                                         # set the fibreSwitch channel
    # laserTime = 5                                       # time for program to wait before locking the laser (i.e. laser operating time)
    # sepiaUser.laser_soft_lock_off(iDevIdx, iSlotID)                         # unlock the laser
    # time.sleep(laserTime)                                                   # make Python sleep while laser is working 

    # iDevIdx,iModuleType,iSlotID = sepiaUser.initialise()                    # re-initialise Sepia 
    # sepiaUser.laser_soft_lock_on(iDevIdx, iSlotID)                          # soft lock on
    # sepiaUser.close(iDevIdx)                                                # close the Sepia box down...
    
    # time.sleep(1)

def setFibreSwitch(fs_input_channel,fs_output_channel):
    channel_number = ((fs_input_channel - 1) * 14) + fs_output_channel      # pick the correct channel number
    print(channel_number)
    fs.SetFSChannel(channel_number)
    
    
#USE THIS FOR TESTING AND CONTROLLING THE LASEER
#Testing and controling the different outputs from the fibre switch
#OPERATION MODE: 0 (80MHz), 1 (40MHz), 2 (20MHz), 3 (10MHz), 4 (5MHz), 5 (2.5MHz), 6 (external rising edge), 7 (external falling edge)

#Manually check to see this makes sense 
def firstRun():
    ls_channel = 3                #choose the laser
    operation_mode = 6                      #DO NOT USE 0 OR 1 !!!!!!!!!!!!!!!
    intensity = 0                           #this is in percentage of the intensity

    #Set to safe states
    iDevIdx,iModuleType,iSlotID = sepiaUser.initialise() 
    set_to_safe_state(iDevIdx, iSlotID)                                     # set all the laser parameters to safe values
    
    initialSetLaser(ls_channel,operation_mode,intensity)

    #Set the fibre switch to check this is working fine 
    fibre_switch_input_channel = 1
    fibre_switch_ouput_channel = 10

    setFibreSwitch(fibre_switch_input_channel,fibre_switch_ouput_channel)
    #sepiaUser.laser_soft_lock_off(iDevIdx, iSlotID)                         # unlock the laser
    #laserTime = 10
    #sepiaUser.laser_soft_lock_on(iDevIdx, iSlotID)
    #time.sleep(1)
    #sepiaUser.close(iDevIdx)

def cycleFibreSwitch(fs_input_channel,ls_channel):

    operation_mode = 6

    iDevIdx,iModuleType,iSlotID = sepiaUser.initialise() 
    set_to_safe_state(iDevIdx, iSlotID)

    iDevIdx,iModuleType,iSlotID = sepiaUser.initialise() 
    set_laser_switch_channel(ls_channel)

    iDevIdx,iModuleType,iSlotID = sepiaUser.initialise()                    # re-initialise Sepia 
    sepiaUser.laser_soft_lock_on(iDevIdx, iSlotID)                          # soft lock on

    sepiaUser.set_laser_frequency(operation_mode, iDevIdx)

    intensity_value = 0

    print "FibreSwitchInput:" + str(fs_input_channel)
    print "LaserChannel:" + str(ls_channel)

    for intensity_iterator in range(0,80):

        intensity_value = 100 - intensity_iterator

        sepiaUser.set_laser_intensity(intensity_value, iDevIdx)
                                                   
        for fs_output_channel in range(7, 13):

            channel_number = ((fs_input_channel - 1) * 14) + fs_output_channel
            print "Intensity Value:" + str(intensity_value) +" FibreSwitchOutput:" + str(fs_output_channel)
            fs.SetFSChannel(channel_number) # set the fibreSwitch channel
            
            sepiaUser.laser_soft_lock_off(iDevIdx, iSlotID) # unlock the laser
            time.sleep(5) 
            sepiaUser.laser_soft_lock_on(iDevIdx, iSlotID)
            time.sleep(1)
        
    sepiaUser.laser_soft_lock_on(iDevIdx, iSlotID)                          # soft lock on
    sepiaUser.close(iDevIdx)                                                # close the Sepia box down... 
    
    time.sleep(1)

def main2():
    firstRun()
    #cycleFibreSwitch()

#main2()

iDevIdx,iModuleType,iSlotID = sepiaUser.initialise() 
set_to_safe_state(iDevIdx, iSlotID)
initialSetLaser(4,6,60)
time.sleep(5)
setFibreSwitch(4,8)

#cycleFibreSwitch(3,2)


    




