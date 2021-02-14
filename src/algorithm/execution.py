def check_and_run(circuit_synthesis, mat, sec_size):

    size = len(mat)
    if (size != len(mat[0])):
        print("Please provide a square matrix")
        return

    if (size < 2):
        print("Matrix dimensions should exceed 2")
        return

    if (sec_size < 2):
        print("Subsections should be bigger than 2")
        return

    mat, circuit = circuit_synthesis(mat, size, sec_size)

    ### CHECKING IF OUTPUT MATRIX IS AN IDENTITY MATRIX (I.E. INPUT WAS NON-SINGULAR) ###
    non_singular = True

    # check for zeros on diagonal
    for i in range(0, size):
        if (mat[i][i] == 0 and non_singular):
            flag = False
            print("Input matrix singular. Zero on diagonal of output matrix.")
            break

    # if all ones on diagonal check the rest of the matrix
    if (non_singular):
        for i in range(0, size):
            for j in range(0, size):
                if (i != j and mat[i][j] != 0 and non_singular):
                    non_singular = False
                    print("Input matrix singular. Off diagonal entry contains a one.")
                    break

    return mat, circuit, non_singular