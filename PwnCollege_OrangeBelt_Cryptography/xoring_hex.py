def xor_decrypt(hex_key, hex_encrypted):
    # Convert hexadecimal strings to integers
    key = int(hex_key, 16)
    encrypted = int(hex_encrypted, 16)

    # Perform XOR operation
    decrypted = key ^ encrypted

    # Convert decrypted value to hexadecimal and decimal
    hex_result = hex(decrypted)
    decimal_result = decrypted

    # Convert to ASCII if printable
    try:
        ascii_result = chr(decrypted) if 32 <= decrypted <= 126 else 'Non-printable'
    except:
        ascii_result = 'Invalid'

    # Print results
    print(f"Key: {hex_key}")
    print(f"Encrypted: {hex_encrypted}")
    print(f"Decrypted (hex): {hex_result}")
    print(f"Decrypted (decimal): {decimal_result}")
    print(f"Decrypted (ASCII): {ascii_result}")

# Example usage
xor_decrypt('0x79', '0xba')
