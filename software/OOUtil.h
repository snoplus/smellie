#include "extcode.h"
#ifdef __cplusplus
extern "C" {
#endif

/*!
 * OOUtil_AnalogIn_Create
 */
uint64_t __cdecl OOUtil_AnalogIn_Create(void);
/*!
 * OOUtil_AnalogIn_Destroy
 */
void __cdecl OOUtil_AnalogIn_Destroy(uint64_t AnalogIn);
/*!
 * OOUtil_AnalogIn_getVoltageIn
 */
double __cdecl OOUtil_AnalogIn_getVoltageIn(uint64_t AnalogIn);
/*!
 * OOUtil_AnalogOut_analogoutCountsToVolts
 */
double __cdecl OOUtil_AnalogOut_analogoutCountsToVolts(uint64_t AnalogOut, 
	int32_t counts);
/*!
 * OOUtil_AnalogOut_Create
 */
void __cdecl OOUtil_AnalogOut_Create(void);
/*!
 * OOUtil_AnalogOut_Destroy
 */
void __cdecl OOUtil_AnalogOut_Destroy(uint64_t AnalogOut);
/*!
 * OOUtil_AnalogOut_getDACIncrement
 */
int32_t __cdecl OOUtil_AnalogOut_getDACIncrement(uint64_t AnalogOut);
/*!
 * OOUtil_AnalogOut_getDACMaximum
 */
int32_t __cdecl OOUtil_AnalogOut_getDACMaximum(uint64_t AnalogOut);
/*!
 * OOUtil_AnalogOut_getDACMinimum
 */
int32_t __cdecl OOUtil_AnalogOut_getDACMinimum(uint64_t AnalogOut);
/*!
 * OOUtil_AnalogOut_getDACPins
 */
int32_t __cdecl OOUtil_AnalogOut_getDACPins(uint64_t AnalogOut);
/*!
 * OOUtil_AnalogOut_isDACPresent
 */
uint8_t __cdecl OOUtil_AnalogOut_isDACPresent(uint64_t AnalogOut);
/*!
 * OOUtil_AnalogOut_setDACCounts
 */
uint64_t __cdecl OOUtil_AnalogOut_setDACCounts(uint64_t AnalogOutIn, 
	int32_t Counts, int32_t Index);
/*!
 * OOUtil_BoardTemperature_Create
 */
uint64_t __cdecl OOUtil_BoardTemperature_Create(void);
/*!
 * OOUtil_BoardTemperature_Destroy
 */
void __cdecl OOUtil_BoardTemperature_Destroy(uint64_t BoardTemperature);
/*!
 * OOUtil_BoardTemperature_getBoardTemperatureCelsius
 */
double __cdecl OOUtil_BoardTemperature_getBoardTemperatureCelsius(
	uint32_t BoardTemperature);
/*!
 * OOUtil_ContinuousStrobe_continuousStrobeCountsToMicros
 */
double __cdecl OOUtil_ContinuousStrobe_continuousStrobeCountsToMicros(
	uint64_t ContinuousStrobe, int32_t counts);
/*!
 * OOUtil_ContinuousStrobe_Create
 */
uint64_t __cdecl OOUtil_ContinuousStrobe_Create(void);
/*!
 * OOUtil_ContinuousStrobe_Destroy
 */
void __cdecl OOUtil_ContinuousStrobe_Destroy(uint64_t ContinuousStrobe);
/*!
 * OOUtil_ContinuousStrobe_getContinuousStrobeDelayIncrement
 */
int32_t __cdecl OOUtil_ContinuousStrobe_getContinuousStrobeDelayIncrement(
	uint64_t ContinuousStrobe);
/*!
 * OOUtil_ContinuousStrobe_getContinuousStrobeDelayMaximum
 */
int32_t __cdecl OOUtil_ContinuousStrobe_getContinuousStrobeDelayMaximum(
	uint64_t ContinuousStrobe);
/*!
 * OOUtil_ContinuousStrobe_getContinuousStrobeDelayMinimum
 */
int32_t __cdecl OOUtil_ContinuousStrobe_getContinuousStrobeDelayMinimum(
	uint32_t ContinuousStrobe);
/*!
 * OOUtil_ContinuousStrobe_setContinuousStrobeDelay
 */
void __cdecl OOUtil_ContinuousStrobe_setContinuousStrobeDelay(
	uint64_t ContinuousStrobeIn, int32_t delay);
/*!
 * OOUtil_ExternalTriggerDelay_Create
 */
uint64_t __cdecl OOUtil_ExternalTriggerDelay_Create(void);
/*!
 * OOUtil_ExternalTriggerDelay_Destroy
 */
void __cdecl OOUtil_ExternalTriggerDelay_Destroy(void);
/*!
 * OOUtil_ExternalTriggerDelay_getExternalTriggerDelayIncrement
 */
int32_t __cdecl OOUtil_ExternalTriggerDelay_getExternalTriggerDelayIncrement(
	uint64_t ExternalTriggerDelay);
/*!
 * OOUtil_ExternalTriggerDelay_getExternalTriggerDelayMaximum
 */
int32_t __cdecl OOUtil_ExternalTriggerDelay_getExternalTriggerDelayMaximum(
	uint64_t ExternalTriggerDelay);
/*!
 * OOUtil_ExternalTriggerDelay_getExternalTriggerDelayMinimum
 */
int32_t __cdecl OOUtil_ExternalTriggerDelay_getExternalTriggerDelayMinimum(
	uint32_t ExternalTriggerDelay);
/*!
 * OOUtil_ExternalTriggerDelay_setExternalTriggerDelay
 */
void __cdecl OOUtil_ExternalTriggerDelay_setExternalTriggerDelay(
	uint64_t ExternalTriggerDelayIn, int32_t microseconds);
/*!
 * OOUtil_ExternalTriggerDelay_triggerDelayCountsToMicroseconds
 */
double __cdecl OOUtil_ExternalTriggerDelay_triggerDelayCountsToMicroseconds(
	uint64_t ExternalTriggerDelay, int32_t Counts);
/*!
 * OOUtil_SingleStrobe_Create
 */
uint64_t __cdecl OOUtil_SingleStrobe_Create(void);
/*!
 * OOUtil_SingleStrobe_Destroy
 */
void __cdecl OOUtil_SingleStrobe_Destroy(uint64_t SingleStrobe);
/*!
 * OOUtil_SingleStrobe_getSingleStrobeCountsToMicros
 */
double __cdecl OOUtil_SingleStrobe_getSingleStrobeCountsToMicros(
	uint64_t SingleStrobe, int32_t counts);
/*!
 * OOUtil_SingleStrobe_getSingleStrobeHigh
 */
int32_t __cdecl OOUtil_SingleStrobe_getSingleStrobeHigh(
	uint64_t SingleStrobe);
/*!
 * OOUtil_SingleStrobe_getSingleStrobeIncrement
 */
int32_t __cdecl OOUtil_SingleStrobe_getSingleStrobeIncrement(
	uint64_t SingleStrobe);
/*!
 * OOUtil_SingleStrobe_getSingleStrobeLow
 */
int32_t __cdecl OOUtil_SingleStrobe_getSingleStrobeLow(uint64_t SingleStrobe);
/*!
 * OOUtil_SingleStrobe_getSingleStrobeMaximum
 */
int32_t __cdecl OOUtil_SingleStrobe_getSingleStrobeMaximum(
	uint64_t SingleStrobe);
/*!
 * OOUtil_SingleStrobe_getSingleStrobeMinimum
 */
int32_t __cdecl OOUtil_SingleStrobe_getSingleStrobeMinimum(
	uint64_t SingleStrobe);
/*!
 * OOUtil_SingleStrobe_setSingleStrobeHigh
 */
void __cdecl OOUtil_SingleStrobe_setSingleStrobeHigh(uint64_t SingleStrobeIn, 
	int32_t SingleStrobeHigh);
/*!
 * OOUtil_SingleStrobe_setSingleStrobeLow
 */
void __cdecl OOUtil_SingleStrobe_setSingleStrobeLow(uint64_t SingleStrobeIn, 
	int32_t SingleStrobeLow);
/*!
 * OOUtil_Wrapper_closeAllSpectrometers
 */
void __cdecl OOUtil_Wrapper_closeAllSpectrometers(uint64_t WrapperIn);
/*!
 * OOUtil_Wrapper_Create
 */
uint64_t __cdecl OOUtil_Wrapper_Create(void);
/*!
 * OOUtil_Wrapper_Destroy
 */
void __cdecl OOUtil_Wrapper_Destroy(uint64_t Wrapper);
/*!
 * OOUtil_Wrapper_exportToGramsSPC
 */
void __cdecl OOUtil_Wrapper_exportToGramsSPC(uint64_t Wrapper, int32_t Index, 
	char OutputPathName[], double double_array[], char UserName[], 
	uint64_t *Wrapper2, uint8_t *returnType, int32_t len);
/*!
 * OOUtil_Wrapper_getApiVersion
 */
void __cdecl OOUtil_Wrapper_getApiVersion(uint64_t Wrapper, 
	char APIVersion[], int32_t len);
/*!
 * OOUtil_Wrapper_getBench
 */
uint64_t __cdecl OOUtil_Wrapper_getBench(uint64_t Wrapper, int32_t Index);
/*!
 * OOUtil_Wrapper_getBoxcarWidth
 */
int32_t __cdecl OOUtil_Wrapper_getBoxcarWidth(uint64_t Wrapper, 
	int32_t Index);
/*!
 * OOUtil_Wrapper_getBuildNumber
 */
int32_t __cdecl OOUtil_Wrapper_getBuildNumber(uint64_t Wrapper);
/*!
 * OOUtil_Wrapper_getExternalTriggerMode
 */
int32_t __cdecl OOUtil_Wrapper_getExternalTriggerMode(uint64_t Wrapper, 
	int32_t Index);
/*!
 * OOUtil_Wrapper_getFeatureControllerAnalogIn
 */
uint64_t __cdecl OOUtil_Wrapper_getFeatureControllerAnalogIn(
	uint64_t Wrapper, int32_t Index);
/*!
 * OOUtil_Wrapper_getFeatureControllerAnalogOut
 */
uint64_t __cdecl OOUtil_Wrapper_getFeatureControllerAnalogOut(
	uint64_t Wrapper, int32_t Index);
/*!
 * OOUtil_Wrapper_getFeatureControllerBoardTemperature
 */
uint64_t __cdecl OOUtil_Wrapper_getFeatureControllerBoardTemperature(
	uint64_t Wrapper, int32_t index);
/*!
 * OOUtil_Wrapper_getFeatureControllerContinuousStrobe
 */
uint64_t __cdecl OOUtil_Wrapper_getFeatureControllerContinuousStrobe(
	uint64_t Wrapper, int32_t Index);
/*!
 * OOUtil_Wrapper_getFeatureControllerExternalTriggerDelay
 */
uint64_t __cdecl OOUtil_Wrapper_getFeatureControllerExternalTriggerDelay(
	uint64_t Wrapper, int32_t Index);
/*!
 * OOUtil_Wrapper_getFeatureControllerGPIO
 */
uint64_t __cdecl OOUtil_Wrapper_getFeatureControllerGPIO(uint64_t Wrapper, 
	int32_t Index);
/*!
 * OOUtil_Wrapper_getFeatureControllerIrradianceCalibrationFactor
 */
uint64_t __cdecl OOUtil_Wrapper_getFeatureControllerIrradianceCalibrationFactor(
	uint64_t Wrapper, int32_t index);
/*!
 * OOUtil_Wrapper_getFeatureControllerLS450
 */
uint64_t __cdecl OOUtil_Wrapper_getFeatureControllerLS450(uint64_t Wrapper, 
	int32_t SpectrometerIndex);
/*!
 * OOUtil_Wrapper_getFeatureControllerNonlinearityCorrectionProvider
 */
uint64_t __cdecl OOUtil_Wrapper_getFeatureControllerNonlinearityCorrectionProvider(
	uint64_t Wrapper, int32_t index);
/*!
 * OOUtil_Wrapper_getFeatureControllerSingleStrobe
 */
uint64_t __cdecl OOUtil_Wrapper_getFeatureControllerSingleStrobe(
	uint64_t Wrapper, int32_t index);
/*!
 * OOUtil_Wrapper_getFeatureControllerSPIBus
 */
uint64_t __cdecl OOUtil_Wrapper_getFeatureControllerSPIBus(uint64_t Wrapper, 
	int32_t index);
/*!
 * OOUtil_Wrapper_getFeatureControllerStrayLightCorrection
 */
uint64_t __cdecl OOUtil_Wrapper_getFeatureControllerStrayLightCorrection(
	uint64_t Wrapper, int32_t index);
/*!
 * OOUtil_Wrapper_getFeatureControllerThermoElectric
 */
uint64_t __cdecl OOUtil_Wrapper_getFeatureControllerThermoElectric(
	uint64_t Wrapper, int32_t Index);
/*!
 * OOUtil_Wrapper_getFeatureControllerVersion
 */
uint64_t __cdecl OOUtil_Wrapper_getFeatureControllerVersion(uint64_t Wrapper, 
	int32_t index);
/*!
 * OOUtil_Wrapper_getFeatureControllerWavelengthCalibraionProvider
 */
uint64_t __cdecl OOUtil_Wrapper_getFeatureControllerWavelengthCalibraionProvider(
	uint64_t Wrapper, int32_t index);
/*!
 * OOUtil_Wrapper_getFirmwareVersion
 */
void __cdecl OOUtil_Wrapper_getFirmwareVersion(uint64_t Wrapper, 
	int32_t Index, char Firmware[], int32_t len);
/*!
 * OOUtil_Wrapper_getIntegrationTime
 */
int32_t __cdecl OOUtil_Wrapper_getIntegrationTime(uint64_t Wrapper, 
	int32_t Index);
/*!
 * OOUtil_Wrapper_getLastException
 */
void __cdecl OOUtil_Wrapper_getLastException(uint64_t Wrapper, 
	char LastException[], int32_t len);
/*!
 * OOUtil_Wrapper_getLastExceptionStackTrace
 */
void __cdecl OOUtil_Wrapper_getLastExceptionStackTrace(uint64_t Wrapper, 
	char LastExceptionStackTrace[], int32_t len);
/*!
 * OOUtil_Wrapper_getMaximumIntegrationTime
 */
int32_t __cdecl OOUtil_Wrapper_getMaximumIntegrationTime(uint64_t Wrapper, 
	int32_t Index);
/*!
 * OOUtil_Wrapper_getMaximumIntensity
 */
int32_t __cdecl OOUtil_Wrapper_getMaximumIntensity(uint64_t Wrapper, 
	int32_t Index);
/*!
 * OOUtil_Wrapper_getMinimumIntegrationTime
 */
int32_t __cdecl OOUtil_Wrapper_getMinimumIntegrationTime(uint64_t Wrapper, 
	int32_t Index);
/*!
 * OOUtil_Wrapper_getName
 */
void __cdecl OOUtil_Wrapper_getName(int32_t Index, uint64_t Wrapper, 
	char SpectrometerName[], int32_t len);
/*!
 * OOUtil_Wrapper_getNumberOfDarkPixels
 */
int32_t __cdecl OOUtil_Wrapper_getNumberOfDarkPixels(uint64_t Wrapper, 
	int32_t Index);
/*!
 * OOUtil_Wrapper_getNumberOfPixels
 */
int32_t __cdecl OOUtil_Wrapper_getNumberOfPixels(uint64_t Wrapper, 
	int32_t Index);
/*!
 * OOUtil_Wrapper_getNumberOfSpectrometersFound
 */
void __cdecl OOUtil_Wrapper_getNumberOfSpectrometersFound(uint64_t WrapperIn, 
	uint64_t *WrapperOut, int32_t *NumberOfSpectrometers);
/*!
 * OOUtil_Wrapper_getScansToAverage
 */
int32_t __cdecl OOUtil_Wrapper_getScansToAverage(uint64_t Wrapper, 
	int32_t Index);
/*!
 * OOUtil_Wrapper_getSerialNumber
 */
void __cdecl OOUtil_Wrapper_getSerialNumber(uint64_t Wrapper, int32_t Index, 
	char SerialNumber[], int32_t len);
/*!
 * OOUtil_Wrapper_getSpectrum
 */
void __cdecl OOUtil_Wrapper_getSpectrum(uint64_t Wrapper, int32_t Index, 
	double SpectrumValues[], int32_t *Length, int32_t len);
/*!
 * OOUtil_Wrapper_getStrobeEnable
 */
int32_t __cdecl OOUtil_Wrapper_getStrobeEnable(uint64_t Wrapper, 
	int32_t Index);
/*!
 * OOUtil_Wrapper_getWavelength
 */
double __cdecl OOUtil_Wrapper_getWavelength(uint64_t Wrapper, 
	int32_t SpectrometerIndex, int32_t Pixel);
/*!
 * OOUtil_Wrapper_getWavelengths
 */
void __cdecl OOUtil_Wrapper_getWavelengths(uint64_t Wrapper, int32_t Index, 
	double WLValues[], int32_t *Length, int32_t len);
/*!
 * OOUtil_Wrapper_highSpdAcq_AllocateBuffer
 */
void __cdecl OOUtil_Wrapper_highSpdAcq_AllocateBuffer(uint64_t WrapperIN, 
	uint32_t SpectrometerIndex, int32_t numberOfSpectra);
/*!
 * OOUtil_Wrapper_highSpdAcq_GetNumberOfSpectraAcquired
 */
int32_t __cdecl OOUtil_Wrapper_highSpdAcq_GetNumberOfSpectraAcquired(
	uint64_t Wrapper);
/*!
 * OOUtil_Wrapper_highSpdAcq_GetSpectrum
 */
void __cdecl OOUtil_Wrapper_highSpdAcq_GetSpectrum(uint64_t Wrapper, 
	int32_t SpectrumNumber, double SpectrumValues[], int32_t *Length, 
	int32_t len);
/*!
 * OOUtil_Wrapper_highSpdAcq_GetTimeStamp
 */
uint64_t __cdecl OOUtil_Wrapper_highSpdAcq_GetTimeStamp(uint64_t Wrapper, 
	int32_t SpectrumNumber);
/*!
 * OOUtil_Wrapper_highSpdAcq_StartAquisition
 */
void __cdecl OOUtil_Wrapper_highSpdAcq_StartAquisition(uint64_t WrapperIn, 
	int32_t SpectrometerIndex);
/*!
 * OOUtil_Wrapper_hightSpdAcq_IsSaturated
 */
uint8_t __cdecl OOUtil_Wrapper_hightSpdAcq_IsSaturated(uint64_t Wrapper, 
	int32_t SpectrumNumber);
/*!
 * OOUtil_Wrapper_hightSpdAcq_StopAcquisition
 */
void __cdecl OOUtil_Wrapper_hightSpdAcq_StopAcquisition(uint64_t WrapperIn);
/*!
 * OOUtil_Wrapper_insertKey
 */
uint8_t __cdecl OOUtil_Wrapper_insertKey(uint64_t Wrapper, char String[]);
/*!
 * OOUtil_Wrapper_isFeatureSupportedLS450
 */
uint8_t __cdecl OOUtil_Wrapper_isFeatureSupportedLS450(uint64_t Wrapper, 
	int32_t SpectrometerIndex);
/*!
 * OOUtil_Wrapper_isSaturated
 */
uint8_t __cdecl OOUtil_Wrapper_isSaturated(uint64_t Wrapper, int32_t Index);
/*!
 * OOUtil_Wrapper_openAllSpectrometers
 */
void __cdecl OOUtil_Wrapper_openAllSpectrometers(uint64_t WrapperIn, 
	int32_t *NumberOfSpectrometers);
/*!
 * OOUtil_Wrapper_openNetworkSpectrometer
 */
void __cdecl OOUtil_Wrapper_openNetworkSpectrometer(uint64_t Wrapper, 
	char IpAddress[], uint64_t *Wrapper2, int32_t *AssignedIndex);
/*!
 * OOUtil_Wrapper_removeKey
 */
void __cdecl OOUtil_Wrapper_removeKey(uint64_t WrapperIn);
/*!
 * OOUtil_Wrapper_setAutoToggleStrobeLampEnable
 */
void __cdecl OOUtil_Wrapper_setAutoToggleStrobeLampEnable(uint64_t WrapperIn, 
	int32_t Index, uint8_t Enable);
/*!
 * OOUtil_Wrapper_setBoxcarWidth
 */
void __cdecl OOUtil_Wrapper_setBoxcarWidth(uint64_t WrapperIn, int32_t Index, 
	int32_t BoxcarWidth);
/*!
 * OOUtil_Wrapper_setCorrectForDetectorNonlinearity
 */
void __cdecl OOUtil_Wrapper_setCorrectForDetectorNonlinearity(
	uint64_t WrapperIn, int32_t Index, int32_t OnOff);
/*!
 * OOUtil_Wrapper_setCorrectForElectricalDark
 */
void __cdecl OOUtil_Wrapper_setCorrectForElectricalDark(uint64_t WrapperIn, 
	int32_t Index, int32_t OnOff);
/*!
 * OOUtil_Wrapper_setEEPromInfo
 */
void __cdecl OOUtil_Wrapper_setEEPromInfo(uint64_t WrapperIn, 
	int32_t SpectrometerIndex, int32_t Slot, char String[], uint64_t *WrapperOut, 
	uint8_t *Valid);
/*!
 * OOUtil_Wrapper_setExternalTriggerMode
 */
void __cdecl OOUtil_Wrapper_setExternalTriggerMode(uint64_t WrapperIn, 
	int32_t Index, int32_t TriggerMode);
/*!
 * OOUtil_Wrapper_setIntegrationTime
 */
void __cdecl OOUtil_Wrapper_setIntegrationTime(uint64_t WrapperIn, 
	int32_t Index, int32_t IntegrationTime);
/*!
 * OOUtil_Wrapper_setScansToAverage
 */
void __cdecl OOUtil_Wrapper_setScansToAverage(uint64_t WrapperIn, 
	int32_t Index, int32_t Average);
/*!
 * OOUtil_Wrapper_setStrobeEnable
 */
void __cdecl OOUtil_Wrapper_setStrobeEnable(uint64_t WrapperIn, 
	int32_t Index, int32_t OnOff);
/*!
 * OOUtil_Wrapper_stopAveraging
 */
void __cdecl OOUtil_Wrapper_stopAveraging(uint64_t WrapperIn, 
	int32_t SpectrometerIndex);

MgErr __cdecl LVDLLStatus(char *errStr, int errStrLen, void *module);

#ifdef __cplusplus
} // extern "C"
#endif

