import h5py
import DAQT7_Obj as DAQ
import SeaBreeze_Obj as SB
import time
import numpy as np
from multiprocessing import Process, Pipe, Value, Array
from labjack import ljm
import SeaBreeze_Obj as SB
import matplotlib.pyplot as plt
time_start =  time.time()


# ######################### Naming the DAQ ports ########################## '''
Laser_Port = "DAC1"
Shutter_Port = "DAC0"
PhotoDiod_Port = "AIN0"


# ####################### Interrupt like delays (s) ####################### '''
# Usage Ex: Px = Process(target=Timer_Multi_Process, args=(Timer_time,))
# Px.start() and in your code constantly check for "Timer_Is_Done"

def Timer_Multi_Process(Time_In_Seconds):
    if Timer_Is_Done.value is 1:
        print 'Error: This timer can be run one at a time. Either the previous timer is still running, or Timer_Is_Done bit is reset from previous timer run'
    time.sleep(Time_In_Seconds)
    Timer_Is_Done.value = 1 
    

# # A function for initializing the spectrometer (integration time and triggering mode '''
def SB_Init_Process(Spec_handle,Integration_time, Trigger_mode):
    print 'Spectrometer is initialized'
    SB.Init(Spec_handle,Integration_time, Trigger_mode)
    
    
# ########## A function for reading the spectrometer intensities ########### '''
def SB_Read_Process(Spec_handle):

    print 'Spectrumeter is waiting'
    Correct_dark_counts = True
    Correct_nonlinearity = True
    Intensities = SB.Read(Spec_handle, Correct_dark_counts, Correct_nonlinearity)   
    #print Intensities 
    SB_Current_Record[:] = Intensities
    SB_Is_Done.value = 1 
    print "Intensities are read"
    return


# ######## A function for reading the DAQ analogue inpute on AINX ######## '''
def DAQ_Read():
    results = DAQ.AIN_Read(DAQ_handle, PhotoDiod_Port)
    read_signal[DAC_Sampl_Index] = results[0]
    read_time = time.time()
    return results[0], read_time


if __name__ == "__main__":
    # ################# Detecting the spectrometer and the DAQ ###########'''
    Spec_handle = SB.Detect()
    DAQ_handle = DAQ.Init()
    DAQ.DAC_Write(DAQ_handle, Laser_Port, 0)       #Laser is off
    DAQ.DAC_Write(DAQ_handle, Shutter_Port, 0)       #Shutter is close
    
    
    # ############# Inititalizing the main loop for optrode ##############'''
    DAC_Sampl_Index = 0    
    Spec_Sampl_Index = 0

    
    # ##################### Initializing the variables ###################'''
    Integration_list = [8000, 16000, 32000, 64000, 128000, 256000, 512000]
    No_DAC_Sample = 10000 # Number of samples for Photodiod per iteration of the laser exposer. Every sample takes ~3 ms.
    SB_Is_Done = Value('i', 0)
    SB_Current_Record = Array('f', np.zeros(shape=( len(Spec_handle.wavelengths()) ,1), dtype = float ))
    SB_Is_Done.value = 0 
    Timer_Is_Done = Value('i', 0)    
    Timer_Is_Done.value = 0
    SB_Full_Records = np.zeros(shape=(len(Spec_handle.wavelengths()), len(Integration_list) ), dtype = float )
    read_signal = np.zeros(No_DAC_Sample*len(Integration_list))
    read_time   = np.zeros(No_DAC_Sample*len(Integration_list))
    
    
    # ########### The file containing the records (HDF5 format)###########'''
    File_name = "Opterode_Recording_At" + str('%i' %time.time())+ ".hdf5"
    f = h5py.File(File_name, "w")
    Spec_sub1 = f.create_group("Spectrumeter")
    Spec_specification = Spec_sub1.create_dataset("Spectrumeter", (10,), dtype='f')
    Spec_specification.attrs['Serial Number'] = np.string_(Spec_handle.serial_number)
    Spec_specification.attrs['Model'] = np.string_(Spec_handle.model)
    Spec_wavelength = f.create_dataset('Spectrumeter/Wavelength', data = Spec_handle.wavelengths())
    

    
    # ## The main loop for recording the spectrometer and the photodiod ##'''
    for Integration_index in Integration_list:
        
        # ####### First process for initializing the spectrometer ########'''
        P1 = Process(target=SB_Init_Process, args=(Spec_handle,Integration_index,3))
        P1.start()
        # ########## First process for reading the spectrometer ##########'''
        P2 = Process(target=SB_Read_Process, args=(Spec_handle,))
        P2.start()
        Half_Cycle = No_DAC_Sample*(Spec_Sampl_Index) + No_DAC_Sample/2
        Full_Cycle = No_DAC_Sample*(Spec_Sampl_Index) + No_DAC_Sample
        
        DAQ.DAC_Write(DAQ_handle, Laser_Port, 5)       #Laser is on
        P_Timer = Process(target=Timer_Multi_Process, args=(1.0,)) #1.0 s keep the laser on before opening the shutter
        P_Timer.start()
        
        print 'Integration_index: %i' %Integration_index
        #while DAC_Sampl_Index < Half_Cycle:
        while Timer_Is_Done.value == 0:
            read_signal[DAC_Sampl_Index], read_time[DAC_Sampl_Index] = DAQ_Read()
            DAC_Sampl_Index += 1   
        
        DAQ.DAC_Write(DAQ_handle, Shutter_Port, 5)       #Shutter opens in ~22ms since now
        Timer_Is_Done.value = 0
        P_Timer = Process(target=Timer_Multi_Process, args=((Integration_index*2)/1000000 + 0.8,))
        P_Timer.start()
        while Timer_Is_Done.value == 0:  
            if  SB_Is_Done.value == 1:               # At this point the spectrometer is done
                DAQ.DAC_Write(DAQ_handle, Laser_Port, 0)       #Laser is off
                DAQ.DAC_Write(DAQ_handle, Shutter_Port, 0)       #Shutter is close
                SB_Is_Done.value = 0
            read_signal[DAC_Sampl_Index], read_time[DAC_Sampl_Index] = DAQ_Read()
            DAC_Sampl_Index += 1    
        Timer_Is_Done.value = 0
        
        SB_Full_Records[:,Spec_Sampl_Index] = SB_Current_Record[:]
        Spec_Sampl_Index += 1
        
        # ### An if statement to check if the spectrometer is stalled #### '''
        if  P2.is_alive():
            P2.terminate()
            print "############################################################"    
            print "Recording failed, spectrumeter is stalled. Disconnect both spectromer and the DAQ and rerun the code."
            break
        
    # ########### Saving the recorded signals in HDF5 format ############ '''
    read_signal2 = np.zeros(DAC_Sampl_Index)
    read_time2   = np.zeros(DAC_Sampl_Index)
    read_signal2[:] = read_signal[0:DAC_Sampl_Index]
    read_time2[:] = read_time[0:DAC_Sampl_Index]
    Spec_intensities = f.create_dataset('Spectrumeter/Intensities', data = SB_Full_Records)
    Spec_intensities = f.create_dataset('DAQT7/DAC_Readings', data = read_signal2)
    Spec_intensities = f.create_dataset('DAQT7/DAC_Time_Stamps', data = read_time2)
    f.close()
        
        
    time_end = time.time()
    print 'Duration of the session: %.3f s' %(time_end - time_start)
        
    time.sleep(0.5) 
    DAQ.DAC_Write(DAQ_handle, Laser_Port, 5)       #Laser is on

    SB.Close(Spec_handle)
    DAQ.Close(DAQ_handle)

    
