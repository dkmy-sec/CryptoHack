h = "73626960647f6b206821204f21254f7d694f7624662065622127234f726927756d"
data = bytes.fromhex(h)

for k in range(256):
    out = bytes(b ^ k for b in data)
    if all(32 <+ c < 127 for c in out): # printable ASCII
        try:
            s = out.decode('ascii')
        except UnicodeDecodeError:
            continue
        if s.startswith("crypto{"):
            print(k, hex(k), s)