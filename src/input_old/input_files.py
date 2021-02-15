import os
import psutil
import re
import src.input.bitfields as bitf
import src.input.matrix_gen as gen
import torch


def get_txt_files(directory, prefix):

    txt_files = []

    for filename in os.listdir(directory):
        regex_string = f"({prefix}).*\.txt"
        if re.match(regex_string, filename):
            txt_files.append(filename)

    return txt_files


def extract_numbers(file_name, first_regex, second_regex):

    first_matches = re.findall(first_regex, file_name)
    second_matches = re.findall(second_regex, file_name)

    if len(second_matches) > 1 or len(second_matches) > 1:
        raise ValueError('More than one match for one regex.')

    if len(second_matches) < 1 or len(second_matches) < 1:
        raise ValueError('No match for one regex.')

    first_number_matches = re.findall(r'\d+', first_matches[0])
    second_number_matches = re.findall(r'\d+', second_matches[0])

    if len(first_number_matches) < 1 or len(second_number_matches) < 1:
        raise ValueError('One regex does not search for numbers.')

    first_number = int(first_number_matches[0])
    second_number = int(second_number_matches[0])

    return first_number, second_number

def generate_input_files(mat_size, input_file_name):

    pid = os.getpid()
    ps = psutil.Process(pid)

    initial_cpu_times = ps.cpu_times()
    mat = gen.non_singular_matrix(mat_size)
    final_cpu_times = ps.cpu_times()

    process_time = final_cpu_times.user + final_cpu_times.system - initial_cpu_times.user - initial_cpu_times.system

    file = open(input_file_name, "w")
    file.write(f"Matrix size: {mat_size}\n")
    file.write(f"Generation time (seconds): {process_time}\n")
    for row in mat:
        file.write(f"{row}\n")
    file.close()


def file_to_matrix(input_directory, file_name):

    size, run = extract_numbers(file_name, r'_\d+_', r'_\d+\.')

    with open(rf"..\{input_directory}\{file_name}", 'r') as input_file:
        lines = input_file.read().splitlines()

    matrix = []
    for line in lines[2:]:
        row = bitf.to_bitfield(int(line), size)
        matrix.append(row)

    return matrix, size, run


def file_to_tensor(input_directory, file_name):

    size, run = extract_numbers(file_name, r'_\d+_', r'_\d+\.')

    with open(rf"..\{input_directory}\{file_name}", 'r') as input_file:
        lines = input_file.read().splitlines()

    format_string = f'#0{size + 2}b'

    matrix = []
    for line in lines[2:]:
        row = [(int(bit) > 0.5) for bit in format(int(line), format_string)[2:]]
        matrix.append(row)

    tensor = torch.Tensor(matrix, dtype=torch.bool)

    return tensor, size, run






