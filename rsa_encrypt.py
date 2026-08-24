from Crypto.Util import number

def generate_prime():
    c = number.getPrime(1024)
    return c

def ETF_generate(P, Q):
    fxn = (P-1)*(Q-1)
    return fxn

def secret_key_generate(m):
    e = 65537
    d = pow(e, -1, m)
    #big fix here. pythhon 3.8 does the extended euclidian algo directly.
    #it does the modular inverse perfectly
    return d

P = generate_prime()
Q = generate_prime()
N = P*Q

euiler_totient = ETF_generate(P, Q)
d = secret_key_generate(euiler_totient)

