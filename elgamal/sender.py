import socket
import random

def is_prime(n):
    if n <= 1: return False
    for i in range(2, int(n**0.5) + 1):
        if n % i == 0: return False
    return True

def get_random_prime(min_val, max_val):
    while True:
        p = random.randint(min_val, max_val)
        if is_prime(p):
            return p

def mod_inverse(a, m):
    # This works in Python 3.8+
    return pow(a, -1, m)

def decrypt_message(encrypted_chars, c1, private_key, q):
    decrypted_chars = []
    # K = (C1)^XA mod q
    shared_secret_K = pow(c1, private_key, q)
    # M = (C2 * K^-1) mod q
    K_inverse = mod_inverse(shared_secret_K, q)
    for c2 in encrypted_chars:
        # M = (C2 * K^-1) mod q
        m = (c2 * K_inverse) % q
        decrypted_chars.append(chr(m))
    return ''.join(decrypted_chars)

server = socket.socket()
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

try:
    server.bind(("0.0.0.0", 5009))
    server.listen(1)
    print("Server listening on port 5009...")
    
    # Generate Parameters
    prime_q = get_random_prime(1000, 5000) 
    generator_g = random.randint(2, prime_q - 1)
    alice_private_key = random.randint(2, prime_q - 2)
    alice_public_key = pow(generator_g, alice_private_key, prime_q)
    
    print("\n--- Alice's Keys ---")
    print(f"Public Elements (q, g): ({prime_q}, {generator_g})")
    print(f"Alice's Public Key (YA): {alice_public_key}")
    print(f"Alice's Private Key (XA): {alice_private_key}")
    
    conn, addr = server.accept()
    print(f"\nConnection from {addr}")
    
    # Send Public Key to Client
    public_key_packet = f"{prime_q},{generator_g},{alice_public_key}"
    conn.send(public_key_packet.encode())
    
    # Receive Ciphertext
    data = conn.recv(4096).decode()
    if not data:
        print("\nClient disconnected or sent empty message.")
    else:
        try:
            parts = data.split("|")
            c1_public_random = int(parts[0])
            # Handle empty or malformed C2 lists
            c2_encrypted_chars = list(map(int, parts[1].split(",")))
            
            print(f"\nReceived Ciphertext (C1): {c1_public_random}")
            print(f"Received Ciphertext (C2): {c2_encrypted_chars}")
            
            plaintext = decrypt_message(c2_encrypted_chars, c1_public_random, 
                                        alice_private_key, prime_q)
            print(f"\nDecrypted Message: {plaintext}")
            
        except (ValueError, IndexError):
            print("\nError: Received malformed data.")
            
    conn.close()

except Exception as e:
    print(f"\nServer Error: {e}")
finally:
    server.close()
    print("Server closed.")
