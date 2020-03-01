from cellulariot import cellulariot
import time

#node = cellulariot.CellularIoT() # for Sixfab CellularIoT HAT
node = cellulariot.CellularIoTApp() # for Sixfab CellularIoT App. Shield
node.setupGPIO()

node.disable()
time.sleep(1)
node.enable()
time.sleep(1)

print("\nPress USER button to turn on LED\r")
print("Ctrl-C to cancel...\r\n")

try:
   while 1:
      if (node.readUserButton() == 1):
         node.turnOffUserLED()
      else:
         node.turnOnUserLED()
except KeyboardInterrupt:
   pass

node.disable()
