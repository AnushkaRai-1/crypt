import socket
import _thread

alphabet = 'abcdefghijklmnopqrstuvwxyz'

def decrypt(ciphertext, key):
    result = ''
    key = key.lower()
    key_index = 0
    for char in ciphertext.lower():
        if char in alphabet:
            c = alphabet.index(char)
            k = alphabet.index(key[key_index % len(key)])
            p = (c - k) % 26
            result += alphabet[p]
            key_index += 1
        else:
            result += char
    return result

# Input
IP_address = input("Enter local IP address to bind (e.g., 0.0.0.0): ")
Port = int(input("Enter local port number: "))
key_str = input("Enter Vigenere key (word): ")

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

print(f"\nThe receiver is listening on port {Port}...")
server.bind((IP_address, Port))
server.listen(5)
print(f"The receiver is ready to accept connections.\n")

def clientthread(conn, addr):
    conn.send("Welcome to Vigenere Cipher System by 23BCE1454!".encode())
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
