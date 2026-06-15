import requests
from Crypto.Util.strxor import strxor

URL = "https://aes.cryptohack.org/ecbcbcwtf"

# Step 1: get ciphertext
r = requests.get(f"{URL}/encrypt_flag/")
ciphertext = bytes.fromhex(r.json()["ciphertext"])

# Step 2: split blocks
blocks = [ciphertext[i:i+16] for i in range(0, len(ciphertext), 16)]

plaintext = b""

# Step 3: recover each block
for i in range(1, len(blocks)):
    c_prev = blocks[i-1]
    c_cur = blocks[i]

    # query ECB decrypt
    r = requests.get(f"{URL}/decrypt/{c_cur.hex()}/")
    d = bytes.fromhex(r.json()["plaintext"])

    # XOR to recover plaintext
    p = strxor(d, c_prev)
    plaintext += p

print(plaintext)