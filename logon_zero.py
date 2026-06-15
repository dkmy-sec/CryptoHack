from pwn import *
import json
from os import urandom

HOST = "socket.cryptohack.org"
PORT = 13399

def send(r, data):
    r.sendline(json.dumps(data).encode())
    while True:
        line = r.recvline()
        try:
            return json.loads(line)
        except:
            continue

def try_empty_login(r):
    res = send(r, {"option": "authenticate", "password": ""})
    return "flag" in res.get("msg", "")

r = remote(HOST, PORT)
print(r.recvline())  # banner

# Create base ciphertext
ct = bytearray(urandom(32))

# Brute-force last 4 bytes
for i in range(4):
    pos = len(ct) - 1 - i
    print(f"[*] Solving byte {i} (position {pos})")

    for guess in range(256):
        ct[pos] = guess

        # Send reset_password with modified ciphertext
        send(r, {
            "option": "reset_password",
            "token": ct.hex()
        })

        if try_empty_login(r):
            print(f"[+] Found byte {i}: {hex(guess)}")
            break

print("[*] Attempting final login...")
print(send(r, {"option": "authenticate", "password": ""}))

r.close()