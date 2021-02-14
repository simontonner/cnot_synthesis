#          REMARKS:
#
#          We start counting from 0, since this results in cleaner code.
#          Only the indices for the qubits in the final circuit start from 1.
#
#          diagonal-row                       ... the row with the same index as the column we are currently looking at
#          reverse_circuit                    ... the order of the C-NOT gates goes from right to left
#          upper_triangular/lower_triangular  ... referring to the triangular shape of the matrix
#          switched_circuit                   ... the control/target bits of the C-NOT gates are switched



def cnot_synthesis(A, n, m):

     # synthesise lower triangular part
     A, lower_triangular_reverse_circuit = lower_triangular_cnot_synthesis(A, n, m)

     # reversing circuit resulting from lower triangular matrix
     lower_triangular_circuit = lower_triangular_reverse_circuit[::-1]

     # transposing the matrix
     A = [[A[j][i] for j in range(len(A))] for i in range(len(A[0]))]

     # synthesise upper triangular part
     A, upper_triangular_switched_circuit = lower_triangular_cnot_synthesis(A, n, m)

     # switching control/target bit in the circuit resulting from the upper triangular matrix
     upper_triangular_circuit = [(t[1], t[0]) for t in upper_triangular_switched_circuit]

     # combine lower/upper triangular synthesis
     total_circuit = upper_triangular_circuit + lower_triangular_circuit

     return A, total_circuit


def lower_triangular_cnot_synthesis(A, n, m):

     # the circuit is represented as an array of pairs of row-indices
     reverse_circuit = []

     # cutting off the decimal places (same as math.ceil(n/m))
     number_of_sections = (n + m - 1) // m

     # iterate over sections
     for section in range(number_of_sections):

          first_index_in_section = section*m
          last_index_in_section = (section+1)*m-1

          # the index of the last section can exceed the matrix dimensions
          if (last_index_in_section > n-1):
               last_index_in_section = n-1

          ### REMOVE DUPLICATE SUB ROWS IN SECTION (STEP A) ###

          # initialize a dictionary to save row indices for sub row patterns (max size 2^m)
          patterns = dict()

          # iterate over sub-rows from diagonal downwards
          # using the first section-index as row-index we land on the diagonal
          for row_index in range(first_index_in_section, n):

               # get subrow
               sub_row = A[row_index][first_index_in_section:last_index_in_section+1]

               # check if sub_row contains ones
               if (sum(sub_row) > 0):

                    # convert sub_row to bitstring so that it can be used as a dictionary key
                    sub_row_pattern = "".join(str(x) for x in sub_row)

                    # if no entry for pattern in dictionary add row index of pattern
                    if (sub_row_pattern not in patterns.keys()):
                         patterns[sub_row_pattern] = row_index

                    # otherwise eliminate duplicate sub-row (row addition using boolean algebra)
                    else:
                         for j in range(n):
                              A[row_index][j] ^= A[patterns[sub_row_pattern]][j]

                         # Adding row operation into circuit-array as 2-tuple
                         reverse_circuit.append((patterns[sub_row_pattern]+1, row_index+1))

          ### USE GAUSSIAN ELIMINATION FOR REMAINING ENTRIES IN COLUMN SECTION ###

          for column_index in range(first_index_in_section, last_index_in_section+1):

               # check for 1 on diagonal (doing this each time in the for-loop would add a multiplicative factor)
               diagonal_entry = 1
               if (A[column_index][column_index] == 0):
                    diagonal_entry = 0

               # remove ones in this column from diagonal downwards
               for row_index in range(column_index+1, n):

                    # check if row-entry is 1
                    if (A[row_index][column_index] == 1):

                          # if the entry on the diagonal is 0 then add this row onto diagonal-row first (STEP B)
                         if (diagonal_entry == 0):
                              for j in range(n):
                                   A[column_index][j] ^= A[row_index][j]
                              reverse_circuit.append((row_index+1, column_index+1))
                              diagonal_entry = 1

                         # continue by adding the diagonal-row onto each row containing a 1 (STEP C)
                         for j in range(n):
                              A[row_index][j] ^= A[column_index][j]
                         reverse_circuit.append((column_index+1, row_index+1))

     return A, reverse_circuit
