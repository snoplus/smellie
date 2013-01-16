import ctypes,sys ,os,time,heapq

##Check the ddl path is correct
ddl_path = "C:\Users\LocalAdmin\Desktop\Pysepia\Sepia2_Lib.dll"

if (os.path.exists(ddl_path) == True):
	print '\n DLL path is correct \n'
else:
	sys.exit('\n Need to give the correct path for the Sepia2_Lib.dll file \n')
print ddl_path
#sepiadll = ctypes.WinDLL(ddl_path)
sepiadll = ctypes.OleDLL(ddl_path)

##I need to make some of these function return certain arguments which are used later on by other functions 

## Opens up the .ddl library version and returns this version number
def SEPIA2_LIB_GetVersion(): 	
	cLibVersion = " "
	SEPIA2_LIB_GetVersion_Proto = ctypes.WINFUNCTYPE(ctypes.c_int,ctypes.c_char_p)
	SEPIA2_LIB_GetVersion_Params = (1,"p1",0),
	SEPIA2_LIB_GetVersion_API = SEPIA2_LIB_GetVersion_Proto(("SEPIA2_LIB_GetVersion",sepiadll),SEPIA2_LIB_GetVersion_Params)
	p1 = ctypes.c_char_p(cLibVersion)
	SEPIA2_LIB_GetVersion_API(p1)
	return p1.value

## Opens up the USB device and returns the device ID. REQUIRED BEFORE ALL OTHER FUNCTIONS 
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
		print 'Connected to USB Device of serial number:' + p2.value
	else:
		print 'Not Connected to USB Device'
        return p1.value
        
## Closes the USB drive and prints if the USB has been sucessfully disconnected - REQUIRED AT THE END OF EACH PROGRAM        
def SEPIA2_USB_CloseDevice(iDevIdx):
	SEPIA2_USB_CloseDevice_Proto = ctypes.WINFUNCTYPE(ctypes.c_int,ctypes.c_int)
	SEPIA2_USB_CloseDevice_Params = (1,"p1",0),
	SEPIA2_USB_CloseDevice_API = SEPIA2_USB_CloseDevice_Proto(("SEPIA2_USB_CloseDevice",sepiadll),SEPIA2_USB_CloseDevice_Params)
	p1 = ctypes.c_int(iDevIdx)
	iRetVal = 27
	iRetVal = SEPIA2_USB_CloseDevice_API(p1)
	if (iRetVal == 0):
		print 'Disconnected from USB Device'	
	else:
		print 'Failure to disconnect from USB Device'
	return iRetVal 

## Opens the Module Map AND INITIALISES ALL THE LIBRARIES. THIS IS REQUIRED WITH SEPIA2_USB_OpenDevice BEFORE ANY FUNCTIONS CAN BE CALLED!
def SEPIA2_FWR_GetModuleMap(iDevIdx): ## Not sure about how the integer pointer is being used
		
	iPerformRestart = 0 ## No_restart is 0 and Restart is 1 (Boolean number)
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

	##print p3.contents.value
	return iRetVal

## Frees the module map and is required at the end of a program 
def SEPIA2_FWR_FreeModuleMap(iDevIdx):
	SEPIA2_FWR_FreeModuleMap_Proto = ctypes.WINFUNCTYPE(ctypes.c_int,ctypes.c_int)
	SEPIA2_FWR_FreeModuleMap_Params = (1,"p1",0),
	SEPIA2_FWR_FreeModuleMap_API = SEPIA2_FWR_FreeModuleMap_Proto(("SEPIA2_FWR_FreeModuleMap",sepiadll),SEPIA2_FWR_FreeModuleMap_Params)
	p1 = ctypes.c_int(iDevIdx)
	iRetVal = SEPIA2_FWR_FreeModuleMap_API(p1)
	return iRetVal

## Non-essential functions 
def SEPIA2_USB_GetStrDescriptor(iDevIdx):
	cDescriptor = " "
	SEPIA2_USB_GetStrDescriptor_Proto = ctypes.WINFUNCTYPE(ctypes.c_int,ctypes.c_int,ctypes.c_char_p)
	SEPIA2_USB_GetStrDescriptor_Params = (1,"p1",0),(1,"p2",0),
	SEPIA2_USB_GetStrDescriptor_API = SEPIA2_USB_GetStrDescriptor_Proto(("SEPIA2_USB_GetStrDescriptor",sepiadll),SEPIA2_USB_GetStrDescriptor_Params)
	p1 = ctypes.c_int(iDevIdx)
	p2 = ctypes.c_char_p(cDescriptor)
	SEPIA2_USB_GetStrDescriptor_API(p1,p2)
	return p2.value

def SEPIA2_LIB_DecodeError():
	iErrCode = 0
	cErrorString = " "
	SEPIA2_LIB_DecodeError_Proto = ctypes.WINFUNCTYPE(ctypes.c_int,ctypes.c_int,ctypes.c_char_p)
	SEPIA2_LIB_DecodeError_Params = (1,"p1",0),(1,"p2",0),
	SEPIA2_LIB_DecodeError_API = SEPIA2_LIB_DecodeError_Proto(("SEPIA2_LIB_DecodeError",sepiadll),SEPIA2_LIB_DecodeError_Params)	
	p1 = ctypes.c_int(iErrCode)
	p2 = ctypes.c_char_p(cErrorString)
	SEPIA2_LIB_DecodeError_API(p1,p2)

def SEPIA2_FWR_DecodeErrPhaseName():
	iErrPhase = 0
	cErrorPhase = " "
	SEPIA2_FWR_DecodeErrPhaseName_Proto = ctypes.WINFUNCTYPE(ctypes.c_int,ctypes.c_int,ctypes.c_char_p)
	SEPIA2_FWR_DecodeErrPhaseName_Params = (1,"p1",0),(1,"p2",0),
	SEPIA2_FWR_DecodeErrPhaseName_API = SEPIA2_FWR_DecodeErrPhaseName_Proto(("SEPIA2_FWR_DecodeErrPhaseName",sepiadll),SEPIA2_FWR_DecodeErrPhaseName_Params)
	p1 = ctypes.c_int(iErrPhase)	   ##integer returned by firmware function GetLastError
	p2 = ctypes.c_char_p(cErrorPhase)  ##error phase string
	SEPIA2_FWR_DecodeErrPhaseName_API(p1,p2)
	return p2.value

def SEPIA2_FWR_GetVersion(iDevIdx):
	cFWVersion = " "
	SEPIA2_FWR_GetVersion_Proto = ctypes.WINFUNCTYPE(ctypes.c_int,ctypes.c_int,ctypes.c_char_p)
	SEPIA2_FWR_GetVersion_Params = (1,"p1",0),(1,"p2",0),
	SEPIA2_FWR_GetVersion_API = SEPIA2_FWR_GetVersion_Proto(("SEPIA2_FWR_GetVersion",sepiadll),SEPIA2_FWR_GetVersion_Params)
	p1 = ctypes.c_int(iDevIdx)	   ##integer returned by firmware function GetLastError
	p2 = ctypes.c_char_p(cFWVersion)  ##error phase string
	SEPIA2_FWR_GetVersion_API(p1,p2)
	return p2.value

def SEPIA2_FWR_GetLastError(iDevIdx): ## Not sure about how the integer pointer is being used	
	piErrCode = 0 ## No_restart is 0 and Restart is 1 (Boolean number)
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
	
	print p3  #There is definately a memory allocation problem here and possibly where all my problems arise


def SEPIA2_COM_DecodeModuleType(iModuleType): 

	cModuleType = " "
	
	SEPIA2_COM_DecodeModuleType_Proto = ctypes.WINFUNCTYPE(ctypes.c_int,ctypes.c_int,ctypes.c_char_p)
	SEPIA2_COM_DecodeModuleType_Params = (1,"p1",0),(1,"p2",0),
	SEPIA2_COM_DecodeModuleType_API = SEPIA2_COM_DecodeModuleType_Proto(("SEPIA2_COM_DecodeModuleType",sepiadll),SEPIA2_COM_DecodeModuleType_Params)
	
	p1 = ctypes.c_int(iModuleType)	   ##integer returned by firmware function GetLastError
	p2 = ctypes.c_char_p(cModuleType)  ##error phase string

	SEPIA2_COM_DecodeModuleType_API(p1,p2)

	print 'Module Type: ' + p2.value

def SEPIA2_COM_GetModuleType(iDevIdx,iSlotId,iGetPrimary): ## Not sure about how the integer pointer is being used
		
	##iGetPrimary = 1 for primary module and =0 for secondary module 
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

def SEPIA2_SCM_GetLaserSoftLock(iDevIdx,iSlotId): 

	pbSoftLocked = " " ##this produces a copy of previous memory
	##pbSoftLocked = "10" ## this produces 10
	
	SEPIA2_SCM_GetLaserSoftLock_Proto = ctypes.WINFUNCTYPE(ctypes.c_int,ctypes.c_int,ctypes.c_int,ctypes.c_char_p)
	SEPIA2_SCM_GetLaserSoftLock_Params = (1,"p1",0),(1,"p2",0),(1,"p3",0),
	SEPIA2_SCM_GetLaserSoftLock_API = SEPIA2_SCM_GetLaserSoftLock_Proto(("SEPIA2_SCM_GetLaserSoftLock",sepiadll),SEPIA2_SCM_GetLaserSoftLock_Params)
	
	p1 = ctypes.c_int(iDevIdx)	   
	p2 = ctypes.c_int(iSlotId)  
	p3 = ctypes.c_char_p(pbSoftLocked)

	SEPIA2_SCM_GetLaserSoftLock_API(p1,p2,p3)
	
	print p3.value 

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
        UCHARP = ctypes.POINTER(ctypes.c_ubyte) ## sets up an unsigned character pointer

	SEPIA2_SCM_GetLaserLocked_Proto = ctypes.WINFUNCTYPE(ctypes.c_int,ctypes.c_int,ctypes.c_int,UCHARP)
	SEPIA2_SCM_GetLaserLocked_Params = (1,"p1",0),(1,"p2",0),(1,"p3",0),
	SEPIA2_SCM_GetLaserLocked_API = SEPIA2_SCM_GetLaserLocked_Proto(("SEPIA2_SCM_GetLaserLocked",sepiadll),SEPIA2_SCM_GetLaserLocked_Params)
	
	p1 = ctypes.c_int(iDevIdx)	   
	p2 = ctypes.c_int(iSlotId)
	
	char_sepia = ctypes.c_int(pbLocked)	
	addr = ctypes.addressof(char_sepia)
	p3 = ctypes.cast(addr, UCHARP)

	SEPIA2_SCM_GetLaserLocked_API(p1,p2,p3)
	
	return p3.value

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
        UCHARP = ctypes.POINTER(ctypes.c_ubyte) ## sets up an unsigned character pointer

        SEPIA2_SLM_GetParameters_Proto = ctypes.WINFUNCTYPE(ctypes.c_int,ctypes.c_int,ctypes.c_int,INTP,UCHARP,INTP,UCHARP)
	SEPIA2_SLM_GetParameters_Params = (1,"p1",0),(1,"p2",0),(1,"p3",0),(1,"p4",0),(1,"p5",0),(1,"p6",0),
	SEPIA2_SLM_GetParameters_API = SEPIA2_SLM_GetParameters_Proto(("SEPIA2_SLM_GetParameters",sepiadll),SEPIA2_SLM_GetParameters_Params)

        p1 = ctypes.c_int(iDevIdx)
        p2 = ctypes.c_int(iSlotId)
        
        num = ctypes.c_int(iFreqTrigMode)	
	addr = ctypes.addressof(num)
	p3 = ctypes.cast(addr, INTP)

	##p4 = ctypes.c_char_p(bPulseMode)

        char_sepia = ctypes.c_ubyte(bPulseMode)
        addr = ctypes.addressof(char_sepia)
        p4 = ctypes.cast(addr,UCHARP)
	
	num2 = ctypes.c_int(iHead)	
	addr2 = ctypes.addressof(num2)
	p5 = ctypes.cast(addr2, INTP)

	##p6 = ctypes.c_char_p(bIntensity) ## this should be an unsigned interger is that a problem ?

        char_sepia2 = ctypes.c_ubyte(bIntensity) ##     DONT REPEAT VARIABLE 
        addr2 = ctypes.addressof(char_sepia2)
        p6 = ctypes.cast(addr2,UCHARP)

        
        returnval = SEPIA2_SLM_GetParameters_API(p1,p2,p3,p4,p5,p6)
        ##print "sucess or not for get parameters 0 or <0: " + str(returnval)
        print "Intensity = " + str(p6.contents.value) + "%"
        print "Frequency number = " + str(p3.contents.value)
        print "Pulse Mode = " + str(p4.contents.value)
        print "Head ID = " + str(p5.contents.value)
	## this was added on 11/01/2013
	return p6.contents.value,p3.contents.value,p4.contents.value,p5.contents.value 	## this was added on 11/01/2013

def SEPIA2_SLM_SetParameters(iDevIdx,iSlotId,iFreq,bIntensity):

        bPulseMode = 1
        # z`ITS VERY IMPORTANT PULSE MODE IS ENABLED!
        if (bPulseMode != 1):
                bPulseMode = 1 ## this sets
                print 'Pulse has to be enabled to "1" for "Pulses enabled". Continuous mode "0" would break the laser'

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

        ## p3.contents - dereferences the pointer of p3 
	return p3.contents.value ##returns the value of piHasSecondary 


## BE CAREFUL WITH GLOBAL VARIABLES IN PYTHON AND LOCAL VARIABLES WITHIN THE INDIVIDUAL FILES !!


##print "1st Parameter Set :\n"
##SEPIA2_SLM_SetParameters(iDevIdx,200,2,60)
##time.sleep(5)
##SEPIA2_SLM_GetParameters(iDevIdx, 200)

##bIntensity = 100
##print "\n 2nd Parameter Set :\n"
##SEPIA2_SLM_SetParameters(iDevIdx,200,1,bIntensity)
##print 'Setting parameters'

##SEPIA2_SLM_GetParameters(iDevIdx, 200)
##time.sleep(5)

##SEPIA2_SCM_SetLaserSoftLock(iDevIdx,iSlotID,0)

##time.sleep(180)

##SEPIA2_SCM_SetLaserSoftLock(iDevIdx,iSlotID,1) ## 1 is locked and 0 in unlocked 










