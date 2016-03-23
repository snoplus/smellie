#!/usr/bin/env python
from SimpleXMLRPCServer import SimpleXMLRPCServer
import sys, time, os,ctypes
from orcaConnection_PQ import *

#Start a simple XML-RPC Protocol server hosted on the SNODROP machine on a port 
port = 5020
server = SimpleXMLRPCServer(("0.0.0.0", port))

#Gives the server access to these functions
server.register_function(set_fibre_switch)
server.register_function(set_safe_states)
server.register_function(set_laser_switch)
server.register_function(set_laser_intensity)
server.register_function(set_soft_lock_on)
server.register_function(set_soft_lock_off)
server.register_function(pulse_master_mode)
server.register_function(laser_testing_mode)
server.register_function(kill_sepia_and_nimax)
server.register_function(set_gain_control)
server.serve_forever()
