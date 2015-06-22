
import DAQT7_Obj as DAQ
import SeaBreeze_Obj as SB
import time
import numpy as np
from multiprocessing import Process, Pipe, Value
from labjack import ljm
import SeaBreeze_Obj as SB

spec = SB.Detect()
handle = DAQ.Init()
Integration_list = [8000, 16000, 32000, 64000, 128000, 256000, 512000]
No_Sample = 1400 # Number of samples for Photodiod per iteration of the laser exposer

SB_Is_Done = Value('i', 0)
SB_Is_Done.value = 0 

read_signal = np.zeros(No_Sample*len(Integration_list))
read_time   = np.zeros(No_Sample*len(Integration_list))



def SB_Init(spec,Integration_time, Trigger_mode):
    print 'SB is initialized'
    spec.trigger_mode(Trigger_mode)
    spec.integration_time_micros(Integration_time)
   # spec.wavelengths()

def SB_Main(spec,No_itteration,DAQ_handle):
    I = 0
    print 'helloooooooooooo'
    while I < No_itteration:
        #try:
        print 'spetp 1'
        Intensities = spec.intensities(correct_dark_counts=True, correct_nonlinearity=True)
        Intensities[0] = np.float(time.time())     
        SB_Is_Done.value = 1
        print 'spetp 2'    
        #print Intensities   
        I += 1
    
    print 'spetp 3'    
    Output = open(str('%.3f' %Intensities[0])+'.txt', 'w')
    Output.write("\n")
    Output.close()
    f_handle = file(str('%.3f' %Intensities[0])+'.txt', 'a')
    np.savetxt(f_handle, Intensities)
    #Output.write( str(time.time()) + "\n")
    f_handle.close()
    #time.sleep(.300)
    #spec.close()
    print 'spetp 4'
    return



I = 0    
II = 0
numFrames = 1
names = ["AIN0"]
results = ljm.eReadNames(handle, numFrames, names)
read_signal[I] = results[0]
read_time[I] = time.time()
I += 1
 
for Integration_index in Integration_list:
    
    #SB.Init(spec,Integration_index,3)
    Process(target=SB_Init, args=(spec,Integration_index,3)).start()
    Process(target=SB_Main, args=(spec,1,handle)).start()
    
    Half_Cycle = No_Sample*(II) + No_Sample/2
    Full_Cycle = No_Sample*(II) + No_Sample
    
    ljm.eWriteName(handle, "DAC1", 5)       #Laser is on
    
    results = ljm.eReadNames(handle, numFrames, names)
    read_signal[I] = results[0]
    read_time[I] = time.time()
    I += 1
    II += 1
    print 'Integration_index: %i' %Integration_index
    while I < Half_Cycle:
        results = ljm.eReadNames(handle, numFrames, names)
        read_signal[I] = results[0]
        read_time[I] = time.time()
        I += 1    
    ljm.eWriteName(handle, "DAC0", 5)       #Shutter opens in ~22ms since now
    while I < Full_Cycle:
        if SB_Is_Done.value == 1:
            ljm.eWriteName(handle, "DAC1", 0)       #Laser off
            ljm.eWriteName(handle, "DAC0", 0)       #Shutter close
            SB_Is_Done.value = 0
        results = ljm.eReadNames(handle, numFrames, names)
        read_signal[I] = results[0]
        read_time[I] = time.time()
        I += 1    

    
print 'time2: %.3f' %time.time()
SB.Close(spec)
print 'time4: %.3f' %time.time()
DAQ.Close(handle)
print 'time5: %.3f' %time.time()
Output = open("Output2.txt", 'w')
Output.write("\n")
Output.close()
f_handle = file('Output2.txt', 'a')
np.savetxt(f_handle, (read_time, read_signal))
#Output.write( str(time.time()) + "\n")
f_handle.close()


