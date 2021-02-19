import os
import psutil
from src.input.read_files import file_to_circuit, file_to_matrix
from src.input.circuits_and_matrices import circuit_to_matrix



def check_and_run(circuit_synthesis, mat, sec_size):

    size = len(mat)
    if (size != len(mat[0])):
        print("Please provide a square matrix")
        return

    if (size < 2):
        print("Matrix dimensions should exceed 2")
        return

    if (sec_size < 2):
        print("Subsections should be bigger than 2")
        return

    mat, circuit = circuit_synthesis(mat, size, sec_size)

    ### CHECKING IF OUTPUT MATRIX IS AN IDENTITY MATRIX (I.E. INPUT WAS NON-SINGULAR) ###

    is_non_singular = True

    # check for zeros on diagonal
    for idx in range(0, size):
        if (mat[idx][idx] == 0 and is_non_singular):
            flag = False
            print("Input matrix singular. Zero on diagonal of output matrix.")
            break

    # if diagonal full of ones, check the rest of the matrix
    if (is_non_singular):
        for row_idx in range(0, size):
            for col_idx in range(0, size):
                if (row_idx != col_idx and mat[row_idx][col_idx] != 0 and is_non_singular):
                    is_non_singular = False
                    print("Input matrix singular. Off diagonal entry contains a one.")
                    break

    return mat, circuit, is_non_singular


def check_and_benchmark(circuit_synthesis, mat, sec_size):

    size = len(mat)
    if (size != len(mat[0])):
        print("Please provide a square matrix")
        return

    if (size < 2):
        print("Matrix dimensions should exceed 2")
        return

    if (sec_size < 2):
        print("Subsections should be bigger than 2")
        return

    pid = os.getpid()
    ps = psutil.Process(pid)

    initial_rss = ps.memory_info().rss
    initial_cpu_times = ps.cpu_times()

    mat, circuit = circuit_synthesis(mat, size, sec_size)

    final_cpu_times = ps.cpu_times()
    final_rss = ps.memory_info().rss

    is_non_singular = True

    for idx in range(0, size):
        if (mat[idx][idx] == 0 and is_non_singular):
            flag = False
            print("Input matrix singular. Zero on diagonal of output matrix.")
            break

    if (is_non_singular):
        for row_idx in range(0, size):
            for col_idx in range(0, size):
                if (row_idx != col_idx and mat[row_idx][col_idx] != 0 and is_non_singular):
                    is_non_singular = False
                    print("Input matrix singular. Off diagonal entry contains a one.")
                    break

    process_time = final_cpu_times.user + final_cpu_times.system - initial_cpu_times.user - initial_cpu_times.system

    return mat, circuit, is_non_singular, process_time, initial_rss, final_rss


def load_circuit_and_benchmark(circuit_synthesis, input_dir, input_file_name, sec_size):

    print(f'Loading circuit from file {input_file_name} and converting it to matrix ...')

    circuit, size, sample = file_to_circuit(input_dir, input_file_name)

    mat = circuit_to_matrix(circuit, size)

    print(mat)

    print(f'Benchmarking sample {sample} ... matrix size: {size}, section size: {sec_size}')
    _, circuit, _, process_time, initial_rss, final_rss = check_and_benchmark(circuit_synthesis, mat, sec_size)

    num_gates = len(circuit)

    return size, sample, sec_size, num_gates, process_time, initial_rss, final_rss


def load_matrix_and_benchmark(circuit_synthesis, input_dir, input_file_name, sec_size):

    print(f'Loading matrix from file {input_file_name} ...')

    mat, size, sample = file_to_matrix(input_dir, input_file_name)

    print(f'Benchmarking sample {sample} ... matrix size: {size}, section size: {sec_size}')
    _, circuit, _, process_time, initial_rss, final_rss = check_and_benchmark(circuit_synthesis, mat, sec_size)

    num_gates = len(circuit)

    return size, sample, sec_size, num_gates, process_time, initial_rss, final_rss
