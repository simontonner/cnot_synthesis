import random as rn


def rand_circuit(size, num_gates):

    circuit = []

    for gate_idx in range(num_gates):

        # select two random qubits
        [target_qubit_idx, control_qubit_idx] = rn.sample(range(size), 2)

        circuit.append((target_qubit_idx, control_qubit_idx))

    return circuit


def identity(size):

    matrix = []
    for row_idx in range(size):
        row = [0]*size
        row[row_idx] = 1
        matrix.append(row)

    return matrix


def circuit_to_matrix(size, circuit):

    matrix = identity(size)

    for (target_row_idx, add_row_idx) in circuit:

        # row addition by iterating over the bits of a row
        for column_idx in range(size):
            matrix[target_row_idx][column_idx] ^= matrix[add_row_idx][column_idx]

    return matrix


def gen_rand_circuit(size):

    num_gates = size*size

    circuit = rand_circuit(size, num_gates)

    return circuit


def int_identity(size):

    identity = []
    for row_idx in range(size - 1, -1, -1):
        identity.append(2 ** row_idx)

    return identity


def circuit_to_int_matrix(size, circuit):

    matrix = int_identity(size)

    for (target_row_idx, add_row_idx) in circuit:

        # row addition by bitwise xor of two integers
        matrix[target_row_idx] ^= matrix[add_row_idx]

    return matrix


def gen_rand_int_matrix(size):

    num_gates = size*size

    circuit = rand_circuit(size, num_gates)

    matrix = circuit_to_int_matrix(size, circuit)

    return matrix


#circuit = rand_circuit(6, 3)

#print(circuit)

#print(circuit_to_matrix(6, circuit))


