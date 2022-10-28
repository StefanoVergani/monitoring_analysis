import numpy as np
import os
import h5py as h5
import pandas as pd
import sys

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
    @staticmethod
    def time_file_creator(path,channels,your_name):
        display_array = []
        directory = os.fsencode(path)
        for file in os.listdir(directory):
            filename = os.fsdecode(file)
            if filename.startswith(your_name): 
                df = pd.read_hdf(os.sep.join([path, filename]))
                temp = []
                for i in range(channels.size):
                    temp.append(df.iat[0,i])
                display_array.append(temp)
                continue
            else:
                continue

        return display_array
    
    #this function looks into a given folder in path and store for each file one line containing
    #the all the std for that file
    #rember to define beforehands a void 
    @staticmethod
    def time_file_creator_bis(path,array,channels):
        display_array = []
        for i in range(len(array)):
            df = pd.read_hdf(os.sep.join([path, array[i]]))
            temp = []
            for i in range(channels.size):
                temp.append(df.iat[0,i])
            display_array.append(temp)

        return display_array

    
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


     #this function checks that your file exists
    @staticmethod
    def file_checker(your_file):
        if(os.path.isfile(your_file)==False):
            print(your_file)
            sys.exit("File not found!")

    #this function convertes the name of the input/outfolder from double slashes to single slashes
    @staticmethod
    def slash_converter(your_file):
        your_file = your_file.replace("//","/")


    #this function loops over files inside a given folder returning the latest event with a given name
    @staticmethod
    def file_looper(your_folder_in_str, your_name):
        directory = os.fsencode(your_folder_in_str)
        filename_list = []
        for file in os.listdir(directory):
            filename = os.fsdecode(file)
            if filename.startswith(your_name): 
                filename_list.append(filename)
                # print(os.path.join(directory, filename))
                continue
            else:
                continue
        for i in range (len(filename_list)):
            if i==(len(filename_list)-1):
                return filename_list[i]
            
    #this function loops over files inside a given folder returning the latest x-events with a given name
    @staticmethod
    def file_looper_amount(your_folder_in_str, your_name, amount):
        directory = os.fsencode(your_folder_in_str)
        filename_list = []
        printout_list = []
        for file in os.listdir(directory):
            filename = os.fsdecode(file)
            if filename.startswith(your_name): 
                filename_list.append(filename)
                # print(os.path.join(directory, filename))
                continue
            else:
                continue
        for i in range(len(filename_list)):
            if i>(len(filename_list)-amount) or i==(len(filename_list)-amount):
                printout_list.append(filename_list[i])
        return printout_list


    #this function extracts the std values from a single std file
    #rember to define beforehands a void 
    #array = []
    #and at the end convert it to np.array
    #array = np.array(display_array)
    @staticmethod
    def std_extractor(file_name,channels):
        df = pd.read_hdf(file_name)
        array=[]
        for i in range(channels.size):
            array.append(df.iat[0,i])
        return array

    #this function analyses the rms coming from data and from the baseline and if the module difference is greater than N times
    #the standard deviation of the baseline, then the pixel becomes white.
    #it returns a list of pixels, one per channel. 0 non-triggered 1 triggered. 
    @staticmethod
    def triggering_pixel_finder(rms_data_list, rms_baseline_list, std_baseline_list, channels,N):
        triggered_list = []
        for i in range(len(channels)):
            if((abs(rms_data_list[i]-rms_baseline_list[i])>N*std_baseline_list[i])):
                triggered_list.append(1)
                continue
            else:
                triggered_list.append(0.1)
                continue
        return triggered_list


    #this function fills a predefined void list faulty_array with 1 if two subsequent pixels have entry different
    #than -999 in alarmed_array and 0.1 if not. As before, rembember to convert faulty_array into a np.array
    @staticmethod
    def alarm_finder(triggers_list, alarmed_array, percentage_array, baseline_array):
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

        

    #this function creates the official matrix in the specific case we have one array 1D to be stored
    @staticmethod
    def structured_matrix_1D(array_display_0, array_display_1, array_display_2):
        temp = []
        temp.append(array_display_0)
        temp.append(array_display_1)
        temp.append(array_display_2)
        return temp
    
    @staticmethod
    def alarm_creator(array_1, array_2, channel_0, channel_1, channel_2):
        temp = []
        for i in range(len(channel_0)):
            if (array_1[0][i]==0.1 and array_2[0][i]==0.1):
                temp[0][i].append(1)
            else:
                temp[0][i].append(0.1)
        for j in range(len(channel_1)):
            if (array_1[1][j]==0.1 and array_2[1][j]==0.1):
                temp[1][j].append(1)
            else:
                temp[1][j].append(0.1)
        for k in range(len(channel_2)):
            if (array_1[2][k]==0.1 and array_2[2][k]==0.1):
                temp[2][k].append(1)
            else:
                temp[2][k].append(0.1)
        return temp
          
            
        
                        
     







