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

def DAC_wrting(Volt):
    name = "DAC0"
    aValue = [Volt] # 2.5 V
#    Shutter_open = 'n'
#    Shutter_open = raw_input("Press Y to open the shutter and srart recording:").lower()
#    print Shutter_open
#    if Shutter_open == 'y':
#        aValues[0] = int(raw_input("Enter the voltage"))
    ljm.eWriteName(handle, name, aValue[0])
#        break
    return



#A2D setup
info = ljm.getHandleInfo(handle)
print("Opened a LabJack with Device type: %i, Connection type: %i,\n" \
    "Serial number: %i, IP address: %s, Port: %i,\nMax bytes per MB: %i" % \
    (info[0], info[1], info[2], ljm.numberToIP(info[3]), info[4], info[5]))
# Setup and call eWriteNames to configure AINs on the LabJack.
numFrames = 3
names = ["AIN0_NEGATIVE_CH", "AIN0_RANGE", "AIN0_RESOLUTION_INDEX"]
aValues = [199, 2, 1]
ljm.eWriteNames(handle, numFrames, names, aValues)

print("\nSet configuration:")
for i in range(numFrames):
    print("    %s : %f" % (names[i], aValues[i]))

# Setup and call eReadNames to read AINs from the LabJack.
numFrames = 1
names = ["AIN0"]
#Main loop

print("\nStarting read loop.  Press Ctrl+C to stop.")
delay = .1 #delay between readings (in sec)

''' ************** Initialization for the Spectrumeter OceanOptics **************** '''
devices = sb.list_devices()
print devices
'''spec = sb.Spectrometer(devices[0])
print 'Serial number:%s' % spec.serial_number
print 'Model:%s' % spec.model
print 'minimum_integration_time_micros:' 
spec.minimum_integration_time_micros

spec.trigger_mode(0)
spec.integration_time_micros(900)
spec.wavelengths()
WaveLengths = spec.wavelengths()
'''

III = -1
read_signal2 = np.zeros(1000)
read_time = np.zeros(1000)
shutter_time = np.zeros(1)
while III < 999:
    III += 1
    if III == 499:
        DAC_wrting(5)
        shutter_time = time.time()
        #print time.time()
    
    results = ljm.eReadNames(handle, numFrames, names)
    read_signal2[III] = results[0]
    read_time[III] = time.time()
    
    '''   
    print results[0]
    plt.clf()
    plt.plot(results[0],'r*')
    plt.pause(0.1)
    
    Intensities = spec.intensities(correct_dark_counts=True, correct_nonlinearity=True)
    Intensities[0] = np.float(time.time())        
    print("\nAIN0 : %f V, AIN1 : %f V" % (results[0], results[1]))
    plt.figure(1)
    plt.clf()
    plt.plot(results[0])
    #plt.ion()
    #plt.show()
    #time.sleep(1)
    plt.figure(2)
    plt.clf()
    plt.plot(WaveLengths[1::], Intensities[1::])
    plt.pause(0.1)
    

    time.sleep(delay) 
    '''
DAC_wrting(0)
# Close handle
ljm.close(handle)

#spec.close()
