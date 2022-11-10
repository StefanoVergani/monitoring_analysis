#from multiprocess import Process #, Queue
#import multiprocess
from multiprocessing import Process, Manager, Pipe
import time
import datetime
import traceback
import inotify.adapters
import json
import configparser
from AnalyserTools import AnalyserTools
from AnalyserFunctions import AnalyserFunctions
from Assembler import Assembler

class process(Process):

    def __init__(self, *args, **kwargs):
        #multiprocess.Process.__init__(self, *args, **kwargs)
        Process.__init__(self, *args, **kwargs)
        #self._pconn, self._cconn = multiprocess.Pipe()
        self._pconn, self._cconn = Pipe()
        self._exception = None

    def run(self):
        try:
            #multiprocess.Process.run(self)
            Process.run(self)
            self._cconn.send(None)
        except Exception as e:
            tb = traceback.format_exc()
            self._cconn.send((e, tb))
            print(tb)
            #raise e  # You can still rise this exception if you need to

    @property
    def exception(self):
        if self._pconn.poll():
            self._exception = self._pconn.recv()
        return self._exception


def testfunc(process_inputs, process_outdir, process_cache, custom_config):
    print("-------------------------------------------------------------")
    print("Process iteration @ " + str(datetime.datetime.now()))
    if (len(process_inputs) > 0):
      print("Custom config says:")
      for config_item in custom_config:
        print(str(config_item))
      for input_list in process_inputs:
        for input_file in input_list:
          print("FILE: " + str(input_file) + " HAS BEEN CHOSEN FOR " + str(process_outdir))
      if (len(process_cache) == 0):
        process_cache.append(1)
      else:
        process_cache[0] += 1
      print("Successful triggers: " + str(process_cache[0]))
      return
    else:
      print("No new input to process")
      return
   

#NO LONGER USED: fn to process directly from inotify trigger
#-----------------------------------------------------------
#def watch_and_process(process, indir, outdir, cache_file, cache_data):
#    i = inotify.adapters.Inotify()
#
#    i.add_watch(indir)
#
#    counter=0
#
#    for event in i.event_gen(yield_nones=False):
#        (_, type_names, path, filename) = event
#
#        event_typename = "{}".format(type_names)
#
#        if (event_typename == "['IN_MODIFY']"):
#            counter = counter +1
#            process(indir, outdir, cache_file, cache_data, filename)


def watch_and_cache(cache, indir):
    i = inotify.adapters.Inotify()

    i.add_watch(indir)

    counter=0

    for event in i.event_gen(yield_nones=False):
        (_, type_names, path, filename) = event

        event_typename = "{}".format(type_names)

        if (event_typename == "['IN_MODIFY']"):
           print("Received file " + str(filename))
           cache_pair = (filename, datetime.datetime.now())
           cachecopy = cache
           cachecopy.append(cache_pair)
           cache[:] = cachecopy
           #print("Cache:")
           #print(cache)

def execute_from_cache(process, process_cache, input_cache, process_prefix_list, process_indir, process_outdir, deltat_accept, interval, custom_config):
    while True:
      #print(input_cache)
      print("Assembling input for process " + str(process))
      process_inputs = Assembler(input_cache, process_prefix_list, deltat_accept)
      if(process_inputs):
        process(process_inputs, process_indir, process_outdir, process_cache, custom_config)
      time.sleep(interval)

#--------------------------
if __name__ == '__main__':

    parser = configparser.ConfigParser()
    parser.read("alarm_assembler_config.txt")
    
    processes      = parser.get("config", "process_list")
    input_dirs     = parser.get("config", "process_input")
    output_dirs    = parser.get("config", "process_output")
    prefixes       = parser.get("config", "process_prefixes")
    acceptances    = parser.get("config", "process_accept")
    intervals      = parser.get("config", "process_interval")
    custom         = parser.get("config", "process_custom")

    processes_list      = json.loads(processes)
    input_dirs_list     = json.loads(input_dirs)
    output_dirs_list    = json.loads(output_dirs)
    prefix_lists        = json.loads(prefixes)
    acceptance_list     = json.loads(acceptances)
    interval_list       = json.loads(intervals)
    custom_list         = json.loads(custom)

    processDictionary = {"test_process":testfunc, "triggers_producer": AnalyserFunctions.triggers_producer}
    threadmanager = Manager()
    
    for i, processKey in enumerate(processes_list):
      input_cache   = threadmanager.list()
      process_cache = threadmanager.list()
      input_dir     = input_dirs_list[i]
      output_dir    = output_dirs_list[i]
      prefix_list   = prefix_lists[i]
      deltat_accept = acceptance_list[i]
      interval      = interval_list[i]
      custom_config = custom_list[i]

      #Set up an inotify watch on the input directory, depositing new files of interest into the cache.
      watch_proc = process(target=watch_and_cache, args=[input_cache,input_dir])
      watch_proc.start()
      #Set up the analysis itself to run periodically over what it sees in the cache.
      analyser_proc = process(target=execute_from_cache, args=[processDictionary[processKey],process_cache,input_cache,prefix_list,input_dir,output_dir,deltat_accept,interval,custom_config])
      analyser_proc.start()

    try:
      watch_proc.join()
      if watch_proc.exception:
        raise watch_proc.exception
    except Exception as e:
      print( "Exception caught in watcher!" )

    try:
      analyser_proc.join()
      if analyser_proc.exception:
        raise analyser_proc.exception
    except Exception as e:
      print( "Exception caught in analyser!" )
