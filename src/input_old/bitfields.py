import random as rn


def rand_array(n):
    result = []
    for i in range(n):
        rand_bit = rn.sample(range(2), 1)[0]
        result.append(rand_bit)
    return result


def to_bitfield(integer, field_len):

  format_string = f'#0{field_len+2}b'

  return [int(bit) for bit in format(integer, format_string)[2:]]


def from_bitfield(bitfield):

    return int("".join([str(bitfield[i]) for i in range(len(bitfield))]), 2)


def xor_bitfields(bitfield_1, bitfield_2):

    len_bitfield_1 = len(bitfield_1)

    if len_bitfield_1 != len(bitfield_2):
        raise ValueError('The bitfields are not of the same length.')

    xorred_bitfield = []

    for i in range(len_bitfield_1):
        xorred_bitfield.append(bitfield_1[i] ^ bitfield_2[i])

    return xorred_bitfield


def compare_bitfields(bitfield_1, bitfield_2):

    len_bitfield_1 = len(bitfield_1)

    if len_bitfield_1 != len(bitfield_2):
        raise ValueError('The bitfields are not of the same length.')

    for i in range(len_bitfield_1):
        if (bitfield_1[i] != bitfield_2[i]):
            return False

    return True







### TESTING CONVERSION

#n = 10000

#x = identity(n)

#start_time_conv = ti.time()
#for i in range(n):
#    x[i] = bitfield(x[i], n)
#end_time_conv = ti.time()

#print("Execution time for conversion of n =", n, " was:", (end_time_conv - start_time_conv), "seconds")