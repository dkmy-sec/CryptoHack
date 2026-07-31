import jwt
import requests


URL = "https://aes.cryptohack.org/"

# Known weak key from PyJWT README
SECRET = "secret"


def forge_admin_token():
    payload = {
        "admin": True,
        "username": "drunkenmunky"
    }

    token = jwt.encode(payload, SECRET, algorithm="HS256")

    # PyJWT may return byes in older versions
    if isinstance(token, bytes):
        token = token.decode()

    return token


def get_flag():
    token = forge_admin_token()

    url = f"{URL}/jwt-secrets/authorise/{token}/"
    response = requests.get(url)

    print("[+] Status Code:", response.status_code)
    print("[+] Raw Response:\n", response.text)

    try:
        print("[+] Parsed JSON:", response.json())
    except Exception:
        print("[!] Response is not JSON")


if __name__ == "__main__":
    get_flag()