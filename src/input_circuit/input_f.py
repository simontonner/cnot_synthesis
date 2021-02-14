import os
import psutil
import src.input_circuit.input_gen as gen
import re
import ast

def generate_circuit_file(size, input_file_name):

    pid = os.getpid()
    ps = psutil.Process(pid)

    initial_cpu_times = ps.cpu_times()
    circuit = gen.gen_rand_circuit(size)
    final_cpu_times = ps.cpu_times()

    process_time = final_cpu_times.user + final_cpu_times.system - initial_cpu_times.user - initial_cpu_times.system

    file = open(input_file_name, "w")
    file.write(f"Circuit size: {size}\n")
    file.write(f"Generation time (seconds): {process_time}\n")
    file.write(f"{circuit}\n")
    file.close()


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


def file_to_circuit(input_directory, file_name):

    size, run = extract_numbers(file_name, r'_\d+_', r'_\d+\.')

    with open(rf"..\{input_directory}\{file_name}", 'r') as input_file:
        lines = input_file.read().splitlines()

    circuit = ast.literal_eval(lines[2])

    return circuit, size, run