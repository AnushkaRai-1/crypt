import socket
import random

def encrypt_message(msg, q, g, alice_public_key):
    encrypted_chars = []
    # Choose a random session key k
    random_k = random.randint(2, q - 2)
    
    # K = (YA)^k mod q (Shared Secret)
    shared_secret_K = pow(alice_public_key, random_k, q)
    
    # C1 = g^k mod q (Sent to Alice so she can derive K)
    c1_public_random = pow(g, random_k, q)
    
    for char in msg:
        m = ord(char)
        if m >= q:
            raise ValueError(f"Prime q ({q}) is too small to encode character '{char}' ({m})")
        
        # C2 = (M * K) mod q
        c2 = (m * shared_secret_K) % q
        encrypted_chars.append(c2)
        
    return c1_public_random, encrypted_chars

client = socket.socket()

try:
    # Ensure this matches the server's IP and Port
    client.connect(("127.0.0.1", 5009))
    print("Connected to Alice (Server)")
    
    # Receive Public Keys: q, g, and YA
    data = client.recv(1024).decode()
    prime_q, generator_g, alice_public_key = map(int, data.split(","))
    
    print("\n--- Received Public Keys ---")
    print(f"Prime (q): {prime_q}")
    print(f"Generator (g): {generator_g}")
    print(f"Alice's Public Key (YA): {alice_public_key}")
    
    msg = input("\nEnter Message to send: ")
    
    if not msg:
        print("Empty message, encryption not possible.")
    else:
        # Generate the ciphertext
        c1, c2_list = encrypt_message(msg, prime_q, generator_g, alice_public_key)
        
        # Format: "C1|C2_1,C2_2,C2_3..."
        cipher_packet = str(c1) + "|" + ",".join(map(str, c2_list))
        client.send(cipher_packet.encode())
        
        print("\nCiphertext sent successfully.")
        print(f"Sent C1: {c1}")
        print(f"Sent C2 list: {c2_list}")

except ValueError as e:
    print(f"\nData Error: {e}")
except Exception as e:
    print(f"\nConnection Error: {e}")
finally:
    client.close()
    print("Connection closed.")
