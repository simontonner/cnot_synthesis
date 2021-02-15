from src.input.circuits_and_matrices import rand_circuit



def int_identity(size):

    identity = []

    for row_idx in range(size - 1, -1, -1):
        identity.append(2 ** row_idx)

    return identity


def circuit_to_int_matrix(circuit, size):

    matrix = int_identity(size)

    for (target_row_idx, add_row_idx) in circuit:
        matrix[target_row_idx] ^= matrix[add_row_idx]

    return matrix


def rand_int_matrix(size, num_gates):

    circuit = rand_circuit(size, num_gates)

    matrix = circuit_to_int_matrix(size, circuit)

    return matrix