h = "0e0b213f26041e480b26217f27342e175d0e070a3c5b103e2526217f27342e175d0e077e263451150104"
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