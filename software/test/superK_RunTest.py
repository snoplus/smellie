#!/usr/bin/env python
import sys, time, os, string,time
from ctypes import *
import orcaConnection_superK as sk
import niADC as ni 

def main():
    retValue = 0
    errorCode = 0

    COMPort = c_char_p("COM6")
    superKBitCluster = sk.statusBitStructure()
    variaBitCluster = sk.statusBitStructure()
    superKControlCluster = sk.superKControlStructure()

    if (errorCode==0): errorCode += sk.portOpen(COMPort)

    if (errorCode==0): errorCode += sk.initialise(COMPort, superKControlCluster, superKBitCluster, variaBitCluster)
    
    if (errorCode==0): errorCode += sk.superKSafeStates(COMPort, superKControlCluster, superKBitCluster, variaBitCluster)
    

    #errorCode += sk.setSuperKControlInterlock(COMPort,1,superKBitCluster)
    #time.sleep(3)
    
    #errorCode += sk.setVariaControls(COMPort,0,6200,6100,superKBitCluster,variaBitCluster)
    #time.sleep(10)
    #errorCode += sk.getVariaControls(COMPort)
    
    #errorCode += sk.setSuperKControlEmission(COMPort,1,superKBitCluster,variaBitCluster)
    #time.sleep(3)
    
    #ni.setDevName('dev2')
    #digi_trig = ni.GenerateDigitalTrigger(int(100), int(100))
    #digi_trig.start()
    #digi_trig.stop()
    
    #errorCode += sk.superKSafeStates(COMPort)
    #time.sleep(3)


    if (errorCode==0): errorCode += sk.portClose(COMPort)

    if (errorCode!=0):
        retValue = "Error: " + str(errorCode)
    return errorCode

main()
