import torch

def synthesise_circuit(tensor, size, sec_size):

    tensor, lower_triangular_reverse_circuit = synthesise_lower_triangular_circuit(tensor, size, sec_size)

    lower_triangular_circuit = lower_triangular_reverse_circuit[::-1]

    tensor = tensor.transpose(0, 1)

    tensor, upper_triangular_switched_circuit = synthesise_lower_triangular_circuit(tensor, size, sec_size)

    upper_triangular_circuit = [(t[1], t[0]) for t in upper_triangular_switched_circuit]

    total_circuit = upper_triangular_circuit + lower_triangular_circuit

    return tensor, total_circuit


def synthesise_lower_triangular_circuit(tensor, size, sec_size):

    reverse_circuit = []

    num_sec = (size + sec_size - 1) // sec_size

    for sec in range(num_sec):

        first_sec_idx = sec * sec_size
        last_sec_idx = (sec + 1) * sec_size - 1

        if (last_sec_idx > size - 1):
            last_sec_idx = size - 1

        patterns = dict()

        for row_idx in range(first_sec_idx, size):

            sub_row = tensor[row_idx][first_sec_idx : last_sec_idx + 1]

            if (sum(sub_row) > 0):

                sub_row_pattern = ''.join(str(bit) for bit in sub_row)

                if (sub_row_pattern not in patterns.keys()):
                    patterns[sub_row_pattern] = row_idx

                else:
                    tensor[row_idx] = torch.logical_xor(tensor[row_idx], tensor[patterns[sub_row_pattern]])

                    reverse_circuit.append((patterns[sub_row_pattern], row_idx))

        for sec_col_idx in range(first_sec_idx, last_sec_idx + 1):

            diagonal_entry = True
            if (tensor[sec_col_idx][sec_col_idx] is False):
                diagonal_entry = False

            for row_idx in range(sec_col_idx + 1, size):

                if (tensor[row_idx][sec_col_idx] is True):

                    if (diagonal_entry is False):
                        tensor[sec_col_idx] = torch.logical_xor(tensor[sec_col_idx], tensor[row_idx])

                        reverse_circuit.append((row_idx, sec_col_idx))
                        diagonal_entry = 1

                    tensor[row_idx] = torch.logical_xor(tensor[row_idx], tensor[sec_col_idx])

                    reverse_circuit.append((sec_col_idx, row_idx))

    return tensor, reverse_circuit



