import sys
from AnalyserTools import AnalyserTools as ant
from BenchmarkFunctions import BenchmarkFunctions as bcf
from AnalyserFunctions import AnalyserFunctions as anf

#call it in this way: python3 benchmarkmaker.py <process_number> <amount_of_data> e.g. python3 benchmarkmaker.py 0 10

baseline_initial_files_dir ="/home/svergani/monitoring/files_3_2/pip_files_baseline" #for pip is "/home/pip/DQM_Analysis_Package/testDB/input_files"
baseline_work_dir = "/home/svergani/monitoring/files_3_2/try_pre_baseline" #for pip is "/home/pip/DQM_Analysis_Package/testDB/analysis_work_dir"
baseline_folder_dir = "/home/svergani/monitoring/files_3_2/try_pre_baseline" #for pip is "/home/pip/DQM_Analysis_Package/testDB/benchmark_files"

bcf.time_files_producer_benchmark(int(sys.argv[1]), int(sys.argv[2]), baseline_initial_files_dir, baseline_work_dir)

bcf.baseline_calculator(baseline_work_dir, baseline_folder_dir)