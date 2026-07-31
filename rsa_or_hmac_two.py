import requests
import jwt
import base64
from hashlib import sha256
from math import gcd
from itertools import combinations
from Crypto.PublicKey import RSA

# === CONFIG ===
BASE_URL = "https://web.cryptohack.org/rsa-or-hmac-2"
e = 65537


# =========================
# Step 1: Get Tokens
# =========================
def get_token():
    r = requests.get(f"{BASE_URL}/create_session/test/")
    return r.json()["session"]


def get_tokens(count=12):  # increased count
    return [get_token() for _ in range(count)]


# =========================
# Step 2: Helpers
# =========================
def b64url_decode(data):
    return base64.urlsafe_b64decode(data + '=' * (-len(data) % 4))


def parse_jwt(token):
    return token.split('.')


def sig_to_int(sig_b64):
    return int.from_bytes(b64url_decode(sig_b64), 'big')


# ASN.1 prefix for SHA256
ASN1_SHA256 = bytes.fromhex(
    "3031300d060960864801650304020105000420"
)


def emsa_pkcs1_v15_encode(message, key_len=256):
    digest = sha256(message).digest()
    t = ASN1_SHA256 + digest
    padding_len = key_len - len(t) - 3
    return b'\x00\x01' + b'\xff' * padding_len + b'\x00' + t


# =========================
# Step 3: Recover modulus
# =========================
def recover_modulus(tokens):
    vals = []

    for token in tokens:
        header, payload, sig = parse_jwt(token)

        s = sig_to_int(sig)

        # THIS is the trick:
        # we don't rebuild m — we let RSA give it to us
        m = pow(s, e)  # this equals encoded message mod n

        # Instead of subtracting a guessed m,
        # we compare differences between signatures
        vals.append(m)

    print("[+] Values collected")

    G = []

    for a, b in combinations(vals, 2):
        g = gcd(a - b, b)  # CRITICAL CHANGE

        if g > 1:
            G.append(g)

    if not G:
        raise Exception("No GCD candidates")

    n = min(G)

    print("[+] Bit length:", n.bit_length())

    return n


# =========================
# Step 4: Build Public Key
# =========================
def build_pem(n, e):
    key = RSA.construct((n, e))
    return key.export_key(format='PEM', pkcs=1).decode()


# =========================
# Step 5: Forge Token
# =========================
def forge_token(public_key_pem):
    payload = {"admin": True}

    print("[+] Forging token...")

    token = jwt.encode(payload, public_key_pem, algorithm="HS256")

    # PyJWT sometimes returns bytes
    if isinstance(token, bytes):
        token = token.decode()

    return token


# =========================
# Step 6: Exploit
# =========================
def exploit(token):
    print("[+] Sending exploit...")
    r = requests.get(f"{BASE_URL}/authorise/{token}/")
    return r.text


# =========================
# MAIN
# =========================
print("[+] Getting tokens...")
tokens = get_tokens(20)

print("[+] Recovering modulus...")
n = recover_modulus(tokens)
print(f"[+] Recovered modulus: {n}")
print(f"[*] n bit length: {n.bit_length()}")

print("[+] Building public key...")
pem = build_pem(n, e)

print("[+] Public key ready")

admin_token = forge_token(pem)

result = exploit(admin_token)

print("\n=== RESPONSE ===")
print(result)