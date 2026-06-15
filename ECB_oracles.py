import requests
import string
import time

URL = "https://aes.cryptohack.org/ecb_oracle/encrypt/"
session = requests.Session()

def encrypt(data_bytes):
    hex_data = data_bytes.hex()
    while True:
        try:
            r = session.get(URL + hex_data + "/", timeout=5)
            return bytes.fromhex(r.json()["ciphertext"])
        except:
            time.sleep(0.1)

BLOCK_SIZE = 16
flag = b""

CHARSET = string.ascii_letters + string.digits + "{}_"

while True:
    pad_len = BLOCK_SIZE - (len(flag) % BLOCK_SIZE) - 1
    padding = b"A" * pad_len

    ct = encrypt(padding)
    block_index = len(flag) // BLOCK_SIZE

    start = block_index * BLOCK_SIZE
    end = (block_index + 1) * BLOCK_SIZE

    target_block = ct[start:end]

    found = False
    for c in CHARSET:
        guess = padding + flag + c.encode()
        ct_guess = encrypt(guess)
        guess_block = ct_guess[start:end]

        if guess_block == target_block:
            flag += c.encode()
            print(flag)
            found = True
            break

    if not found or flag.endswith(b"}"):
        break

    time.sleep(0.01)

print("FLAG:", flag.decode())