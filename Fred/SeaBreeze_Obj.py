
#from labjack import ljm
#def SeaBreeze_Libs():
import matplotlib.pyplot as plt
import numpy as np
import time
import seabreeze.spectrometers as sb
import time

''' ************** Initialization for the Spectrumeter OceanOptics **************** '''
def Detect ():
    devices = sb.list_devices()
    print devices
    spec = sb.Spectrometer(devices[0])
    print 'Serial number:%s' % spec.serial_number
    print 'Model:%s' % spec.model
    print 'minimum_integration_time_micros:' 
    spec.minimum_integration_time_micros
    
    spec.trigger_mode(0)            #Flushing the stuff!
    spec.integration_time_micros(10000)
    spec.wavelengths()
    Intensities = spec.intensities(correct_dark_counts=True, correct_nonlinearity=True)
    Intensities = spec.intensities(correct_dark_counts=True, correct_nonlinearity=True)
    return spec

def Init(spec,Integration_time, Ttigger_mode):
    spec.trigger_mode(Ttigger_mode)
    #spec.integration_time_micros(10000)
    spec.integration_time_micros(Integration_time)
    return

def Close(spec):
    spec.close()
    
def Main(spec,No_itteration):
    I = 0
    while I < No_itteration:
        I += 1
        Intensities = spec.intensities(correct_dark_counts=True, correct_nonlinearity=True)
        Intensities[0] = np.float(time.time())        
        #    plt.figure(2)
        #    plt.clf()
        #    plt.plot(spec.wavelengths()[1::],Intensities[1::])
        #plt.plot(WaveLengths[1::], Intensities[1::])
        #    plt.pause(0.1)
        #    time.sleep(0.1)
    return Intensities
