import os
import pandas as pd
import h5py as h5
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
from mpl_toolkits import mplot3d
from matplotlib.ticker import MaxNLocator
from AnalyserTools import AnalyserTools as ant

class AnalyserFunctions:



    #this is a test function

    @staticmethod
    def test_function(path_dir, path_dir_output):
        print('path dir is ', path_dir)
        print('path out is ', path_dir_output)


    #this function opens files containing the std and rms. If the rms for a given pixel is more than n std and this happens in two suqsequent
    #pixels, than it raises an alarm. It then assignes the value 1 to alarmed pixels and 0 to the others. It saves these values on a hdf5 files.
    @staticmethod
    def alarm(path_dir, path_dir_output):

        print('test 1')

        ant.file_checker(os.sep.join([path_dir, "std_display_0_2022_05_22.hdf5"]))
        ant.file_checker(os.sep.join([path_dir, "std_display_1_2022_05_22.hdf5"]))
        ant.file_checker(os.sep.join([path_dir, "std_display_2_2022_05_22.hdf5"]))
        ant.file_checker(os.sep.join([path_dir, "rms_display_0_2022_05_22.hdf5"]))
        ant.file_checker(os.sep.join([path_dir, "rms_display_1_2022_05_22.hdf5"]))
        ant.file_checker(os.sep.join([path_dir, "rms_display_2_2022_05_22.hdf5"]))
        ant.file_checker(os.sep.join([path_dir, "baselines_2022_05_22.hdf5"]))

        print("successfully opened the files")

        target_0 = h5.File(os.sep.join([path_dir, "std_display_0_2022_05_22.hdf5"]), 'r')
        target_1 = h5.File(os.sep.join([path_dir, "std_display_1_2022_05_22.hdf5"]), 'r')
        target_2 = h5.File(os.sep.join([path_dir, "std_display_2_2022_05_22.hdf5"]), 'r')
        target_0_rms = h5.File(os.sep.join([path_dir, "rms_display_0_2022_05_22.hdf5"]), 'r')
        target_1_rms = h5.File(os.sep.join([path_dir, "rms_display_1_2022_05_22.hdf5"]), 'r')
        target_2_rms = h5.File(os.sep.join([path_dir, "rms_display_2_2022_05_22.hdf5"]), 'r')
        baselines = h5.File(os.sep.join([path_dir, "baselines_2022_05_22.hdf5"]), 'r')

        #std over time from file
        std_0 = np.array(target_0.get('std_display_0').value)
        std_1 = np.array(target_1.get('std_display_1').value)
        std_2 = np.array(target_2.get('std_display_2').value)
        #rms over time from file
        rms_0 = np.array(target_0_rms.get('rms_display_0').value)
        rms_1 = np.array(target_1_rms.get('rms_display_1').value)
        rms_2 = np.array(target_2_rms.get('rms_display_2').value)
        #channel numbers from file
        channels_0 = np.array(target_0.get('channels').value)
        channels_1 = np.array(target_1.get('channels').value)
        channels_2 = np.array(target_2.get('channels').value)
        #std baselines per channel
        bl_0_std_array = np.array(baselines.get('mean_std_display_0').value)
        bl_1_std_array = np.array(baselines.get('mean_std_display_1').value)
        bl_2_std_array = np.array(baselines.get('mean_std_display_2').value)
        #std baseline from display (single number)
        bl_0_std_total = baselines.get('total_std_mean_0').value
        bl_1_std_total = baselines.get('total_std_mean_1').value
        bl_2_std_total = baselines.get('total_std_mean_2').value
        #rms baselines per channel
        bl_0_rms_array = np.array(baselines.get('mean_rms_display_0').value)
        bl_1_rms_array = np.array(baselines.get('mean_rms_display_1').value)
        bl_2_rms_array = np.array(baselines.get('mean_rms_display_2').value)
        #rms baseline from display (single number)
        bl_0_rms_total = baselines.get('total_rms_mean_0').value
        bl_1_rms_total = baselines.get('total_rms_mean_1').value
        bl_2_rms_total = baselines.get('total_rms_mean_2').value
        #channel numbers from baselines
        channels_bl_0 = baselines.get('channels_bl_0').value
        channels_bl_1 = baselines.get('channels_bl_1').value
        channels_bl_2 = baselines.get('channels_bl_2').value

        #each baseline file must have the same number of channel of the file you are checking
        #if not, it means you are comparing the wrong display and it will raise an error

        equal_arrays_0 = (channels_0 == channels_bl_0).all()
        equal_arrays_1 = (channels_1 == channels_bl_1).all()
        equal_arrays_2 = (channels_2 == channels_bl_2).all()

        if(equal_arrays_0==True and equal_arrays_1==True and equal_arrays_2==True):
            print("The displays you are using have the same structures of the baselines. all good!")
        else:
            print("Error! you are not using the right baseline!")
            if(equal_arrays_0==False):
                print("Display 0 is wrong!")
            if(equal_arrays_1==False):
                print("Display 1 is wrong!")
            if(equal_arrays_2==False):
                print("Display 2 is wrong!")

        threshold_std = 0.68
        threshold_rms = 0.34

        faulty_sigma_0 = []
        channel_0_sigma_alarms = []
        channel_0_sigma_perc = []

        ant.sigma_creator(channel_0_sigma_alarms, channel_0_sigma_perc, rms_0, bl_0_rms_array, 2, bl_0_std_array)

        channel_0_sigma_alarms = np.array(channel_0_sigma_alarms)
        channel_0_sigma_perc= np.array(channel_0_sigma_perc)

        ant.faulty_sigma_finder(faulty_sigma_0, channel_0_sigma_alarms, channel_0_sigma_perc, bl_0_rms_array)
        faulty_sigma_0 = np.array(faulty_sigma_0)

        faulty_sigma_1 = []
        channel_1_sigma_alarms = []
        channel_1_sigma_perc = []

        ant.sigma_creator(channel_1_sigma_alarms, channel_1_sigma_perc, rms_1, bl_1_rms_array, 2, bl_1_std_array)

        channel_1_sigma_alarms = np.array(channel_1_sigma_alarms)
        channel_1_sigma_perc= np.array(channel_1_sigma_perc)

        ant.faulty_sigma_finder(faulty_sigma_1, channel_1_sigma_alarms, channel_1_sigma_perc, bl_1_rms_array)
        faulty_sigma_1 = np.array(faulty_sigma_1)

        faulty_sigma_2 = []
        channel_2_sigma_alarms = []
        channel_2_sigma_perc = []

        ant.sigma_creator(channel_2_sigma_alarms, channel_2_sigma_perc, rms_2, bl_2_rms_array, 2, bl_2_std_array)

        channel_2_sigma_alarms = np.array(channel_2_sigma_alarms)
        channel_2_sigma_perc= np.array(channel_2_sigma_perc)

        ant.faulty_sigma_finder(faulty_sigma_2,channel_2_sigma_alarms, channel_2_sigma_perc, bl_2_rms_array)
        faulty_sigma_2 = np.array(faulty_sigma_2)

        alarm_file = h5.File(os.sep.join([path_dir_output, "alarm_file_2022_05_22.hdf5"]), 'w')
        alarm_file.create_dataset('faulty_sigma_0', data=faulty_sigma_0)
        alarm_file.create_dataset('faulty_sigma_1', data=faulty_sigma_1)
        alarm_file.create_dataset('faulty_sigma_2', data=faulty_sigma_2)
        alarm_file.close()

    def baseline_calculator(path_dir, path_dir_output):

        ant.file_checker(os.sep.join([path_dir, "std_display_0_2022_05_22.hdf5"]))
        ant.file_checker(os.sep.join([path_dir, "std_display_1_2022_05_22.hdf5"]))
        ant.file_checker(os.sep.join([path_dir, "std_display_2_2022_05_22.hdf5"]))
        ant.file_checker(os.sep.join([path_dir, "rms_display_0_2022_05_22.hdf5"]))
        ant.file_checker(os.sep.join([path_dir, "rms_display_1_2022_05_22.hdf5"]))
        ant.file_checker(os.sep.join([path_dir, "rms_display_2_2022_05_22.hdf5"]))

        print("successfully opened the files")

        bl_0 = h5.File(os.sep.join([path_dir_baseline, "std_display_0_2022_05_22.hdf5"]), 'r')
        bl_1 = h5.File(os.sep.join([path_dir_baseline, "std_display_1_2022_05_22.hdf5"]), 'r')
        bl_2 = h5.File(os.sep.join([path_dir_baseline, "std_display_2_2022_05_22.hdf5"]), 'r')
        bl_0_rms = h5.File(os.sep.join([path_dir_baseline, "rms_display_0_2022_05_22.hdf5"]), 'r')
        bl_1_rms = h5.File(os.sep.join([path_dir_baseline, "rms_display_1_2022_05_22.hdf5"]), 'r')
        bl_2_rms = h5.File(os.sep.join([path_dir_baseline, "rms_display_2_2022_05_22.hdf5"]), 'r')

        #now we evaluate the baseline for each channel and the baseline for each display
        #at this stage, it is just a lazy mean but later on I can do something more fancy is required

        mean_std_display_0 = []
        mean_std_display_1 = []
        mean_std_display_2 = []
        mean_rms_display_0 = []
        mean_rms_display_1 = []
        mean_rms_display_2 = []

        for i in range(std_bl_0.shape[1]):
            mean_std_display_0.append(np.mean(std_bl_0[:,i]))
            mean_rms_display_0.append(np.mean(rms_bl_0[:,i]))
    
        for i in range(std_bl_1.shape[1]):
            mean_std_display_1.append(np.mean(std_bl_1[:,i]))
            mean_rms_display_1.append(np.mean(rms_bl_1[:,i]))
    
        for i in range(std_bl_2.shape[1]):
            mean_std_display_2.append(np.mean(std_bl_2[:,i]))
            mean_rms_display_2.append(np.mean(rms_bl_2[:,i]))
    
        mean_std_display_0 = np.array(mean_std_display_0)
        mean_std_display_1 = np.array(mean_std_display_1)
        mean_std_display_2 = np.array(mean_std_display_2)
        mean_rms_display_0 = np.array(mean_rms_display_0)
        mean_rms_display_1 = np.array(mean_rms_display_1)
        mean_rms_display_2 = np.array(mean_rms_display_2)
        #now let's do a mean of all the mean arrays inside a display
        #that is basically the average value of the entire display
        #it is not the smartest way and it will be changed, but for now I use this

        total_std_mean_0 = np.mean(mean_std_display_0)
        total_std_mean_1 = np.mean(mean_std_display_1)
        total_std_mean_2 = np.mean(mean_std_display_2)
        total_rms_mean_0 = np.mean(mean_rms_display_0)
        total_rms_mean_1 = np.mean(mean_rms_display_1)
        total_rms_mean_2 = np.mean(mean_rms_display_2)

        #now I store the baseline values as hdf5 files

        hf_target = h5.File(os.sep.join([path_dir_output, "baselines_2022_05_22.hdf5"]), 'w')

        hf_target.create_dataset('mean_std_display_0', data=mean_std_display_0)
        hf_target.create_dataset('mean_std_display_1', data=mean_std_display_1)
        hf_target.create_dataset('mean_std_display_2', data=mean_std_display_2)
        hf_target.create_dataset('total_std_mean_0', data=total_std_mean_0)
        hf_target.create_dataset('total_std_mean_1', data=total_std_mean_1)
        hf_target.create_dataset('total_std_mean_2', data=total_std_mean_2)
        hf_target.create_dataset('mean_rms_display_0', data=mean_rms_display_0)
        hf_target.create_dataset('mean_rms_display_1', data=mean_rms_display_1)
        hf_target.create_dataset('mean_rms_display_2', data=mean_rms_display_2)
        hf_target.create_dataset('total_rms_mean_0', data=total_rms_mean_0)
        hf_target.create_dataset('total_rms_mean_1', data=total_rms_mean_1)
        hf_target.create_dataset('total_rms_mean_2', data=total_rms_mean_2)
        hf_target.create_dataset('channels_bl_0', data=channels_bl_0)
        hf_target.create_dataset('channels_bl_1', data=channels_bl_1)
        hf_target.create_dataset('channels_bl_2', data=channels_bl_2)

        hf_target.close()
        



	
