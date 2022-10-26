import os
import pandas as pd
import h5py as h5
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
from datetime import datetime
#from tables import *
from mpl_toolkits import mplot3d
from matplotlib.ticker import MaxNLocator
from AnalyserTools import AnalyserTools as ant

class BenchmarkFunctions:
    
    
    @staticmethod
    def time_files_producer_benchmark(process, amount, path_dir, path_output):
        print("process ",process)
        print("amount ",amount)
        if(process==0):
            print("benchmark will be evaluated for the monitor alarm")
        if(process!=0):
            print("ERROR! the process values go from 0 to 0")
            return None
        #######create arrays containing the names of the files you need
        target_0_rms_name_array=ant.file_looper_amount(path_dir, "rms-0", amount)
        target_1_rms_name_array=ant.file_looper_amount(path_dir, "rms-1", amount)
        target_2_rms_name_array=ant.file_looper_amount(path_dir, "rms-2", amount)
        target_0_std_name_array=ant.file_looper_amount(path_dir, "std-0", amount)
        target_1_std_name_array=ant.file_looper_amount(path_dir, "std-1", amount)
        target_2_std_name_array=ant.file_looper_amount(path_dir, "std-2", amount)
        for i in range(len(target_0_rms_name_array)):
            print("target_0_rms_name_array[",i,"] ",target_0_rms_name_array[i])
        ######extract the values of the channels
        target_0_rms_name = ant.file_looper(path_dir, "rms-0")
        target_1_rms_name = ant.file_looper(path_dir, "rms-1")
        target_2_rms_name = ant.file_looper(path_dir, "rms-2")
        
        f_0 = h5.File(os.sep.join([path_dir, target_0_rms_name]), "r")
        channels_0 = np.array(f_0.get('data/axis0').value)
        f_1 = h5.File(os.sep.join([path_dir, target_1_rms_name]), "r")
        channels_1 = np.array(f_1.get('data/axis0').value)
        f_2 = h5.File(os.sep.join([path_dir, target_2_rms_name]), "r")
        channels_2 = np.array(f_2.get('data/axis0').value)
        #########################
        std_0 = np.array(ant.time_file_creator_bis(path_dir,target_0_std_name_array,channels_0))
        std_1 = np.array(ant.time_file_creator_bis(path_dir,target_1_std_name_array,channels_1))
        std_2 = np.array(ant.time_file_creator_bis(path_dir,target_2_std_name_array,channels_2))
        rms_0 = np.array(ant.time_file_creator_bis(path_dir,target_0_rms_name_array,channels_0))
        rms_1 = np.array(ant.time_file_creator_bis(path_dir,target_1_rms_name_array,channels_1))
        rms_2 = np.array(ant.time_file_creator_bis(path_dir,target_2_rms_name_array,channels_2))
        #creating hdf5 containing all these pieces of information
        hf_target = h5.File(os.sep.join([path_output, "baseline_values_"+"{:%Y_%m_%d_%H_%M_%S}".format(datetime.now())+".hdf5"]), 'w')
        hf_target.create_dataset('channels_0', data=channels_0)
        hf_target.create_dataset('channels_1', data=channels_1)
        hf_target.create_dataset('channels_2', data=channels_2)
        hf_target.create_dataset('std_0', data=std_0)
        hf_target.create_dataset('std_1', data=std_1)
        hf_target.create_dataset('std_2', data=std_2)
        hf_target.create_dataset('rms_0', data=rms_0)
        hf_target.create_dataset('rms_1', data=rms_1)
        hf_target.create_dataset('rms_2', data=rms_2)  
        hf_target.close() 
        
        