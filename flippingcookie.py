import requests

URL = "https://aes.cryptohack.org/flipping_cookie"

# Get cookie
r = requests.get(f"{URL}/get_cookie/")
data = bytes.fromhex(r.json()["cookie"])

iv = data[:16]
ct = data[16:]

# Flip "False" -> "True;"
original = b"False"
target   = b"True;"
offset = 6

new_iv = bytearray(iv)

for i in range(len(original)):
    new_iv[offset + i] ^= original[i] ^ target[i]

# Send attack
r = requests.get(
    f"{URL}/check_admin/{ct.hex()}/{bytes(new_iv).hex()}/"
)

print(r.json())
