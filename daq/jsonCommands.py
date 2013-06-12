# Commands to Read in Parameters from the SMELLIE JSON file
# Written by Christopher Jones (11/03/2013)
# Additional changes by Krish Majumdar (15/03/2013)
# Updates to test and check the JSON files (4/06/2013) 

# This Python script is highly reliant upon the JSON file being in the correct format!! 
# Any value error/deliminter compiler errors for this script will most likely be the 
# JSON file you are trying to read is in an incorrect format 

import simplejson as json

# Read in the JSON parameter-file
def ReadJSON(filename):
    dataDict = json.load(open(filename))
    return dataDict


# Return the Run number for future reference
def returnRun(dict, run,run_name):
    for i in range(0, len(dict[run_name]), 1):
        idValue = run_name[:-5]
        idValue = idValue + "_id"
        if dict[run_name][i][idValue] == run:
            return i


# Return the SubRun number for future reference
def returnSubRun(dict, subrun,run_name,run_tracker):
    for i in range(0, len(dict[run_name]), 1):
        # "sub_run_id" is an example of run_name
        # "hw" is an example of the run_name 
        if dict[run_name][i][run_tracker] == subrun:
            return i	

# Read the Run parameters from the JSON Script
def getRunParameters(run):
    file = './SMELLIE_very_short.json'
    dict = ReadJSON(file)
    
    irun = returnRun(dict, run,'run_list')
    run_id = dict['run_list'][irun]['run_id']
    laser_id = dict['run_list'][irun]['laser_selected'][0]
    number_of_pulses = dict['run_list'][irun]['nb_pulses']
    pulse_frequency = dict['run_list'][irun]['smellie_pulse_frequency']
    return run_id,laser_id,number_of_pulses,pulse_frequency

		
# Reads the subrun parameters from the JSON file
def getSubRunParameters(subrun):
    file = './SMELLIE_very_short.json'
    dict = ReadJSON(file)    
    isubrun = returnSubRun(dict, subrun,"hw","sub_run_id")
    subrun_id = dict['hw'][isubrun]['sub_run_id']
    fsInputChannel = dict['hw'][isubrun]['fibre_switch_channel']
    return subrun_id,fsInputChannel
	
def getSubRunParameters(run, subrun):
    file = './SMELLIE_very_short.json'
    dict = ReadJSON(file) 
    irun = returnRun(dict, run,'run_list')
    nameList = ['laser_id','author','time_stamp','make_smellie_calibration_table','smellie_calibration_table_reference','trigger_mode','laser_selected','smellie_deriven','number_of_pulses','pulse_frequency']
    valueList = [' ',' ',' ',' ',' ',' ',' ',' ',' ',' ']    
    valueList[0] = dict['run_list'][irun]['laser_selected'][0]
    valueList[1] = dict['run_list'][irun]['author']
    valueList[2] = dict['run_list'][irun]['time_stamp']
    valueList[3] = dict['run_list'][irun]['make_smellie_calibration_table']
    valueList[4] = dict['run_list'][irun]['smellie_calibration_table_reference']
    valueList[5] = dict['run_list'][irun]['trigger_mode']
    valueList[6] = dict['run_list'][irun]['laser_selected']
    valueList[7] = dict['run_list'][irun]['smellie_driven']
    valueList[8] = dict['run_list'][irun]['nb_pulses']
    valueList[9] = dict['run_list'][irun]['smellie_pulse_frequency']
	
    isubrun = returnSubRun(dict, subrun,"hw","sub_run_id")
    subrun_id = dict['hw'][isubrun]['sub_run_id']
    fsInputChannel = dict['hw'][isubrun]['fibre_switch_channel']
    print "Configuration parameters are:"
    for i in range(0,10):
        print str(nameList[i]) + "\t" +  str(valueList[i])
    #print "\nSubRun Parameters are:"
    #print subrun_id,fsInputChannel

def getConfigurationParameters(configId):
     filename = './smellie_config.json'
     dict = ReadJSON(filename)
     iconfig = returnRun(dict,configId,'config_list')
     print iconfig
     nameList = ['config_id','config_rev','time_stamp','tcpip_communication_timeouts','safe_laser_switch_output','safe_fibre_switch_output','fibre_switch_serial_port','fibre_switch_baud_rate','fibre_switch_from_laser_head_map','fibre_switch_to_detector_fibre_map','laser_switch_wait','laser_head_to_fibre_splitter_map','laser_switch_to_laser_head_map','sepia_laser_driver_module_slotID','sepia_laser_driver_primary_id','snodrop_ip_address','orca_ip_address','orca_server_port','snodrop_client_port','tcpip_communication_max_string_length','snodrop_max_number_listening_connections','detector_database_server_ip_address','NI_device_name','self_test_number_of_pulses','self_test_trigger_frequency','self_test_sampling_frequency','self_test_number_of_samples_per_pulse','self_test_NI_trigger_output_pin','self_test_NI_analogue_input_pin']
     valueList = [' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ']
     for i in range(0,29): 
         if (i == 3): #tcpip_communication_timeouts 
             nameList[i] = dict['tcpip_communication_timeouts'][configId-1]['timeout_name']
             valueList[i] = dict['tcpip_communication_timeouts'][configId-1]['timeout_value']
             print valueList[i]
         elif(i == 8):
             nameList[i] = dict['fibre_switch_from_laser_head_map'][configId-1]['input_channel']
             valueList[i] = dict['fibre_switch_from_laser_head_map'][configId-1]['laser_head_wavelength']
             print valueList[i]
         elif(i ==9):
             nameList[i] = dict['fibre_switch_to_detector_fibre_map'][configId-1]['output_channel']
             valueList[i] = dict['fibre_switch_to_detector_fibre_map'][configId-1]['detector_fibre']
             print valueList[i]
         elif(i ==11):
             nameList[i] = dict['laser_head_to_fibre_splitter_map'][configId-1]['fibre_splitter_id']
             valueList[i] = dict['laser_head_to_fibre_splitter_map'][configId-1]['fibre_spliter_type']
             print valueList[i]
         elif(i== 12):
             nameList[i] = dict['laser_switch_to_laser_head_map'][configId-1]['output_channel']
             valueList[i] = dict['laser_switch_to_laser_head_map'][configId-1]['laser_head_wavelength']
             print valueList[i]
         else:
             valueList[i] = dict['config_list'][iconfig][nameList[i]]
             print nameList[i],valueList[i]
         
     
     for i in range(0,5):
         print dict['laser_switch_to_laser_head_map'][0]['output_channel'][i],dict['laser_switch_to_laser_head_map'][0]['laser_head_wavelength'][i] # this will print the first configuration in the database 
         
        
getSubRunParameters(2,1)
getConfigurationParameters(1)
