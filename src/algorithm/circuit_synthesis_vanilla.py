#          REMARKS:
#
#          We start counting from zero, since this results in cleaner code.
#          Only the indices for the qubits in the final circuit start from one.
#
#          diagonal-row                       ... the row with the same index as the column we are currently looking at
#          reverse_circuit                    ... the order of the C-NOT gates goes from right to left
#          upper_triangular/lower_triangular  ... referring to the triangular shape of the matrix
#          switched_circuit                   ... the control and target bits of the C-NOT gates are switched



def synthesise_circuit(mat, size, sec_size):

    # synthesise part from lower triangular matrix
    mat, lower_triangular_reverse_circuit = synthesise_lower_triangular_circuit(mat, size, sec_size)

    # reverse circuit
    lower_triangular_circuit = lower_triangular_reverse_circuit[::-1]

    # transpose matrix
    mat = [[mat[row_idx][col_idx] for row_idx in range(len(mat))] for col_idx in range(len(mat[0]))]

    # synthesise part from upper triangular matrix
    mat, upper_triangular_switched_circuit = synthesise_lower_triangular_circuit(mat, size, sec_size)

    # switch control and target bit
    upper_triangular_circuit = [(t[1], t[0]) for t in upper_triangular_switched_circuit]

    # combine lower and upper circuit parts
    total_circuit = upper_triangular_circuit + lower_triangular_circuit

    return mat, total_circuit


def synthesise_lower_triangular_circuit(mat, size, sec_size):

    # represent circuit as array of tuples containing row indices
    reverse_circuit = []

    # cut off the decimal places (same as math.ceil(size/sec_size))
    num_sec = (size + sec_size - 1) // sec_size

    # iterate over sections
    for sec in range(num_sec):

        first_sec_idx = sec * sec_size
        last_sec_idx = (sec + 1) * sec_size - 1

        # index of last section can exceed matrix dimensions
        if (last_sec_idx > size - 1):
            last_sec_idx = size - 1

        ### REMOVE DUPLICATE SUB ROWS IN SECTION (STEP A) ###

        # initialize a dictionary to save row indices for sub-row patterns (max size 2^sec_size)
        patterns = dict()

        # iterate over sub-rows from diagonal downwards (first section index same as row index on diagonal)
        for row_idx in range(first_sec_idx, size):

            # get sub-row
            sub_row = mat[row_idx][first_sec_idx : last_sec_idx + 1]

            # check if sub-row contains ones
            if (sum(sub_row) > 0):

                # convert sub-row to bitstring for dictionary key
                sub_row_pattern = "".join(str(bit) for bit in sub_row)

                # if sub-row pattern not already in dictionary, add corresponding row index to it
                if (sub_row_pattern not in patterns.keys()):
                    patterns[sub_row_pattern] = row_idx

                # otherwise, eliminate duplicate sub-row by bitwise XOR
                else:
                    for col_idx in range(size):
                        mat[row_idx][col_idx] ^= mat[patterns[sub_row_pattern]][col_idx]

                    # add row operation into circuit array as tuple
                    reverse_circuit.append((patterns[sub_row_pattern] + 1, row_idx + 1))

        ### USE GAUSSIAN ELIMINATION FOR REMAINING ENTRIES IN COLUMN SECTION ###

        for sec_col_idx in range(first_sec_idx, last_sec_idx + 1):

            # check for a one on diagonal (doing this each time in the for-loop would add a multiplicative factor)
            diagonal_entry = 1
            if (mat[sec_col_idx][sec_col_idx] == 0):
                diagonal_entry = 0

            # remove ones in this column from diagonal downwards
            for row_idx in range(sec_col_idx + 1, size):

                # check if row entry is a one
                if (mat[row_idx][sec_col_idx] == 1):

                    # if entry on diagonal is zero then XOR this row onto the diagonal-row first (STEP B)
                    if (diagonal_entry == 0):
                        for col_idx in range(size):
                            mat[sec_col_idx][col_idx] ^= mat[row_idx][col_idx]
                        reverse_circuit.append((row_idx + 1, sec_col_idx + 1))
                        diagonal_entry = 1

                    # continue by adding the diagonal-row onto each row containing a one (STEP C)
                    for col_idx in range(size):
                        mat[row_idx][col_idx] ^= mat[sec_col_idx][col_idx]

                    reverse_circuit.append((sec_col_idx + 1, row_idx + 1))

    return mat, reverse_circuit



