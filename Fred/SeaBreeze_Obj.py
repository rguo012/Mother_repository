
import numpy as np
import time
import seabreeze.spectrometers as sb


''' ************** Detection of the Spectrumeter OceanOptics **************** '''
def Detect ():
    devices = sb.list_devices()
    print devices
    spec = sb.Spectrometer(devices[0])
    print 'Serial number:%s' % spec.serial_number
    print 'Model:%s' % spec.model
    print 'minimum_integration_time_micros:' 
    spec.minimum_integration_time_micros
    
    spec.trigger_mode(0)            #Flushing the stuff down and make the spectrometer ready for next steps!
    spec.integration_time_micros(10000)
    spec.wavelengths()
    Intensities = spec.intensities(correct_dark_counts=True, correct_nonlinearity=True)
    Intensities = spec.intensities(correct_dark_counts=True, correct_nonlinearity=True)
    return spec


''' Initialization for the inegration time and the trigger mode. 
For HR2000+ Ttigger_mode =

0 ==> free running mode
1 ==> external level trigger mode
3 ==> external edge trigger mode

For MayaPro Ttigger_mode =
0 ==> free running mode
1 ==> external edge trigger mode  !!!
3 ==> external edge trigger mode
'''
def Init(spec,Integration_time, Trigger_mode):
    spec.trigger_mode(Trigger_mode)
    #spec.integration_time_micros(10000)
    spec.integration_time_micros(Integration_time)
    return


''' Reading the intensities.
Important! the first element in the Intensities array is the unix time for when the reading is finished.
''' 
def Read(spec,Correct_dark_counts, Correct_nonlinearity):
    Intensities = spec.intensities(correct_dark_counts=Correct_dark_counts, correct_nonlinearity=Correct_nonlinearity)
    Intensities[0] = np.float(time.time())        
    return Intensities


''' Closing the device '''
def Close(spec):
    spec.close()
    