def extended_gcd(a, b):
    # Base case: if b is 0, gcd is a, and coefficients are (1, 0)
    if b == 0:
        return a, 1, 0
    else:
        # Recursive call
        gcd, x1, y1 = extended_gcd(b, a % b)
        # Update coefficients
        x = y1
        y = x1 - (a // b) * y1
        return gcd, x, y

# Example with given primes
p = 26513
q = 32321

gcd, u, v = extended_gcd(p, q)

print(f"gcd({p}, {q}) = {gcd}")
print(f"u = {u}, v = {v}")
print(f"Smaller of u and v: {min(u, v)}")
