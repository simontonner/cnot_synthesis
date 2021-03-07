import os
import psutil
from src.input.read_files import file_to_circuit, file_to_matrix, file_to_tensor
from src.input.circuits_and_matrices import circuit_to_matrix



def check_and_run(circuit_synthesis, mat, sec_size):

    size = len(mat)
    if (size != len(mat[0])):
        raise ValueError('Not a square matrix.')

    if (size < 2):
        raise ValueError('Matrix dimensions should exceed 2.')

    if (sec_size < 2):
        raise ValueError('Subsections should be bigger than 2.')

    mat, circuit = circuit_synthesis(mat, size, sec_size)

    ### CHECKING IF OUTPUT MATRIX IS AN IDENTITY MATRIX (I.E. INPUT WAS NON-SINGULAR) ###

    # check for zeros on diagonal
    for idx in range(0, size):
        if (mat[idx][idx] == 0):
             raise ValueError('Input matrix was singular. Zero on diagonal of output matrix.')

    # if diagonal full of ones, check the rest of the matrix
    for row_idx in range(0, size):
        for col_idx in range(0, size):
            if (row_idx != col_idx and mat[row_idx][col_idx] != 0):
                raise ValueError('Input matrix was singular. Output matrix has off diagonal entries.')


    return mat, circuit


def check_and_benchmark(circuit_synthesis, mat, sec_size):

    size = len(mat)
    if (size != len(mat[0])):
        raise ValueError('Not a square matrix.')

    if (size < 2):
        raise ValueError('Matrix dimensions should exceed 2.')

    if (sec_size < 2):
        raise ValueError('Subsections should be bigger than 2.')

    pid = os.getpid()
    ps = psutil.Process(pid)

    initial_rss = ps.memory_info().rss
    initial_cpu_times = ps.cpu_times()

    mat, circuit = circuit_synthesis(mat, size, sec_size)

    final_cpu_times = ps.cpu_times()
    final_rss = ps.memory_info().rss

    for idx in range(0, size):
        if (mat[idx][idx] == 0):
            raise ValueError('Input matrix was singular. Zero on diagonal of output matrix.')

    # if diagonal full of ones, check the rest of the matrix
    for row_idx in range(0, size):
        for col_idx in range(0, size):
            if (row_idx != col_idx and mat[row_idx][col_idx] != 0):
                raise ValueError('Input matrix was singular. Output matrix has off diagonal entries.')

    process_time = final_cpu_times.user + final_cpu_times.system - initial_cpu_times.user - initial_cpu_times.system

    return mat, circuit, process_time, initial_rss, final_rss


def check_tensor_and_benchmark(circuit_synthesis, tensor, sec_size):

    size = len(tensor)
    if (size != len(tensor[0])):
        raise ValueError('Not a square tensor.')

    if (size < 2):
        raise ValueError('Tensor dimensions should exceed 2.')

    if (sec_size < 2):
        raise ValueError('Subsections should be bigger than 2.')

    pid = os.getpid()
    ps = psutil.Process(pid)

    initial_rss = ps.memory_info().rss
    initial_cpu_times = ps.cpu_times()

    tensor, circuit = circuit_synthesis(tensor, size, sec_size)

    final_cpu_times = ps.cpu_times()
    final_rss = ps.memory_info().rss

    for idx in range(0, size):
        if (tensor[idx][idx] is False):
             raise ValueError('Input tensor was singular. FALSE on diagonal of output tensor.')

    # if diagonal full of ones, check the rest of the matrix
    for row_idx in range(0, size):
        for col_idx in range(0, size):
            if (row_idx != col_idx and tensor[row_idx][col_idx] is True):
                raise ValueError('Input tensor was singular. Output tensor has off diagonal entries containing TRUE.')

    process_time = final_cpu_times.user + final_cpu_times.system - initial_cpu_times.user - initial_cpu_times.system

    return tensor, circuit, process_time, initial_rss, final_rss


def load_circuit_and_benchmark(circuit_synthesis, size, sec_size, sample, path):

    print(f'Loading circuit from {path} and converting it to a matrix ...')

    circuit = file_to_circuit(path)

    mat = circuit_to_matrix(circuit, size)

    print(f'Benchmarking sample {sample} ... matrix size: {size}, section size: {sec_size}')
    _, circuit, process_time, initial_rss, final_rss = check_and_benchmark(circuit_synthesis, mat, sec_size)

    num_gates = len(circuit)

    return size, sample, sec_size, num_gates, process_time, initial_rss, final_rss


def load_matrix_and_benchmark(circuit_synthesis, size, sec_size, sample, path):

    print(f'Loading matrix from {path} ...')

    mat = file_to_matrix(size, path)

    print(f'Benchmarking sample {sample} ... matrix size: {size}, section size: {sec_size}')
    _, circuit, process_time, initial_rss, final_rss = check_and_benchmark(circuit_synthesis, mat, sec_size)

    num_gates = len(circuit)

    return size, sample, sec_size, num_gates, process_time, initial_rss, final_rss


def load_tensor_and_benchmark(circuit_synthesis, size, sec_size, sample, path, device):

    print(f'Loading matrix from {path} and allocating tensor ...')

    tensor = file_to_tensor(size, path, device)

    print(f'Tensor allocated on {tensor.device.type} ...')

    print(f'Benchmarking sample {sample} ... matrix size: {size}, section size: {sec_size}')
    _, circuit, process_time, initial_rss, final_rss = check_tensor_and_benchmark(circuit_synthesis, tensor, sec_size)

    num_gates = len(circuit)

    return size, sample, sec_size, num_gates, process_time, initial_rss, final_rss



