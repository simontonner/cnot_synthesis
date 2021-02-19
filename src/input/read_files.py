import os
import re
from src.optimization.section_size import normal_section_size
import numpy as np
import ast
from src.input.bitfields import to_bitfield
import torch



def find_files(directory, regex):

    file_names = []

    for file_name in os.listdir(directory):
        if re.match(regex, file_name):
            file_names.append(file_name)

    return file_names


def number_from_text(text, regex):

    matches = re.findall(regex, text)

    if len(matches) > 1:
        raise ValueError('More than one match for regex.')

    if len(matches) < 1:
        raise ValueError('No match for regex.')

    number_matches = re.findall(r'\d+', matches[0])

    if len(number_matches) < 1:
        raise ValueError('Regex does not search for numbers.')

    number = int(number_matches[0])

    return number


def numbers_from_file_name(file_name, first_regex, second_regex):

    first_number = number_from_text(file_name, first_regex)
    second_number = number_from_text(file_name, second_regex)

    return first_number, second_number


def normal_sec_size_int_from_file_name(file_name, size_regex):

    size = number_from_text(file_name, size_regex)

    sec_size = normal_section_size(size)

    sec_size_int = np.rint(sec_size).astype(int)

    return sec_size_int


def file_to_circuit(input_dir, file_name):

    size, sample = numbers_from_file_name(file_name, r'_\d+_', r'_\d+\.')

    with open(rf"..\{input_dir}\{file_name}", 'r') as input_file:
        lines = input_file.read().splitlines()

    circuit = ast.literal_eval(lines[2])

    return circuit, size, sample


def file_to_matrix(input_dir, file_name):

    size, sample = numbers_from_file_name(file_name, r'_\d+_', r'_\d+\.')

    with open(rf"..\{input_dir}\{file_name}", 'r') as input_file:
        lines = input_file.read().splitlines()

    matrix = []
    for line in lines[2:]:
        row = to_bitfield(int(line), size)
        matrix.append(row)

    return matrix, size, sample


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