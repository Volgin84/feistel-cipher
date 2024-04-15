import numpy as np
from bit_operations import rotate_left, input_key


def rotate_odd_rounds(current_key_bits):
    """Rotates bits for odd rounds and concatenates them"""
    left_half_rotated = rotate_left(current_key_bits[:4])
    right_half_rotated = rotate_left(current_key_bits[4:])
    current_key_bits = np.concatenate((left_half_rotated, right_half_rotated))  # current state of key bits
    selected_bits = np.array([left_half_rotated[0], left_half_rotated[2], right_half_rotated[0], right_half_rotated[2]])
    return current_key_bits, selected_bits  # updated state of key bits after processing the odd round, selected bits from the rotated halves


def rotate_even_rounds(current_key_bits):
    """Rotates bits for even rounds and selects specific bits"""
    rotated_whole = rotate_left(current_key_bits)
    selected_bits = rotated_whole[np.array([0, 2, 4, 6])]
    return rotated_whole, selected_bits  # updated state of key bits after processing the even round, selected bits from the whole rotated key


def generate_and_select_keys(initial_key):
    """Generates cryptographic keys by rotating bits as per specified cryptographic rules, initial_key (str) is the initial hexadecimal string input"""
    current_key_bits = input_key(initial_key) if isinstance(initial_key, str) else initial_key
    selected_bits_all_rounds = []

    for round_number in range(1, 9):  # 8 rounds of generating
        if round_number % 2 != 0:  # check if odd or even
            current_key_bits, selected_bits = rotate_odd_rounds(current_key_bits)
        else:
            current_key_bits, selected_bits = rotate_even_rounds(current_key_bits)

        selected_bits_all_rounds.append(selected_bits.tolist())

    return selected_bits_all_rounds  # list containing lists of selected 4-bit keys from each round
