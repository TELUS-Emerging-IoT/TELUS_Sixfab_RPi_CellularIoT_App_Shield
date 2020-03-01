#!/usr/bin/env python3
 
from cellulariot import cellulariot
import time
 
node = cellulariot.CellularIoTApp()
node.setupGPIO()
 
node.disable()          # clean up before anything else
time.sleep(0.5)
node.enable()
time.sleep(0.5)
 
node.sendATComm("ATE1","OK\r\n")        # set echo ON
 
# retrieve hardware information
node.getIMEI()                  # get IMEI of the module
node.getFirmwareInfo()          # get firmware info of the module
node.getHardwareInfo()          # get the module model e.g. BG96
node.sendATComm("AT+CIMI","OK\r\n")     # get IMSI
 
print("turning GPS on...\r\n")
node.turnOffGNSS()
time.sleep(1)
node.turnOnGNSS()
print("success...\r\n")

# get Latitude and Longitude
try:
   while 1:
      node.sendATComm("AT+QGPSLOC=2","OK\r\n")  # get Long / Lat
      time.sleep(15)                            # every 60 seconds
except KeyboardInterrupt:
   pass

time.sleep(1)
node.turnOffGNSS()
