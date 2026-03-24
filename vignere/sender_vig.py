import socket
import select
import sys

alphabet = 'abcdefghijklmnopqrstuvwxyz'

def encrypt(plaintext, key):
    result = ''
    key = key.lower()
    key_index = 0
    for char in plaintext.lower():
        if char in alphabet:
            p = alphabet.index(char)
            # Use the key character at the current shifting index
            k = alphabet.index(key[key_index % len(key)])
            c = (p + k) % 26
            result += alphabet[c]
            key_index += 1
        else:
            # Keep spaces/punctuation as they are
            result += char
    return result

# Input
IP_address = input("Enter receiver IP address: ")
Port = int(input("Enter receiver port number: "))
key_str = input("Enter Vigenere key (word): ")

print("\nEncryption Technique Used: Vigenere Cipher")
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
                
            print(f"The sender is sending message: {text}")
            encrypted = encrypt(text, key_str)
            print(f"The encrypted message: {encrypted}")
            server.send(encrypted.encode())
            print("The message is sent\n")

server.close()
