import os
import re
import ast
from src.input.bitfields import to_bitfield
import torch



def find_files(directory, regex):

    file_names = []

    for file_name in os.listdir(directory):
        if re.match(regex, file_name):
            file_names.append(file_name)

    return file_names


def numbers_from_file_name(file_name, first_regex, second_regex):

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


def file_to_circuit(input_dir, file_name):

    size, run = numbers_from_file_name(file_name, r'_\d+_', r'_\d+\.')

    with open(rf"..\{input_dir}\{file_name}", 'r') as input_file:
        lines = input_file.read().splitlines()

    circuit = ast.literal_eval(lines[2])

    return circuit, size, run


def file_to_matrix(input_dir, file_name):

    size, run = numbers_from_file_name(file_name, r'_\d+_', r'_\d+\.')

    with open(rf"..\{input_dir}\{file_name}", 'r') as input_file:
        lines = input_file.read().splitlines()

    matrix = []
    for line in lines[2:]:
        row = to_bitfield(int(line), size)
        matrix.append(row)

    return matrix, size, run


def file_to_tensor(input_dir, file_name):

    size, run = numbers_from_file_name(file_name, r'_\d+_', r'_\d+\.')

    with open(rf"..\{input_dir}\{file_name}", 'r') as input_file:
        lines = input_file.read().splitlines()

    format_string = f'#0{size + 2}b'

    matrix = []
    for line in lines[2:]:
        row = [(int(bit) > 0.5) for bit in format(int(line), format_string)[2:]]
        matrix.append(row)

    tensor = torch.Tensor(matrix, dtype=torch.bool)

    return tensor, size, run