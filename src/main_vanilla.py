from src.benchmarking.vanilla.benchmark_vanilla import check_and_benchmark
import sys

# RANDOM BIG MAT

import numpy as np


size = 100
sec_size = 5

mat = np.random.randint(2, size=(size, size)).tolist()

print(f"{mat[0][1]} {sys.getsizeof(mat[0][1])}")
print(sys.getsizeof(mat))

sum = 0
for i in range(0, size):
    for j in range(0, size):
        sum += sys.getsizeof(mat[i][j])

print(sum)

opt_mat, circuit, _, process_time, initial_rss, final_rss = check_and_benchmark(mat, sec_size)

print(sum)


print(f"process time: {process_time} seconds")
print(f"initial memory: {initial_rss / 1048576} mb")
print(f"final memory: {final_rss / 1048576} mb")

import os
import psutil
from src.algorithm.vanilla.cnot_synthesis import cnot_synthesis

pid = os.getpid()
ps = psutil.Process(pid)

print(ps.num_threads())