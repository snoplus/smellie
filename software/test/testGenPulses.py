import niADC as ni
var = 1
while var==1 :
    digi_trig = ni.GenerateDigitalTrigger(int(100), int(1000))
    digi_trig.start()
    digi_trig.stop()
        
