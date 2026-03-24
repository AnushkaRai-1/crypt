import socket
import select
import sys

key = 'abcdefghijklmnopqrstuvwxyz' # Fixed alphabet (Caesar Cipher)

def encrypt(n, plaintext):
    result = ''
    for l in plaintext.lower():
        try:
            # Shift the index and handle wrapping with modulo 26
            i = (key.index(l) + n) % 26
            result += key[i]
        except ValueError:
            # If the character isn't in the alphabet (like a space), keep it as is
            result += l
    return result

# Input
IP_address = input("Enter receiver IP address: ")
Port = int(input("Enter receiver port number: "))
offset = int(input("Enter offset (shift value): "))

print("\nEncryption Technique Used: Caesar Cipher")
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
            print(message)
        else:
            text = sys.stdin.readline().strip()
            if not text:
                continue
                
            print(f"The sender is sending message: {text}")
            encrypted = encrypt(offset, text)
            print(f"The encrypted message: {encrypted}")
            server.send(encrypted.encode())
            print("The message is sent\n")

server.close()
