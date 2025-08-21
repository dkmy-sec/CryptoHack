# 1. Start with the plaintext
s = 'aloha'

# 2. Convert each char to its ASCII code (ord)
codes = [ord(c) for c in s]
print("ASCII codes: ", codes)

# 3. XOR each code with 13 (the ^ operator is XOR)
xored = [code ^ 13 for code in codes]
print("XORed with 13: ", xored)

# 4. Convert back to characters (chr) and join
new_string = "".join(chr(n) for n in xored)
print("new_string: ", new_string)

# 5. Wrap it in the flag format
flag = f"crypto{{{new_string}}}"
print(flag)
