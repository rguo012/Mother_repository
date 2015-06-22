"""
Demonstrates reading 2 analog inputs (AINs) in a loop from a LabJack.

"""

from labjack import ljm
import matplotlib.pyplot as plt
import numpy as np
import time

import seabreeze.spectrometers as sb
import scipy.io as sio
import time




read_signal = np.zeros(100)

# Open first found LabJack
handle = ljm.open(ljm.constants.dtANY, ljm.constants.ctANY, "ANY")
#handle = ljm.openS("ANY", "ANY", "ANY")

''' ************** Initialization for the DAQT7 **************** '''
#DAC0 setup
# Setup and call eWriteName to write a value to the LabJack.
names = "DAC0"
aValues = [2.5] # 2.5 V

Shutter_open = 'n'
i = 10
while i  > 1:
    i = i - 1
    Shutter_open = raw_input("Press Y to open the shutter and srart recording:").lower()
    print Shutter_open
    if Shutter_open == 'y':
        aValues[0] = int(raw_input("Enter the voltage"))
        ljm.eWriteName(handle, names, aValues[0])
        break
    
#A2D setup
info = ljm.getHandleInfo(handle)
print("Opened a LabJack with Device type: %i, Connection type: %i,\n" \
    "Serial number: %i, IP address: %s, Port: %i,\nMax bytes per MB: %i" % \
    (info[0], info[1], info[2], ljm.numberToIP(info[3]), info[4], info[5]))
# Setup and call eWriteNames to configure AINs on the LabJack.
numFrames = 6
names = ["AIN0_NEGATIVE_CH", "AIN0_RANGE", "AIN0_RESOLUTION_INDEX",
         "AIN1_NEGATIVE_CH", "AIN1_RANGE", "AIN1_RESOLUTION_INDEX"]
aValues = [199, 10, 0,
           199, 10, 0]
ljm.eWriteNames(handle, numFrames, names, aValues)

print("\nSet configuration:")
for i in range(numFrames):
    print("    %s : %f" % (names[i], aValues[i]))

# Setup and call eReadNames to read AINs from the LabJack.
numFrames = 2
names = ["AIN0", "AIN1"]

#Main loop

print("\nStarting read loop.  Press Ctrl+C to stop.")
delay = .1 #delay between readings (in sec)

''' ************** Initialization for the Spectrumeter OceanOptics **************** '''
devices = sb.list_devices()
print devices
spec = sb.Spectrometer(devices[0])
print 'Serial number:%s' % spec.serial_number
print 'Model:%s' % spec.model
print 'minimum_integration_time_micros:' 
spec.minimum_integration_time_micros

spec.trigger_mode(0)
spec.integration_time_micros(900)
spec.wavelengths()
WaveLengths = spec.wavelengths()



II = 20

while II > 0:
    II = II - 1
    try:
        results = ljm.eReadNames(handle, numFrames, names)
        read_signal[1:] = read_signal[0:99]   
        read_signal[0] = results[0]
        Intensities = spec.intensities(correct_dark_counts=True, correct_nonlinearity=True)
        Intensities[0] = np.float(time.time())        
        print("\nAIN0 : %f V, AIN1 : %f V" % (results[0], results[1]))
        plt.figure(1)
        plt.clf()
        plt.plot(read_signal)
        #plt.ion()
        #plt.show()
        #time.sleep(1)
        plt.figure(2)
        plt.clf()
        plt.plot(WaveLengths[1::], Intensities[1::])
        plt.pause(0.1)
        

        time.sleep(delay)
    except KeyboardInterrupt:
        break
    except Exception:
        import sys
        print(sys.exc_info()[1])
        break

# Close handle
ljm.close(handle)
spec.close()
