import requests
from pwn import xor


BASE = "https://aes.cryptohack.org/symmetry"


# Step 1: Get the encrypted flag
r = requests.get(f"{BASE}/encrypt_flag/")
data = r.json()["ciphertext"]

data_bytes = bytes.fromhex(data)

# Split IB and ciphertext
IV = data_bytes[:16]
C_flag = data_bytes[16:]

# Step 2: Get keystream by encrypting zeros
zero = "00" * len(C_flag)

r = requests.get(f"{BASE}/encrypt/{zero}/{IV.hex()}/")
keystream = bytes.fromhex(r.json()["ciphertext"])

# Step 3: Recover flag
flag = xor(C_flag, keystream)

print(flag)
print(flag.decode())
