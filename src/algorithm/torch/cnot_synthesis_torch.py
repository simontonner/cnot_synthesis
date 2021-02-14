import torch


def cnot_synthesis(mat, size, sec_size):

     # synthesise lower triangular part
     mat, lower_triangular_reverse_circuit = lower_triangular_cnot_synthesis(mat, size, sec_size)

     # reversing circuit resulting from lower triangular matrix
     lower_triangular_circuit = lower_triangular_reverse_circuit[::-1]

     # transposing the matrix
     mat = mat.transpose(0, 1)

     # synthesise upper triangular part
     mat, upper_triangular_switched_circuit = lower_triangular_cnot_synthesis(mat, size, sec_size)

     # switching control/target bit in the circuit resulting from the upper triangular matrix
     upper_triangular_circuit = [(t[1], t[0]) for t in upper_triangular_switched_circuit]

     # combine lower/upper triangular synthesis
     total_circuit = upper_triangular_circuit + lower_triangular_circuit

     return mat, total_circuit


def lower_triangular_cnot_synthesis(mat, size, sub_size):

     # the circuit is represented as an array of pairs of row-indices
     reverse_circuit = []

     # cutting off the decimal places (same as math.ceil(n/m))
     number_of_sections = (size + sub_size - 1) // sub_size

     # iterate over sections
     for section in range(number_of_sections):

          first_index_in_section = section*sub_size
          last_index_in_section = (section+1)*sub_size-1

          # the index of the last section can exceed the matrix dimensions
          if (last_index_in_section > size-1):
               last_index_in_section = size-1

          ### REMOVE DUPLICATE SUB ROWS IN SECTION (STEP A) ###

          # initialize a dictionary to save row indices for sub row patterns (max size 2^m)
          patterns = dict()

          # iterate over sub-rows from diagonal downwards
          # using the first section-index as row-index we land on the diagonal
          for row_index in range(first_index_in_section, size):

               # get subrow
               sub_row = mat[row_index][first_index_in_section:last_index_in_section+1]

               # check if sub_row contains ones
               if (sum(sub_row) > 0):

                    # convert sub_row to bitstring so that it can be used as a dictionary key
                    sub_row_pattern = "".join(str(x) for x in sub_row)

                    # if no entry for pattern in dictionary add row index of pattern
                    if (sub_row_pattern not in patterns.keys()):
                         patterns[sub_row_pattern] = row_index

                    # otherwise eliminate duplicate sub-row (row addition using boolean algebra)
                    else:
                         mat[row_index] = torch.logical_xor(mat[row_index], mat[patterns[sub_row_pattern]])

                         # Adding row operation into circuit-array as 2-tuple
                         reverse_circuit.append((patterns[sub_row_pattern]+1, row_index+1))

          ### USE GAUSSIAN ELIMINATION FOR REMAINING ENTRIES IN COLUMN SECTION ###

          for column_index in range(first_index_in_section, last_index_in_section+1):

               # check for 1 on diagonal (doing this each time in the for-loop would add a multiplicative factor)
               diagonal_entry = True
               if (mat[column_index][column_index] == False):
                    diagonal_entry = False

               # remove ones in this column from diagonal downwards
               for row_index in range(column_index+1, size):

                    # check if row-entry is 1
                    if (mat[row_index][column_index] == True):

                          # if the entry on the diagonal is 0 then add this row onto diagonal-row first (STEP B)
                         if (diagonal_entry is False):
                              mat[column_index] = torch.logical_xor(mat[column_index], mat[row_index])

                              reverse_circuit.append((row_index+1, column_index+1))
                              diagonal_entry = True

                         # continue by adding the diagonal-row onto each row containing a 1 (STEP C)
                         mat[row_index] = torch.logical_xor(mat[row_index], mat[column_index])
                         reverse_circuit.append((column_index+1, row_index+1))

     return mat, reverse_circuit