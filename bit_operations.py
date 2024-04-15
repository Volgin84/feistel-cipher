import numpy as np


def rotate_left(bits):
    """Applies RL1 rotation to a list of bits"""
    return np.roll(bits, -1)


def input_key(hex_input):
    """Converts input from hexadecimal to a list of binary digits"""
    n = int(hex_input, 16)
    binary_array = np.array([int(bit) for bit in format(n, '08b')])
    return binary_array


def format_hex_input(user_input):
    """Checks if the input is a valid hex and fits in 8 bits"""
    try:
        user_input = user_input.strip().upper()  # strip any leading or trailing whitespace and convert to uppercase

        int(user_input, 16)  # convert input to an integer base 16 to check if it's a valid hexadecimal

        if len(user_input) > 2:  # check that the hex length is <= 2 characters, representing up to 8 bits
            raise ValueError("Input exceeds 8 bits.")

        return user_input.zfill(2)  # ensure it is exactly two characters long for consistent processing (pads with 0 if necessary)

    except ValueError as e:  # print the error and return None if the input is invalid
        print(f"Invalid input: {e}")
        return None
