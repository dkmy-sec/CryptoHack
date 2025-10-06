def xor_decrypt(encrypted_char, xor_key_hex):
    # Convert the encrypted character to its ASCII byte value
    ascii_value = ord(encrypted_char)

    # Convert the hexadecimal XOR key to an integer
    xor_key = int(xor_key_hex, 16)

    # Perform XOR operation
    decrypted_value = ascii_value ^ xor_key

    # Convert the result back to a character
    decrypted_char = chr(decrypted_value)

    return decrypted_char

# Example usage
encrypted_char = '2'
xor_key_hex = '0x0c'
decrypted_char = xor_decrypt(encrypted_char, xor_key_hex)

print(f"Encrypted Character: {encrypted_char}")
print(f"XOR Key: {xor_key_hex}")
print(f"Decrypted Character: {decrypted_char}")