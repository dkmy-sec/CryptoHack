# Python Script to find Euler's totient

p = 857504083339712752489993810777
q = 1029224947942998075080348647219

def euler_totient_from_primes(p, q):
    totient = (p - 1) * (q - 1)
    return totient

print(euler_totient_from_primes(p, q))