#!/usr/bin/env python
from ctypes import *
import logging

dll = cdll.LoadLibrary("OOUtil.dll")
libc = cdll.msvcrt

def createWrapper(runnumber):
    #uint64_t __cdecl OOUtil_Wrapper_Create(void);
    wrapper = c_uint64( dll.OOUtil_Wrapper_Create() ).value
    logging.basicConfig(filename='OOspectrometerLogRun{}.log'.format(runnumber), level=logging.INFO)
    logging.info( 'Create Wrapper: {}'.format(wrapper) )
    return wrapper

def destroyWrapper(wrapper):
    #void __cdecl OOUtil_Wrapper_Destroy(uint64_t Wrapper);
    wrapperIn = c_uint64(wrapper)
    dll.OOUtil_Wrapper_Destroy(wrapperIn)
    logging.info( 'Destroy Wrapper: {}'.format(wrapperIn.value) )

def openAllSpectrometers(wrapper):
    #void __cdecl OOUtil_Wrapper_openAllSpectrometers(uint64_t WrapperIn, int32_t *NumberOfSpectrometers);
    wrapperIn = c_uint64(wrapper)
    numberOfSpectrometers = c_int32(0)
    dll.OOUtil_Wrapper_openAllSpectrometers(wrapperIn, byref(numberOfSpectrometers) )
    logging.info( 'Open All Spectrometers: {}, number of spectrometers: {}'.format(wrapperIn.value, numberOfSpectrometers.value) )

def closeAllSpectrometers(wrapper):
    #void __cdecl OOUtil_Wrapper_closeAllSpectrometers(uint64_t WrapperIn);
    wrapperIn = c_uint64(wrapper)
    dll.OOUtil_Wrapper_closeAllSpectrometers(wrapperIn)
    logging.info( 'Close All Spectrometers: {}'.format(wrapperIn.value) )

def getFirmwareVersion(wrapper):
    #void __cdecl OOUtil_Wrapper_getFirmwareVersion(uint64_t Wrapper, int32_t Index, char Firmware[], int32_t len);
    wrapperIn = c_uint64(wrapper)
    index = c_int32(0)
    messageBuff = int(30)
    message = (c_char_p*messageBuff)()
    dll.OOUtil_Wrapper_getFirmwareVersion(wrapperIn, index, byref(message), c_int32(messageBuff) )
    message = str(cast(message,c_char_p).value)
    logging.info( 'get Firmware Version: {}'.format(message) )
    return message 

def getName(wrapper):
    #void __cdecl OOUtil_Wrapper_getName(int32_t Index, uint64_t Wrapper, char SpectrometerName[], int32_t len);
    wrapperIn = c_uint64(wrapper)
    index = c_int32(0)
    messageBuff = int(20)
    message = (c_char_p*messageBuff)()
    dll.OOUtil_Wrapper_getName(index, wrapperIn, byref(message), c_int32(messageBuff) )
    message = str(cast(message,c_char_p).value)
    logging.info( 'Spectrometer Name: {}'.format(message) )
    return message

def getSerialNumber(wrapper):
    #void __cdecl OOUtil_Wrapper_getSerialNumber(uint64_t Wrapper, int32_t Index, char SerialNumber[], int32_t len);
    wrapperIn = c_uint64(wrapper)
    index = c_int32(0)
    messageBuff = int(30)
    message = (c_char_p*messageBuff)()
    dll.OOUtil_Wrapper_getSerialNumber( wrapperIn, index, byref(message), c_int32(messageBuff) )
    message = str(cast(message,c_char_p).value)
    logging.info( 'Serial Number: {}'.format(message) )
    return message 

def getIntegrationTime(wrapper):
    #int32_t __cdecl OOUtil_Wrapper_getIntegrationTime(uint64_t Wrapper, int32_t Index);
    wrapperIn = c_uint64(wrapper)
    index = c_int32(0)
    retValue = c_int32( dll.OOUtil_Wrapper_getIntegrationTime(wrapperIn, index) ).value
    logging.info( 'Get Integration Time: {}'.format(retValue) )
    return retValue

def setIntegrationTime(wrapper,value):
    #void __cdecl OOUtil_Wrapper_setIntegrationTime(uint64_t WrapperIn, int32_t Index, int32_t IntegrationTime);
    wrapperIn = c_uint64(wrapper)
    index = c_int32(0)
    integrationTime = c_int32(value)
    minIntegrationTime = getMinimumIntegrationTime(wrapper)
    maxIntegrationTime = getMaximumIntegrationTime(wrapper)
    
    if (value>=minIntegrationTime or value<=maxIntegrationTime):
        dll.OOUtil_Wrapper_setIntegrationTime(wrapperIn, index, integrationTime)
        #int32_t __cdecl OOUtil_Wrapper_getIntegrationTime(uint64_t Wrapper, int32_t Index);
        retValue = c_int32( dll.OOUtil_Wrapper_getIntegrationTime(wrapperIn, index) ).value
        logging.info( 'Set Integration Time: {}'.format(retValue) )
        if (retValue!=integrationTime.value):
            logging.error( 'Unable to Set Integration Time. Tried: {}, Current: {}'.format(integrationTime.value,retValue) )
    else:
        logging.error( 'Unable to Set Integration Time. Tried: {}. Must be greater than {} and less than {}.'.format(integrationTime.value,minIntegrationTime,maxIntegrationTime) )

def getScansToAverage(wrapper):
    #int32_t __cdecl OOUtil_Wrapper_getScansToAverage(uint64_t Wrapper, int32_t Index);
    wrapperIn = c_uint64(wrapper)
    index = c_int32(0)
    retValue = c_int32( dll.OOUtil_Wrapper_getScansToAverage(wrapperIn, index) ).value
    logging.info( 'Get Scans to average: {}'.format(retValue) )
    return retValue

def setScansToAverage(wrapper,value):
    #void __cdecl OOUtil_Wrapper_setScansToAverage(uint64_t WrapperIn, int32_t Index, int32_t Average);
    wrapperIn = c_uint64(wrapper)
    index = c_int32(0)
    average = c_int32(value)
    dll.OOUtil_Wrapper_setScansToAverage(wrapperIn, index, average)
    
    #int32_t __cdecl OOUtil_Wrapper_getScansToAverage(uint64_t Wrapper, int32_t Index);
    retValue = c_int32( dll.OOUtil_Wrapper_getScansToAverage(wrapperIn, index) ).value
    logging.info( 'Set Scans to average: {}'.format(retValue) )
    if (retValue!=average.value):
        logging.error( 'Unable to Set Scans to Average. Tried: {}, Current: {}'.format(average.value,retValue) )

def getSpectrum(wrapper):
    #void __cdecl OOUtil_Wrapper_getSpectrum  (uint64_t Wrapper, int32_t Index, double SpectrumValues[], int32_t *Length, int32_t len);
    wrapperIn = c_uint64(wrapper)
    index = c_int32(0)
    length = int(getNumberOfPixels(wrapper))
    spectrumLength = c_int32(0)
    spectrumValues = (c_double*length)()

    integrationTime = dll.OOUtil_Wrapper_getSpectrum(wrapperIn, index, byref(spectrumValues), byref(spectrumLength), c_int32(length) )
    #print "Get Spectrum:"
    #print list(spectrumValues)
    logging.info( 'Get Spectrum, SpectrumLength: {}'.format(spectrumLength.value) )
    return list(spectrumValues)

def getWavelengths(wrapper):
    #void __cdecl OOUtil_Wrapper_getWavelengths(uint64_t Wrapper, int32_t Index, double WLValues[], int32_t *Length, int32_t len);
    wrapperIn = c_uint64(wrapper)
    index = c_int32(0)
    length = int(getNumberOfPixels(wrapper))
    wavelengthLength = c_int32(0)
    wavelengthValues = (c_double*length)()

    integrationTime = dll.OOUtil_Wrapper_getWavelengths(wrapperIn, index, byref(wavelengthValues), byref(wavelengthLength), c_int32(length) )
    #print "Get Wavelengths:"
    #print list(wavelengthValues)
    logging.info( 'Get Wavelengths, WavelengthLength: {}'.format(wavelengthLength.value) )
    return list(wavelengthValues)

def writeSpectrum(runNumber,wavelengthData,spectrumData):
    fileOut = open('OOspectrometerDataRun{}.csv'.format(runNumber), 'a')
    fileOut.write( 'Wavelength(nm),Intensity(arb)\n')
    for i,j in zip(wavelengthData,spectrumData):
        fileOut.write( '{},{}\n'.format( i,j ) )
    fileOut.closed

def getFeatureControllerIrradianceCalibrationFactor(wrapper):
    #uint64_t __cdecl OOUtil_Wrapper_getFeatureControllerIrradianceCalibrationFactor(uint64_t Wrapper, int32_t index);
    wrapperIn = c_uint64(wrapper)
    index = c_int32(0)
    retValue = c_uint64( dll.OOUtil_Wrapper_getFeatureControllerIrradianceCalibrationFactor(wrapperIn, index) ).value
    logging.info( 'Get FeatureControllerIrradianceCalibrationFactor: {}'.format(retValue) )
    return retValue

def getFeatureControllerExternalTriggerDelay(wrapper):
    #uint64_t __cdecl OOUtil_Wrapper_getFeatureControllerExternalTriggerDelay(uint64_t Wrapper, int32_t Index);
    wrapperIn = c_uint64(wrapper)
    index = c_int32(0)
    retValue = c_uint64( dll.OOUtil_Wrapper_getFeatureControllerExternalTriggerDelay(wrapperIn, index) ).value
    logging.info( 'Get FeatureControllerExternalTriggerDelay: {}'.format(retValue) )
    return retValue

def getExternalTriggerMode(wrapper):
    #int32_t __cdecl OOUtil_Wrapper_getExternalTriggerMode(uint64_t Wrapper, int32_t Index);
    wrapperIn = c_uint64(wrapper)
    index = c_int32(0)
    retValue = c_int32( dll.OOUtil_Wrapper_getExternalTriggerMode(wrapperIn, index) ).value
    logging.info( 'Get External Trigger Mode: {}'.format(retValue) )
    return retValue

def setExternalTriggerMode(wrapper,value):
    #void __cdecl OOUtil_Wrapper_setExternalTriggerMode(uint64_t WrapperIn, int32_t Index, int32_t TriggerMode);
    wrapperIn = c_uint64(wrapper)
    index = c_int32(0)
    triggerMode = c_int32(value)
    dll.OOUtil_Wrapper_setExternalTriggerMode(wrapperIn, index, triggerMode)

    #int32_t __cdecl OOUtil_Wrapper_getExternalTriggerMode(uint64_t Wrapper, int32_t Index);
    retValue = c_int32( dll.OOUtil_Wrapper_getExternalTriggerMode(wrapperIn, index) ).value
    logging.info( 'Set External Trigger Mode: {}'.format(retValue) )
    if (retValue!=triggerMode.value):
        logging.error( 'Unable to Set External Trigger Mode. Tried: {}, Current: {}'.format(triggerMode.value,retValue) )

def setCorrectForElectricalDark(wrapper,value):
    #void __cdecl OOUtil_Wrapper_setCorrectForElectricalDark(uint64_t WrapperIn, int32_t Index, int32_t OnOff);
    wrapperIn = c_uint64(wrapper)
    index = c_int32(0)
    flag = c_int32(value)
    if (flag.value==0 or flag.value==1):
        dll.OOUtil_Wrapper_setCorrectForElectricalDark(wrapperIn, index, flag)
        logging.info( 'Set Correct For Electrical Dark: {}'.format(flag.value) )
    else:
        logging.error( 'Unable to Set Correct For Electrical Dark. Tried: {}. Note: must be 0 or 1.'.format(flag.value) )

def setCorrectForDetectorNonlinearity(wrapper,value):
    #void __cdecl OOUtil_Wrapper_setCorrectForDetectorNonlinearity(uint64_t WrapperIn, int32_t Index, int32_t OnOff);
    wrapperIn = c_uint64(wrapper)
    index = c_int32(0)
    flag = c_int32(value)
    if (flag.value==0 or flag.value==1):
        dll.OOUtil_Wrapper_setCorrectForDetectorNonlinearity(wrapperIn, index, flag)
        logging.info( 'Set Correct For Detector Nonlinearity: {}'.format(flag.value) )
    else:
        logging.error( 'Unable to Set Correct For Detector Nonlinearity. Tried: {}. Note: must be 0 or 1.'.format(flag.value) )

def getBoxcarWidth(wrapper):
    #int32_t __cdecl OOUtil_Wrapper_getBoxcarWidth(uint64_t Wrapper, int32_t Index);
    wrapperIn = c_uint64(wrapper)
    index = c_int32(0)
    boxcarWidth = c_int32( dll.OOUtil_Wrapper_getBoxcarWidth(wrapperIn, index) ).value
    logging.info( 'Get Boxcar Width: {}'.format(boxcarWidth) )
    return retValue

def setBoxcarWidth(wrapper,value):
    #void __cdecl OOUtil_Wrapper_setBoxcarWidth(uint64_t WrapperIn, int32_t Index, int32_t BoxcarWidth);
    wrapperIn = c_uint64(wrapper)
    index = c_int32(0)
    boxcarWidth = c_int32(value)
    dll.OOUtil_Wrapper_setBoxcarWidth(wrapperIn, index, boxcarWidth)

    #int32_t __cdecl OOUtil_Wrapper_getBoxcarWidth(uint64_t Wrapper, int32_t Index);
    retValue = c_int32( dll.OOUtil_Wrapper_getBoxcarWidth(wrapperIn, index) ).value
    logging.info( 'Set Boxcar Width: {}'.format(retValue) )
    if (retValue!=boxcarWidth.value):
        logging.error( 'Unable to Set Boxcar Width. Tried: {}, Current: {}'.format(boxcarWidth.value,retValue) )

def getMaximumIntensity(wrapper):
    #int32_t __cdecl OOUtil_Wrapper_getMaximumIntensity(uint64_t Wrapper, int32_t Index);
    wrapperIn = c_uint64(wrapper)
    index = c_int32(0)
    retValue = c_int32( dll.OOUtil_Wrapper_getMaximumIntensity(wrapperIn, index) ).value
    logging.info( 'Get Maximum Intensity: {}'.format(retValue) )
    return retValue

def getMaximumIntegrationTime(wrapper):
    #int32_t __cdecl OOUtil_Wrapper_getMaximumIntegrationTime(uint64_t Wrapper, int32_t Index);
    wrapperIn = c_uint64(wrapper)
    index = c_int32(0)
    retValue = c_int32( dll.OOUtil_Wrapper_getMaximumIntegrationTime(wrapperIn, index) ).value
    logging.info( 'Get Maximum Integration Time: {}'.format(retValue) )
    return retValue

def getMinimumIntegrationTime(wrapper):
    #int32_t __cdecl OOUtil_Wrapper_getMinimumIntegrationTime(uint64_t Wrapper, int32_t Index);
    wrapperIn = c_uint64(wrapper)
    index = c_int32(0)
    retValue = c_int32( dll.OOUtil_Wrapper_getMinimumIntegrationTime(wrapperIn, index) ).value
    logging.info( 'Get Minimum Integration Time: {}'.format(retValue) )
    return retValue

def getNumberOfDarkPixels(wrapper):
    #int32_t __cdecl OOUtil_Wrapper_getNumberOfDarkPixels(uint64_t Wrapper, int32_t Index);
    wrapperIn = c_uint64(wrapper)
    index = c_int32(0)
    retValue = c_int32( dll.OOUtil_Wrapper_getNumberOfDarkPixels(wrapperIn, index) ).value
    logging.info( 'Get Number Of Dark Pixels: {}'.format(retValue) )
    return retValue

def getNumberOfPixels(wrapper):
    #int32_t __cdecl OOUtil_Wrapper_getNumberOfPixels(uint64_t Wrapper, int32_t Index);
    wrapperIn = c_uint64(wrapper)
    index = c_int32(0)
    retValue = c_int32( dll.OOUtil_Wrapper_getNumberOfPixels(wrapperIn, index) ).value
    logging.info( 'Get Number Of Pixels: {}'.format(retValue) )
    return retValue

def isSaturated(wrapper):
    #uint8_t __cdecl OOUtil_Wrapper_isSaturated(uint64_t Wrapper, int32_t Index);
    wrapperIn = c_uint64(wrapper)
    index = c_int32(0)
    retValue = c_uint8( dll.OOUtil_Wrapper_isSaturated(wrapperIn, index) ).value
    logging.info( 'is Saturated?: {}'.format(retValue) )
    return retValue

def getLastException(wrapper):
    #void __cdecl OOUtil_Wrapper_getLastException(uint64_t Wrapper, char LastException[], int32_t len);
    wrapperIn = c_uint64(wrapper)
    messageBuff = int(300)
    message = (c_char_p*messageBuff)()
    dll.OOUtil_Wrapper_getLastException(wrapperIn, byref(message), c_int32(messageBuff) )
    message = str(cast(message,c_char_p).value)
    logging.info( 'Get Last Exception: {}'.format(message) )
    return message

def destroyExternalTriggerDelay():
    #void __cdecl OOUtil_ExternalTriggerDelay_Destroy(void);
    dll.OOUtil_ExternalTriggerDelay_Destroy()
    logging.info( 'Destroy external Trigger Delay.' )

def getExternalTriggerDelayMaximum(externalTriggerDelay):
    #int32_t __cdecl OOUtil_ExternalTriggerDelay_getExternalTriggerDelayMaximum(uint64_t ExternalTriggerDelay);
    externalTriggerDelayIn = c_uint64(externalTriggerDelay)
    retValue = c_int32( dll.OOUtil_ExternalTriggerDelay_getExternalTriggerDelayMaximum(externalTriggerDelayIn) ).value
    logging.info( 'Get External Trigger Delay Maximum: {}'.format(retValue) )
    return retValue

def getExternalTriggerDelayMinimum(externalTriggerDelay):
    #int32_t __cdecl OOUtil_ExternalTriggerDelay_getExternalTriggerDelayMinimum(uint32_t ExternalTriggerDelay);
    externalTriggerDelayIn = c_uint64(externalTriggerDelay)
    retValue = c_int32( dll.OOUtil_ExternalTriggerDelay_getExternalTriggerDelayMinimum(externalTriggerDelayIn) ).value
    logging.info( 'Get External Trigger Delay Minimum: {}'.format(retValue) )
    return retValue

def setExternalTriggerDelay(externalTriggerDelay,value):
    #void __cdecl OOUtil_ExternalTriggerDelay_setExternalTriggerDelay(uint64_t ExternalTriggerDelayIn, int32_t microseconds);
    externalTriggerDelayIn = c_uint64(externalTriggerDelay)
    delayTime = c_int32(value)
    minTime = getExternalTriggerDelayMinimum(externalTriggerDelay)
    maxTime = getExternalTriggerDelayMaximum(externalTriggerDelay)
    if (value>=minTime or value<=maxTime):
        dll.OOUtil_ExternalTriggerDelay_setExternalTriggerDelay(externalTriggerDelayIn, delayTime)
        logging.info( 'Set External Trigger Delay: {}'.format(delayTime.value) )
    else:
        logging.error( 'Unable to Set External Trigger Delay. Tried: {}. Must be greater than {} and less than {}.'.format(delayTime.value,minTime,maxTime) )

def initialise(runNumber):
    wrapper = createWrapper(runNumber)
    openAllSpectrometers(wrapper)
    getName(wrapper)
    getFirmwareVersion(wrapper)
    getSerialNumber(wrapper)
    
    #set acquisition parameters
    setExternalTriggerMode(wrapper,0)
    setBoxcarWidth(wrapper, 0)
    setCorrectForDetectorNonlinearity(wrapper,1)
    setCorrectForElectricalDark(wrapper,1)
    setIntegrationTime(wrapper,10000)
    setScansToAverage(wrapper,1)
    
    #set external trigger delay
    extTrigDelay = getFeatureControllerExternalTriggerDelay(wrapper)
    setExternalTriggerDelay(extTrigDelay,1000)
    return wrapper

def shutdown(wrapper):
    destroyExternalTriggerDelay()
    closeAllSpectrometers(wrapper)    
    destroyWrapper(wrapper)
