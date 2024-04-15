from bit_operations import input_key, format_hex_input
from key_generator_builder import generate_and_select_keys
import numpy as np
import sys


def s_block_transform(x1, x2, x3, x4, key):
    """Functions apply 'XOR' and 'AND' operations based on the s-block design of the Feistel network to
       transform the input bits.

    x1(int): first bit of the input
    x2(int): second bit of the input
    x3(int): third bit of the input
    x4(int): fourth bit of the input
    then key bits by index"""
    f1 = x1 ^ (x1 & x3) ^ (x2 & x4) ^ (x2 & x3 & x4) ^ (x1 & x2 & x3 & x4) ^ key[0]
    f2 = x2 ^ (x1 & x3) ^ (x1 & x2 & x4) ^ (x1 & x3 & x4) ^ (x1 & x2 & x3 & x4) ^ key[1]
    f3 = 1 ^ x3 ^ (x1 & x4) ^ (x1 & x2 & x4) ^ (x1 & x2 & x3 & x4) ^ key[2]
    f4 = 1 ^ (x1 & x2) ^ (x3 & x4) ^ (x1 & x2 & x4) ^ (x1 & x3 & x4) ^ (x1 & x2 & x3 & x4) ^ key[3]
    return [f1, f2, f3, f4]  # bits transformed by the functions from the coding s-block


def transform_bits(left_half, right_half, keys_for_round):
    """Applies the transformations for the Feistel cipher."""
    transformed_right = s_block_transform(right_half[0], right_half[1], right_half[2], right_half[3], keys_for_round)  # output of the s-block
    return [left_half[i] ^ transformed_right[i] for i in range(4)]  # output of the left side of the cipher


def feistel_cipher_operation(initial_hex_input, initial_hex_key, rounds=8):
    """Forward cipher"""
    try:
        selected_keys_all_rounds = generate_and_select_keys(initial_hex_key)
        # print(f"Message for encryption: {initial_hex_input}\n"
        #       f"Coding key: {initial_hex_key.format()}")
        current_state = input_key(initial_hex_input)

        for round_number in range(1, rounds + 1):
            left_half, right_half = current_state[:4], current_state[4:]
            keys_for_round = selected_keys_all_rounds[round_number - 1]

            new_right_half = transform_bits(left_half, right_half, keys_for_round)

            if round_number == rounds:
                new_state = np.concatenate((new_right_half, right_half))  # concatenate without swap in the final round
            else:
                new_state = np.concatenate((right_half,
                                            new_right_half))  # swap: old right becomes new left, transformed left becomes new right

            current_state = new_state

        final_state_hex = ''.join(str(bit) for bit in current_state)
        final_state_hex = f"{int(final_state_hex, 2):02X}".upper()
        return final_state_hex
    except Exception as e:
        print(f"Error occurred: {e}")
        return None


def feistel_cipher_operation_reversed(initial_hex_input, initial_hex_key, rounds=8):
    """Reverse cipher"""
    try:
        selected_keys_all_rounds = generate_and_select_keys(initial_hex_key)
        current_state = input_key(initial_hex_input)

        for round_number in range(1, rounds + 1):
            left_half, right_half = current_state[:4], current_state[4:]
            keys_for_round = selected_keys_all_rounds[rounds - round_number]  # decryption keys from the end

            new_right_half = transform_bits(left_half, right_half, keys_for_round)

            if round_number == rounds:
                new_state = np.concatenate((new_right_half, right_half))  # concatenate without swap in the final round
            else:
                new_state = np.concatenate((right_half,
                                            new_right_half))  # swap: old right becomes new left, transformed left becomes new right

            current_state = new_state

        binary_string = ''.join(str(bit) for bit in current_state)
        final_state_hex = f"{int(binary_string, 2):02X}"
    except Exception as e:
        print(f"Error occurred: {e}")
        return None

    return final_state_hex


def process_batch_operations(num_operations=3):
    messages, keys, encrypted_messages = [], [], []  # collect messages, keys and encrypted messages into lists

    print("\n")
    for i in range(num_operations):
        while True:
            message = format_hex_input(input(f"Enter message {i + 1} to encrypt (in hex): ").strip())
            if message is not None:
                break

        while True:
            key = format_hex_input(input(f"Enter key {i + 1} for encryption (in hex): ").strip())
            if key is not None:
                break
        messages.append(message)
        keys.append(key)

    print("\n--- Encryption Process ---")
    for i in range(num_operations):
        encrypted_message = feistel_cipher_operation(messages[i], keys[i])
        encrypted_messages.append(encrypted_message)
        print(f"Msg {i + 1}: {messages[i]} | Key: {keys[i]} -> Encrypted: {encrypted_message}")
    print("\n--- Decryption Process ---")
    for i, encrypted_message in enumerate(encrypted_messages, start=1):
        decrypted_message = feistel_cipher_operation_reversed(encrypted_message, keys[i-1])
        print(f"Encrypted Msg {i}: {encrypted_message} | Key: {keys[i - 1]} -> Decrypted: {decrypted_message}")


def cipher_game():
    while True:
        process_batch_operations()
        player_choice = input("\nContinue using this cipher (Y/N)?: ").strip().lower()
        if player_choice == 'n':
            print("\nThanks for using our game, have a great day 😎")
            sys.exit()


if __name__ == "__main__":
    game = cipher_game
    game()
