import random as rn



def rand_circuit(size, num_gates):

    circuit = []

    for gate_idx in range(num_gates):
        [control_qubit_idx, target_qubit_idx] = rn.sample(range(size), 2)
        circuit.append((control_qubit_idx, target_qubit_idx))

    return circuit


def identity(size):

    identity = []

    for row_idx in range(size):
        row = [0] * size
        row[row_idx] = 1
        identity.append(row)

    return identity

def circuit_to_matrix(circuit, size):

    matrix = identity(size)

    for (control_row_idx, target_row_idx) in circuit:
        for col_idx in range(size):
            matrix[target_row_idx][col_idx] ^= matrix[control_row_idx][col_idx]

    return matrix


#import numpy as np
#def circuit_to_matrix(circuit, size):

  #  matrix = identity(size)

   # for (control_row_idx, target_row_idx) in circuit:

   #     print(np.matrix(matrix))

    #    for col_idx in range(size):
     #       matrix[target_row_idx][col_idx] ^= matrix[control_row_idx][col_idx]

   # print(np.matrix(matrix))

   # return matrix



#circuit = [(1, 3), (2, 1), (0, 3), (2, 3), (1, 2), (1, 3), (3, 1), (0, 3), (2, 3), (3, 2), (3, 2), (2, 0), (0, 1), (3, 1), (0, 3), (3, 1)]


#circuit_to_matrix(circuit,4)

