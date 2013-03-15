# Commands to Read in Parameters from the SMELLIE JSON file
# Written by Christopher Jones (11/03/2013)
# Additional changes by Krish Majumdar (15/03/2013)

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



##### THE FUNCTIONS BELOW NEEDS MAJOR WORK ... RELATED TO WORK ON JSON PARAMETERS #####

# Read the Run parameters from the JSON Script
def get_run_parameters(run):
	file = './SMELLIE_very_short.json'
	dict = ReadJSON(file)
    
	irun = returnRun(dict, run)
	run_id = dict['run_list'][irun]['run_id']
	laser_id = dict['run_list'][irun]['laser_selected'][0]
	number_of_pulses = dict['run_list'][irun]['nb_pulses']
	pulse_frequency = dict['run_list'][irun]['smellie_pulse_frequency']
	return run_id,laser_id,number_of_pulses,pulse_frequency

		
# Read the Run parameters from the JSON Script
def get_subrun_parameters(subrun):
	file = './SMELLIE_very_short.json'
	dict = ReadJSON(file)
    
	isubrun = returnSubRun(dict, subrun)
	subrun_id = dict['hw'][isubrun]['sub_run_id']
	fsInputChannel = dict['hw'][isubrun]['fs_input_channel']
	fsOutputChannel = dict['hw'][isubrun]['fs_output_channel']
	intensity = dict['hw'][isubrun]['intensity']
	return subrun_id,fsInputChannel,fsOutputChannel,intensity
	
	
def StartSubrun(run, subrun):
    file = './SMELLIE_very_short.json'
    dict = ReadJSON(file)
    
	irun = returnRun(dict, run)
	laser_id = dict['run_list'][irun]['laser_selected'][0]
    number_of_pulses = dict['run_list'][irun]['nb_pulses']
	pulse_frequency = dict['run_list'][irun]['smellie_pulse_frequency']
	
    isubrun = returnSubrun(dict, subrun)
	fsInputChannel = dict['hw'][isubrun]['fs_input_channel']
	fsOutputChannel = dict['hw'][isubrun]['fs_output_channel']
	intensity = dict['hw'][isubrun]['intensity']
	
    # print stuff here

StartSubRun(1)
