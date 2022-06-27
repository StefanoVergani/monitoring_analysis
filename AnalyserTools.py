import numpy as np
import os
import h5py as h5
import pandas as pd

class AnalyserTools:

    @staticmethod
    def rms_func(x):
        return np.sqrt(np.mean(x**2))

    #creates rms file from raw waveforms. path_raw is where raw waveforms live and path_rms where you want the files to be created
    @staticmethod
    def rms_creator(path_raw, path_rms):
        directory = os.fsencode(path_raw)
        for file in os.listdir(directory):
            filename = os.fsdecode(file)
            if filename.endswith(".hdf5"): 
                df = pd.read_hdf(os.sep.join([path_raw, filename]))
                f = h5.File(os.sep.join([path_raw, filename]), "r")
                channels = np.array(f.get('data/axis0').value)
                rms = []
                for i in range(channels.size):
                    rms.append(np.sqrt(np.mean(df.iat[0,i]**2)))        
                filename_rms = 'rms'+filename[3:]
                hf_target = h5.File(os.sep.join([path_rms,filename_rms]), 'w')
                hf_target.create_dataset('rms', data=rms)
                hf_target.create_dataset('channels', data=channels)
                hf_target.close()
                del rms
                continue
            else:
                continue

    #this function looks into a given folder in path and store for each file one line containing
    #the all the rms for that file
    #rember to define beforehands a void 
    #display_array = []
    #and at the end convert it to np.array
    #display_array = np.array(display_array)
    @staticmethod
    def file_creator(path, display_array):
        directory = os.fsencode(path)
        for file in os.listdir(directory):
            filename = os.fsdecode(file)
            if filename.endswith(".hdf5"): 
                f = h5.File(os.sep.join([path, filename]), "r")
                value = np.array(f.get('rms').value)
                display_array.append(value)
                continue
            else:
                continue


    #this function looks into a given folder in path and store for each file one line containing
    #the all the std for that file
    #rember to define beforehands a void 
    #display_array = []
    #and at the end convert it to np.array
    #display_array = np.array(display_array)
    @staticmethod
    def std_file_creator(path, display_array,channels):
        directory = os.fsencode(path)
        for file in os.listdir(directory):
            filename = os.fsdecode(file)
            if filename.endswith(".hdf5"): 
                df = pd.read_hdf(os.sep.join([path, filename]))
                temp = []
                for i in range(channels.size):
                    temp.append(df.iat[0,i])
                display_array.append(temp)
                continue
            else:
                continue

    
    #here I define two very important functions to created the alarms
    #percentage_creator takes the following:
    #alarmed_array = a predefined void list which gets filled with -999 if the difference between target and baseline
    #is less than threshold, or the value of target if this difference is greater than threshold
    # percentage_array = a predefined void list which gets filled which the unit target/baseline in units of baseline
    #target_array = the file you want to study
    #baseline_array = the baseline you are using
    #threshold = the threshold value you decided
    #!!attention!! after calling this function rember to convert alarmed_array and percentage_array into a np array
    #somehow inside the function that doesn't work

    #beforehand define 
    #faulty_array = []
    #allarmed_array = []
    #percentage_array = []
    @staticmethod
    def percentage_creator(alarmed_array, percentage_array, target_array, baseline_array, threshold):
        for i in range(target_array.shape[1]):#channels:
            temp = []
            temp_perc = []
            for j in range(target_array.shape[0]):#measurements
                temp_perc.append((target_array[j][i]-baseline_array[i])/baseline_array[i])
                if((abs(target_array[j][i]-baseline_array[i])/baseline_array[i])>threshold):
                    temp.append(target_array[j][i])
                else:
                    temp.append(-999)
            alarmed_array.append(temp)
            percentage_array.append(temp_perc)

        #alarmed_array= np.array(allarmed_array)
        #percentage_array= np.array(percentage_array)

        del temp
        del temp_perc
    
    #this function fills a predefined void list faulty_array with 1 if two subsequent pixels have entry different
    #than -999 in alarmed_array and 0.1 if not. As before, rembember to convert faulty_array into a np.array
    
    @staticmethod
    def faulty_finder(faulty_array, alarmed_array, percentage_array, baseline_array):
        for i in range(alarmed_array.shape[0]):#channels
            temp = []
            for j in range(alarmed_array.shape[1]):#measurements
                if(j<(alarmed_array.shape[1]-1) and alarmed_array[i][j]!=-999 and alarmed_array[i][j+1]!=-999):
                    percentage=round((alarmed_array[i][j]-baseline_array[i])/baseline_array[i],2)
                    temp.append(1)
                    #I am commenting out the next print only because github gets a bit crazy, but use it when running it!
                    #print("alarm! In channel",i,"at time",time_0[j],"we had a value",percentage," away from mean and this happened in two subsequent pixels")
                else:
                    temp.append(0.1)
            faulty_array.append(temp)
        del temp
        #faulty_array = np.array(faulty_array)


    #this is a slightly different version which takes into account the difference between target and baseline in
    #terms of units of standard deviations.
    #the biggest difference is that threshold is now an array and N is the number of sigmas we want
    @staticmethod
    def sigma_creator(alarmed_array, percentage_array, target_array, baseline_array, N, threshold_array):
    
        for i in range(target_array.shape[1]):#channels:
            temp = []
            temp_perc = []
            for j in range(target_array.shape[0]):#measurements
                temp_perc.append((target_array[j][i]-baseline_array[i]))
                if((abs(target_array[j][i]-baseline_array[i]))>N*threshold_array[i]):
                    temp.append(target_array[j][i])
                else:
                    temp.append(-999)
            alarmed_array.append(temp)
            percentage_array.append(temp_perc)

        #allarmed_array= np.array(allarmed_array)
        #percentage_array= np.array(percentage_array)

        del temp
        del temp_perc
    
    #this function fills a predefined void list faulty_array with 1 if two subsequent pixels have entry different
    #than -999 in alarmed_array and 0.1 if not. As before, rembember to convert faulty_array into a np.array
    @staticmethod
    def faulty_sigma_finder(faulty_array, alarmed_array, percentage_array, baseline_array):
        for i in range(alarmed_array.shape[0]):#channels
            temp = []
            for j in range(alarmed_array.shape[1]):#measurements
                if(j<(alarmed_array.shape[1]-1) and alarmed_array[i][j]!=-999 and alarmed_array[i][j+1]!=-999):
                    percentage=alarmed_array[i][j]-baseline_array[i]
                    temp.append(1)
                    #I am commenting out the next print only because github gets a bit crazy, but use it when running it!
                    #print("alarm! In channel",i,"at time",time_0[j],"we had a value",percentage," away from mean and this happened in two subsequent pixels")
                else:
                    temp.append(0.1)
            faulty_array.append(temp)
        del temp
        #faulty_array = np.array(faulty_array)






