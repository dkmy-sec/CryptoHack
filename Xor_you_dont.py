import binascii

# Encrypted hex string
hex_str = "0xea"

# Convert hex string to bytes
encrypted_bytes = binascii.unhexlify(hex_str)

# Key used for XOR encryption
key = b"0x60"

# Repeat the key to match the length of the encrypted message
full_key = (key * (len(encrypted_bytes) // len(key) + 1))[:len(encrypted_bytes)]

# XOR decryption
decrypted_bytes = bytes([b ^ k for b, k in zip(encrypted_bytes, full_key)])

# Decode the decrypted bytes to string
decrypted_message = decrypted_bytes.decode()

print("FLAG: ", decrypted_message)

