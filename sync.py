import time,ctypes
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
data = MyList()
id_a = create_callbackdata_id(data)

def EveryNCallback_py(taskHandle, everyNsamplesEventType, nSamples, callbackData_ptr):
    callbackdata = get_callbackdata_from_id(callbackData_ptr)
    read = int32()
    data = zeros(1000)
    DAQmxWriteAnalogF64(taskHandle,1000,10.0,DAQmx_Val_GroupByChannel,data,1000,byref(read),None)
    callbackdata.extend(data.tolist())
    print "Acquired total %d samples"%len(data)
    

## MAIN FUNCTION        

AItaskHandle = TaskHandle(0)
AOtaskHandle = TaskHandle(0)
terminalname = ctypes.c_char_p("ai/StartTrigger")
trigName = ctypes.c_char_p("")


DAQmxCreateTask("",byref(AItaskHandle))

DAQmxCreateAIVoltageChan(AItaskHandle,"Dev1/ai0","",DAQmx_Val_Cfg_Default,-10.0,10.0,DAQmx_Val_Volts,None)
DAQmxCfgSampClkTiming(AItaskHandle,"",10000.0,DAQmx_Val_Rising,DAQmx_Val_ContSamps,1000)
#terminalname,trigName = GetTerminalNameWithDevPrefix(AItaskHandle,terminalname, trigName)
#print terminalname,trigName

DAQmxCreateTask("",byref(AOtaskHandle))
DAQmxCreateAOVoltageChan(AOtaskHandle,"Dev1/ao0","",-10.0,10.0,DAQmx_Val_Volts,None)
DAQmxCfgSampClkTiming(AOtaskHandle,"",5000.0,DAQmx_Val_Rising,DAQmx_Val_ContSamps,1000)
## maybe keep this in 
#DAQmxCfgDigEdgeStartTrig(AOtaskHandle,trigName,DAQmx_Val_Rising)
EveryNCallback = DAQmxEveryNSamplesEventCallbackPtr(EveryNCallback_py)
DAQmxRegisterEveryNSamplesEvent(AItaskHandle,DAQmx_Val_Acquired_Into_Buffer,1000,0,EveryNCallback,None)
DAQmxRegisterDoneEvent(AItaskHandle,0,DAQmxDoneEventCallbackPtr(),None)

number_of_measurements = 1000
AOdata = numpy.zeros((number_of_measurements,), dtype=numpy.float64)
for i in range(0,100):
    AOdata[i] = 1  

#print AOdata

DAQmxWriteAnalogF64(AOtaskHandle, number_of_measurements, False, 10.0, DAQmx_Val_GroupByChannel, AOdata, None, None)

DAQmxStartTask(AOtaskHandle)
DAQmxStartTask(AItaskHandle)

	#DAQmxErrChk (DAQmxCreateTask("",&AOtaskHandle));
	#DAQmxErrChk (DAQmxCreateAOVoltageChan(AOtaskHandle,"Dev1/ao0","",-10.0,10.0,DAQmx_Val_Volts,NULL));
	#DAQmxErrChk (DAQmxCfgSampClkTiming(AOtaskHandle,"",5000.0,DAQmx_Val_Rising,DAQmx_Val_ContSamps,1000));
	#DAQmxErrChk (DAQmxCfgDigEdgeStartTrig(AOtaskHandle,trigName,DAQmx_Val_Rising));

	#DAQmxErrChk (DAQmxRegisterEveryNSamplesEvent(AItaskHandle,DAQmx_Val_Acquired_Into_Buffer,1000,0,EveryNCallback,NULL));
	#DAQmxErrChk (DAQmxRegisterDoneEvent(AItaskHandle,0,DoneCallback,NULL));
#
	#GenSineWave(1000,1.0,1.0/1000,&phase,AOdata);

	#DAQmxErrChk (DAQmxWriteAnalogF64(AOtaskHandle, 1000, FALSE, 10.0, DAQmx_Val_GroupByChannel, AOdata, NULL, NULL));

	
#static int32 GetTerminalNameWithDevPrefix(TaskHandle taskHandle, const char terminalName[], char triggerName[])
#{
#	int32	error=0;#
	#char	device[256];
	#int32	productCategory;
	#uInt32	numDevices,i=1;

	#DAQmxErrChk (DAQmxGetTaskNumDevices(taskHandle,&numDevices));
	#while( i<=numDevices ) {
#		DAQmxErrChk (DAQmxGetNthTaskDevice(taskHandle,i++,device,256));
#		DAQmxErrChk (DAQmxGetDevProductCategory(device,&productCategory));
#		if( productCategory!=DAQmx_Val_CSeriesModule && productCategory!=DAQmx_Val_SCXIModule ) {
#			*triggerName++ = '/';
#			strcat(strcat(strcpy(triggerName,device),"/"),terminalName);
#			break;
#		}
	#}
