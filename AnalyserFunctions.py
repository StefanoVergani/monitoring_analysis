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

        ant.slash_converter(path_dir)
        ant.slash_converter(path_dir_output)
    
        ant.file_checker(os.sep.join([path_dir, "std_display_0_2022_05_22.hdf5"]))
        ant.file_checker(os.sep.join([path_dir, "std_display_1_2022_05_22.hdf5"]))
        ant.file_checker(os.sep.join([path_dir, "std_display_2_2022_05_22.hdf5"]))
        ant.file_checker(os.sep.join([path_dir, "rms_display_0_2022_05_22.hdf5"]))
        ant.file_checker(os.sep.join([path_dir, "rms_display_1_2022_05_22.hdf5"]))
        ant.file_checker(os.sep.join([path_dir, "rms_display_2_2022_05_22.hdf5"]))
        ant.file_checker(os.sep.join([path_dir_output, "benchmarks/baselines_2022_05_22.hdf5"]))

        target_0 = h5.File(os.sep.join([path_dir, "std_display_0_2022_05_22.hdf5"]), 'r')
        target_1 = h5.File(os.sep.join([path_dir, "std_display_1_2022_05_22.hdf5"]), 'r')
        target_2 = h5.File(os.sep.join([path_dir, "std_display_2_2022_05_22.hdf5"]), 'r')
        target_0_rms = h5.File(os.sep.join([path_dir, "rms_display_0_2022_05_22.hdf5"]), 'r')
        target_1_rms = h5.File(os.sep.join([path_dir, "rms_display_1_2022_05_22.hdf5"]), 'r')
        target_2_rms = h5.File(os.sep.join([path_dir, "rms_display_2_2022_05_22.hdf5"]), 'r')
        baselines = h5.File(os.sep.join([path_dir_output, "benchmarks/baselines_2022_05_22.hdf5"]), 'r')

        print("files has been opened")

        #std over time from file
        std_0 = np.array(target_0.get('std_display_0').value)
        std_1 = np.array(target_1.get('std_display_1').value)
        std_2 = np.array(target_2.get('std_display_2').value)
        #rms over time from file
        rms_0 = np.array(target_0_rms.get('rms_display_0').value)
        rms_1 = np.array(target_1_rms.get('rms_display_1').value)
        rms_2 = np.array(target_2_rms.get('rms_display_2').value)
        #channel numbers from file
        channels_0 = np.array(target_0.get('channels_0').value)
        channels_1 = np.array(target_1.get('channels_1').value)
        channels_2 = np.array(target_2.get('channels_2').value)
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

    #this function opens one file containing the std and one the rms, and it takes only the latest elements. If the rms for a given pixel is more than n std and this happens in two suqsequent
    #pixels, than it raises an alarm. It then assignes the value 1 to alarmed pixels and 0 to the others. It saves these values on a hdf5 files.
    @staticmethod
    def triggers_producer(inputs, path_dir, path_dir_output, cache_data, custom_config):
    #def triggers_producer(path_dir, path_dir_output, cache_file, cache_data, filename):

        #benchmark_dir = "/home/pip/DQM_Analysis_Package/testDB/benchmark_files"
        benchmark_dir = path_dir_out+"benchmark_files"

        #OBSOLETE - assembler handles this now
        #-----------------------------------------------
        #cache_file.append(filename)
        #print('len(cache_file) ',len(cache_file))
        #print('cache_file ',cache_file)
        #if(len(cache_file)<6):
        #    return 17
        #
        #cache_file.clear()

        #ant.slash_converter(path_dir)
        #ant.slash_converter(path_dir_output)

        #target_0_rms_name=ant.file_looper(path_dir, "rms-0")
        #target_1_rms_name=ant.file_looper(path_dir, "rms-1")
        #target_2_rms_name=ant.file_looper(path_dir, "rms-2")
        #baselines_name = ant.file_looper(path_dir_output, "baselines_")
        #---------------------------------------------------------------

        print("Inputs:")
        print(inputs)
        print("inputs[0]:")
        print(inputs[0])
        print("inputs[0][0]:")
        print(inputs[0][0])
        target_0_rms_name = inputs[0][0][0]
        target_1_rms_name = inputs[0][1][0]
        target_2_rms_name = inputs[0][2][0]
        baselines_name = ant.file_looper(benchmark_dir, "baselines_")

        #print('Trigger: ',filename,' ',target_0_rms_name)
        #print('Trigger: ',filename,' ',target_1_rms_name)
        #print('Trigger: ',filename,' ',target_2_rms_name)
        print('Baseline: ',baselines_name)

        #here I am checking that those files exist
        ant.file_checker(os.sep.join([path_dir, target_0_rms_name]))
        ant.file_checker(os.sep.join([path_dir, target_1_rms_name]))
        ant.file_checker(os.sep.join([path_dir, target_2_rms_name]))
        #ant.file_checker(os.sep.join([path_dir_output, baselines_name]))
        ant.file_checker(os.sep.join([benchmark_dir, baselines_name]))
        #here I am opening the files and writing a confirmation message
        target_0_rms = h5.File(os.sep.join([path_dir, target_0_rms_name]), 'r')
        target_1_rms = h5.File(os.sep.join([path_dir, target_1_rms_name]), 'r')
        target_2_rms = h5.File(os.sep.join([path_dir, target_2_rms_name]), 'r')
        #baselines = h5.File(os.sep.join([path_dir_output, baselines_name]), 'r')
        baselines = h5.File(os.sep.join([benchmark_dir, baselines_name]), 'r')

        #print(filename,' ',"files have been opened")

        channels_0 = np.array(target_0_rms.get('data/axis0')[()])
        channels_1 = np.array(target_1_rms.get('data/axis0')[()])
        channels_2 = np.array(target_2_rms.get('data/axis0')[()])

        rms_0=np.array(ant.std_extractor((os.sep.join([path_dir, target_0_rms_name])),channels_0))
        rms_1=np.array(ant.std_extractor((os.sep.join([path_dir, target_1_rms_name])),channels_1))
        rms_2=np.array(ant.std_extractor((os.sep.join([path_dir, target_2_rms_name])),channels_2))

        #std baselines per channel
        bl_0_std_array = np.array(baselines.get('mean_std_display_0')[()])
        bl_1_std_array = np.array(baselines.get('mean_std_display_1')[()])
        bl_2_std_array = np.array(baselines.get('mean_std_display_2')[()])
        #rms baselines per channel
        bl_0_rms_array = np.array(baselines.get('mean_rms_display_0')[()])
        bl_1_rms_array = np.array(baselines.get('mean_rms_display_1')[()])
        bl_2_rms_array = np.array(baselines.get('mean_rms_display_2')[()])
        #channel numbers from baselines
        channels_bl_0 = baselines.get('channels_bl_0')[()]
        channels_bl_1 = baselines.get('channels_bl_1')[()]
        channels_bl_2 = baselines.get('channels_bl_2')[()]

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

        how_many_std = 2

        triggers_0 = []
        triggers_1 = []
        triggers_2 = []
        triggers_0 = ant.triggering_pixel_finder(rms_0, bl_0_rms_array, bl_0_std_array, channels_0,how_many_std)
        triggers_1 = ant.triggering_pixel_finder(rms_1, bl_1_rms_array, bl_1_std_array, channels_1,how_many_std)
        triggers_2 = ant.triggering_pixel_finder(rms_2, bl_2_rms_array, bl_2_std_array, channels_2,how_many_std)


        print("checkpoint A")
        #I create a matrix following the official structure: array with display numbers, array with channel numbers, matrix size (1)

        triggers_matrix = []
        triggers_matrix = ant.structured_matrix_1D(triggers_0,triggers_1,triggers_2)

        if not cache_data:
            print("checkpoint B")
            cache_data.append(triggers_matrix)
        else:
            print("checkpoint C")
            triggers_matrix_before = []
            triggers_matrix_before = cache_data
            #cache_data.clear()
            cache_data[:] = []
            cache_data.append(triggers_matrix)
            alarm_pixel = []
            alarm_pixel = ant.alarm_creator(triggers_matrix_before,triggers_matrix,target_0_rms.get('data/axis0')[()],target_1_rms.get('data/axis0')[()],target_2_rms.get('data/axis0')[()])
            alarm_pixel_0 = alarm_pixel[0]
            alarm_pixel_1 = alarm_pixel[1]
            alarm_pixel_2 = alarm_pixel[2]
            #now it creates a hdf5 file containing the alarms
            print(path_dir_output)
            f_2 = h5.File(os.sep.join([path_dir_output, "alarms_"+"{:%Y_%m_%d_%H_%M_%S}".format(datetime.now())+".hdf5"]), 'w')
            f_2.create_dataset('alarm_pixel_0', data=alarm_pixel_0)
            f_2.create_dataset('alarm_pixel_1', data=alarm_pixel_1)
            f_2.create_dataset('alarm_pixel_2', data=alarm_pixel_2)
            f_2.create_dataset('channels_0',data=channels_0)
            f_2.create_dataset('channels_1',data=channels_1)
            f_2.create_dataset('channels_2',data=channels_2)
            f_2.close()
            
           
         


    def baseline_calculator(path_dir, path_dir_output, cache_file, cache_data, filename):

        ant.slash_converter(path_dir)
        ant.slash_converter(path_dir_output)
        
        baseline_value_file_name=ant.file_looper(path_dir,"baseline_values_")
        print('baseline_value_file_name ',baseline_value_file_name)

        ant.file_checker(os.sep.join([path_dir, baseline_value_file_name]))
        
        print("os.sep.join([path_dir, baseline_value_file_name]) ",os.sep.join([path_dir, baseline_value_file_name]))

        bl_file = h5.File(os.sep.join([path_dir, baseline_value_file_name]), 'r')

        #here some issues with trigger

        std_bl_0 = np.array(bl_file.get('std_0').value)
        std_bl_1 = np.array(bl_file.get('std_1').value)
        std_bl_2 = np.array(bl_file.get('std_2').value)
        rms_bl_0 = np.array(bl_file.get('rms_0').value)
        rms_bl_1 = np.array(bl_file.get('rms_1').value)
        rms_bl_2 = np.array(bl_file.get('rms_2').value)
        channels_bl_0 = np.array(bl_file.get('channels_0').value)
        channels_bl_1 = np.array(bl_file.get('channels_1').value)
        channels_bl_2 = np.array(bl_file.get('channels_2').value)

        print('std_bl_0.shape ',std_bl_0.shape)

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

        #now I store the baseline values as hdf5 file

        #hf_target = h5.File(os.sep.join([path_dir_output, "benchmarks/baselines_"+"{:%Y_%m_%d_%H_%M_%S}".format(datetime.now())+".hdf5"]), 'w')
        hf_target = h5.File(os.sep.join([path_dir_output, benchmark_dir+"baselines_"+"{:%Y_%m_%d_%H    _%M_%S}".format(datetime.now())+".hdf5"]), 'w')

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



    def time_files_producer(path_dir, path_dir_output, cache_file, cache_data, filename):
         
        ant.slash_converter(path_dir)
        ant.slash_converter(path_dir_output)
        ####super lazy way to extract the channels, it will be soon changed
        #path_dir_0: str = r"/home/svergani/monitoring/files/rmsm_display_0/"
        #path_dir_1: str = r"/home/svergani/monitoring/files/rmsm_display_1/"
        #path_dir_2: str = r"/home/svergani/monitoring/files/rmsm_display_2/"
        path_dir_0: str = r"/home/pip/DQM_Analysis_Package/testDB/input_files/"
        path_dir_1: str = r"/home/pip/DQM_Analysis_Package/testDB/input_files/"
        path_dir_2: str = r"/home/pip/DQM_Analysis_Package/testDB/input_files/"

        f_0 = h5.File(os.sep.join([path_dir_0, "rmsm_display-0-220525-151538.hdf5"]), "r")
        channels_0 = np.array(f_0.get('data/axis0').value)
        f_1 = h5.File(os.sep.join([path_dir_1, "rmsm_display-1-220525-151538.hdf5"]), "r")
        channels_1 = np.array(f_1.get('data/axis0').value)
        f_2 = h5.File(os.sep.join([path_dir_2, "rmsm_display-2-220525-151538.hdf5"]), "r")
        channels_2 = np.array(f_2.get('data/axis0').value)
        ####################################################################
        #I should add some checks that the same amount of std and rms files are received before getting triggered
        std_0 = np.array(ant.time_file_creator(path_dir,channels_0,"std-0"))
        std_1 = np.array(ant.time_file_creator(path_dir,channels_1,"std-1"))
        std_2 = np.array(ant.time_file_creator(path_dir,channels_2,"std-2"))
        rms_0 = np.array(ant.time_file_creator(path_dir,channels_0,"rms-0"))
        rms_1 = np.array(ant.time_file_creator(path_dir,channels_0,"rms-0"))
        rms_2 = np.array(ant.time_file_creator(path_dir,channels_0,"rms-0"))
        #creating hdf5 containing all these pieces of information
        hf_target = h5.File(os.sep.join([path_dir_output, "baseline_values_"+"{:%Y_%m_%d_%H_%M_%S}".format(datetime.now())+".hdf5"]), 'w')
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

        



	
