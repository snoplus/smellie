import pysepiaUser as p
import laserSwitch as rs

#iDevIdx,iModuleType,iSlotID = p.initialise()
#p.set_laser_intensity(int("10"), iDevIdx)
#p.close(iDevIdx)
iDevIdx,iModuleType,iSlotID = p.initialise()
rs.SetSelectedChannel(3)
p.close(iDevIdx)
rs.Execute() 
