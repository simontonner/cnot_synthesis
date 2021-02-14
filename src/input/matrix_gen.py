import random as rn


def non_singular_matrix(n):

    num_scrambles = n*n

    A = identity(n)

    A = reverse_gauss_scramble(A, n, num_scrambles)

    return A


def identity(n):

    result = []
    for i in range(n-1, -1, -1):
        result.append(2**i)
    return result


def reverse_gauss_scramble(A, n, num_scrambles):

    for i in range(num_scrambles):

        # get two random rows
        [target_row_index, add_row_index] = rn.sample(range(n), 2)

        # row addition using boolean algebra
        A[target_row_index] ^= A[add_row_index]

    return A







