Hardware Information
=======

* The information in this folder is for SMELLIE users to refer to while setting up and actually using the hardware  
* It also acts a repository for useful procedures and online technical data  
* More technical information will (eventually) be available in (a / the) User's Manual  

-------------------------


List of SMELLIE Hardware Components:  

* 4 laser-heads  
-- these produce (almost) monochromatic light at wavelengths of 375, 407, 446 and 495nm  

* PicoQuant SEPIA II Laser Driver Unit  
-- this powers and operates the 4 laser-heads and is software-controlled  
-- it can only do so for a single laser-head at a time (since there is only a single driver unit)  

* Laser Switch Unit  
-- this allows us to drive all 4 laser-heads (non-simultaneously) from the single Sepia Driver Unit  
-- it removes the problem of manually having to change LEMO cables in and out of the Sepia unit, since the laserSwitch is software-controlled  
-- there are 2 identical units ... one is at SNOLab as part of the SMELLIE system, and the other is at Oxford University  
-- both were designed and built at Oxford University by Mr. Rik Elliot (r.elliott2@physics.ox.ac.uk)  

* Laser Components 5x14 Fibre Switch Unit  
-- this takes light from any one of the lasers (5 [4 + 1 spare] inputs) and routes it to one of 14 (12 + 2 spare) output fibres that go directly into the detector  
-- this makes it possible to send light from any single laser to any one of the 12 allocated SMELLIE positions in the detector via computer-control  

* Monitoring PMT Unit  
-- this allows us to monitor the per-pulse laser intensity  
-- this is important to know, since it relates to a) the voltage supplied to the SNO+ CAEN ADCs for data-taking, and b) the number of photons entering the detector  
-- the PMT Unit also converts the incoming internal / ORCA trigger signal from the standard (0 to 5)V to the (-2 to +1)V that is required by the SEPIA Unit  
-- there are 2 identical units ... one is at SNOLab as part of the SMELLIE system, and the other is at Oxford University  
-- both were designed and built at Oxford University by Mr. John Saunders (j.saunders1@physics.ox.ac.uk)  

* Power Supply Unit  
-- this supplies power to the Monitoring PMT Unit  
-- there are 2 identical units (one for each Monitoring PMT Unit) ... one is at SNOLab as part of the SMELLIE system, and the other is at Oxford University  
-- both were designed and built at Oxford University by Mr. John Saunders (j.saunders1@physics.ox.ac.uk)  

* Beamsplitters  
-- the light from each laser is split into 2 parts, one of which enters the detector via the fibreSwitch, and the other is sent to the Monitoring PMT  
-- there is one beamsplitter for each laser (although the splitting ratios may be different since the laser powers are not identical)  

* National Instruments ADC Unit  
-- this performs several functions for the SMELLIE system:  
		1) it provides an internal trigger signal source for the lasers (as opposed to the external trigger that can be supplied by ORCA)  
		2) it reads out the output voltage from the Monitoring PMT Unit in order to check the per-pulse laser intensity  
-- this unit is software-controlled  
