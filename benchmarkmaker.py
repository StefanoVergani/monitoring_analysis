import sys
from AnalyserTools import AnalyserTools as ant
from BenchmarkFunctions import BenchmarkFunctions as bcf
from AnalyserFunctions import AnalyserFunctions as anf

#call it in this way: python3 benchmarkmaker.py <process_number> <amount_of_data> e.g. python3 benchmarkmaker.py 0 10

bcf.time_files_producer_benchmark(int(sys.argv[1]), int(sys.argv[2]), "/home/svergani/monitoring/files_3_2/pip_files_baseline", "/home/svergani/monitoring/files_3_2/try_pre_baseline")

bcf.baseline_calculator("/home/svergani/monitoring/files_3_2/try_pre_baseline", "/home/svergani/monitoring/files_3_2/try_pre_baseline")