import sys, time, os,ctypes
import pysepiaUser as sepiaUser
import pysepia
import subprocess as sub
import laserSwitch as rs
import fibreSwitch as fs
import socket as conn                # socket constructor and constants
import niADCDoublePulse as ni
import niADC as ni_old

def pulse_master_mode(master_mode_trigger_frequency,master_mode_number_of_pulses):
    retValue = 0
    try:
##        print "Starting a Master mode sub run with trig frequency: " + str(master_mode_trigger_frequency) + "Hz and num_of_pulses:" + str(master_mode_number_of_pulses)
        digi_trig = ni.GenerateDigitalTriggerDoublePulse(int(master_mode_trigger_frequency), int(master_mode_number_of_pulses))
        i =10
        while(i ==10):
            digi_trig.start()
            digi_trig.stop()
            time.sleep(0.01)
    except ValueError, Argument:
        retValue = "Error: " + str(ValueError) + "  " + str(Argument)
    return retValue

def pulse_master_mode_old(master_mode_trigger_frequency,master_mode_number_of_pulses):
    retValue = 0
    try:
##        print "Starting a Master mode sub run with trig frequency: " + str(master_mode_trigger_frequency) + "Hz and num_of_pulses:" + str(master_mode_number_of_pulses)
        digi_trig = ni_old.GenerateDigitalTrigger(int(master_mode_trigger_frequency), int(master_mode_number_of_pulses))
        digi_trig.start()
        digi_trig.stop()
    except ValueError, Argument:
        retValue = "Error: " + str(ValueError) + "  " + str(Argument)
    return retValue


##i = 10
##while(i == 10):
pulse_master_mode(20000000,2)
##    time.sleep(0.05)
