'''
import h5py
fname = 'mytestfile.hdf5'

file = h5py.File(fname,'r')
dataset = file['mydataset']
subgroup1 = dataset[0:]
print subgroup1
print len(subgroup1)

dataset2 = file['subgroup2/dataset_three']
print dataset2[0:]
print len(dataset2)
'''



'''
import h5py
import matplotlib.pyplot as plt
import numpy as np
import time

File_name = "Opterode_RecordingAt" + str('%i' %time.time())+ ".hdf5"
f = h5py.File(File_name, "w")
Spec_sub1 = f.create_group("Spectrumeter")
Spec_specification = Spec_sub1.create_dataset("Spectrumeter", (10,), dtype='f')
Spec_specification.attrs['Serial Number'] = np.string_('12345')
Spec_specification.attrs['Model'] = np.string_('H1+123')
wavelength = np.random.rand(2048,1)
Spec_wavelength =  f.create_dataset('Spectrumeter/Wavelength', data = wavelength) 
#Spec_wavelength =  f.create_dataset('Spectrumeter/Wavelength',  (len(wavelength),), dtype='f')
#Spec_wavelength = wavelength
intensities = np.random.rand(2048,2)
Spec_intensities = f.create_dataset('Spectrumeter/Intensities', data = intensities)
#Spec_intensities = f.create_dataset('Spectrumeter/Intensities', (len(wavelength),2), dtype='f')
#Spec_intensities = intensities
f.close()
'''



import h5py
import matplotlib.pyplot as plt
import numpy as np


f = h5py.File('Opterode_RecordingAt1435718038.hdf5','r')

ks = f.keys()

len(f[ks[0]].values())
(f[ks[1]].values()[0]).shape
(f[ks[1]].values()[1]).shape
(f[ks[1]].values()[2]).shape

Intensities = f[ks[1]].values()[0]
Spectrumeter = np.array(f[ks[1]].values()[1])
Wavelength = np.array(f[ks[1]].values()[2])

DAC_Reading = f[ks[0]].values()[0]

plt.plot(DAC_Reading)
'''
for index,key in enumerate(ks[:]):
    print index, key
    data = np.array(f[key].values())
    plt.plot(data.ravel())
'''
