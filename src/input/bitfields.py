import random as rn



def rand_bitfield(field_len):

    bitfield = []

    for idx in range(field_len):
        rand_bit = rn.sample(range(2), 1)[0]
        bitfield.append(rand_bit)

    return bitfield


def to_bitfield(integer, field_len):

  format_string = f'#0{field_len + 2}b'

  return [int(bit) for bit in format(integer, format_string)[2:]]


def from_bitfield(bitfield):

    return int(''.join([str(bitfield[idx]) for idx in range(len(bitfield))]), 2)


def xor_bitfields(bitfield_1, bitfield_2):

    len_bitfield_1 = len(bitfield_1)

    if len_bitfield_1 != len(bitfield_2):
        raise ValueError('The bitfields are not of the same length.')

    xorred_bitfield = []

    for idx in range(len_bitfield_1):
        xorred_bitfield.append(bitfield_1[idx] ^ bitfield_2[idx])

    return xorred_bitfield


def compare_bitfields(bitfield_1, bitfield_2):

    len_bitfield_1 = len(bitfield_1)

    if len_bitfield_1 != len(bitfield_2):
        raise ValueError('The bitfields are not of the same length.')

    for idx in range(len_bitfield_1):
        if (bitfield_1[idx] != bitfield_2[idx]):
            return False

    return True