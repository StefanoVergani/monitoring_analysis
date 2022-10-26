#from multiprocess import Process #, Queue
import multiprocess
import time
import traceback
import inotify.adapters
import json
import configparser
from AnalyserTools import AnalyserTools
from AnalyserFunctions import AnalyserFunctions

class Process(multiprocess.Process):

    def __init__(self, *args, **kwargs):
        multiprocess.Process.__init__(self, *args, **kwargs)
        self._pconn, self._cconn = multiprocess.Pipe()
        self._exception = None

    def run(self):
        try:
            multiprocess.Process.run(self)
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

def fun1(filename, outdir):
    print("FUN1:")
    #target_0 = h5.file("/home/svergani/monitoring/hdf5_created_files/std_display_0_2022_05_22.hdf5",r)
    print("middle check")
    print(filename)
    print(outdir)

def test_function(filename, outdir):
    print('path dir is ', path_dir)
    print('path out is ', path_dir_output)

def fun2(filename, outdir):
    print("FUN2:")
    print(filename)
    print(outdir)

#def watch(dir):
#    i = inotify.adapters.Inotify()
#
#    i.add_watch(dir)
#
#    for event in i.event_gen(yield_nones=False):
#        (_, type_names, path, filename) = event
#
#        event_typename = "{}".format(type_names)
#        
#        if (event_typename == "['IN_MODIFY']"): 
#          print("New file created!")
#          print("{}".format(filename))
#
#        print("PATH=[{}] FILENAME=[{}] EVENT_TYPES={}".format(
#              path, filename, type_names))

def watch_and_process(process, indir, outdir, cache_file, cache_data):
    i = inotify.adapters.Inotify()

    i.add_watch(indir)

    counter=0

    for event in i.event_gen(yield_nones=False):
        (_, type_names, path, filename) = event

        event_typename = "{}".format(type_names)

       ######things in this if means that the code gets triggered only if new files are introduced 
        #if not cache_data:
        #    print("CHACHE IS EMPTY!") 
        if (event_typename == "['IN_MODIFY']"):
            counter = counter +1
            process(indir, outdir, cache_file, cache_data, filename)
            #if counter==3:
            #    process(indir, outdir, cache, filename)

          #try:
          #  process(filename, outdir)
          #except:
          #  print("oh noooo")
          #  #raise BaseException("Process failed")


#--------------------------
if __name__ == '__main__':

    parser = configparser.ConfigParser()
    parser.read("analyser_config.txt")
    
    processes      = parser.get("config", "process_list")
    input_dirs     = parser.get("config", "process_input")
    output_dirs    = parser.get("config", "process_output")
    prefixes       = parser.get("config", "process_prefix")

    processes_list      = json.loads(processes)
    input_dirs_list     = json.loads(input_dirs)
    output_dirs_list    = json.loads(output_dirs)
    prefixes_list       = json.loads(prefixes)

    print(processes_list)
    print(input_dirs_list)
    print(output_dirs_list)
    print(prefixes_list)

    processDictionary = {"process_1":fun1, "triggers_producer": AnalyserFunctions.triggers_producer,"baseline_calculator":AnalyserFunctions.baseline_calculator,"time_files_producer":AnalyserFunctions.time_files_producer}
    #activeProcessList = []
    
   

    for i, processKey in enumerate(processes_list):
      cache_file = []
      cache_data = [] 
      input_dir = input_dirs_list[i]
      output_dir = output_dirs_list[i]
      process_prefix = prefixes_list[i]
      proc = Process(target=watch_and_process, args=[processDictionary[processKey],input_dir,output_dir,cache_file,cache_data])
      #prefix_dump_list=s.split(',')
      #int green_light = 0
      #for j in range(prefix_dump_list.size()):
      #    if(if prefix_dump_list[j] in filename):
      #        green_light = 1

      #proc = Process(target=processDictionary[processKey], args=[input_dir, output_dir, cache])

      #if(green_light==1):
      #    proc.start()
      proc.start()

    try:
      proc.join()
      if proc.exception:
        raise proc.exception
    except Exception as e:
      print( "Exception caught!" )


    #try:
    #  proc.join()
    #  #if proc.exception:
    #  #    raise proc.exception
    #except Exception as e:
    #  print( "Exception caught!" )
    #  raise e
    #  #print("Shutting down")
    #  #for process in activeProcessList:
    #  #  process.join()
    #  #  process.kill()



    
    #p1 = Process(target=watch, args=['test_dir_1'])
    #p1.start()
    #p1.join(0)
    #p2 = Process(target=watch, args=['test_dir_2'])
    #p2.start()
    #p2.join(0)
