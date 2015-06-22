#import seabreeze			# for pyseabreeze only
#seabreeze.use('pyseabreeze')		# for pyseabreeze only
import matplotlib.pyplot as plt
import seabreeze.spectrometers as sb
import time
devices = sb.list_devices()
#print devices
spec = sb.Spectrometer(devices[0])
print 'Serial number:%s' % spec.serial_number
print 'Model:%s' % spec.model
print 'minimum_integration_time_micros:' 
spec.minimum_integration_time_micros

#spec.trigger_mode(0)
spec.continuous_strobe_set_enable(1)
spec.continuous_strobe_set_period_micros(1000000)
spec.integration_time_micros(30000)
spec.trigger_mode(1)
spec.wavelengths()


WaveLengths = spec.wavelengths()
plt.ion()
plt.plot(range(10))	
#plt.show()

#for I in range(100):
Time_Label = [time.time()]
while True:
    Intensities = spec.intensities(correct_dark_counts=True, correct_nonlinearity=True)
    #Intensities = spec.intensities()
    #WaveLengths = spec.wavelengths()
    #Spectrum    = spec.spectrum(correct_dark_counts=True, correct_nonlinearity=True) 
    #Spectrum    = spec.spectrum()

    #plt.plot(Spectrum[0], Spectrum[1])
    #plt.plot(WaveLengths, Intensities)
    #plt.plot(range(I))	
    # plt.ion()
    # plt.show()
    #plt.ion()
    #plt.show()
    #time.sleep(1)
    #plt.pause(0.1)
    #plt.clf()
    #time.sleep(.01)
    Time_Label.append([time.time()])
    print time.time()

spec.close()
plt.close('all')
'''
Output = open("Output.txt", 'w')
for I in range(len(WaveLengths)):
	Output.write(str(Spectrum[0][I]) + "	"+ str(Spectrum[1][I]) + "	"+ str(Intensities[I]) + "	"+ str(WaveLengths[I]) + "\n")

Output.close()
'''
