#include "extcode.h"
#ifdef __cplusplus
extern "C" {
#endif
typedef struct {
	uint16_t trigLevelSetpointmV;
	uint8_t displayBacklightPercent;
	uint8_t trigMode;
	uint16_t internalPulseFreqHz;
	uint16_t burstPulses;
	uint8_t watchdogIntervalSec;
	uint32_t internalPulseFreqLimitHz;
} Cluster;
typedef struct {
	int16_t _0Emission;
	int16_t _1InterlockOff;
	int16_t _2InterlockPowerFailure;
	int16_t _3InterlockLoopOff;
	int16_t _4NC;
	int16_t _5SupplyVoltageLow;
	int16_t _6ModuleTempRange;
	int16_t _7PumpTempHigh;
	int16_t _8PulseOverrun;
	int16_t _9TrigSignalLevel;
	int16_t _10TrigEdge;
	int16_t _11NC;
	int16_t _12NC;
	int16_t _13NC;
	int16_t _14NC;
	int16_t _15ErrorCodePresent;
} Cluster1;
typedef struct {
	int16_t _0NC;
	int16_t _1InterlockOff;
	int16_t _2InterlockLoopIn;
	int16_t _3InterlockLoopOut;
	int16_t _4NC;
	int16_t _5SupplyVoltageLow;
	int16_t _6ModuleTempRange;
	int16_t _7NC;
	int16_t _8ShutterSensor1;
	int16_t _9ShutterSensor2;
	int16_t _10NC;
	int16_t _11NC;
	int16_t _12Filter1Moving;
	int16_t _13Filter2Moving;
	int16_t _14Filter3Moving;
	int16_t _15ErrorCodePresent;
} Cluster2;

/*!
 * PortClose
 */
int32_t __cdecl PortClose(char COMport[]);
/*!
 * GetSuperKControls
 */
int32_t __cdecl GetSuperKControls(char COMport[], Cluster *outputCluster);
/*!
 * GetSuperKInfo
 */
int32_t __cdecl GetSuperKInfo(char COMport[], char moduleSerialNumber[], 
	int32_t len, int32_t *moduleType, uint16_t *firmwareVersion, 
	char extendedVersionInfo[], int32_t len2);
/*!
 * GetSuperKReadings
 */
int32_t __cdecl GetSuperKReadings(char COMport[], 
	double *opticalPulseFreqkHz, double *actualInternalTrigFreqkHz, 
	uint8_t *powerReadoutPercent, double *heatSinkTempC, double *supplyVoltagemV, 
	uint8_t displayInfo[], int32_t len);
/*!
 * GetSuperKStatusBits
 */
int32_t __cdecl GetSuperKStatusBits(char COMport[], int32_t *bitMaskDecimal, 
	Cluster1 *statusBitCluster);
/*!
 * GetVariaControls
 */
int32_t __cdecl GetVariaControls(char COMport[], 
	uint16_t *NDFilterSetpointPercentx10, uint16_t *SWFilterSetpointAngstrom, 
	uint16_t *LPFilterSetpointAngstrom);
/*!
 * GetVariaInfo
 */
int32_t __cdecl GetVariaInfo(char COMport[], char moduleSerialNumber[], 
	int32_t len, int32_t *moduleType, uint16_t *firmwareVersion, 
	char extendedVersionInfo[], int32_t len2);
/*!
 * GetVariaReadings
 */
int32_t __cdecl GetVariaReadings(char COMport[], double *monitorInputPercent);
/*!
 * GetVariaStatusBits
 */
int32_t __cdecl GetVariaStatusBits(char COMport[], int32_t *bitMaskDecimal, 
	Cluster2 *statusBitCluster);
/*!
 * PortOpen
 */
int32_t __cdecl PortOpen(char COMport[]);
/*!
 * PortUtil
 */
int32_t __cdecl PortUtil(char COMport[], uint8_t Array[], 
	LVBoolean WriteNotRead, uint8_t Destination, uint8_t Register, int32_t *Long, 
	uint8_t PayloadByteArray[], int32_t len, int32_t len2);
/*!
 * SetSuperKControls
 */
int32_t __cdecl SetSuperKControls(char COMport[], Cluster *outputCluster);
/*!
 * SetVariaControls
 */
int32_t __cdecl SetVariaControls(char COMport[], 
	uint16_t NDFilterSetpointPercentx10, uint16_t SWFilterSetpointAngstrom, 
	uint16_t LPFilterSetpointAngstrom);
/*!
 * SetSuperKControlEmission
 */
int32_t __cdecl SetSuperKControlEmission(char COMport[], uint8_t emission);
/*!
 * SetSuperKControlInterlock
 */
int32_t __cdecl SetSuperKControlInterlock(char COMport[], uint8_t interlock);

MgErr __cdecl LVDLLStatus(char *errStr, int errStrLen, void *module);

#ifdef __cplusplus
} // extern "C"
#endif

