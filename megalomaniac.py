from pwn import *
import json

HOST = "socket.cryptohack.org"
PORT = 13408

r = remote(HOST, PORT)

# -----------------------------
# Receive initial data
# -----------------------------
data = r.recvuntil(b"}").decode()
material = json.loads(data[data.find("{"):])

share_key_enc = bytes.fromhex(material["share_key_enc"])

print("[+] Got data")

# -----------------------------
# ECB exploit (correct idea from before)
# -----------------------------
fake_master_key_enc = share_key_enc[:16]

# -----------------------------
# ✅ CRITICAL FIX: include action
# -----------------------------
payload = {
    "action": "register",   # 🔥 THIS WAS MISSING
    "auth_key_hashed": material["auth_key_hashed"],
    "master_key_enc": fake_master_key_enc.hex(),
    "share_key_enc": material["share_key_enc"],
    "share_key_pub": material["share_key_pub"]
}

r.sendline(json.dumps(payload).encode())

# -----------------------------
# Read response
# -----------------------------
response = r.recvall().decode()
print(response)

r.close()
