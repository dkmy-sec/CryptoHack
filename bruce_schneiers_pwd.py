import json
import socket
import random
import string
import numpy as np
from Crypto.Util.number import isPrime
import re

HOST = "socket.cryptohack.org"
PORT = 13400

chars = string.ascii_letters + string.digits

def query(pw):
    s = socket.socket()
    s.connect((HOST, PORT))

    s.recv(4096)  # banner

    s.sendall((json.dumps({"password": pw}) + "\n").encode())
    resp = s.recv(4096).decode()

    s.close()
    return resp

while True:
    # Step 1: build locally
    pw = ['A', 'a', '1']  # guarantees constraints

    for _ in range(10):
        pw.append(random.choice(chars))

    pw = ''.join(pw)

    # Step 2: filter locally (sum only)
    s_val = sum(ord(c) for c in pw)

    if not isPrime(s_val):
        continue  # skip useless candidates

    print(f"[+] Trying {pw} (sum prime: {s_val})")

    # Step 3: query server
    resp = query(pw)

    if "Wrong password" in resp:
        match = re.search(r"product was (-?\d+)", resp)

        if not match:
            print("Parse error:", resp)
            continue

        p_val = int(match.group(1))

        print(f"    product (server): {p_val}")

        if isPrime(p_val):
            print("\n🔥 FOUND PASSWORD:", pw)
            print(resp)
            break

    else:
        print("\n✅ FLAG:", resp)
        break