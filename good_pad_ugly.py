from pwn import *
import json
import time

HOST = "socket.cryptohack.org"
PORT = 13422

HEX_BYTES = b"0123456789abcdef"

# --- connection ---
def connect():
    return remote(HOST, PORT)
r = connect()

def recv_json():
    while True:
        line = r.recvline().decode().strip()
        try:
            return json.loads(line)
        except json.JSONDecodeError:
            continue

def send(req):
    global r
    while True:
        try:
            r.sendline(json.dumps(req).encode())
            return recv_json()
        except:
            print("[!] Reconnecting...")
            try:
                r.close()
            except:
                pass
            r = connect()

# --- fast noisy filter ---
def quick_oracle(ct_hex):
    for _ in range(2):
        res = send({"option": "unpad", "ct": ct_hex})
        time.sleep(0.002)
        if not res["result"]:
            return False
    return True

# --- strong confirmation ---
def strong_check(ct_hex, trials=6):
    for _ in range(trials):
        res = send({"option": "unpad", "ct": ct_hex})
        time.sleep(0.002)
        if not res["result"]:
            return False
    return True

# --- get ciphertext ---
data = send({"option": "encrypt"})
ct = bytes.fromhex(data["ct"])

blocks = [ct[i:i+16] for i in range(0, len(ct), 16)]
recovered = b""

print(f"[+] Total blocks: {len(blocks)}")

# --- attack each block ---
for block_index in range(1, len(blocks)):

    while True:  # retry loop if block fails
        try:
            print(f"[+] Attacking block {block_index}")

            prev_block = bytearray(blocks[block_index - 1])
            curr_block = blocks[block_index]

            intermediate = [0] * 16
            plaintext_block = [0] * 16

            for pad_len in range(1, 17):
                i = 16 - pad_len
                print(f"  [*] Byte position {i}")

                candidates = []

                # --- phase 1: collect candidates ---
                for guess in range(256):
                    modified = prev_block[:]

                    for j in range(15, i, -1):
                        modified[j] = intermediate[j] ^ pad_len

                    modified[i] = guess

                    test_ct = bytes(modified) + curr_block
                    test_hex = test_ct.hex()

                    if quick_oracle(test_hex):
                        candidates.append(guess)

                if not candidates:
                    raise Exception("No candidates found")

                # --- phase 2: confirm + filter with hex constraint ---
                valid_choices = []

                for guess in candidates:
                    modified = prev_block[:]

                    for j in range(15, i, -1):
                        modified[j] = intermediate[j] ^ pad_len

                    modified[i] = guess

                    test_ct = bytes(modified) + curr_block
                    test_hex = test_ct.hex()

                    if not strong_check(test_hex):
                        continue

                    val = guess ^ pad_len
                    pt_byte = val ^ prev_block[i]

                    # 🔥 critical filter (hex only)
                    if pt_byte in HEX_BYTES:
                        valid_choices.append((guess, pt_byte))

                if not valid_choices:
                    print("    [!] No hex candidates, relaxing filter...")

                    # fallback: accept any strongly valid candidate
                    for guess in candidates:
                        modified = prev_block[:]

                        for j in range(15, i, -1):
                            modified[j] = intermediate[j] ^ pad_len

                        modified[i] = guess

                        test_ct = bytes(modified) + curr_block
                        test_hex = test_ct.hex()

                        if strong_check(test_hex, trials=6):  # lighter confirm
                            val = guess ^ pad_len
                            pt_byte = val ^ prev_block[i]

                            intermediate[i] = val
                            plaintext_block[i] = pt_byte

                            print(f"    [+] (fallback) Found byte: {pt_byte:02x}")
                            found = True
                            break

                    if not found:
                        raise Exception("Byte recovery failed")
                    continue

                # pick first valid
                guess, pt_byte = valid_choices[0]

                intermediate[i] = guess ^ pad_len
                plaintext_block[i] = pt_byte

                print(f"    [+] Found byte: {pt_byte:02x}")

            block_bytes = bytes(plaintext_block)
            print(f"    [DEBUG] block: {block_bytes}")

            # sanity check: must be hex
            hex_count = sum(c in HEX_BYTES for c in block_bytes)
            if hex_count < 12:
                raise Exception("Corrupted block")

            recovered += block_bytes
            break

        except Exception as e:
            print(f"[!] Retrying block {block_index} due to error: {e}")
            continue

print("\n[+] Raw recovered:", recovered)

# --- remove padding ---
pad_len = recovered[-1]
recovered = recovered[:-pad_len]

message = recovered.decode()
print("[+] Message:", message)

# --- submit ---
res = send({"option": "check", "message": message})
print("[+] Flag:", res)