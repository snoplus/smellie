# Commands to Control the National Instruments ADC
# Written by Christopher Jones (05/03/2013)
# Additional changes by Krish Majumdar (15/03/2013)
# Corrections by Christopher Jones (21/03/2013)

import time, ctypes,sys
import numpy as np
import pprint as p
from DAQmxFunctions import *
from DAQmxConstants import *
from DAQmxTypes import *
from DAQmxConfig import *
from DAQmxCallBack import *

global devName, triggerOutputPin, analogueInputPin
devName = str("Dev1")
triggerOutputPin = str("/Ctr0")
analogueInputPin = str("/ai0:1")

def setDevName(newDevName):
        global devName
        devName = str(newDevName)

def getDevName():
        return devName

def setTriggerOutputPin(newTrigPin):
        global triggerOutputPin
        triggerOutputPin = str(newTrigPin)

def getTriggerOutputPin():
        return triggerOutputPin

def setAnalogueInput(newAnaloguePin):
        global analogueInputPin
        analogueInputPin = newAnaloguePin

def getAnalogueInput():
        return analogueInputPin


class GenerateDigitalTrigger():

	def __init__(self, frequency, number_of_pulses):
		taskHandle = TaskHandle(0)
		DAQmxCreateTask("",byref(taskHandle))
		high_time = 0.0000005	
		low_time = 1 / (1.0 * frequency) - high_time
		if(low_time < 0.0001):
                        low_time = 0.0001                
                pulseDetails = str(devName + triggerOutputPin)
		DAQmxCreateCOPulseChanTime(taskHandle,pulseDetails,"",DAQmx_Val_Seconds,DAQmx_Val_Low,0.0,low_time,high_time)
		DAQmxCfgImplicitTiming(taskHandle,DAQmx_Val_FiniteSamps,number_of_pulses)    

		self.taskHandle = taskHandle

	def start(self):
		DAQmxStartTask(self.taskHandle)

	def stop(self):
		DAQmxWaitUntilTaskDone(self.taskHandle,-1) #not sure if the second argument in here is correct ?
		DAQmxStopTask(self.taskHandle)

	def clear(self):
		DAQmxClearTask(self.taskHandle)

class GenerateDigitalTriggerDoublePulse():

	def __init__(self, frequency, number_of_pulses):
		taskHandle = TaskHandle(0)
		DAQmxCreateTask("",byref(taskHandle))
		high_time = 0.00000008 	##150ns high time
		low_time =  0.00000016
##		low_time = 1 / (1.0 * frequency) - high_time
		if(low_time < 0.00000005):
                        low_time = 0.00000005                
                pulseDetails = str(devName + triggerOutputPin)
		DAQmxCreateCOPulseChanTime(taskHandle,pulseDetails,"",DAQmx_Val_Seconds,DAQmx_Val_Low,0.0,low_time,high_time)
		DAQmxCfgImplicitTiming(taskHandle,DAQmx_Val_FiniteSamps,number_of_pulses)    

		self.taskHandle = taskHandle

	def start(self):
		DAQmxStartTask(self.taskHandle)

	def stop(self):
		DAQmxWaitUntilTaskDone(self.taskHandle,-1) #not sure if the second argument in here is correct ?
		DAQmxStopTask(self.taskHandle)

	def clear(self):
		DAQmxClearTask(self.taskHandle)

class AcquireAnalogue():

	def __init__(self, number_of_measurements, reset = False):
		taskHandle = TaskHandle(0)
		DAQmxCreateTask("",byref(taskHandle))
		self.number_of_measurements = number_of_measurements
		sampling_frequency = 100000
                aiDetails = str(devName + analogueInputPin)
		DAQmxCreateAIVoltageChan(taskHandle,aiDetails,"",DAQmx_Val_Diff,0.0,5.0,DAQmx_Val_Volts,None)
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
#if __name__ == "__main__":

	#DAQmxEveryNSamplesEventCallbackPtr = CFUNCTYPE(int32, TaskHandle, int32, uInt32, c_void_p)
	#DAQmxDoneEventCallbackPtr = CFUNCTYPE(int32, TaskHandle, int32, c_void_p)
	#DAQmxSignalEventCallbackPtr = CFUNCTYPE(int32, TaskHandle, int32, c_void_p) 

	#digitrig_on = AcquireAnalogue(1000)
	#data = digitrig_on.start()
	#writeDataFiles(data)

	#print data 

	#digitrig_on.stop()
	#digitrig_on.clear()
