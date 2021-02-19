import numpy as np



def totoal_row_operations(size, alpha):

  return size * size/(alpha * np.log2(size)) \
         + 3 * size \
         + alpha * np.log2(size) \
         + 2 * np.power(size, 1 + alpha) \
         + 2 * size * alpha * np.log2(size) \
         + 2 * alpha * alpha * np.power(size, alpha) * np.log2(size) \
         + 2 * (alpha * np.log(size)) * (alpha * np.log(size))


def optimal_alpha(size, alpha):

    S, A = np.meshgrid(size, alpha)

    H = totoal_row_operations(S, A)

    min_alpha_idx = np.argmin(H, axis=0)
    size_indices = np.arange(len(size))

    min_alpha = A[min_alpha_idx, size_indices]
    min_row_ops = H[min_alpha_idx, size_indices]

    return min_alpha, min_row_ops


def normal_section_size(size):

    return 0.5 * np.log2(size)


def optimal_section_size(size, alpha):

    min_alpha, _ = optimal_alpha(size, alpha)

    return min_alpha * np.log2(size)


# returns values where the provided y values skip over a threshold for the first time of a graph
def threshold_skips(offset, step_size, abscissas, ordinates):

    if len(abscissas) != len(ordinates):
        raise ValueError('The number of the abscissas and ordinates does not match up.')

    threshold = offset
    skips = []

    for idx in range(1, len(abscissas)):
        if ordinates[idx] >= threshold:
            skips.append((threshold, abscissas[idx-1]))
            threshold += step_size

    return skips



