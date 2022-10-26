import sys
from AnalyserTools import AnalyserTools as ant
from BenchmarkFunctions import BenchmarkFunctions as bcf

bcf.time_files_producer_benchmark(int(sys.argv[1]), int(sys.argv[2]), "/home/svergani/monitoring/files_3_2/pip_files_baseline", "/home/svergani/monitoring/files_3_2/try_baseline")