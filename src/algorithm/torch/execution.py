import os
import psutil
from src.input.read_files import file_to_tensor



def check_and_benchmark(circuit_synthesis, tensor, sec_size):

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


def load_tensor_and_benchmark(circuit_synthesis, size, sec_size, sample, path, device):

    print(f'Loading matrix from {path} and allocating tensor ...')

    tensor = file_to_tensor(size, path, device)

    print(f'Tensor allocated on {tensor.device.type} ...')

    print(f'Benchmarking sample {sample} ... matrix size: {size}, section size: {sec_size}')
    _, circuit, process_time, initial_rss, final_rss = check_and_benchmark(circuit_synthesis, tensor, sec_size)

    num_gates = len(circuit)

    return size, sample, sec_size, num_gates, process_time, initial_rss, final_rss



