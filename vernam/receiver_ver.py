import socket
import _thread
import sys
import re

alphabet = 'abcdefghijklmnopqrstuvwxyz'

def decrypt(ciphertext, key):
    ciphertext = ciphertext.lower()
    key = key.lower()
    
    clean_cipher = re.sub(r'[^a-z]', '', ciphertext)
    if len(key) < len(clean_cipher):
        print("Error: Key length must be >= message length (Vernam Cipher)")
        return "DECRYPTION_ERROR: KEY_TOO_SHORT"
        
    result = ''
    k_idx = 0
    for char in ciphertext:
        if char in alphabet:
            c = alphabet.index(char)
            k_val = alphabet.index(key[k_idx])
            p = (c - k_val) % 26
            result += alphabet[p]
            k_idx += 1
        else:
            result += char
    return result

# Input
IP_address = input("Enter bind IP address (e.g. 0.0.0.0): ")
Port = int(input("Enter receiver port number: "))
key_str = input("Enter Vernam key: ")

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

print(f"\nThe receiver is listening on port {Port}...")
server.bind((IP_address, Port))
server.listen(5)
print(f"The receiver is ready for connections.\n")

def clientthread(conn, addr):
    conn.send("Welcome to Vernam Cipher by 23BCE1454".encode())
    while True:
        try:
            message = conn.recv(2048).decode().strip()
            if message:
                print(f"The receiver received the encrypted message: {message}")
                decrypted = decrypt(message, key_str)
                print(f"The decrypted message: {decrypted}")
                print("The conversion is successful\n")
            else:
                break
        except:
            break
    conn.close()

while True:
    conn, addr = server.accept()
    print(f"Connected to sender: {addr}")
    _thread.start_new_thread(clientthread, (conn, addr))

server.close()
