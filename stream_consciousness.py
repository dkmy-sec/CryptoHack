import requests
from pwn import xor
from collections import Counter


URL = "https://aes.cryptohack.org/stream_consciousness/encrypt/"


# Step 1: collect samples
ciphertexts = []
for _ in range(1000):
    ct = requests.get(URL).json()["ciphertext"]
    ciphertexts.append(bytes.fromhex(ct))

max_len = max(len(c) for c in ciphertexts)


# Step 2: pad to same length
cts = [c + b'\x00' * (max_len - len(c)) for c in ciphertexts]


# Step 3: detect spaces
space_scores = [Counter() for _ in range(max_len)]

for i in range(len(cts)):
    for j in range(i + 1, len(cts)):
        x = xor(cts[i], cts[j])
        for pos, val in enumerate(x):
            if 65 <= val <= 90 or 97 <= val <= 122: # A-Z, a-z
                space_scores[pos][i] += 1
                space_scores[pos][j] += 1


# Step 4: build keystream guess
keystream = bytearray(max_len)

for pos in range(max_len):
    if not space_scores[pos]:
        continue

    # ciphertext index most likely containing a space
    best_ct_index = space_scores[pos].most_common(1)[0][0]

    # assume plaintext[best] has space at pos
    keystream[pos] = cts[best_ct_index][pos] ^ 0x20


# Step 5: decrypt all ciphertexts
for c in cts:
    pt = xor(c, keystream)
    if b'crypto{' in pt:
        print(pt)

