import base64
from Crypto.Util.number import bytes_to_long

with open("bruce_rsa.pub", "r") as f:
    key = f.read().strip()

# split into parts
parts = key.split()

# base64 blob is the second field
b64_key = parts[1]

data = base64.b64decode(b64_key)


def read_int(data, i):
    length = int.from_bytes(data[i:i+4], byteorder='big')
    i += 4
    value = data[i:i+length]
    i += length
    return value, i


i = 0

# read "ssh-rsa"
_, i = read_int(data, i)

# read e
e_bytes, i = read_int(data, i)

# read n
n_bytes, i = read_int(data, i)

n = bytes_to_long(n_bytes)
print(n)