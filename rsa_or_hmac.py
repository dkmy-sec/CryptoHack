import requests
import base64
import json
import hmac
import hashlib

BASE = "https://web.cryptohack.org/rsa-or-hmac"

def b64url(data):
    return base64.urlsafe_b64encode(data).rstrip(b'=')

# Step 1: Get public key
headers = {"User-Agent": "Mozilla/5.0"}
resp = requests.get(f"{BASE}/get_pubkey/", headers=headers)
pubkey = resp.json()["pubkey"].encode()

print("[+] Got public key")

# Step 2: Create malicious JWT manually
header = {"alg": "HS256", "typ": "JWT"}
payload = {"username": "attacker", "admin": True}

header_b64 = b64url(json.dumps(header).encode())
payload_b64 = b64url(json.dumps(payload).encode())

message = header_b64 + b"." + payload_b64

signature = hmac.new(pubkey, message, hashlib.sha256).digest()
signature_b64 = b64url(signature)

token = (message + b"." + signature_b64).decode()

print("[+] Forged token:\n", token)

# Step 3: Send to server
resp = requests.get(f"{BASE}/authorise/{token}/", headers=headers)

print("\n[+] Server response:")
print(resp.text)
