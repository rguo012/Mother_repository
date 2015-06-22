import h5py
import DAQT7_Obj as DAQ
import SeaBreeze_Obj as SB
import time
import numpy as np
from multiprocessing import Process, Pipe, Value, Array
from labjack import ljm
import SeaBreeze_Obj as SB
import matplotlib.pyplot as plt


Spec_handle = SB.Detect()
DAQ_handle = DAQ.Init()
Integration_list = [8000, 16000, 32000, 64000, 128000, 256000, 512000]
No_Sample = 1400 # Number of samples for Photodiod per iteration of the laser exposer

SB_Is_Done = Value('i', 0)
SB_Current_Record = Array('f', np.zeros(shape=( len(Spec_handle.wavelengths()) ,1), dtype = float ))
SB_Is_Done.value = 0 
SB_Full_Records = np.zeros(shape=(len(Spec_handle.wavelengths()), len(Integration_list) ), dtype = float )
#np.random.rand(len(Integration_list), len(Spec_handle.wavelengths()))

read_signal = np.zeros(No_Sample*len(Integration_list))
read_time   = np.zeros(No_Sample*len(Integration_list))

File_name = "Opterode_RecordingAt" + str('%i' %time.time())+ ".hdf5"
f = h5py.File(File_name, "w")
Spec_sub1 = f.create_group("Spectrumeter")
Spec_specification = Spec_sub1.create_dataset("Spectrumeter", (10,), dtype='f')
Spec_specification.attrs['Serial Number'] = np.string_(Spec_handle.serial_number)
Spec_specification.attrs['Model'] = np.string_(Spec_handle.model)
Spec_wavelength = f.create_dataset('Spectrumeter/Wavelength', data = Spec_handle.wavelengths()) 





def SB_Init(Spec_handle,Integration_time, Trigger_mode):
    print 'SB is initialized'
    Spec_handle.trigger_mode(Trigger_mode)
    Spec_handle.integration_time_micros(Integration_time)

def SB_Main(Spec_handle,No_itteration):
    I = 0
    print 'helloooooooooooo'
    while I < No_itteration:
        #try:
        print 'spetp 1'
        Intensities = Spec_handle.intensities(correct_dark_counts=True, correct_nonlinearity=True)
        Intensities[0] = np.float(time.time())     
        SB_Is_Done.value = 1
        print 'spetp 2'    
        #print Intensities   
        I += 1
        
    SB_Current_Record[:] = Intensities
    print "Is Done"
    return



I = 0    
II = 0
numFrames = 1
names = ["AIN0"]
results = ljm.eReadNames(DAQ_handle, numFrames, names)
read_signal[I] = results[0]
read_time[I] = time.time()
I += 1

for Integration_index in Integration_list:
    
    Process(target=SB_Init, args=(Spec_handle,Integration_index,3)).start()
    Process(target=SB_Main, args=(Spec_handle,1)).start()
    
    Half_Cycle = No_Sample*(II) + No_Sample/2
    Full_Cycle = No_Sample*(II) + No_Sample
    
    ljm.eWriteName(DAQ_handle, "DAC1", 5)       #Laser is on
    
    results = ljm.eReadNames(DAQ_handle, numFrames, names)
    read_signal[I] = results[0]
    read_time[I] = time.time()
    I += 1
    
    print 'Integration_index: %i' %Integration_index
    while I < Half_Cycle:
        results = ljm.eReadNames(DAQ_handle, numFrames, names)
        read_signal[I] = results[0]
        read_time[I] = time.time()
        I += 1    
    ljm.eWriteName(DAQ_handle, "DAC0", 5)       #Shutter opens in ~22ms since now
    while I < Full_Cycle:
        if SB_Is_Done.value == 1:
            ljm.eWriteName(DAQ_handle, "DAC1", 0)       #Laser off
            ljm.eWriteName(DAQ_handle, "DAC0", 0)       #Shutter close
            SB_Is_Done.value = 0
        results = ljm.eReadNames(DAQ_handle, numFrames, names)
        read_signal[I] = results[0]
        read_time[I] = time.time()
        I += 1    
    
    SB_Full_Records[:,II] = SB_Current_Record[:]
    #plt.plot(SB_Current_Record[1:])
    #plt.pause(1)
    II += 1
    

Spec_intensities = f.create_dataset('Spectrumeter/Intensities', data = SB_Full_Records)
Spec_intensities = f.create_dataset('DAQT7/DAC_Readings', data = read_signal)
Spec_intensities = f.create_dataset('DAQT7/DAC_Time_Stamps', data = read_time)
f.close()

SB.Close(Spec_handle)
DAQ.Close(DAQ_handle)

