import time,subprocess,os

#retValue = 0
#print subprocess.Popen("taskkill /F /T /PID 4552", shell=True)
#retValue = subprocess.call("taskill /im Sepia2.exe /f",shell=True)
#print retValue
#
import ctypes

#sepiaInfo = os.system('tasklist /FI "IMAGENAME eq Sepia2.exe" /FO CSV /NH')
#print sepiaInfo

def findnth(haystack, needle, n):
    parts= haystack.split(needle, n+1)
    if len(parts)<=n+1:
        return -1
    return len(haystack)-len(parts[-1])-len(needle)

import subprocess as sub
p = sub.Popen('tasklist /FI "IMAGENAME eq Sepia2.exe" /FO CSV /NH',stdout=sub.PIPE,stderr=sub.PIPE)
sepiaPid, errors = p.communicate()
startIndex = findnth(sepiaPid,'"',2)
endIndex = findnth(sepiaPid,'"',3)
sepiaPid = sepiaPid[startIndex+1:endIndex]
print "Sepia PID: " + sepiaPid

PROCESS_TERMINATE = 1
handle = ctypes.windll.kernel32.OpenProcess(PROCESS_TERMINATE,False,int(sepiaPid))
retValue = ctypes.windll.kernel32.TerminateProcess(handle,-1)
print retValue
