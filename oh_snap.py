import requests


URL = "https://aes.cryptohack.org/challenges/oh_snap/send_cmd"

flag = b""

while True:
    for guess in range(256):

        nonce = b"A" * (255 - len(flag))
        test_byte = bytes([guess])

        key_guess = nonce + flag + test_byte

        # generate RC$ keystream locally
        from Crypto.Cipher import ARC4
        cipher = ARC4.new(key_guess)
        keystream = cipher.encrypt(b"\x00" * 4)

        # want plaintext = ping
        target = b"ping"
        ciphertext = bytes([a ^ b for a,b in zip(keystream, target)])

        r = requests.get(f"{URL}/{ciphertext.hex()}/{nonce.hex()}/")

        if "Pong" in r.text:
            flag += test_byte
            print(flag)
            break