"""
Demonstrates reading 2 analog inputs (AINs) in a loop from a LabJack.

"""
from labjack import ljm
import matplotlib.pyplot as plt
import numpy as np
import time

global read_signal
read_signal = np.zeros(1000)
global read_time
read_time   = np.zeros(1000)
'''
Output = open("Output.txt", 'w')
Output.write( str(time.time()) + "\n")
Output.close()
'''
#read_signal = np.zeros(500)
#read_time   = np.zeros(500)

#DAC0 setup
# Setup and call eWriteName to write a value to the LabJack.
def Init():
    # Open first found LabJack
    handle = ljm.open(ljm.constants.dtANY, ljm.constants.ctANY, "ANY")
    #handle = ljm.openS("ANY", "ANY", "ANY")
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
    #return handle, Info
    return handle

def Close(handle):
    ljm.close(handle)

    
def DAC_Volt(handle,Volt): # Volt is an integer (Used for clossing or openning Shutter: 0=close, 5=open). DO NOT use this when the Main function is running
    name = "DAC0"
    aValue = [Volt] # in V
    ljm.eWriteName(handle, name, aValue[0])
    return

# Setup and call eReadNames to read AINs from the LabJack.


#Main loop

def Main(handle,No_Sample):
    
    numFrames = 1
    names = ["AIN0"]
   # read_signal = np.zeros(No_Sample)
   # read_time = np.zeros(No_Sample)

    time.sleep(1)    
    
    I = 0    
    ljm.eWriteName(handle, "DAC0", 5)
    results = ljm.eReadNames(handle, numFrames, names)
    read_signal[I] = results[0]
    read_time[I] = time.time()
    I += 1
    
    while I < No_Sample:

        results = ljm.eReadNames(handle, numFrames, names)
        read_signal[I] = results[0]
        read_time[I] = time.time()
        '''    
        plt.figure(1)
        plt.clf()
        plt.plot(read_signal)
        #plt.plot(WaveLengths[1::], Intensities[1::])
        plt.pause(0.1) 
        '''
        I += 1    
    
    ljm.eWriteName(handle, "DAC0", 0)   
    ljm.close(handle) 
    Output = open("Output2.txt", 'w')
    Output.write("\n")
    Output.close()
    f_handle = file('Output2.txt', 'a')
    np.savetxt(f_handle, (read_time, read_signal))
    #Output.write( str(time.time()) + "\n")
    f_handle.close()
    
    return


def Return_Vals(handle):   
    return read_signal, read_time
  
