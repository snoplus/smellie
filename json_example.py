import json

def ReadRATDB(filename):
    dataDict = json.load(open(filename))
    return dataDict

def returnSubrun(dict, subrun):
	for i in range(0, len(dict['run_list']), 1):
		if dict['run_list'][i]['run_id'] == subrun:
			return i

def returnChannel(dict, laser):
	for i in range(0, len(dict['hw']), 1):
		if dict['hw'][i]['sub_run_id'] == laser:
			return i
def initialise(subrun):
    file = './SMELLIE_very_short.json'
    dict = ReadRATDB(file)
    
    isubrun = returnSubrun(dict, subrun)

    laser = dict['run_list'][isubrun]['laser_selected'][0]
    laserID = returnChannel(dict, laser)
    print laserID

    relay_switch_channel  = dict['hw'][laserID]['relay_switch_channel']
    set_intensity   = dict['hw'][laserID]['set_intensity']

    print relay_switch_channel,set_intensity
    


initialise(1)
