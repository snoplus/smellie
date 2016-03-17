#!/usr/bin/env python
import sys, time, os, string,time
from ctypes import *
import orcaConnection_superK as sk
import niADC as ni 

def main():
    retValue = 0
    ValueError = 0

    COMPort = c_char_p("COM6")
    superKBitCluster = sk.statusBitStructure()
    variaBitCluster = sk.statusBitStructure()
    superKControlCluster = sk.superKControlStructure()

    if (ValueError==0): ValueError += sk.portOpen(COMPort)

    if (ValueError==0): ValueError += sk.initialise(COMPort, superKControlCluster, superKBitCluster, variaBitCluster)
    
    if (ValueError==0): ValueError += sk.superKSafeStates(COMPort, superKControlCluster, superKBitCluster, variaBitCluster)
    

    #ValueError += sk.setSuperKControlInterlock(COMPort,1,superKBitCluster)
    #time.sleep(3)
    
    #ValueError += sk.setVariaControls(COMPort,0,6200,6100,superKBitCluster,variaBitCluster)
    #time.sleep(10)
    #ValueError += sk.getVariaControls(COMPort)
    
    #ValueError += sk.setSuperKControlEmission(COMPort,1,superKBitCluster,variaBitCluster)
    #time.sleep(3)
    
    #ni.setDevName('dev2')
    #digi_trig = ni.GenerateDigitalTrigger(int(100), int(100))
    #digi_trig.start()
    #digi_trig.stop()
    
    #ValueError += sk.superKSafeStates(COMPort)
    #time.sleep(3)


    if (ValueError==0): ValueError += sk.portClose(COMPort)

    if (ValueError!=0):
        retValue = "Error: " + str(ValueError)
    return ValueError

main()
