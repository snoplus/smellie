# Commands to Control the NKT 'SuperK Compact' Supercontinuum laser
# written by Jeff Lidgard (12/Jan/2016)
# in style of niADC.py by Christopher Jones 


import time, ctypes,sys
import numpy as np
import pprint as p
from DAQmxFunctions import *
from DAQmxConstants import *
from DAQmxTypes import *
from DAQmxConfig import *
from DAQmxCallBack import *

global devName, triggerOutputPin, analogueInputPin, analogueOutputPin
devName = str("Dev1")
triggerOutputPin = str("/Ctr0")
analogueInputPin = str("/ai0:1")
analogueOutputPin = str("/ao0:1")



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

def setAnalogueOutput(newAnaloguePin):
        global analogueOutputPin
        analogueOutputPin = str(newAnaloguePin)

def getAnalogueInput():
        return analogueInputPin

def getAnalogueOutput():
        return analogueOutputPin


class GenerateDigitalTrigger():

	def __init__(self, frequency, number_of_pulses):
		taskHandle = TaskHandle(0)
		DAQmxCreateTask("",byref(taskHandle))
		high_time = 0.0000005	
		low_time =  1 / (1.0 * frequency) - high_time
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


class GenerateAnalogueCont():


        def __init__(self, vMin, vMax, number_of_samples, sampling_frequency):  
                taskHandle = TaskHandle(0)
                DAQmxCreateTask("",byref(taskHandle))
                self.number_of_samples = number_of_samples
		self.sampling_frequency = sampling_frequency
                aoDetails = str(devName + analogueOutputPin)#not in use below for testing purposes. Forced with "Dev1/ao1" argument.
                vAmp = ((vMax - vMin)/2)
                if(vMax > 1.0 or vMin < 0.5):
                        print "Aborted. Voltage must be set between 0.5V and 1.0V to avoid damage to MPU"
                        exit(0)           
                DAQmxCreateAOVoltageChan(taskHandle,"Dev1/ao1","",vMin,vMax,DAQmx_Val_Volts,None) 
                DAQmxCfgSampClkTiming(taskHandle,"",sampling_frequency,DAQmx_Val_Rising,DAQmx_Val_ContSamps,self.number_of_samples)
                
                self.taskHandle = taskHandle

                #Creating and shaping the data buffer:
                data = np.zeros(3000, dtype = numpy.float64)
                data_length = data.shape[0]
                for i in range(0, data_length):
                        data[i]= vAmp*np.sin(i*2.0*np.pi/100.0)+(vAmp+vMin)           
                DAQmxWriteAnalogF64(self.taskHandle,3000,0,10.0,DAQmx_Val_GroupByChannel,data,None,None)



        def start(self): 
		DAQmxStartTask(self.taskHandle)


	def stop(self):
		DAQmxWaitUntilTaskDone(self.taskHandle,10.0)
		DAQmxStopTask(self.taskHandle)

	def clear(self):
		DAQmxClearTask(self.taskHandle)


class GenerateGainVoltage():


        def __init__(self, vGain, number_of_samples, sampling_frequency):  
                taskHandle = TaskHandle(0)
                DAQmxCreateTask("",byref(taskHandle))
                self.number_of_samples = number_of_samples
		self.sampling_frequency = sampling_frequency
		self.taskHandle = taskHandle
                aoDetails = str(devName + analogueOutputPin)#not in use below for testing purposes. Forced with "Dev1/ao1" argument.
                vMin = 0.0                      
                vMax = 1.0
                vRes = 0.0044 # Residual voltage on MPU 
                if(vGain > 1.0 or vGain < 0.0124): 
                        print "Aborted. Gain voltage must be set between 0.1V and 1.0V to avoid damage to MPU"
                        exit(0)           
                DAQmxCreateAOVoltageChan(taskHandle,"Dev1/ao0","",vMin,vMax,DAQmx_Val_Volts,None) 
                DAQmxCfgSampClkTiming(taskHandle,"",sampling_frequency,DAQmx_Val_Rising,DAQmx_Val_ContSamps,self.number_of_samples)

                #Creating and shaping the data buffer:
                data = np.zeros(3000, dtype = numpy.float64)
                data_length = data.shape[0]
                for i in range(0, data_length):
                        data[i]= vGain - vRes 
                DAQmxWriteAnalogF64(self.taskHandle,3000,0,10.0,DAQmx_Val_GroupByChannel,data,None,None)


        def start(self): 
		DAQmxStartTask(self.taskHandle)

	def stop(self):		
		DAQmxStopTask(self.taskHandle)

	def clear(self):
		data = np.zeros(3000, dtype = numpy.float64)
                data_length = data.shape[0]
                for i in range(0, data_length):
                        data[i]= 0.0
                DAQmxWriteAnalogF64(self.taskHandle,3000,0,10.0,DAQmx_Val_GroupByChannel,data,None,None)

                DAQmxClearTask(self.taskHandle)

class StopGainVoltage():


        def __init__(self):  
                taskHandle = TaskHandle(0)
                DAQmxCreateTask("",byref(taskHandle))

                aoDetails = str(devName + analogueOutputPin)#not in use below for testing purposes. Forced with "Dev1/ao0" argument.
                self.taskHandle = taskHandle

                #forcing the NI box to output a null DC voltage
                number_of_samples = 0
		sampling_frequency = 1000
                vGain = 0.0
                vMin = 0.0                      
                vMax = 0.001    

                DAQmxCreateAOVoltageChan(taskHandle,"Dev1/ao0","",vMin,vMax,DAQmx_Val_Volts,None) 
                DAQmxCfgSampClkTiming(taskHandle,"",sampling_frequency,DAQmx_Val_Rising,DAQmx_Val_ContSamps,number_of_samples)

                #Creating and shaping the data buffer:
                data = np.zeros(3000, dtype = numpy.float64)
                data_length = data.shape[0]
                for i in range(0, data_length):
                        data[i]= vGain
                DAQmxWriteAnalogF64(self.taskHandle,3000,0,10.0,DAQmx_Val_GroupByChannel,data,None,None)       
                
        def start(self): 
		DAQmxStartTask(self.taskHandle)

	def stop(self):
		DAQmxStopTask(self.taskHandle)
		DAQmxTaskControl(self.taskHandle,DAQmx_Val_Task_Abort)

	def clear(self):
                DAQmxClearTask(self.taskHandle)

                          



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
