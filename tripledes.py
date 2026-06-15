import requests
from Crypto.Util.Padding import unpad

BASE = "https://aes.cryptohack.org/triple_des"

# ✅ Correct key (K1 = K3, valid parity)
key = "0101010101010101FEFEFEFEFEFEFEFE0101010101010101"

# 1. get encrypted flag
C_flag = requests.get(
    f"{BASE}/encrypt_flag/{key}/"
).json()["ciphertext"]

# 2. encrypt again
result = bytes.fromhex(requests.get(
    f"{BASE}/encrypt/{key}/{C_flag}/"
).json()["ciphertext"])

print(result)

# 3. remove padding
flag = unpad(result, 8)
print(flag.decode())
