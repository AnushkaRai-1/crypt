import random
import sys
def is_prime(n, k=40):
    #Returns True if n is likely prime, False if composite.
    if n == 2 or n == 3: return True
    if n % 2 == 0 or n < 2: return False
    r, d = 0, n - 1
    while d % 2 == 0:
        r += 1
        d //= 2
    for _ in range(k):
        a = random.randrange(2, n - 1)
        x = pow(a, d, n)
        if x == 1 or x == n - 1:
            continue
        for _ in range(r - 1):
            x = pow(x, 2, n)
            if x == n - 1:
                break
        else:
            return False
    return True
def generate_prime(bits):
    #Generates a prime number with the specified number of bits.
    while True:
        # Generate a random odd number of length 'bits'
        candidate = random.getrandbits(bits)
        candidate |= (1 << bits - 1) | 1  # Ensure it's the right length and odd
        if is_prime(candidate):
            return candidate
def extended_gcd(a, b):
    #EEA for MI
    if a == 0:
        return b, 0, 1
    gcd, x1, y1 = extended_gcd(b % a, a)
    x = y1 - (b // a) * x1
    y = x1
    return gcd, x, y
def mod_inverse(e, phi):
    #(d * e) % phi == 1
    gcd, x, y = extended_gcd(e, phi)
    if gcd != 1:
        raise Exception('Modular inverse does not exist')
    return x % phi

def main():
    # 1. Input
    try:
        message = input("Message: ")
    except NameError:
        pass 
    if not message:
        print("Error: Message cannot be empty.")
        return
    print("\nGenerating 1024-bit primes (this may take a few seconds)...")
    # 2.Key Generation
    p = generate_prime(1024)
    q = generate_prime(1024)
    while p == q:
        q = generate_prime(1024)
    n = p * q
    phi = (p - 1) * (q - 1)
    e = 65537
    d = mod_inverse(e, phi)
    # 3. Encryption
    m_int = int.from_bytes(message.encode('utf-8'), byteorder='big')
    if m_int >= n:
        print("Error: Message is too long for the key size.")
        return
    c_int = pow(m_int, e, n)
    # 4. Decryption
    decrypted_int = pow(c_int, d, n)
    try:
        decrypted_text = decrypted_int.to_bytes((decrypted_int.bit_length() + 7) // 8, byteorder='big').decode('utf-8')
    except:
        decrypted_text = "[Error decoding text]"
    # 5. Cipher
    print("\n" + "="*20 + " OUTPUT (HEX) " + "="*20)  
    print(f"p value:\n{p:#x}\n")
    print(f"q value:\n{q:#x}\n")
    print(f"n=p.q:\n{n:#x}\n")
    print(f"phi(n):\n{phi:#x}\n")
    print(f"e:\n{e:#x}\n")
    print(f"d:\n{d:#x}\n")
    print(f"encrypted text:\n{c_int:#x}\n")
    print(f"decrypted text:\n{decrypted_text}")
    print("="*54)
if __name__ == "__main__":
    main()