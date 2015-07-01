#import seabreeze			# for pyseabreeze only
#seabreeze.use('pyseabreeze')		# for pyseabreeze only
import matplotlib.pyplot as plt
import seabreeze.spectrometers as sb
import scipy.io as sio
import time
import numpy as np

devices = sb.list_devices()
print devices
spec = sb.Spectrometer(devices[0])
print 'Serial number:%s' % spec.serial_number
print 'Model:%s' % spec.model
print 'minimum_integration_time_micros:' 
spec.minimum_integration_time_micros
# ############################Flushes the spectrumeter###################
spec.trigger_mode(0)            #Flushing the stuff!
spec.integration_time_micros(10000)
spec.wavelengths()
Intensities = spec.intensities(correct_dark_counts=True, correct_nonlinearity=True)
Intensities = spec.intensities(correct_dark_counts=True, correct_nonlinearity=True)
# ################################ Done #################################



spec.trigger_mode(3)
spec.integration_time_micros(10000)
spec.wavelengths()

plt.ion()
plt.plot(range(10))	
#plt.show()

'''
Output = open("Output.txt", 'w')
Output.write( str(time.time()) + "\n")
Output.close()
'''
WaveLengths = spec.wavelengths()


for I in range(10):


    Intensities = spec.intensities(correct_dark_counts=True, correct_nonlinearity=True)
    Intensities[0] = np.float(time.time())
    #Intensities = spec.intensities()
    #WaveLengths = spec.wavelengths()
    #Spectrum    = spec.spectrum(correct_dark_counts=True, correct_nonlinearity=True) 
    #Spectrum    = spec.spectrum()

    #plt.plot(Spectrum[0], Spectrum[1])
    #plt.plot(Spectrum[0], Intensities)
    plt.plot(WaveLengths[1::], Intensities[1::])
    #plt.plot(range(I))	
    # plt.ion()
    # plt.show()
    #plt.ion()
    #plt.show()
    #time.sleep(1)
    plt.pause(0.1)
    plt.clf()
    '''
    Output = open("Output.txt", 'a')
    sio.savemat
    for I in range(2):
        Output.write( str(Intensities[0+(I)*1000:1000*(I+1)]) + "\n")
    Output.write( str(Intensities[2000:2067]) + "\n")
    Output.write( str(time.time()) + "\n")'''
    
    f_handle = file('Output.txt', 'a')
    np.savetxt(f_handle, Intensities)
    #Output.write( str(time.time()) + "\n")
    f_handle.close()
    print Intensities[0]
spec.close()
Output.close()

#plt.close('all')

'''#import seabreeze			# for pyseabreeze only
#seabreeze.use('pyseabreeze')		# for pyseabreeze only
import matplotlib.pyplot as plt
import seabreeze.spectrometers as sb
import time
devices = sb.list_devices()
print devices
spec = sb.Spectrometer(devices[0])
print 'Serial number:%s' % spec.serial_number
print 'Model:%s' % spec.model
print 'minimum_integration_time_micros:' 
spec.minimum_integration_time_micros

spec.trigger_mode(0)
spec.integration_time_micros(7200)
spec.wavelengths()

plt.ion()
plt.plot(range(10))	
#plt.show()

for I in range(200):
	

	#Intensities = spec.intensities(correct_dark_counts=True, correct_nonlinearity=True)
	#Intensities = spec.intensities()
	#WaveLengths = spec.wavelengths()
	Spectrum    = spec.spectrum(correct_dark_counts=True, correct_nonlinearity=True) 
	#Spectrum    = spec.spectrum()

	#plt.plot(Spectrum[0], Spectrum[1])
	#plt.plot(Spectrum[0], Intensities)
	#plt.plot(range(I))	
	# plt.ion()
	# plt.show()
	#plt.ion()
	#plt.show()
	#time.sleep(1)
	#plt.pause(0.1)
	#plt.clf()
	Output = open("Output.txt", 'w')
	for I in range(len(Spectrum[0])):
		Output.write( str(Spectrum[1][I]) + "\n")

	Output.close()
	print time.time()


#plt.close('all') '''

