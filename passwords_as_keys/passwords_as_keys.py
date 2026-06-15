from Crypto.Cipher import AES
import hashlib


ciphertext = bytes.fromhex("c92b7734070205bdf6c0087a751466ec13ae15e6f1bcdd3f3a535ec0f4bbae66")


with open("words.txt", "r") as f:
    words = [w.strip() for w in f]


for word in words:
    key = hashlib.md5(word.encode()).digest()
    cipher = AES.new(key, AES.MODE_ECB)

    plaintext = cipher.decrypt(ciphertext)
    try:
        decoded = plaintext.decode()
        if "crypto{" in decoded:
            print("[+] Found flag: ", decoded)
            break
    except:
        continue