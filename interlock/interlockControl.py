#Test script for multithreading 
import subprocess, sys, time,os
print "hello"
#This will start a process in the background 
p = subprocess.Popen([sys.executable, 'C:/Users/LocalAdmin/Desktop/interlockSMELLIE.py'])
print "goodbye"
time.sleep(10)
print p.pid
# This will close the process in the background on windows. 
returnval = p.terminate()

