# Commands to Control the SMELLIE interlock for the laser system
import serial,time

global interlockSerialPortNumber,interlockserialPortBR
interlockserialPortBR = 57600

def keepAlivePulse():
    serialPortBaudRate = 57600
    interlockSerialPortNumber = 3 #corresponds to COM4
    keepAlive = 1
    interlockSerial = serial.Serial(interlockSerialPortNumber,interlockserialPortBR)
    print interlockSerial 
    try:
        while (keepAlive == 1):
            interlockSerial.write("01010101") 
    except KeyboardInterrupt:
        print "interlockSMELLIE::Keyboard Interrupt has locked the Laser. Please Restart"
        pass
        
    interlockSerial.close()
    
keepAlivePulse()    
    

