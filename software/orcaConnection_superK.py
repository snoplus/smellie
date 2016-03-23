#!/usr/bin/env python
import time, logging
from ctypes import *

class statusBitStructure(Structure):
        _fields_ = [("bit0", c_int16),("bit1", c_int16),("bit2", c_int16),("bit3", c_int16),("bit4", c_int16),("bit5", c_int16), ("bit6", c_int16),("bit7", c_int16),("bit8", c_int16),("bit9", c_int16),("bit10", c_int16),("bit11", c_int16),("bit12", c_int16),("bit13", c_int16),("bit14", c_int16),("bit15", c_int16)]

class superKControlStructure(Structure):
        _fields_ = [("trigLevelSetpointmV", c_uint16),("displayBacklightPercent", c_uint8),("trigMode", c_uint8),("internalPulseFreqHz", c_uint16),("burstPulses", c_uint16),("watchdogIntervalSec", c_uint8),("internalPulseFreqLimitHz", c_uint32)]

# for loading NI LV dll's see NI white paper http://www.ni.com/white-paper/8911/en/
# http://digital.ni.com/public.nsf/allkb/A3804F88FCDB1E6286257CE00043C1A7
# https://decibel.ni.com/content/docs/DOC-9076
# https://decibel.ni.com/content/docs/DOC-9079

dll = cdll.LoadLibrary("superKUtil.dll")
libc = cdll.msvcrt

def portOpen(COMPort):
    #int32_t __cdecl PortOpen(char COMport[]);
    errorCode = 0
    logging.basicConfig(filename='superKLogRun{}.log'.format(runnumber), level=logging.INFO)
    errorCode += dll.PortOpen(COMPort)
    if (errorCode==0):
        logging.info( 'Port Opened: {}'.format(COMPort.value) )
    else:
        logging.error( 'Could not open port. Tried: {}, ErrorCode: {}'.format( COMPort.value, errorCode ) )
    return errorCode 

def portClose(COMPort):
    #int32_t __cdecl PortClose(char COMport[]);
    errorCode = 0
    errorCode += dll.PortClose(COMPort)
    if (errorCode==0):
        logging.info( 'Port Closed: {}'.format(COMPort.value) )
    else:
        logging.error( 'Could not close port. Tried: {}, ErrorCode: {}'.format( COMPort.value, errorCode ) )
    return errorCode

def getSuperKInfo(COMPort):
    #int32_t __cdecl GetSuperKInfo(char COMport[], char moduleSerialNumber[],int32_t len, int32_t *moduleType, uint16_t *firmwareVersion, char extendedVersionInfo[], int32_t len2);
    errorCode = 0
    serialBuff = int(8)
    serial = (c_char_p*serialBuff)()
    moduleType = c_int32(0)
    firmware = c_uint16(0)
    versionInfoBuff = int(26)
    versionInfo = (c_char_p*versionInfoBuff)()

    errorCode += dll.GetSuperKInfo(COMPort, byref(serial), serialBuff, byref(moduleType), byref(firmware), byref(versionInfo), versionInfoBuff)
    
    serial = str(cast(serial,c_char_p).value)
    versionInfo = str(cast(versionInfo,c_char_p).value)
    
    if (errorCode==0):
        logging.info( 'SuperK Info.\n\tFirmware: {}\n\tVersion Info: {}\n\tModule Type: {}\n\tSerial Number: {}'.format(firmware.value,versionInfo,format(moduleType.value,'02X'),serial) )
    else:
        logging.info( 'Could not get SuperK Info. ErrorCode: {}'.format( errorCode ) )
    return errorCode

def getVariaInfo(COMPort):
    #int32_t __cdecl GetVariaInfo(char COMport[], char moduleSerialNumber[],int32_t len, int32_t *moduleType, uint16_t *firmwareVersion, char extendedVersionInfo[], int32_t len2);
    errorCode = 0

    serialBuff = int(8)
    serial = (c_char_p*serialBuff)()
    moduleType = c_int32(0)
    firmware = c_uint16(0)
    versionInfoBuff = int(26)
    versionInfo = (c_char_p*versionInfoBuff)()

    errorCode += dll.GetVariaInfo(COMPort, byref(serial), serialBuff, byref(moduleType), byref(firmware), byref(versionInfo), versionInfoBuff)
    
    serial = str(cast(serial,c_char_p).value)
    versionInfo = str(cast(versionInfo,c_char_p).value)
    
    if (errorCode==0):
        logging.info( 'Varia Info.\n\tFirmware: {}\n\tVersion Info: {}\n\tModule Type: {}\n\tSerial Number: {}'.format(firmware.value,versionInfo,format(moduleType.value,'02X'),serial) )
    else:
        logging.info( 'Could not get Varia Info. ErrorCode: {}'.format( errorCode ) )
    return errorCode

def getVariaReadings(COMPort):
    #int32_t __cdecl GetVariaReadings(char COMport[], double *monitorInputPercent);
    errorCode = 0

    monitorInput = c_double(0)
    errorCode += dll.GetVariaReadings(COMPort, byref(monitorInput))
        
    if (errorCode==0):
        logging.info( 'Varia Readings: {}'.format(monitorInput.value) )
    else:
        logging.error( 'Could not successfully get Varia readings. ErrorCode: {}'.format( errorCode ) )
    return errorCode

def getSuperKReadings(COMPort):
    #int32_t __cdecl GetSuperKReadings(char COMport[], double *opticalPulseFreqkHz, double *actualInternalTrigFreqkHz, uint8_t *powerReadoutPercent, double *heatSinkTempC, double *supplyVoltagemV, uint8_t displayInfo[], int32_t len);
    errorCode = 0
    opticalPulseFreqkHz = c_double(0)
    actualInternalTrigFreqkHz = c_double(0)
    powerReadoutPercent = c_uint8(0)
    heatSinkTempC = c_double(0)
    supplyVoltagemV = c_double(0)
    displayInfoBuff = c_int32(90)
    displayInfo = (c_uint8*displayInfoBuff.value)()
    
    errorCode += dll.GetSuperKReadings(COMPort, byref(opticalPulseFreqkHz), byref(actualInternalTrigFreqkHz), byref(powerReadoutPercent), byref(heatSinkTempC), byref(supplyVoltagemV), byref(displayInfo), displayInfoBuff.value )
    
    if (errorCode==0):
        logging.info( 'SuperK Readings.\n\tOptical Pulse Freq (kHz): {}\n\tActual Internal Trig Freq (kHz): {}\n\tPower Readout (%): {}\n\tHeat Sink Temp (C): {}\n\tSupply Voltage (mV): {}\n\tDisplay Info:\n\t{}'.format(opticalPulseFreqkHz.value,actualInternalTrigFreqkHz.value,powerReadoutPercent.value,heatSinkTempC.value,supplyVoltagemV.value, cast(displayInfo,c_char_p).value ) )
    else:
        logging.error( 'Could not successfully get SuperK Readings. ErrorCode: {}'.format( errorCode ) )
    return errorCode

def getVariaStatusBits(COMPort,bitCluster):
    #int32_t __cdecl GetVariaStatusBits(char COMport[], int32_t *bitMaskDecimal, Cluster2 *statusBitCluster);
    errorCode = 0
    bitMaskDecimal = c_int32(0)
    errorCode += dll.GetVariaStatusBits(COMPort, byref(bitMaskDecimal), byref(bitCluster))    

    if (errorCode==0):
        logging.info( 'Get Varia Status Bits: {}(decimal)'.format(bitMaskDecimal.value) )
    else:
        logging.error( 'Could not get Varia Status Bits. ErrorCode: {}'.format( errorCode ) )
    return errorCode 

def printVariaStatusBits(bitCluster,option="ALL"):
    print "Varia Bit Status:"
    if (option=="ALL"):
        if (bitCluster.bit1 == 0): print "\tbit 1: OFF (Interlock Off)" 
        elif (bitCluster.bit1 == 1): print "\tbit 1: ON (Interlock Off)" 
        else: print "\tbit 1: OutOfRange (Interlock On)"
        
        if (bitCluster.bit2 == 0): print "\tbit 2: OFF (InterlockLoopIn)" 
        elif (bitCluster.bit2 == 1): print "\tbit 2: ON (InterlockLoopIn)" 
        else: print "\tbit 2: OutOfRange (InterlockLoopIn)"
        
        if (bitCluster.bit3 == 0): print "\tbit 3: OFF (InterlockLoopOut)" 
        elif (bitCluster.bit3 == 1): print "\tbit 3: ON (InterlockLoopOut)" 
        else: print "\tbit 3: OutOfRange (InterlockLoopOut)"
        
        if (bitCluster.bit5 == 0): print "\tbit 5: OFF (SupplyVoltageLow)" 
        elif (bitCluster.bit5 == 1): "\tbit 5: ON (SupplyVoltageLow)" 
        else: print "\tbit 5: OutOfRange (SupplyVoltageLow)"
        
        if (bitCluster.bit6 == 0): print "\tbit 6: OFF (ModuleTempRange)" 
        elif (bitCluster.bit6 == 1): print "\tbit 6: ON (ModuleTempRange)" 
        else: print "\tbit 6: OutOfRange (ModuleTempRange)"
        
        if (bitCluster.bit8 == 0): print "\tbit 8: OFF (ShutterSensor1)" 
        elif (bitCluster.bit8 == 1): print "\tbit 8: ON (ShutterSensor1)" 
        else: print "\tbit 8: OutOfRange (ShutterSensor1)"
        
        if (bitCluster.bit9 == 0): print "\tbit 9: OFF (ShutterSensor2)" 
        elif (bitCluster.bit9 == 1): print "\tbit 9: ON (ShutterSensor2)" 
        else: print "\tbit 9: OutOfRange (ShutterSensor2)"
        
        if (bitCluster.bit12 == 0): print "\tbit 12: OFF (Filter1Moving)" 
        elif (bitCluster.bit12 == 1): print "\tbit 12: ON (Filter1Moving)" 
        else: print "\tbit 12: OutOfRange (Filter1Moving)"
        
        if (bitCluster.bit13 == 0): print "\tbit 13: OFF (Filter2Moving)" 
        elif (bitCluster.bit13 == 1): print "\tbit 13: ON (Filter2Moving)" 
        else: print "\tbit 13: OutOfRange (Filter2Moving)"
        
        if (bitCluster.bit14 == 0): print "\tbit 14: OFF (Filter3Moving)" 
        elif (bitCluster.bit14 == 1): print "\tbit 14: ON (Filter3Moving)" 
        else: print "\tbit 14: OutOfRange (Filter3Moving)"
        
        if (bitCluster.bit15 == 0): print "\tbit 15: OFF (ErrorCodePresent)" 
        elif (bitCluster.bit15 == 1): print "\tbit 15: ON (ErrorCodePresent)" 
        else: print "\tbit 15: OutOfRange (ErrorCodePresent)"
    if (option=="ON"):
        if (bitCluster.bit1 == 0): pass
        elif (bitCluster.bit1 == 1): print "\tbit 1: ON (Interlock Off)" 
        else: print "\tbit 1: OutOfRange (Interlock On)"
        
        if (bitCluster.bit2 == 0): pass 
        elif (bitCluster.bit2 == 1): print "\tbit 2: ON (InterlockLoopIn)" 
        else: print "\tbit 2: OutOfRange (InterlockLoopIn)"
        
        if (bitCluster.bit3 == 0): pass
        elif (bitCluster.bit3 == 1): print "\tbit 3: ON (InterlockLoopOut)" 
        else: print "\tbit 3: OutOfRange (InterlockLoopOut)"
        
        if (bitCluster.bit5 == 0): pass
        elif (bitCluster.bit5 == 1): "\tbit 5: ON (SupplyVoltageLow)" 
        else: print "\tbit 5: OutOfRange (SupplyVoltageLow)"
        
        if (bitCluster.bit6 == 0): pass
        elif (bitCluster.bit6 == 1): print "\tbit 6: ON (ModuleTempRange)" 
        else: print "\tbit 6: OutOfRange (ModuleTempRange)"
        
        if (bitCluster.bit8 == 0): pass
        elif (bitCluster.bit8 == 1): print "\tbit 8: ON (ShutterSensor1)" 
        else: print "\tbit 8: OutOfRange (ShutterSensor1)"
        
        if (bitCluster.bit9 == 0): pass
        elif (bitCluster.bit9 == 1): print "\tbit 9: ON (ShutterSensor2)" 
        else: print "\tbit 9: OutOfRange (ShutterSensor2)"
        
        if (bitCluster.bit12 == 0): pass
        elif (bitCluster.bit12 == 1): print "\tbit 12: ON (Filter1Moving)" 
        else: print "\tbit 12: OutOfRange (Filter1Moving)"
        
        if (bitCluster.bit13 == 0): pass
        elif (bitCluster.bit13 == 1): print "\tbit 13: ON (Filter2Moving)" 
        else: print "\tbit 13: OutOfRange (Filter2Moving)"
        
        if (bitCluster.bit14 == 0): pass
        elif (bitCluster.bit14 == 1): print "\tbit 14: ON (Filter3Moving)" 
        else: print "\tbit 14: OutOfRange (Filter3Moving)"
        
        if (bitCluster.bit15 == 0): pass
        elif (bitCluster.bit15 == 1): print "\tbit 15: ON (ErrorCodePresent)" 
        else: print "\tbit 15: OutOfRange (ErrorCodePresent)"

def getSuperKStatusBits(COMPort,bitCluster):
    #int32_t __cdecl GetSuperKStatusBits(char COMport[], int32_t *bitMaskDecimal, Cluster1 *statusBitCluster);
    errorCode = 0

    bitMaskDecimal = c_int32(0)
    errorCode += dll.GetSuperKStatusBits(COMPort, byref(bitMaskDecimal), byref(bitCluster))
    
    if (errorCode==0):
        logging.info( 'Get SuperK Status Bits: {}(decimal)'.format(bitMaskDecimal.value) )
    else:
        logging.error( 'Could not get SuperK Status Bits. ErrorCode: {}'.format( errorCode ) )
    return errorCode 

def printSuperKStatusBits(bitCluster,option="ALL"):
    print "SuperK Bit Status:"
    if (option=="ALL"):
        if (bitCluster.bit0 == 0): print "\tbit 0: OFF (Emission)" 
        elif (bitCluster.bit0 == 1): print "\tbit 0: ON (Emission)" 
        else: print "\tbit 0: OutOfRange (Emission Off)" 
        
        if (bitCluster.bit1 == 0): print "\tbit 1: OFF (Interlock off)" 
        elif (bitCluster.bit1 == 1): print "\tbit 1: ON (Interlock off)"
        else: print "\tbit 1: OutOfRange (Interlock off)"
        
        if (bitCluster.bit2 == 0): print "\tbit 2: OFF (Interlock power failure)" 
        elif (bitCluster.bit2 == 1): print "\tbit 2: ON (Interlock power failure)" 
        else: print "\tbit 2: OutOfRange (Interlock power failure)"
        
        if (bitCluster.bit3 == 0): print "\tbit 3: OFF (Interlock loop off)" 
        elif (bitCluster.bit3 == 1): print "\tbit 3: ON (Interlock loop off)" 
        else: print "\tbit 3: OutOfRange (Interlock loop off)"
        
        if (bitCluster.bit5 == 0): print "\tbit 5: OFF (Supply voltage low)" 
        elif (bitCluster.bit5 == 1): print "\tbit 5: ON (Supply voltage low)" 
        else: print "\tbit 5: OutOfRange (Supply voltage low)"
        
        if (bitCluster.bit6 == 0): print "\tbit 6: OFF (Module temp range)" 
        elif(bitCluster.bit6 == 1): print "\tbit 6: ON (Module temp range)" 
        else: print "\tbit 6: OutOfRange (Module temp range)"
        
        if (bitCluster.bit7 == 0): print "\tbit 7: OFF (Pump temp high)" 
        elif (bitCluster.bit7 == 1): print "\tbit 7: ON (Pump temp high)" 
        else: print "\tbit 7: OutOfRange (Pump temp high)"
        
        if (bitCluster.bit8 == 0): print "\tbit 8: OFF (Pulse overrun)" 
        elif (bitCluster.bit8 == 1): print "\tbit 8: ON (Pulse overrun)" 
        else: print "\tbit 8: OutOfRange (Pulse overrun)"
        
        if (bitCluster.bit9 == 0): print "\tbit 9: OFF (Trig signal level)" 
        elif (bitCluster.bit9 == 1): print "\tbit 9: ON (Trig signal level)" 
        else: print "\tbit 9: OutOfRange (Trig signal level)"
        
        if (bitCluster.bit10 == 0): print "\tbit 10: OFF (Trig edge)" 
        elif (bitCluster.bit10 == 1): print "\tbit 10: ON (Trig edge)" 
        else: print "\tbit 10: OutOfRange (Trig edge)"
        
        if (bitCluster.bit15 == 0): print "\tbit 15: OFF (Error code present)" 
        elif (bitCluster.bit15 == 1): print "\tbit 15: ON (Error code present)" 
        else: print "\tbit 15: OutOfRange (Error code present)"
    if (option=="ON"):
        if (bitCluster.bit0 == 0): pass
        elif (bitCluster.bit0 == 1): print "\tbit 0: ON (Emission)" 
        else: print "\tbit 0: OutOfRange (Emission)" 
        
        if (bitCluster.bit1 == 0): pass
        elif (bitCluster.bit1 == 1): print "\tbit 1: ON (Interlock off)"
        else: print "\tbit 1: OutOfRange (Interlock off)"
        
        if (bitCluster.bit2 == 0): pass
        elif (bitCluster.bit2 == 1): print "\tbit 2: ON (Interlock power failure)" 
        else: print "\tbit 2: OutOfRange (Interlock power failure)"
        
        if (bitCluster.bit3 == 0): pass
        elif (bitCluster.bit3 == 1): print "\tbit 3: ON (Interlock loop off)" 
        else: print "\tbit 3: OutOfRange (Interlock loop off)"
        
        if (bitCluster.bit5 == 0): pass
        elif (bitCluster.bit5 == 1): print "\tbit 5: ON (Supply voltage low)" 
        else: print "\tbit 5: OutOfRange (Supply voltage low)"
        
        if (bitCluster.bit6 == 0): pass
        elif(bitCluster.bit6 == 1): print "\tbit 6: ON (Module temp range)" 
        else: print "\tbit 6: OutOfRange (Module temp range)"
        
        if (bitCluster.bit7 == 0): pass
        elif (bitCluster.bit7 == 1): print "\tbit 7: ON (Pump temp high)" 
        else: print "\tbit 7: OutOfRange (Pump temp high)"
        
        if (bitCluster.bit8 == 0): pass
        elif (bitCluster.bit8 == 1): print "\tbit 8: ON (Pulse overrun)" 
        else: print "\tbit 8: OutOfRange (Pulse overrun)"
        
        if (bitCluster.bit9 == 0): pass
        elif (bitCluster.bit9 == 1): print "\tbit 9: ON (Trig signal level)" 
        else: print "\tbit 9: OutOfRange (Trig signal level)"
        
        if (bitCluster.bit10 == 0): pass
        elif (bitCluster.bit10 == 1): print "\tbit 10: ON (Trig edge)" 
        else: print "\tbit 10: OutOfRange (Trig edge)"
        
        if (bitCluster.bit15 == 0): pass
        elif (bitCluster.bit15 == 1): print "\tbit 15: ON (Error code present)" 
        else: print "\tbit 15: OutOfRange (Error code present)"

def getSuperKControls(COMPort,controlCluster):
    #int32_t __cdecl GetSuperKControls(char COMport[], Cluster *outputCluster);
    errorCode = 0
    errorCode += dll.GetSuperKControls(COMPort, byref(controlCluster))

    if (errorCode==0):
        logging.info( 'Get SuperK Control Readings.\n\tTrig Level Setpoint (mV): {}\n\tDisplay Backlight (%): {}\n\tTrigger Mode: {}\n\tInternal Pulse Freq (Hz): {}\n\tBurst Pulses: {}\n\tWatchdog Interval (Sec): {}\n\tInternal Pulse Freq Limit (Hz): {}'.format(controlCluster.trigLevelSetpointmV,controlCluster.displayBacklightPercent,controlCluster.trigMode,controlCluster.internalPulseFreqHz,controlCluster.burstPulses,controlCluster.watchdogIntervalSec,controlCluster.internalPulseFreqLimitHz) )
    else:
        logging.error( 'Could not get SuperK Status Bits. ErrorCode: {}'.format( errorCode ) )
    return errorCode 

def getVariaControls(COMPort):
    #int32_t __cdecl GetVariaControls(char COMport[], uint16_t *NDFilterSetpointPercentx10, uint16_t *SWFilterSetpointAngstrom, uint16_t *LPFilterSetpointAngstrom);
    errorCode = 0
    NDFilterSetpointPercentx10 = c_uint16(0)
    SWFilterSetpointAngstrom = c_uint16(0)
    LPFilterSetpointAngstrom = c_uint16(0)
    errorCode += dll.GetVariaControls(COMPort, byref(NDFilterSetpointPercentx10), byref(SWFilterSetpointAngstrom), byref(LPFilterSetpointAngstrom))

    if (errorCode==0):
        logging.info( 'Get Varia Control Readings.\n\tND Filter Setpoint (% x 10): {}\n\tSW Filter Setpoint (nm x 10):{}\n\tLP Filter Setpoint (nm x 10): {}'.format(NDFilterSetpointPercentx10.value,SWFilterSetpointAngstrom.value,LPFilterSetpointAngstrom.value) )
    else:
        logging.error( 'Could not open port. Tried: {}, ErrorCode: {}'.format( COMPort.value, str(errorCode) ) )
    return errorCode 

def setSuperKControls(COMPort,controlCluster,bitCluster):
    #int32_t __cdecl SetSuperKControls(char COMport[], Cluster *outputCluster);
    errorCode = 0
    errorCode += dll.SetSuperKControls(COMPort, byref(controlCluster))

    errorCode += getSuperKStatusBits(COMPort,bitCluster)
    printSuperKStatusBits(bitCluster,"ON")
        
    if (errorCode==0):
        logging.info( 'tSet SuperK Controls.\n\tTrig Level Setpoint (mV): {}\n\tDisplay Backlight (%): {}\n\tTrigger Mode: {}\n\tInternal Pulse Freq (Hz): {}\n\tBurst Pulses: {}\n\tWatchdog Interval (Sec): {}\n\tInternal Pulse Freq Limit (Hz): {}'.format(controlCluster.trigLevelSetpointmV,controlCluster.displayBacklightPercent,controlCluster.trigMode,controlCluster.internalPulseFreqHz,controlCluster.burstPulses,controlCluster.watchdogIntervalSec,controlCluster.internalPulseFreqLimitHz) )
    else:
        logging.error( 'Could not set SuperK Status Bits. ErrorCode: {}'.format( errorCode ) )
    return errorCode 

def setSuperKControlEmission(COMPort,state,superKbitCluster,variabitCluster):
    #int32_t __cdecl SetSuperKControlEmission(char COMport[], uint8_t emission);
    errorCode = 0
    errorCode += getSuperKStatusBits(COMPort,superKbitCluster)
    errorCode += getVariaStatusBits(COMPort,variabitCluster)
    
    if (state == 0): 
        errorCode += dll.SetSuperKControlEmission(COMPort, c_uint8(0) )
        logging.info( 'Setting SuperK Control Emission: {}'.format(c_uint8(0).value) )
        time.sleep(2)
        errorCode += getSuperKStatusBits(COMPort,superKbitCluster)
        if (superKbitCluster.bit0 == 1):
            logging.error( 'Setting SuperK emission: ERROR! Emission set to zero but EMISSION IS ON.')
        elif (superKbitCluster.bit0 == 0):
            logging.info( 'Setting SuperK emission: Emission set to zero. Emission is OFF.')
        else:
            logging.error( 'Setting SuperK emission: ERROR! Emission set to zero but EMISSION STATE IS UNKNOWN: {}'.format(superKbitCluster.bit0) )
    
    elif (state == 1):
        if (superKbitCluster.bit15 == 1) or (variabitCluster.bit15 == 1):
            errorCode += dll.SetSuperKControlEmission(COMPort, 0 )
            logging.info( 'Setting SuperK Control Emission: {}'.format(c_uint8(0).value) )
            time.sleep(2)
            errorCode += getSuperKStatusBits(COMPort,superKbitCluster)
            if (superKbitCluster.bit0 == 1):
                logging.error( 'Setting SuperK emission: ERROR present. Emission set to zero. Check system. WARNING EMISSION IS ON.')
            elif (superKbitCluster.bit0 == 0):
                logging.error( 'Setting SuperK emission: ERROR present. Emission set to zero. Emission is OFF.')
            else:
                logging.error( 'Setting SuperK emission: ERROR present. Emission set to zero. Check system. WARNING EMISSION IS UNKNOWN.')
            
        elif (superKbitCluster.bit15 == 0) and (variabitCluster.bit15 == 0):
            if (variabitCluster.bit12 == 0) and (variabitCluster.bit13 == 0) and (variabitCluster.bit14 == 0):
                errorCode += dll.SetSuperKControlEmission(COMPort, c_uint8(state) )
                logging.info( 'Setting SuperK Control Emission: {}'.format(c_uint8(state).value) )
                time.sleep(2)
                errorCode += getSuperKStatusBits(COMPort,superKbitCluster)
                if (superKbitCluster.bit0 == 1):
                    logging.info( 'Setting SuperK emission: {}, Emission is ON.'.format(state) )
                elif (superKbitCluster.bit0 == 0):
                    logging.error( 'Setting SuperK emission: ERROR, emission set to {} but emission is OFF. Check system.'.format(superKbitCluster.bit0) )
                else:
                    logging.error( 'Setting SuperK emission: ERROR, state UNKNOWN: {}. Check system.'.format(superKbitCluster.bit0) )
            else:
                errorCode += dll.SetSuperKControlEmission(COMPort, 0 )
                logging.info( 'Setting SuperK Control Emission: {}'.format(c_uint8(0).value) )
                time.sleep(2)
                errorCode += getSuperKStatusBits(COMPort,superKbitCluster)
                if (superKbitCluster.bit0 == 1):
                    logging.error( 'Setting SuperK emission: Unable to set while Varia filters moving. WARNING Emission is ON.' )
                elif (superKbitCluster.bit0 == 0):
                    logging.error( 'Setting SuperK emission: Unable to set while Varia filters moving. Emission set to zero.' )
                else:
                    logging.error( 'Setting SuperK emission: Unable to set while Varia filters moving. ERROR: Emission set to UNKNOWN state: {}'.format(superKbitCluster.bit0) )
                
                errorCode = errorCode+1

    if (errorCode!=0):
        logging.error( 'Could not set SuperK Emission. ErrorCode: {}'.format( COMPort.value, str(errorCode) ) )
    return errorCode 

def setSuperKControlInterlock(COMPort,state,bitCluster):
    #int32_t __cdecl SetSuperKControlInterlock(char COMport[], uint8_t interlock);
    errorCode = 0
    errorCode += dll.SetSuperKControlInterlock(COMPort, c_uint8(state) )
    time.sleep(2)
    
    errorCode += getSuperKStatusBits(COMPort,bitCluster)
    printSuperKStatusBits(bitCluster, "ON")
    
    if (state == 1):
        if (bitCluster.bit15 == 1):
            if (bitCluster.bit1 == 0):
                logging.error( 'Setting SuperK Control Interlock to {}: ERROR present. Interlock ON. Check system.'.format(state) )
                errorCode = errorCode+1
            elif (bitCluster.bit1 == 1):
                logging.error( 'Setting SuperK Control Interlock to {}: ERROR present. Interlock Off. Check system.'.format(state) )
                errorCode = errorCode+1
            else:
                logging.error( 'Setting SuperK Control Interlock to {}: ERROR present. Interlock state UNKNOWN. Check system.'.format(state) )
                errorCode = errorCode+1
        elif (bitCluster.bit15 == 0):
            if (bitCluster.bit1 == 0):
                logging.error( 'Setting SuperK Control Interlock to {}: ERROR present. Interlock ON. Check system.'.format(state) )
                errorCode = errorCode+1
            elif (bitCluster.bit1 == 1):
                logging.info( 'Setting SuperK Control Interlock to {}: Success. Interlock Off.'.format(state) )
            else:
                logging.error( 'Setting SuperK Control Interlock to {}: ERROR present. Interlock state UNKNOWN. Check system.'.format(state) )
                errorCode = errorCode+1
    elif (state == 0):
        if (bitCluster.bit15 == 1):
            if (bitCluster.bit1 == 0):
                logging.error( 'Setting SuperK Control Interlock to {}: ERROR present. Interlock ON. Check system.'.format(state) )
                errorCode = errorCode+1
            elif (bitCluster.bit1 == 1):
                logging.error( 'Setting SuperK Control Interlock to {}: ERROR present. Interlock Off. Check system.'.format(state) )
                errorCode = errorCode+1
            else:
                logging.error( 'Setting SuperK Control Interlock to {}: ERROR present. Interlock state UNKNOWN. Check system.'.format(state) )
                errorCode = errorCode+1
        elif (bitCluster.bit15 == 0):
            if (bitCluster.bit1 == 0):
                logging.info( 'Setting SuperK Control Interlock to {}: Success. Interlock ON.'.format(state) )
                errorCode = errorCode+1
            elif (bitCluster.bit1 == 1):
                logging.error( 'Setting SuperK Control Interlock to {}: ERROR present. Interlock Off. Check system.'.format(state) )
                errorCode = errorCode+1
            else:
                logging.error( 'Setting SuperK Control Interlock to {}: ERROR present. Interlock state UNKNOWN. Check system.'.format(state) )
                errorCode = errorCode+1

    if (errorCode!=0):
        logging.error( 'Could not set SuperK Interlock. ErrorCode: {}'.format( str(errorCode) ) )
    return errorCode 

def setVariaControls(COMPort, NDFilterSetpointPercentx10, SWFilterSetpointAngstrom, LPFilterSetpointAngstrom, superKBitCluster, variaBitCluster):
    #int32_t __cdecl SetVariaControls(char COMport[], uint16_t NDFilterSetpointPercentx10, uint16_t SWFilterSetpointAngstrom, uint16_t LPFilterSetpointAngstrom);
    errorCode = 0
    NDFilterSetpointPercentx10 = c_uint16(NDFilterSetpointPercentx10)
    SWFilterSetpointAngstrom = c_uint16(SWFilterSetpointAngstrom)
    LPFilterSetpointAngstrom = c_uint16(LPFilterSetpointAngstrom)
    
    errorCode += getVariaStatusBits(COMPort,variaBitCluster)
    
    if (superKBitCluster.bit0 == 0):
        if (variaBitCluster.bit15 == 0):
            if (SWFilterSetpointAngstrom.value > LPFilterSetpointAngstrom.value):
                if ((SWFilterSetpointAngstrom.value - LPFilterSetpointAngstrom.value) >= 100 and (SWFilterSetpointAngstrom.value - LPFilterSetpointAngstrom.value) <= 1000):
                    errorCode += dll.SetVariaControls(COMPort, NDFilterSetpointPercentx10, SWFilterSetpointAngstrom, LPFilterSetpointAngstrom)
                    
                    errorCode += getVariaStatusBits(COMPort,variaBitCluster)
            
                    if (variaBitCluster.bit12 == 0) and (variaBitCluster.bit13 == 0) and (variaBitCluster.bit14 == 0):
                        logging.info( 'Setting Varia Filters to: SW(nm x 10): {} and LP(nm x 10): {}, (ND: (%x10): {}) : Success.'.format(SWFilterSetpointAngstrom.value,LPFilterSetpointAngstrom.value,NDFilterSetpointPercentx10.value) )
                    else:
                        logging.error( 'Setting Varia Filters to: SW(nm x 10): {}and LP(nm x 10): {}, (ND: (%x10): {}. Warning Filters moving, wait and check again.'.format(SWFilterSetpointAngstrom.value, LPFilterSetpointAngstrom.value, NDFilterSetpointPercentx10.value) )
                        errorCode = errorCode+1
                else:
                    logging.error( 'ERROR (setVariaControls): Minimum bandwidth is 10nm. Maximum bandwidth is 100nm. SP & LP filters must differ by at least 10nm and no more than 100nm.')
                    errorCode = errorCode+1
            else: 
                logging.error( 'ERROR (setVariaControls): SWP filter value must be larger than LPP filter value'
                errorCode = errorCode+1
        elif (variaBitCluster.bit15 == 0):
            logging.error( 'Setting Varia Filters: ERROR present. Filters not set. Check system.')
            errorCode = errorCode+1
    elif (superKBitCluster.bit0 == 1):
        logging.error( 'Setting Varia Filters: ERROR: Emission is ON. Cannot set filters without turning off emission.')
        errorCode = errorCode+1

    if (errorCode!=0):
        logging.error( 'Could not set Varia Controls. ErrorCode: {}'.format( errorCode ) )
    return errorCode 

def initialise(COMPort, superKControlCluster, superKBitCluster, variaBitCluster):
    errorCode = 0
    
    logging.info( 'Begin Initialise ---------------------------'
    errorCode += getSuperKInfo(COMPort)
    errorCode += getVariaInfo(COMPort)
    errorCode += getVariaReadings(COMPort)
    errorCode += getSuperKReadings(COMPort)
    errorCode += getSuperKStatusBits(COMPort,superKBitCluster)
    printSuperKStatusBits(superKBitCluster,"ON")
    errorCode += getVariaStatusBits(COMPort,variaBitCluster)
    printVariaStatusBits(variaBitCluster,"ON")
    errorCode += getSuperKControls(COMPort,superKControlCluster)
    errorCode += getVariaControls(COMPort)
    logging.info( 'End Initialise ---------------------------'
    
    if (errorCode==0):
        logging.info( 'Initialised OK.')
    else:
        logging.error( 'Error during Initialisation. ErrorCode: {}'.format( errorCode ) )
    return errorCode 

def setSafeStates(COMPort, superKControlCluster, superKBitCluster, variaBitCluster):
    errorCode = 0

    logging.error( 'Begin superKSafeStates ---------------------------'
    superKControlCluster.trigLevelSetpointmV = c_uint16(1000)
    superKControlCluster.displayBacklightPercent = c_uint8(50)
    superKControlCluster.trigMode = c_uint8(1)
    superKControlCluster.internalPulseFreqHz = c_uint16(0)
    superKControlCluster.burstPulses = c_uint16(1)
    superKControlCluster.watchdogIntervalSec = c_uint8(0)
    superKControlCluster.internalPulseFreqLimitHz = c_uint32(0)

    #if (superKBitCluster.bit0 == 1):
        #errorCode += setSuperKControlEmission(COMPort,0,superKBitCluster,variaBitCluster)
        #time.sleep(1)
    
    errorCode += setSuperKControlInterlock(COMPort,1,superKBitCluster)
    time.sleep(1)
    #errorCode += setSuperKControlEmission(COMPort,0,superKBitCluster,variaBitCluster)
    #errorCode += setSuperKControlInterlock(COMPort,0,superKBitCluster)
    #time.sleep(1)

    #errorCode += setSuperKControls(COMPort,superKControlCluster,superKBitCluster)
    #time.sleep(1)
    #errorCode += setVariaControls(COMPort,0,8000,7900,superKBitCluster,variaBitCluster)
    #time.sleep(5)
    logging.error( 'End superKSafeStates ---------------------------'
    
    if (errorCode==0):
        logging.info( 'Set Safe States OK.')
    else:
        logging.error( 'Error Setting Safe States. ErrorCode: {}'.format( errorCode ) )
    return errorCode 
