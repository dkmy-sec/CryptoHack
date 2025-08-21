def xor(a, b):  # XOR equal-length byte strings
    return bytes(x ^ y for x, y in zip(a, b))

key1 = bytes.fromhex("a6c8b6733c9b22de7bc0253266a3867df55acde8635e19c73313")
k2_x_k1 = bytes.fromhex("37dcb292030faa90d07eec17e3b1c6d8daf94c35d4c9191a5e1e")
k2_x_k3 = bytes.fromhex("c1545756687e7573db23aa1c3452a098b71a7fbf0fddddde5fc1")
chain = bytes.fromhex("04ee9855208a2cd59091d04767ae47963170d1660df7f56f5faf")

key2 = xor(k2_x_k1, key1)
key3 = xor(k2_x_k3, key2)
flag = xor(chain, xor(xor(key1, key3), key2))

print(flag.decode())


