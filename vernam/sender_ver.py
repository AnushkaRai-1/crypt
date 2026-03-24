import socket
import select
import sys
import re

alphabet = 'abcdefghijklmnopqrstuvwxyz'

def encrypt(plaintext, key):
    plaintext = plaintext.lower()
    key = key.lower()
    
    # Check if key is long enough for the actual letters being sent
    clean_text = re.sub(r'[^a-z]', '', plaintext)
    if len(key) < len(clean_text):
        print("Error: Key length must be >= message length (Vernam Cipher)")
        return None
        
    result = ''
    k_idx = 0
    for char in plaintext:
        if char in alphabet:
            p = alphabet.index(char)
            k_val = alphabet.index(key[k_idx])
            c = (p + k_val) % 26
            result += alphabet[c]
            k_idx += 1
        else:
            result += char
    return result

# Input
IP_address = input("Enter receiver IP address: ")
Port = int(input("Enter receiver port number: "))
key_str = input("Enter Vernam key: ")

print("\nEncryption Technique Used: Vernam Cipher")
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

print(f"\nThe sender is connecting to receiver on port {Port}...")
server.connect((IP_address, Port))
print(f"The sender is connected to receiver on port {Port}\n")

while True:
    sockets_list = [sys.stdin, server]
    read_sockets, _, _ = select.select(sockets_list, [], [])
    
    for socks in read_sockets:
        if socks == server:
            message = socks.recv(2048).decode()
            print(f"\n[RECEIVER]: {message}")
        else:
            text = sys.stdin.readline().strip()
            if not text:
                continue
            
            encrypted = encrypt(text, key_str)
            if encrypted:
                print(f"The sender is sending message: {text}")
                print(f"The encrypted message: {encrypted}")
                server.send(encrypted.encode())
                print("The message is sent\n")

server.close()
