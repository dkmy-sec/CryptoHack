import asyncio
import httpx
import string
import time


URL = "https://aes.cryptohack.org/ecb_oracle/encrypt/"

BLOCK_SIZE = 16
CHARSET = string.ascii_letters + string.digits + "{}_"

# limit concurrent requests (important to avoid rate limiting)
SEM = asyncio.Semaphore(10)


async def encrypt(client, data: bytes):
    hex_data = data.hex()

    async with SEM:
        while True:
            try:
                r = await client.get(URL + hex_data + "/", timeout=5.0)
                data = r.json()
                if "ciphertext" in data:
                    return bytes.fromhex(data["ciphertext"])
            except:
                await asyncio.sleep(0.05)


async def find_next_byte(client, padding, flag, block_index):
    start = block_index * BLOCK_SIZE
    end = (block_index + 1) * BLOCK_SIZE

    # Get target block once
    ct = await encrypt(client, padding)
    target_block = ct[start:end]

    tasks = []
    guesses = []

    block_offset = (len(flag) // BLOCK_SIZE) * BLOCK_SIZE
    known_block = flag[block_offset:]

    for c in CHARSET:
        guess = padding + known_block + c.encode()
        guesses.append(c)
        tasks.append(encrypt(client, guess))

    results = await asyncio.gather(*tasks)

    for c, ct_guess in zip(guesses, results):
        if ct_guess[start:end] == target_block:
            return c.encode()

    return None


async def main():
    flag = b""

    async with httpx.AsyncClient() as client:
        while True:
            start_time = time.time()

            pad_len = BLOCK_SIZE - (len(flag) % BLOCK_SIZE) - 1
            padding = b"A" * pad_len
            block_index = len(flag) // BLOCK_SIZE

            next_byte = await find_next_byte(client, padding, flag, block_index)

            elapsed = time.time() - start_time

            if not next_byte:
                print(f"[-] Stuck at {flag} (took {elapsed:.2f}s)")
                break

            flag += next_byte
            print(f"[+] {flag}  ({elapsed:.2f}s)")

            if flag.endswith(b"}"):
                break

    print("\nFLAG:", flag.decode())


if __name__ == "__main__":
    asyncio.run(main())
