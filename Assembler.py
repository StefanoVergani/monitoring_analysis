import threading
import time
import datetime

def prefix_match_list(filename, prefix_list):
    taglist = tuple(prefix_list)
    if filename.startswith(prefix_list):
      return 1
    else:
      return 0

def prefix_match_single(filename, prefix):
    if filename.startswith(prefix):
      return 1
    else:
      return 0

def extract_timestamp(filename):
    timestamp_str = filename[-18:]
    year = int('20' + timestamp_str[0:2])
    month  = int(timestamp_str[2:4]) 
    day    = int(timestamp_str[4:6])
    hour   = int(timestamp_str[7:9])
    minute = int(timestamp_str[9:11])
    second = int(timestamp_str[11:13])
    timestamp = datetime.datetime(year, month, day, hour, minute, second)
    return timestamp

def prune(cache, timeout):
    cachecopy = cache
    for filename_pair in cachecopy:
      now = datetime.datetime.now()
      timestamp = filename_pair[1]
      delta_t = now - timestamp
      if (delta_t.total_seconds() > timeout):
        print ("File " + str(filename_pair[0]) + " has exceeded allowed time of " + str(timeout) + " in cache. DELETING.")
        cachecopy.remove(filename_pair)
    return cachecopy

def snip(cache, shortlists):
    cachecopy = cache
    for shortlist in shortlists:
      for filename_pair in shortlist:
        #print("Removing " + str(filename_pair[0]) + " from cache")
        for cache_filename_pair in cache:
          if (str(filename_pair[0]) == str(cache_filename_pair[0])):
            cachecopy.remove(cache_filename_pair)
    return cachecopy

def Assembler(cache, prefix_list, delta_t_acc, timeout=60.0, backlog_mode=0):
    #interval = 5.0
    #threading.Timer(interval, Assembler(cache, delta_t_acc, timeout, backlog_mode)).start()

    #Build shortlist of matching files in cache
    input_shortlist = []
    for prefix in prefix_list:
      prefix_shortlist = []
      for filename_pair in cache:
        filename = filename_pair[0]
        if prefix_match_single(filename, prefix):
          time_pair = (filename, extract_timestamp(filename))
          prefix_shortlist.append(time_pair)
      #Sort list in time, most recent first
      prefix_shortlist.sort(key = lambda x: x[1])
      prefix_shortlist.reverse()
      #Add list to matrix
      input_shortlist.append(prefix_shortlist)

    #print("Final input shortlist:")
    #print(input_shortlist)

    #Check for correct no. of files
    prefix_filecounts = []
    prefix_index = 0
    for prefix in prefix_list:
      prefix_filecount = 0
      for infile in input_shortlist[prefix_index]:
        filename = str(infile[0])
        if filename.startswith(prefix):
          prefix_filecount += 1
      if (prefix_filecount == 0):
          #print ("No input for required filetype: " + prefix + "-<timestamp>.hdf5")
          emptylist = []
          return emptylist
      prefix_filecounts.append(prefix_filecount)
      prefix_index += 1

    #Build complete sets, starting from most recent files in cache
    #Author's note: this code is written under the assumption that any complete set of input files for a process should be separated from the next set by T >> delta_t.
    #If analyses are defined with sampling on the scale of delta_t then this code will need to be upgraded with more robust combinatorics
    #but ask yourself why you need to do that please :'(
    process_shortlists = []
    for file1 in input_shortlist[0]:
      timestamp1 = file1[1]
      process_shortlist = []
      process_shortlist.append(file1)

      prefix_index = 0
      for prefix_shortlist in input_shortlist:
        if (prefix_index == 0):
          prefix_index += 1
          continue
        else:
          delta_t_min = datetime.timedelta.max
          nearest_index = -1
          current_index = 0
          for file2 in prefix_shortlist:
            timestamp2 = file2[1]
            delta_t = timestamp1 - timestamp2
            #Check within acceptance window
            if (abs(delta_t.total_seconds()) < delta_t_acc):
              #Look for closest match
              if (delta_t < delta_t_min):
                delta_t_min = delta_t
                nearest_index = current_index
            current_index += 1
          if (nearest_index != -1):
            chosen_file = prefix_shortlist.pop(nearest_index)
            process_shortlist.append(chosen_file)
            prefix_index += 1
          else:
            prefix_index += 1
            continue
        
      if (len(process_shortlist) == len(prefix_list)):
        process_shortlists.append(process_shortlist)

    if (backlog_mode): #Return all valid groups of files found in the cache
      cache = prune(cache, timeout)
      cache = snip(cache, process_shortlists)
      return process_shortlists

    else: #Return only the most recent group of files found in the cache
      trunc_process_shortlists = []
      trunc_process_shortlists.append(process_shortlists[0])

      shortlist_index = 0
      for process_shortlist in process_shortlists:
        if (shortlist_index == 0):
          continue
        else:
          for infile in process_shortlist:
            cache.remove(infile[0])
        shortlist_index += 1

      cache = prune(cache, timeout)
      #print("Final selection:")
      #print(trunc_process_shortlists)
      cache = snip(cache, trunc_process_shortlists)
      return trunc_process_shortlists


#def test():
#    cache = [("testfile-1-221101-164101.hdf5", datetime.datetime.now()),("testfile-2-221101-164102.hdf5", datetime.datetime.now()),("testfile-3-221101-164103.hdf5", datetime.datetime.now()),("wrongfile-1-221101-164100.hdf5",datetime.datetime.now()),("testfile-1-221101-174100.hdf5",datetime.datetime.now())]
#
#    interval = 5.0
#    while True:
#      print("CURRENT CACHE:")
#      print(cache)
#      print("Running assembler.")
#      Assembler(cache, 5.0)
#      print("Assembler completed.")
#      time.sleep(interval)
#
#test()
#      
