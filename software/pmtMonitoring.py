import time,ctypes,sys,numpy,os
import safepysepia as sepia
from DAQmxFunctions import *
from DAQmxConstants import *
from DAQmxTypes import *
from DAQmxConfig import *
from DAQmxCallBack import *


def GetTerminalNameWithDevPrefix(taskHandle,terminalName,triggerName):
    terminalName = str(terminalName.value)
    triggerName = str(triggerName.value)
    
    error = int32()
    error.value = 0
    print error.value

    # fill the value into the brackets
    device = ctypes.c_char_p()    #not sure this may be better as a ctypes.c_char_p()
    device.value = ""
    productCategory = int32()
    numDevices = uInt32()
    i = uInt32(1)

    DAQmxGetTaskNumDevices(taskHandle,byref(numDevices))
    while( i.value <= numDevices.value ):
        print DAQmxGetNthTaskDevice(taskHandle,i,device,256)
        i.value = i.value + 1
        DAQmxGetDevProductCategory(device,byref(productCategory))
        if( productCategory != DAQmx_Val_CSeriesModule and productCategory != DAQmx_Val_SCXIModule ):
            triggerName = '/' + triggerName + '/' + terminalName
            break

    terminalName = ctypes.c_char_p(terminalName)
    triggerName = ctypes.c_char_p(triggerName)
    
    return terminalName,triggerName

# one cannot create a weakref to a list directly
# but the following works well
class MyList(list):
    pass

# list where the data are stored
#data = MyList()

def reformat(data):
	f = open("datach1new.txt","a")
	data_length = data.__len__()
	for i in range(0,data_length,2):
		if(i > 5000):
			f.write(str(data[i]) + '\n')
			#print i, data[i]	
	f.close()	
	f = open("datach2new.txt","a")
	data_length = data.__len__()
	for i in range(1,data_length,2):
		if(i > 5000):
			f.write(str(data[i]) + '\n')
		#print i, data[i]	
	f.close()

def prune_data(data,start_trim,threshold,offset,peak_length):
    f = open("data.txt","a") #start_trim = 5000
    data_length = data.__len__()
    #print "data_length " + str(data_length)
    for i in range(start_trim,data_length-2-peak_length-1-2*offset,2):
        #print i
        #print data[i+2]/data[i]
        if(abs(data[i+2]/data[i]) > 1/threshold):
            #print "here"
            data_start = i+2 + 2*offset
            for j in range(0,2*peak_length,2):
                f.write(str(j) + '\t' + str(data[int(data_start) + j]) + '\t' + str(data[int(data_start) + 1 + j]) + '\n')
    f.close()

def EveryNCallback_py(taskHandle, everyNsamplesEventType, nSamples , callbackData_ptr):
    #print "here"
    callbackdata = get_callbackdata_from_id(callbackData_ptr)
    number_of_channels = 2 # this is the number of channels to read simultaneously 
    read = int32()
    data = numpy.zeros((number_of_channels,), dtype=numpy.float64)
    DAQmxReadAnalogF64(taskHandle,-1,0.0,DAQmx_Val_GroupByScanNumber,data,number_of_channels,byref(read),None)
	#DAQmxReadAnalogF64(AItaskHandle,-1,1000,10.0,DAQmx_Val_GroupByChannel,data,1000,byref(read),None)	
    callbackdata.extend(data.tolist())
    #print callbackdata
    #print callbackdata
	#print "Acquired total %d samples"%len(data)
    #print "here"
    #return data
    return 0 

def DoneCallback_py(taskHandle, status, callbackData):
    print "Status",status.value
    return 0 # The function should return an integer
    

## MAIN FUNCTION        
DAQmxResetDevice('dev1')

AItaskHandle = TaskHandle()		#initialise the AItaskHandle object
AOtaskHandle = TaskHandle()		#initialise the AOtaskHandle object

DAQmxCreateTask("",byref(AItaskHandle))	#create analogue input task
DAQmxCreateAIVoltageChan(AItaskHandle,"Dev1/ai0:1","",DAQmx_Val_Cfg_Default,-10.0,10.0,DAQmx_Val_Volts,None) #read analogue signal from ai0 and ai1
#DAQmxCreateAIVoltageChan(AItaskHandle,"Dev1/ai1","",DAQmx_Val_Cfg_Default,-10.0,10.0,DAQmx_Val_Volts,None)

#DAQmxCfgSampClkTiming Function 
# if DAQmx_Val_ContSamps is set as the 5th argument then the 6th argument is the buffer size 
buffer_size = uInt64(1000000)
samplingRate = float64(100000.0) #this is the sampling rate in samples per second per channel 
DAQmxCfgSampClkTiming(AItaskHandle,"",samplingRate,DAQmx_Val_Rising,DAQmx_Val_ContSamps,buffer_size)

DAQmxCreateTask("",byref(AOtaskHandle))
frequency = 10000.0
low_time = 1/(2.0*frequency)
high_time = 1/(2.0*frequency)
DAQmxCreateCOPulseChanTime(AOtaskHandle,"Dev1/ctr0","",DAQmx_Val_Seconds,DAQmx_Val_Low,0.0,low_time,high_time)
DAQmxCfgImplicitTiming(AOtaskHandle,DAQmx_Val_ContSamps,buffer_size)    

data = MyList()
id_a = create_callbackdata_id(data)
EveryNCallback = DAQmxEveryNSamplesEventCallbackPtr(EveryNCallback_py)

DAQmxRegisterEveryNSamplesEvent(AItaskHandle,DAQmx_Val_Acquired_Into_Buffer,100,0,EveryNCallback,id_a)
DoneCallback = DAQmxDoneEventCallbackPtr(DoneCallback_py)
DAQmxRegisterDoneEvent(AItaskHandle,0,DoneCallback,None)

os.system("del data.txt")
os.system("del datach1new.txt")
os.system("del datach2new.txt")

total_data = []
#total_data = numpy.zeros((1,), dtype=numpy.float64)
iDevIdx,iModuleType,iSlotID = sepia.initialise()
for i in range (0,12):
    intensity = int(100 - i*3)
    sepia.set_laser_intensity(intensity,iDevIdx)
    
    DAQmxStartTask(AItaskHandle)
    DAQmxStartTask(AOtaskHandle)
    time.sleep(4.0)
    #raw_input('Acquiring samples continuously. Press Enter to interrupt\n')
    DAQmxStopTask(AItaskHandle)
    DAQmxStopTask(AOtaskHandle)
    
    temp_data = get_callbackdata_from_id(id_a)
    #total_data = total_data.append(temp_data)
    offset = 1
    peak_length = 2
    threshold = 0.3
    time.sleep(3.0)
    
   
    #DAQmxClearTask(AItaskHandle)
    #DAQmxClearTask(AOtaskHandle)
    #time.sleep(12.0)

sepia.close(iDevIdx)
prune_data(temp_data,5000,threshold,offset,peak_length)
reformat(temp_data)

DAQmxClearTask(AItaskHandle)
DAQmxClearTask(AOtaskHandle)
