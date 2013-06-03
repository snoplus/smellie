SMELLIE Specifications for the SNO+ DAQ
=======

* Some file and function names are a work in progress (as indicated at the end of this README)  
* Please update this README when altering or adding to the code  

-------------------------


Contains json files which are SMELLIE Specifications for the SNO+ DAQ:  

* smellie_config.json 
This contains all parameters describing the hardware configuration of SMELLIE. They should only be configurable by an expert user who has reinstalled or reconfigured a hardware part of SMELLIE. These parameters may need to be changed during the installation of SMELLIE and possibly once or twice during the lifetime of the SNO+ detector.   
ORCA tells the SMELLIE DAQ computer which version of this file to use.
This file is read directly by the SMELLIE DAQ computer over the network from the database. 
Analysis users do not need to read this configuration file. 
Please note that the current values in this file are dummy values and will need to change in the near future. 

* SMELLIE_CALIBRATION_TABLE.json   
This table describes the relationship between the intensity setting for any given SMELLIE laser and the number of photons detected in the SNO+ detector. This relationship is a function of the fibres via which the light is delivered to the SNO+ detector and the route through the SMELLIE internal fibre switches. SMELLIE monitors the intensity of each laser shot using a dedicated monitoring PMT. This PMT is read by the CAEN ADC. 

	Therefore a single entry within the SMELLIE calibration table consists of the following data:
	<ul> Number of photons detected</ul> 
	<ul> Voltage of the monitoring PMT read by the CAEN ADC</ul>
	<ul> User defined intensity of the laser </ul>
	<ul> Laser ID </ul>
	<ul> Detector Fibre ID </ul>
Each entry is therefore 16 bytes long. Assuming that we take 10 intensity measurements per fibre-laser combination, there will be 840 entries within the entire SMELLIE calibration table, resulting in a total size of 13440 bytes for each SMELLIE calibration table.

* SMELLIE_very_short.json
This contains the parameters for a SMELLIE run and its sub-runs. This file controls all actions of the SMELLIE hardware. It is read by ORCA and its contents are translated into communications with the SMELLIE DAQ computer. Each event during a SMELLIE run needs to be associated with a SMELLIE run type.

	The file needs to be read by an analysis person looking at SMELLIE. Every time a new user defined run type is created, this run is added to the SMELLIE_very_short.json file. 

	For the ORCA GUI, there should be three run types:
	<ul> Default Run – This runs SMELLIE in default settings (which are pre-determined entries into this json file). The default run operates SMELLIE within the purpose of performing the scattering calibration of SNO+. This is the most common run type, which will happen on a weekly basis.</ul>  
	<ul> User Defined Run – This provides the user with options within the ORCA GUI, to change some of the run parameters of SMELLIE.The configurable parameters are: the laser,the detector fibre(s),the number of pulses per fibre and the number of photons per pulse.This is a run used to debug problems within the detector or analyse other interesting effects. </ul>
	<ul> Calibration Table Build Run – This run is a pre-defined SMELLIE run that collects the data necessary to build a new SMELLIE calibration table. This table is used to determine how many photons have been sent into the SNO+ detector for a given laser, intensity setting and detector fibre. Ideally, this run is performed a few times per year or more frequently if the SMELLIE hardware is seen to be variable. This variability is currently unknown.</ul>  
