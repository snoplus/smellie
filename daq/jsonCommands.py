# Commands to Read in Parameters from the SMELLIE JSON file
# Written by Christopher Jones (11/03/2013)
# Additional changes by Krish Majumdar (15/03/2013)
# Updates to test and check the JSON files (4/06/2013) 

# This Python script is highly reliant upon the JSON file being in the correct format!! 
# Any value error/deliminter compiler errors for this script will most likely be the 
# JSON file you are trying to read is in an incorrect format 

import json

# Read in the JSON parameter-file
def ReadJSON(filename):
    dataDict = json.load(open(filename))
    return dataDict


# Return the Run number for future reference
def returnRun(dict, run):
    for i in range(0, len(dict['run_list']), 1):
        if dict['run_list'][i]['run_id'] == run:
            return i


# Return the SubRun number for future reference
def returnSubRun(dict, subrun):
    for i in range(0, len(dict['hw']), 1):
        if dict['hw'][i]['sub_run_id'] == subrun:
            return i	

# Read the Run parameters from the JSON Script
def getRunParameters(run):
    file = './SMELLIE_very_short.json'
    dict = ReadJSON(file)
    
    irun = returnRun(dict, run)
    run_id = dict['run_list'][irun]['run_id']
    laser_id = dict['run_list'][irun]['laser_selected'][0]
    number_of_pulses = dict['run_list'][irun]['nb_pulses']
    pulse_frequency = dict['run_list'][irun]['smellie_pulse_frequency']
    return run_id,laser_id,number_of_pulses,pulse_frequency

		
# Reads the subrun parameters from the JSON file
def getSubRunParameters(subrun):
    file = './SMELLIE_very_short.json'
    dict = ReadJSON(file)    
    isubrun = returnSubRun(dict, subrun)
    subrun_id = dict['hw'][isubrun]['sub_run_id']
    fsInputChannel = dict['hw'][isubrun]['fibre_switch_channel']
    return subrun_id,fsInputChannel
	
def StartSubRun(run, subrun):
    file = './SMELLIE_very_short.json'
    dict = ReadJSON(file) 
    irun = returnRun(dict, run)
    laser_id = dict['run_list'][irun]['laser_selected'][0]
    number_of_pulses = dict['run_list'][irun]['nb_pulses']
    pulse_frequency = dict['run_list'][irun]['smellie_pulse_frequency']
	
    isubrun = returnSubRun(dict, subrun)
    fsInputChannel = dict['hw'][isubrun]['fibre_switch_channel']
    print fsInputChannel
    
StartSubRun(1,1)
print getRunParameters(2)
print getSubRunParameters(3)
