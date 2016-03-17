#Gain Control Commands
#
#Set gain voltage in first argument of GenerateGainVoltage function
#Gain voltage must be set between 0.1 and 1.0 volts to avoid damage to MPU
#Note that voltages above 0.55 must only be used with extremely low intensity laser input to avoid damaging the PMT

import niADC as ni

gain_trig = ni.GenerateGainVoltage(.377, int(100), int(3000))
gain_trig.start()
gain_trig.stop()
gain_trig.clear()

while True:
    vNew = raw_input('Please enter a new gain voltage between 0.02 - 1.0V, or zero to terminate: ')
    vNew = float(vNew)
    
    if(vNew < 0.02 or vNew > 1.0):
        gain_stop = ni.StopGainVoltage()
        gain_stop.start()
        gain_stop.stop()
        gain_stop.clear()
        print "Gain voltage output terminated."
        break
        
    else:
        gain_trig = ni.GenerateGainVoltage(vNew, int(100), int(3000))
        gain_trig.start()
        gain_trig.stop()
        gain_trig.clear()
        print "Gain voltage output set to %f volts." %vNew

    
    



