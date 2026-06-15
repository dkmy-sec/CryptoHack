import requests
import string


BASE = "https://aes.cryptohack.org/ctrime/encrypt/"

alphabet = string.printable
known = "crypto{"


def get_len(s):
    r = requests.get(BASE + s.encode().hex() + "/")
    return len(r.json()["ciphertext"])

while not known.endswith("}"):
    best_char = None
    best_len = float("inf")

    for c in alphabet:
        test = ("A" * 50) + known + c
        l = get_len(test)

        if l < best_len:
            best_len = l
            best_char = c

    known += best_char
    print(known)

print("FLAG: ", known)