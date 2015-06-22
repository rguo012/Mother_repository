"""
Demonstrates how to set a single digital state on a LabJack.

"""

from labjack import ljm
import time

# Open first found LabJack
handle = ljm.open(ljm.constants.dtANY, ljm.constants.ctANY, "ANY")
#handle = ljm.openS("ANY", "ANY", "ANY")

info = ljm.getHandleInfo(handle)
print("Opened a LabJack with Device type: %i, Connection type: %i,\n" \
    "Serial number: %i, IP address: %s, Port: %i,\nMax bytes per MB: %i" % \
    (info[0], info[1], info[2], ljm.numberToIP(info[3]), info[4], info[5]))

# Setup and call eWriteName to set the DIO state on the LabJack.
name = "FIO6"

while True:
    A = raw_input("1 or 0")
    if  A == '1':
        state = 1
    else:
        state = 0
    time.sleep(1)    
    ljm.eWriteName(handle, name, state)    
    print("\nSet %s state : %f" % (name, state))
'''    
ljm.eWriteName(handle, name, state)    
print("\nSet %s state : %f" % (name, state))
'''


# Close handle
ljm.close(handle)
