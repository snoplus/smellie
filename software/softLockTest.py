import pysepiaUser as sepiaUser
import time

iDevIdx,iModuleType,iSlotID = sepiaUser.initialiseSCMModule()
#print iDevIdx
#print sepiaUser.laser_soft_lock_off(iDevIdx, iSlotID)
#sepiaUser.close(iDevIdx)

time.sleep(1)

#iDevIdx,iModuleType,iSlotID = sepiaUser.initialise()
#print sepiaUser.get_laser_lock_status(iDevIdx, iSlotID)
sepiaUser.close(iDevIdx)
