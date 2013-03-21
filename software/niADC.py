# Commands to Control the National Instruments ADC
# Written by Christopher Jones (05/03/2013)
# Additional changes by Krish Majumdar (15/03/2013)

import time, ctypes
import numpy as np 
from DAQmxFunctions import *
from DAQmxConstants import *
from DAQmxTypes import *
from DAQmxConfig import *
from DAQmxCallBack import *


class GenerateDigitalTrigger():

    def __init__(self, frequency, number_of_pulses):
        taskHandle = TaskHandle(0)
        DAQmxCreateTask("",byref(taskHandle))
        
		low_time = 1 / (2.0 * frequency)
        high_time = 1 / (2.0 * frequency)
        # yes, the low_time and high_time are meant to be the same!

        DAQmxCreateCOPulseChanTime(taskHandle,"Dev1/ctr0","",DAQmx_Val_Seconds,DAQmx_Val_Low,0.0,low_time,high_time)
        DAQmxCfgImplicitTiming(taskHandle,DAQmx_Val_FiniteSamps,number_of_pulses)    

        self.taskHandle = taskHandle
    
	def start(self):
        DAQmxStartTask(self.taskHandle)

    def stop(self):
        DAQmxWaitUntilTaskDone(self.taskHandle,-1)
        DAQmxStopTask(self.taskHandle)

    def clear(self):
        DAQmxClearTask(self.taskHandle)


class AcquireAnalogue():

    def __init__(self, number_of_measurements, reset = False):
        taskHandle = TaskHandle(0)
        DAQmxCreateTask("",byref(taskHandle))

        self.number_of_measurements = number_of_measurements
        sampling_frequency = 100000

        DAQmxCreateAIVoltageChan(taskHandle,"Dev1/ai0:1","",DAQmx_Val_Diff,0.0,5.0,DAQmx_Val_Volts,None)
        DAQmxCfgSampClkTiming(taskHandle,"",sampling_frequency,DAQmx_Val_Rising,DAQmx_Val_FiniteSamps,number_of_measurements)
		
        self.taskHandle = taskHandle
		
    def start(self):
        data = np.zeros((self.number_of_measurements), dtype = numpy.float64)
        read = int32()

        DAQmxStartTask(self.taskHandle)
        DAQmxReadAnalogF64(self.taskHandle,-1,1.0,DAQmx_Val_GroupByScanNumber,data,self.number_of_measurements,byref(read),None)
        
        return data

    def stop(self):
        DAQmxWaitUntilTaskDone(self.taskHandle,-1)
        DAQmxStopTask(self.taskHandle)

    def clear(self):
        DAQmxClearTask(self.taskHandle)
        

def writeDataFiles(data):

    f = open("niADC_data_ch1.txt", "w")
    data_length = data.shape[0]

    for i in range(0, data_length, 2):
        f.write(str(data[i]) + '\n')
        #print i, data[i]	
    
	f.close()	
   
    f = open("niADC_data_ch2.txt", "w")
    data_length = data.shape[0]
    
	for i in range(1, data_length, 2):
        f.write(str(data[i]) + '\n')
        #print i, data[i]	
    
	f.close()	
	

# Example Usage
if __name__ == "__main__":

    #DAQmxEveryNSamplesEventCallbackPtr = CFUNCTYPE(int32, TaskHandle, int32, uInt32, c_void_p)
    #DAQmxDoneEventCallbackPtr = CFUNCTYPE(int32, TaskHandle, int32, c_void_p)
    #DAQmxSignalEventCallbackPtr = CFUNCTYPE(int32, TaskHandle, int32, c_void_p) 

    digitrig_on = AcquireAnalogue(1000)
    
	data = digitrig_on.start()
    writeDataFiles(data)
    
	#print data 
    
	digitrig_on.stop()
    digitrig_on.clear()
