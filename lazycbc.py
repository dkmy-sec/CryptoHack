from pwn import xor
import requests

BASE = "https://aes.cryptohack.org/lazy_cbc"

# Step 1: get ciphertext
r = requests.get(f"{BASE}/encrypt/" + "00"*16)
C1 = bytes.fromhex(r.json()["ciphertext"])

# Step 2: craft payload
payload = C1 + b'\x00'*16 + C1

# Step 3: send payload
r = requests.get(f"{BASE}/receive/{payload.hex()}/")
leak = r.json()["error"].split(": ")[1]
decrypted = bytes.fromhex(leak)

# Step 4: split blocks
P1 = decrypted[:16]
P3 = decrypted[32:48]

# Step 5: recover key
KEY = xor(P1, P3)

# Step 6: get flag
r = requests.get(f"{BASE}/get_flag/{KEY.hex()}/")
flag = bytes.fromhex(r.json()["plaintext"]).decode()

print(flag)