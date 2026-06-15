import requests
from pwn import xor


url = "https://aes.cryptohack.org/bean_counter/encrypt/"
r = requests.get(url)
cipher = bytes.fromhex(r.json()["encrypted"])

# PNG Header
png_header = bytes.fromhex("89504e470d0a1a0a0000000d49484452")

# recover keystream (first block)
ks = xor(cipher[:len(png_header)], png_header)

# repeat keystream to full length
full_keystream = (ks * (len(cipher) // len(ks) + 1))[:len(cipher)]

# decrypt
plaintext = xor(cipher, full_keystream)

# save image
with open("flag.png", "wb") as f:
    f.write(plaintext)

print("saved as flag.png")