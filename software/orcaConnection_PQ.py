#!/usr/bin/env python
import sys, time, os,ctypes
import pysepiaUser as sepiaUser
import pysepia
import gainControl as gc
import subprocess as sub
import laserSwitch as rs
import fibreSwitch as fs

def set_safe_states():
    retValue = 0
    try:
        iDevIdx,iModuleType,iSlotID = sepiaUser.initialise()
        #sepiaUser.laser_soft_lock_on(iDevIdx, iSlotID)   # turn the laser soft-lock on
        sepiaUser.set_laser_intensity(0, iDevIdx)         # set the laser intensity to 0%
        sepiaUser.set_laser_frequency(6, iDevIdx)         # set the laser frequency to external rising-edge trigger
        rs.SetSelectedChannel(0)			      # set the laserSwitch to channel 0 (default)
        sepiaUser.close(iDevIdx)
        rs.Execute()                                      # execute the laserSwitch channel change from above
    except errorCode, Argument:
        retValue = "Error: " + str(errorCode) + "  " + str(Argument)
    return retValue

def set_laser_switch(laser_switch_channel):
    retValue = 0
    try:
        print "Set the Laser switch to channel " + str(laser_switch_channel)
        iDevIdx,iModuleType,iSlotID = sepiaUser.initialise()
        rs.SetSelectedChannel(int(laser_switch_channel))
        sepiaUser.close(iDevIdx)
        rs.Execute() 
    except errorCode, Argument:
        retValue = "Error: " + str(errorCode) + "  " + str(Argument)
    return retValue

def set_fibre_switch(input_channel,output_channel):
    retValue = 0
    try:
        print "Set the Fibre Switch to input Channel:" + str(input_channel) +" and output channel:" + str(output_channel)
        fs.SetIOChannels(int(input_channel), int(output_channel))
    except errorCode, Argument:
        retValue = "Error: " + str(errorCode) + "  " + str(Argument)
    return retValue

def set_laser_intensity(intensity):
    retValue = 0
    try:
        print "Set Laser Intensity to " + str(intensity) + "%"
        iDevIdx,iModuleType,iSlotID = sepiaUser.initialise()
        time.sleep(1.0)
        sepiaUser.set_laser_intensity(int(intensity), iDevIdx)
        time.sleep(1.0)
        sepiaUser.close(iDevIdx)
    except errorCode, Argument:
        retValue = "Error: " + str(errorCode) + "  " + str(Argument)
    return retValue

def set_soft_lock_on():
    retValue = 0
    try:
        print "Set laser soft lock on"
        iDevIdx,iModuleType,iSlotID = sepiaUser.initialiseSCMModule()
        time.sleep(1.0)
        sepiaUser.laser_soft_lock_on(iDevIdx, iSlotID)
        time.sleep(1.0)
        sepiaUser.close(iDevIdx)
    except errorCode, Argument:
        retValue = "Error: " + str(errorCode) + "  " + str(Argument)
    return retValue

def set_gain_control(voltage):
    retValue = 0
    try:
        print "Setting gain control to " + str(voltage) + " mV"
        gc.startGainControl(voltage)
    except errorCode, Argument:
        retValue = "Error:" + str(errorCode) + "  " + str(Argument)    
    return retValue

def set_soft_lock_off():
    retValue = 0
    try:
        print "Set laser soft lock on"
        iDevIdx,iModuleType,iSlotID = sepiaUser.initialiseSCMModule()
        time.sleep(1.0)
        sepiaUser.laser_soft_lock_off(iDevIdx, iSlotID)
        time.sleep(1.0)
        sepiaUser.close(iDevIdx)
    except errorCode, Argument:
        retValue = "Error: " + str(errorCode) + "  " + str(Argument)
    return retValue

def pulse_master_mode(master_mode_trigger_frequency,master_mode_number_of_pulses):
    retValue = 0
    try:
        print "Starting a Master mode sub run with trig frequency: " + str(master_mode_trigger_frequency) + "Hz and num_of_pulses:" + str(master_mode_number_of_pulses)
        digi_trig = ni.GenerateDigitalTrigger(int(master_mode_trigger_frequency), int(master_mode_number_of_pulses))
        digi_trig.start()
        digi_trig.stop()
    except errorCode, Argument:
        retValue = "Error: " + str(errorCode) + "  " + str(Argument)
    return retValue

def laser_testing_mode():
    retValue = 0
    try:
        print "Setting laser to 20MHz testing Mode"
        iDevIdx,iModuleType,iSlotID = sepiaUser.initialise()
        sepiaUser.set_laser_frequency(2, iDevIdx)        # set the laser frequency to 20Mhz
        sepiaUser.close(iDevIdx)
    except errorCode, Argument:
        retValue = "Error: " + str(errorCode) + "  " + str(Argument)
    return retValue

def findnth(haystack, needle, n):
    parts= haystack.split(needle, n+1)
    if len(parts)<=n+1:
        return -1
    return len(haystack)-len(parts[-1])-len(needle)

def kill_sepia_and_nimax():
    retValue = 0
    # 1 - access denied
    # 0 - sucessful kill 
    try:
        #time.sleep(2)
        p = sub.Popen('tasklist /FI "IMAGENAME eq Sepia2.exe" /FO CSV /NH',stdout=sub.PIPE,stderr=sub.PIPE)
        sepiaPid, errors = p.communicate()
        startIndex = findnth(sepiaPid,'"',2)
        endIndex = findnth(sepiaPid,'"',3)
        sepiaPid = sepiaPid[startIndex+1:endIndex]
        print "Sepia PID: " + sepiaPid

        PROCESS_TERMINATE = 1
        handle = ctypes.windll.kernel32.OpenProcess(PROCESS_TERMINATE,False,int(sepiaPid))
        retValue = ctypes.windll.kernel32.TerminateProcess(handle,-1)
        print retValue

        time.sleep(0.1)

        p2 = sub.Popen('tasklist /FI "IMAGENAME eq NIMax.exe" /FO CSV /NH',stdout=sub.PIPE,stderr=sub.PIPE)
        niPid, errors = p2.communicate()
        startIndex = findnth(niPid,'"',2)
        endIndex = findnth(niPid,'"',3)
        niPid = niPid[startIndex+1:endIndex]
        print "NIMAX PID: " + niPid

        PROCESS_TERMINATE = 1
        handle = ctypes.windll.kernel32.OpenProcess(PROCESS_TERMINATE,False,int(niPid))
        retValue = ctypes.windll.kernel32.TerminateProcess(handle,-1)
        print retValue

    except errorCode, Argument:
        retValue = "Error: " + str(errorCode) + "  " + str(Argument)
    print retValue
    return retValue
