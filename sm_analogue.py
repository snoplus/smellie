import time,ctypes
from DAQmxFunctions import *
from DAQmxConstants import *
from DAQmxTypes import *
from DAQmxConfig import *
from DAQmxCallBack import *

class GenerateDigitalTrigger():
    def __init__(self,frequency,number_of_pulses):
    
        taskHandle = TaskHandle(0)

        DAQmxCreateTask("",byref(taskHandle))
        low_time = 1/(2.0*frequency)
        high_time = 1/(2.0*frequency)
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

class AquireAnalogue():
    def __init__(self, reset=False):
        taskHandle = TaskHandle(0)

        DAQmxCreateTask("",byref(taskHandle))
        DAQmxCreateAIVoltageChan(taskHandle,"Dev1/ai1","",DAQmx_Val_Cfg_Default,-10.0,10.0,DAQmx_Val_Volts,None)
        DAQmxCfgSampClkTiming(taskHandle,"",10000.0,DAQmx_Val_Rising,DAQmx_Val_FiniteSamps,1000)

        self.taskHandle = taskHandle
    def start(self,number_of_measurements):
        data = numpy.zeros((number_of_measurements,), dtype=numpy.float64)
        read = int32()
        DAQmxStartTask(self.taskHandle)
        DAQmxReadAnalogF64(self.taskHandle,number_of_measurements,10.0,DAQmx_Val_GroupByChannel,data,number_of_measurements,byref(read),None)
        return data 
    def stop(self):
        DAQmxWaitUntilTaskDone(self.taskHandle,-1)
        DAQmxStopTask(self.taskHandle)
    def clear(self):
        DAQmxClearTask(self.taskHandle)
        

#Example Usage
#if __name__=="__main__":

    #DAQmxEveryNSamplesEventCallbackPtr = CFUNCTYPE(int32, TaskHandle, int32, uInt32, c_void_p)
    #DAQmxDoneEventCallbackPtr = CFUNCTYPE(int32, TaskHandle, int32, c_void_p)
    #DAQmxSignalEventCallbackPtr = CFUNCTYPE(int32, TaskHandle, int32, c_void_p) 
#    digitrig_on = GenerateDigitalTrigger(10000,100000)
#    digitrig_on.start()
#    digitrig_on.stop()

  
   

