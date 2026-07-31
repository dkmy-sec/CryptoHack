from pwn import *
import json


HOST = "socket.cryptohack.org"
PORT = 13421


def send(io, data):
    io.sendline(json.dumps(data).encode())

    while True:
        line = io.recvline().decode().strip()
        try:
            return json.loads(line)
        except json.JSONDecodeError:
            # skip banner or garbage
            continue


def oracle(io, ct):
    return send(io, {"option": "unpad", "ct": ct})["result"]


def get_ciphertext(io):
    return bytes.fromhex(send(io, {"option": "encrypt"})["ct"])


def decrypt_block(io, prev, curr):
    block_size = 16
    intermediate = [0] * block_size
    plaintext = [0] * block_size

    for i in range(15, -1, -1):
        pad = 16 - i

        for guess in range(256):
            modified = bytearray(prev)

            # apply padding adjustments
            for j in range(i+1, 16):
                modified[j] = intermediate[j] ^ pad

            modified[i] = guess

            test_ct = bytes(modified) + curr
            if oracle(io, test_ct.hex()):
                # Stronger verification
                valid = True

                # Try enforcing next padding level
                if pad < 16:
                    test_check = bytearray(modified)

                    # force next padding structure
                    test_check[i] ^= 1

                    if oracle(io, (bytes(test_check) + curr).hex()):
                        valid = False  # suspicious → likely false positive

                if not valid:
                    continue

                intermediate[i] = guess ^ pad
                plaintext[i] = intermediate[i] ^ prev[i]
                break

    return bytes(plaintext)


def main():
    io = remote(HOST, PORT)

    #clear banner and garbage
    io.recvuntil(b'}\n', timeout=0.2) # clears any junk

    ct = get_ciphertext(io)

    iv = ct[:16]
    c1 = ct[16:32]
    c2 = ct[32:48]

    # decrypt blocks
    p2 = decrypt_block(io, c1, c2)
    p1 = decrypt_block(io, iv, c1)

    print("P1:", p1)
    print("P2:", p2)

    message = (p1 + p2).decode('ascii')

    print("Recovered message:", message)

    flag = send(io, {"option": "check", "message": message})
    print("[+]Flag:", flag)

    io.close()


if __name__ == "__main__":
    main()
