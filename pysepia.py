
# THIS SCRIPT SHOULD NOT BE ALTERED
import ctypes, sys, os, time, heapq


# Check the dll path is correct
dll_path = "C:\Users\LocalAdmin\Desktop\Pysepia\Sepia2_Lib.dll"

if (os.path.exists(dll_path) == True):
	print '\n PYSEPIA: The .dll path is correct \n'
else:
	sys.exit('\n PYSEPIA: The .dll path is incorrect - please give the correct path for the Sepia2_Lib.dll file \n')
print dll_path
#sepiadll = ctypes.WinDLL(dll_path)
sepiadll = ctypes.OleDLL(dll_path)


# Open the .dll library and returns the library's version number
def SEPIA2_LIB_GetVersion(): 	
	cLibVersion = " "
	SEPIA2_LIB_GetVersion_Proto = ctypes.WINFUNCTYPE(ctypes.c_int,ctypes.c_char_p)
	SEPIA2_LIB_GetVersion_Params = (1,"p1",0),
	SEPIA2_LIB_GetVersion_API = SEPIA2_LIB_GetVersion_Proto(("SEPIA2_LIB_GetVersion",sepiadll),SEPIA2_LIB_GetVersion_Params)
	p1 = ctypes.c_char_p(cLibVersion)
	SEPIA2_LIB_GetVersion_API(p1)
	return p1.value


def SEPIA2_LIB_DecodeError():
	iErrCode = 0
	cErrorString = " "
	SEPIA2_LIB_DecodeError_Proto = ctypes.WINFUNCTYPE(ctypes.c_int,ctypes.c_int,ctypes.c_char_p)
	SEPIA2_LIB_DecodeError_Params = (1,"p1",0),(1,"p2",0),
	SEPIA2_LIB_DecodeError_API = SEPIA2_LIB_DecodeError_Proto(("SEPIA2_LIB_DecodeError",sepiadll),SEPIA2_LIB_DecodeError_Params)	
	p1 = ctypes.c_int(iErrCode)
	p2 = ctypes.c_char_p(cErrorString)
	SEPIA2_LIB_DecodeError_API(p1,p2)


# Open the USB device and returns the device ID.
# THIS FUNCTION IS REQUIRED BEFORE USING ANY OTHER FUNCTIONS 
def SEPIA2_USB_OpenDevice():
	iDevIdx = 0
	cSerialNumber = " "
	SEPIA2_USB_OpenDevice_Proto = ctypes.WINFUNCTYPE(ctypes.c_int,ctypes.c_int,ctypes.c_char_p)
	SEPIA2_USB_OpenDevice_Params = (1,"p1",0),(1,"p2",0),
	SEPIA2_USB_OpenDevice_API = SEPIA2_USB_OpenDevice_Proto(("SEPIA2_USB_OpenDevice",sepiadll),SEPIA2_USB_OpenDevice_Params)
	p1 = ctypes.c_int(iDevIdx)
	p2 = ctypes.c_char_p(cSerialNumber)
	iRetVal = SEPIA2_USB_OpenDevice_API(p1,p2)
	
	if (iRetVal == 0):
		print 'PYSEPIA: Connected to USB Device with serial number: ' + p2.value
	else:
		print 'PYSEPIA: Not Connected to USB Device'
        return p1.value
        

# Close the USB device and prints whether or not the USB has been successfully disconnected
# THIS FUNCTION IS REQUIRED AT THE END OF EACH PROGRAM        
def SEPIA2_USB_CloseDevice(iDevIdx):
	SEPIA2_USB_CloseDevice_Proto = ctypes.WINFUNCTYPE(ctypes.c_int,ctypes.c_int)
	SEPIA2_USB_CloseDevice_Params = (1,"p1",0),
	SEPIA2_USB_CloseDevice_API = SEPIA2_USB_CloseDevice_Proto(("SEPIA2_USB_CloseDevice",sepiadll),SEPIA2_USB_CloseDevice_Params)
	p1 = ctypes.c_int(iDevIdx)
	iRetVal = 27
	iRetVal = SEPIA2_USB_CloseDevice_API(p1)

	if (iRetVal == 0):
		print 'PYSEPIA: Disconnected from USB Device'	
	else:
		print 'PYSEPIA: Failed to Disconnect from USB Device'
	return iRetVal 


def SEPIA2_USB_GetStrDescriptor(iDevIdx):
	cDescriptor = " "
	SEPIA2_USB_GetStrDescriptor_Proto = ctypes.WINFUNCTYPE(ctypes.c_int,ctypes.c_int,ctypes.c_char_p)
	SEPIA2_USB_GetStrDescriptor_Params = (1,"p1",0),(1,"p2",0),
	SEPIA2_USB_GetStrDescriptor_API = SEPIA2_USB_GetStrDescriptor_Proto(("SEPIA2_USB_GetStrDescriptor",sepiadll),SEPIA2_USB_GetStrDescriptor_Params)
	p1 = ctypes.c_int(iDevIdx)
	p2 = ctypes.c_char_p(cDescriptor)
	SEPIA2_USB_GetStrDescriptor_API(p1,p2)
	return p2.value


# Open the Module Map and initialise all libraries
# THIS FUNCTION IS REQUIRED, ALONG WITH SEPIA2_USB_OpenDevice, BEFORE ANY OTHER FUNCTIONS ARE CALLED
def SEPIA2_FWR_GetModuleMap(iDevIdx):
	iPerformRestart = 0		# Boolean value: 0 = no restart, 1 = restart
	pwModuleCount = 0
	INTP = ctypes.POINTER(ctypes.c_int)  
	SEPIA2_FWR_GetModuleMap_Proto = ctypes.WINFUNCTYPE(ctypes.c_int,ctypes.c_int,ctypes.c_int,INTP)
	SEPIA2_FWR_GetModuleMap_Params = (1,"p1",0),(1,"p2",0),(1,"p3",0),
	SEPIA2_FWR_GetModuleMap_API = SEPIA2_FWR_GetModuleMap_Proto(("SEPIA2_FWR_GetModuleMap",sepiadll),SEPIA2_FWR_GetModuleMap_Params)
	p1 = ctypes.c_int(iDevIdx)
	p2 = ctypes.c_int(iPerformRestart)
	num = ctypes.c_int(pwModuleCount)	
	addr = ctypes.addressof(num)
	p3 = ctypes.cast(addr, INTP)  	
	iRetVal = SEPIA2_FWR_GetModuleMap_API(p1,p2,p3)

	#print p3.contents.value
	return iRetVal


# Free the Module Map
# THIS FUNCTION IS REQUIRED, ALONG WITH SEPIA2_USB_CloseDevice, AT THE END OF EACH PROGRAM  
def SEPIA2_FWR_FreeModuleMap(iDevIdx):
	SEPIA2_FWR_FreeModuleMap_Proto = ctypes.WINFUNCTYPE(ctypes.c_int,ctypes.c_int)
	SEPIA2_FWR_FreeModuleMap_Params = (1,"p1",0),
	SEPIA2_FWR_FreeModuleMap_API = SEPIA2_FWR_FreeModuleMap_Proto(("SEPIA2_FWR_FreeModuleMap",sepiadll),SEPIA2_FWR_FreeModuleMap_Params)
	p1 = ctypes.c_int(iDevIdx)
	iRetVal = SEPIA2_FWR_FreeModuleMap_API(p1)
	return iRetVal


def SEPIA2_FWR_DecodeErrPhaseName():
	iErrPhase = 0
	cErrorPhase = " "
	SEPIA2_FWR_DecodeErrPhaseName_Proto = ctypes.WINFUNCTYPE(ctypes.c_int,ctypes.c_int,ctypes.c_char_p)
	SEPIA2_FWR_DecodeErrPhaseName_Params = (1,"p1",0),(1,"p2",0),
	SEPIA2_FWR_DecodeErrPhaseName_API = SEPIA2_FWR_DecodeErrPhaseName_Proto(("SEPIA2_FWR_DecodeErrPhaseName",sepiadll),SEPIA2_FWR_DecodeErrPhaseName_Params)
	p1 = ctypes.c_int(iErrPhase)		# this is an integer that is returned by the firmware function: FWR_GetLastError
	p2 = ctypes.c_char_p(cErrorPhase)	# this is a string
	SEPIA2_FWR_DecodeErrPhaseName_API(p1,p2)
	return p2.value


def SEPIA2_FWR_GetVersion(iDevIdx):
	cFWVersion = " "
	SEPIA2_FWR_GetVersion_Proto = ctypes.WINFUNCTYPE(ctypes.c_int,ctypes.c_int,ctypes.c_char_p)
	SEPIA2_FWR_GetVersion_Params = (1,"p1",0),(1,"p2",0),
	SEPIA2_FWR_GetVersion_API = SEPIA2_FWR_GetVersion_Proto(("SEPIA2_FWR_GetVersion",sepiadll),SEPIA2_FWR_GetVersion_Params)
	p1 = ctypes.c_int(iDevIdx)
	p2 = ctypes.c_char_p(cFWVersion)
	SEPIA2_FWR_GetVersion_API(p1,p2)
	return p2.value


def SEPIA2_FWR_GetLastError(iDevIdx): 
	piErrCode = 0
	piPhase = 0
	piLocation = 0
	piSlot = 0
	cCondition = " "	
	INTP = ctypes.POINTER(ctypes.c_int)  
	SEPIA2_FWR_GetLastError_Proto = ctypes.WINFUNCTYPE(ctypes.c_int,ctypes.c_int,INTP,INTP,INTP,INTP,ctypes.c_char_p)
	SEPIA2_FWR_GetLastError_Params = (1,"p1",0),(1,"p2",0),(1,"p3",0),(1,"p4",0),(1,"p5",0),(1,"p6",0),
	SEPIA2_FWR_GetLastError_API = SEPIA2_FWR_GetLastError_Proto(("SEPIA2_FWR_GetLastError",sepiadll),SEPIA2_FWR_GetLastError_Params)
	
	p1 = ctypes.c_int(iDevIdx)
	
	num2 = ctypes.c_int(piErrCode)
	addr2 = ctypes.addressof(num2)
	p2 = ctypes.cast(addr2, INTP)  

	num3 = ctypes.c_int(piPhase)	
	addr3 = ctypes.addressof(num3)
	p3 = ctypes.cast(addr3, INTP)  

	num4 = ctypes.c_int(piLocation)	
	addr4 = ctypes.addressof(num4)
	p4 = ctypes.cast(addr4, INTP)  

	num5 = ctypes.c_int(piSlot)	
	addr5 = ctypes.addressof(num5)
	p5 = ctypes.cast(addr5, INTP)  

	p6 = ctypes.c_char_p(cCondition)  
		
	iRetVal = SEPIA2_FWR_GetLastError_API(p1,p2,p3,p4,p5,p6)

	print 'PYSEPIA: ' + p3


def SEPIA2_COM_DecodeModuleType(iModuleType): 
	cModuleType = " "
	
	SEPIA2_COM_DecodeModuleType_Proto = ctypes.WINFUNCTYPE(ctypes.c_int,ctypes.c_int,ctypes.c_char_p)
	SEPIA2_COM_DecodeModuleType_Params = (1,"p1",0),(1,"p2",0),
	SEPIA2_COM_DecodeModuleType_API = SEPIA2_COM_DecodeModuleType_Proto(("SEPIA2_COM_DecodeModuleType",sepiadll),SEPIA2_COM_DecodeModuleType_Params)
	
	p1 = ctypes.c_int(iModuleType)
	p2 = ctypes.c_char_p(cModuleType)

	SEPIA2_COM_DecodeModuleType_API(p1,p2)

	print 'PYSEPIA: Module Type: ' + p2.value


# First argument ... iGetPrimary = 1 for primary module and = 0 for secondary module 
def SEPIA2_COM_GetModuleType(iDevIdx,iSlotId,iGetPrimary): 
	piModuleType = 0

	INTP = ctypes.POINTER(ctypes.c_int)  

	SEPIA2_COM_GetModuleType_Proto = ctypes.WINFUNCTYPE(ctypes.c_int,ctypes.c_int,ctypes.c_int,ctypes.c_int,INTP)
	SEPIA2_COM_GetModuleType_Params = (1,"p1",0),(1,"p2",0),(1,"p3",0),(1,"p4",0),
	SEPIA2_COM_GetModuleType_API = SEPIA2_COM_GetModuleType_Proto(("SEPIA2_COM_GetModuleType",sepiadll),SEPIA2_COM_GetModuleType_Params)
	
	p1 = ctypes.c_int(iDevIdx)
	p2 = ctypes.c_int(iSlotId)
	p3 = ctypes.c_int(iGetPrimary)

	num = ctypes.c_int(piModuleType)	
	addr = ctypes.addressof(num)
	p4 = ctypes.cast(addr, INTP)  
		
	iRetVal = SEPIA2_COM_GetModuleType_API(p1,p2,p3,p4)
	
	return p4.contents.value


def SEPIA2_COM_GetSerialNumber(iDevIdx,iSlotId): 
	iGetPrimary = 1
	cSerialNumber = " "
	
	SEPIA2_COM_GetSerialNumber_Proto = ctypes.WINFUNCTYPE(ctypes.c_int,ctypes.c_int,ctypes.c_int,ctypes.c_int,ctypes.c_char_p)
	SEPIA2_COM_GetSerialNumber_Params = (1,"p1",0),(1,"p2",0),(1,"p3",0),(1,"p4",0),
	SEPIA2_COM_GetSerialNumber_API = SEPIA2_COM_GetSerialNumber_Proto(("SEPIA2_COM_GetSerialNumber",sepiadll),SEPIA2_COM_GetSerialNumber_Params)
	
	p1 = ctypes.c_int(iDevIdx)	   
	p2 = ctypes.c_int(iSlotId)  
	p3 = ctypes.c_int(iGetPrimary)
	p4 = ctypes.c_char_p(cSerialNumber)

	SEPIA2_COM_GetSerialNumber_API(p1,p2,p3,p4)

	#return p4.value


def SEPIA2_COM_HasSecondaryModule(iDevIdx,iSlotId):
	piHasSecondary = 0
	INTP = ctypes.POINTER(ctypes.c_int)

	SEPIA2_COM_HasSecondaryModule_Proto = ctypes.WINFUNCTYPE(ctypes.c_int,ctypes.c_int,ctypes.c_int,INTP)
	SEPIA2_COM_HasSecondaryModule_Params = (1,"p1",0),(1,"p2",0),(1,"p3",0),
	SEPIA2_COM_HasSecondaryModule_API = SEPIA2_COM_HasSecondaryModule_Proto(("SEPIA2_COM_HasSecondaryModule",sepiadll),SEPIA2_COM_HasSecondaryModule_Params)
	
	p1 = ctypes.c_int(iDevIdx)
	p2 = ctypes.c_int(iSlotId)
        
	num = ctypes.c_int(piHasSecondary)	
	addr = ctypes.addressof(num)
	p3 = ctypes.cast(addr, INTP)

	SEPIA2_COM_HasSecondaryModule_API(p1,p2)

	# Using p3.contents dereferences the pointer to p3 
	return p3.contents.value	# return the value of piHasSecondary 


def SEPIA2_SCM_GetLaserSoftLock(iDevIdx,iSlotId): 
	pbSoftLocked = 0		# this produces a copy of previous allocated memory
	UCHARP = ctypes.POINTER(ctypes.c_ubyte)		# sets up an unsigned character pointer
	#pbSoftLocked = "10"
	
	SEPIA2_SCM_GetLaserSoftLock_Proto = ctypes.WINFUNCTYPE(ctypes.c_int,ctypes.c_int,ctypes.c_int,UCHARP)
	SEPIA2_SCM_GetLaserSoftLock_Params = (1,"p1",0),(1,"p2",0),(1,"p3",0),
	SEPIA2_SCM_GetLaserSoftLock_API = SEPIA2_SCM_GetLaserSoftLock_Proto(("SEPIA2_SCM_GetLaserSoftLock",sepiadll),SEPIA2_SCM_GetLaserSoftLock_Params)
	
	p1 = ctypes.c_int(iDevIdx)	   
	p2 = ctypes.c_int(iSlotId)  
        
	char_sepia = ctypes.c_int(pbSoftLocked)	
	addr = ctypes.addressof(char_sepia)
	p3 = ctypes.cast(addr, UCHARP)

	SEPIA2_SCM_GetLaserSoftLock_API(p1,p2,p3)
	
	return p3.contents.value


def SEPIA2_SCM_SetLaserSoftLock(iDevIdx,iSlotId,pbSoftLocked): 
	SEPIA2_SCM_SetLaserSoftLock_Proto = ctypes.WINFUNCTYPE(ctypes.c_int,ctypes.c_int,ctypes.c_int,ctypes.c_ubyte)
	SEPIA2_SCM_SetLaserSoftLock_Params = (1,"p1",0),(1,"p2",0),(1,"p3",0),
	SEPIA2_SCM_SetLaserSoftLock_API = SEPIA2_SCM_SetLaserSoftLock_Proto(("SEPIA2_SCM_SetLaserSoftLock",sepiadll),SEPIA2_SCM_SetLaserSoftLock_Params)
	
	p1 = ctypes.c_int(iDevIdx)	   
	p2 = ctypes.c_int(iSlotId)  
	p3 = ctypes.c_ubyte(pbSoftLocked)

	SEPIA2_SCM_SetLaserSoftLock_API(p1,p2,p3)
	
	return p3.value


def SEPIA2_SCM_GetLaserLocked(iDevIdx,iSlotId): 
	pbLocked = 0
	UCHARP = ctypes.POINTER(ctypes.c_ubyte)		# sets up an unsigned character pointer

	SEPIA2_SCM_GetLaserLocked_Proto = ctypes.WINFUNCTYPE(ctypes.c_int,ctypes.c_int,ctypes.c_int,UCHARP)
	SEPIA2_SCM_GetLaserLocked_Params = (1,"p1",0),(1,"p2",0),(1,"p3",0),
	SEPIA2_SCM_GetLaserLocked_API = SEPIA2_SCM_GetLaserLocked_Proto(("SEPIA2_SCM_GetLaserLocked",sepiadll),SEPIA2_SCM_GetLaserLocked_Params)
	
	p1 = ctypes.c_int(iDevIdx)	   
	p2 = ctypes.c_int(iSlotId)
	
	char_sepia = ctypes.c_int(pbLocked)	
	addr = ctypes.addressof(char_sepia)
	p3 = ctypes.cast(addr, UCHARP)

	SEPIA2_SCM_GetLaserLocked_API(p1,p2,p3)
	
	return p3.contents.value


def SEPIA2_SOM_GetFreqTrigMode(iDevIdx, iSlotID):
	iFreqTrigMode = 0

	INTP = ctypes.POINTER(ctypes.c_int)

	SEPIA2_SOM_GetFreqTrigMode_Proto = ctypes.WINFUNCTYPE(ctypes.c_int,ctypes.c_int,ctypes.c_int,INTP)
	SEPIA2_SOM_GetFreqTrigMode_Params = (1,"p1",0),(1,"p2",0),(1,"p3",0),
	SEPIA2_SOM_GetFreqTrigMode_API = SEPIA2_SOM_GetFreqTrigMode_Proto(("SEPIA2_SOM_GetFreqTrigMode",sepiadll),SEPIA2_SOM_GetFreqTrigMode_Params)

	p1 = ctypes.c_int(iDevIdx)
	p2 = ctypes.c_int(iSlotID)

	num = ctypes.c_int(iFreqTrigMode)	
	addr = ctypes.addressof(num)
	p3 = ctypes.cast(addr, INTP)

	SEPIA2_SOM_GetFreqTrigMode_API(p1,p2,p3)

	return p3.contents.value


def SEPIA2_SLM_GetParameters(iDevIdx, iSlotId):
	iFreqTrigMode = 0
	bPulseMode = 10
	iHead = 0
	bIntensity = 10

	INTP = ctypes.POINTER(ctypes.c_int)
	UCHARP = ctypes.POINTER(ctypes.c_ubyte)		# sets up an unsigned character pointer

	SEPIA2_SLM_GetParameters_Proto = ctypes.WINFUNCTYPE(ctypes.c_int,ctypes.c_int,ctypes.c_int,INTP,UCHARP,INTP,UCHARP)
	SEPIA2_SLM_GetParameters_Params = (1,"p1",0),(1,"p2",0),(1,"p3",0),(1,"p4",0),(1,"p5",0),(1,"p6",0),
	SEPIA2_SLM_GetParameters_API = SEPIA2_SLM_GetParameters_Proto(("SEPIA2_SLM_GetParameters",sepiadll),SEPIA2_SLM_GetParameters_Params)

	p1 = ctypes.c_int(iDevIdx)
	p2 = ctypes.c_int(iSlotId)
        
	num = ctypes.c_int(iFreqTrigMode)	
	addr = ctypes.addressof(num)
	p3 = ctypes.cast(addr, INTP)

	#p4 = ctypes.c_char_p(bPulseMode)

	char_sepia = ctypes.c_ubyte(bPulseMode)
	addr = ctypes.addressof(char_sepia)
	p4 = ctypes.cast(addr,UCHARP)
	
	num2 = ctypes.c_int(iHead)	
	addr2 = ctypes.addressof(num2)
	p5 = ctypes.cast(addr2, INTP)

	#p6 = ctypes.c_char_p(bIntensity)

	char_sepia2 = ctypes.c_ubyte(bIntensity)
	addr2 = ctypes.addressof(char_sepia2)
	p6 = ctypes.cast(addr2,UCHARP)
	
	returnval = SEPIA2_SLM_GetParameters_API(p1,p2,p3,p4,p5,p6)
	#print "PYSEPIA: successful (0) or unsuccessful (< 0) for GetParameters: " + str(returnval)
	#print "PYSEPIA: Intensity = " + str(p6.contents.value) + "%"
	#print "PYSEPIA: Frequency number = " + str(p3.contents.value)
	#print "PYSEPIA: Pulse Mode = " + str(p4.contents.value)
	#print "PYSEPIA: Head ID = " + str(p5.contents.value)
	return p6.contents.value,p3.contents.value,p4.contents.value,p5.contents.value


def SEPIA2_SLM_SetParameters(iDevIdx,iSlotId,iFreq,bIntensity):
	# IT IS VERY IMPORTANT THAT PULSE MODE IS ENABLED!
	bPulseMode = 1
	if (bPulseMode != 1):
		bPulseMode = 1
		print 'PYSEPIA: Pulse Mode must be enabled (set to "1").  Continuous Mode (set to "0") will damage the laserhead!'

	SEPIA2_SLM_SetParameters_Proto = ctypes.WINFUNCTYPE(ctypes.c_int,ctypes.c_int,ctypes.c_int,ctypes.c_int,ctypes.c_int,ctypes.c_int)
	SEPIA2_SLM_SetParameters_Params = (1,"p1",0),(1,"p2",0),(1,"p3",0),(1,"p4",0),(1,"p5",0),
	SEPIA2_SLM_SetParameters_API = SEPIA2_SLM_SetParameters_Proto(("SEPIA2_SLM_SetParameters",sepiadll),SEPIA2_SLM_SetParameters_Params)

	p1 = ctypes.c_int(iDevIdx)
	p2 = ctypes.c_int(iSlotId)
	p3 = ctypes.c_int(iFreq)
	p4 = ctypes.c_int(bPulseMode)
	p5 = ctypes.c_int(bIntensity)

	SEPIA2_SLM_SetParameters_API(p1,p2,p3,p4,p5)


def SEPIA2_SLM_DecodeFreqTrigMode(iFreq):
	cFreqTrigMode = " "

	SEPIA2_SLM_DecodeFreqTrigMode_Proto = ctypes.WINFUNCTYPE(ctypes.c_int,ctypes.c_int,ctypes.c_char_p)
	SEPIA2_SLM_DecodeFreqTrigMode_Params = (1,"p1",0),(1,"p2",0),
	SEPIA2_SLM_DecodeFreqTrigMode_API = SEPIA2_SLM_DecodeFreqTrigMode_Proto(("SEPIA2_SLM_DecodeFreqTrigMode",sepiadll),SEPIA2_SLM_DecodeFreqTrigMode_Params)

	p1 = ctypes.c_int(iFreq)
	p2 = ctypes.c_int(cFreqTrigMode)
        
	ret_trigger = SEPIA2_SLM_DecodeFreqTrigMode_API(p1,p2)
	return ret_trigger


def SEPIA2_SLM_DecodeHeadType(iHeadType):
	cHeadType = " "

	SEPIA2_SLM_DecodeHeadType_Proto = ctypes.WINFUNCTYPE(ctypes.c_int,ctypes.c_int,ctypes.c_char_p)
	SEPIA2_SLM_DecodeHeadType_Params = (1,"p1",0),(1,"p2",0),
	SEPIA2_SLM_DecodeHeadType_API = SEPIA2_SLM_DecodeHeadType_Proto(("SEPIA2_SLM_DecodeHeadType",sepiadll),SEPIA2_SLM_DecodeHeadType_Params)

	p1 = ctypes.c_int(iHeadType)
	p2 = ctypes.c_int(cHeadType)
        
	ret_head = SEPIA2_SLM_DecodeFreqTrigMode_API(p1,p2)
	return ret_head
