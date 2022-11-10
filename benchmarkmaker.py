import sys
from AnalyserTools import AnalyserTools as ant
from BenchmarkFunctions import BenchmarkFunctions as bcf
from AnalyserFunctions import AnalyserFunctions as anf

#call it in this way: python3 benchmarkmaker.py <process_number> <amount_of_data> e.g. python3 benchmarkmaker.py 0 10

bcf.time_files_producer_benchmark(int(sys.argv[1]), int(sys.argv[2]), "/home/pip/DQM_Analysis_Package/testDB/input_files", "/home/pip/DQM_Analysis_Package/testDB/analysis_work_dir")

bcf.baseline_calculator("/home/pip/DQM_Analysis_Package/testDB/analysis_work_dir", "/home/pip/DQM_Analysis_Package/testDB/benchmark_files")
