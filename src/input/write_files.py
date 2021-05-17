import os
import psutil
from src.input.circuits_and_matrices import rand_circuit
from src.input.integer_matrices import rand_int_matrix



def write_circuit_file(size, num_gates, path):

    pid = os.getpid()
    ps = psutil.Process(pid)

    initial_cpu_times = ps.cpu_times()
    circuit = rand_circuit(size, num_gates)
    final_cpu_times = ps.cpu_times()

    process_time = final_cpu_times.user + final_cpu_times.system - initial_cpu_times.user - initial_cpu_times.system

    file = open(path, 'w')
    file.write(f'Circuit size: {size}\n')
    file.write(f'Generation time (seconds): {process_time}\n')

    file.write(f'{circuit}\n')

    file.close()


def write_int_matrix_file(size, num_gates, path):

    pid = os.getpid()
    ps = psutil.Process(pid)

    initial_cpu_times = ps.cpu_times()
    mat = rand_int_matrix(size, num_gates)
    final_cpu_times = ps.cpu_times()

    process_time = final_cpu_times.user + final_cpu_times.system - initial_cpu_times.user - initial_cpu_times.system

    file = open(path, 'w')
    file.write(f'Matrix size: {size}\n')
    file.write(f'Generation time (seconds): {process_time}\n')

    for row in mat:
        file.write(f'{row}\n')

    file.close()