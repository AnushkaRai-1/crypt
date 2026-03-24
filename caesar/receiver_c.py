import socket
import _thread

key = 'abcdefghijklmnopqrstuvwxyz' # Fixed alphabet (Caesar Cipher)

def decrypt(n, ciphertext):
    result = ''
    for l in ciphertext.lower():
        try:
            # Reverse the shift for decryption
            i = (key.index(l) - n) % 26
            result += key[i]
        except ValueError:
            result += l
    return result

# Input
IP_address = input("Enter local IP address to bind (e.g., 0.0.0.0): ")
Port = int(input("Enter local port number: "))
offset = int(input("Enter offset (shift value): "))

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

print(f"\nThe receiver is listening on port {Port}...")
server.bind((IP_address, Port))
server.listen(5)
print(f"The receiver is connected to sender on port {Port}\n")

def clientthread(conn, addr):
    conn.send("Welcome to chatroom!".encode())
    while True:
        try:
            message = conn.recv(2048).decode()
            if message:
                print(f"The receiver received the encrypted message: {message.strip()}")
                decrypted = decrypt(offset, message)
                print(f"The decrypted message: {decrypted.strip()}")
                print("The conversion is successful\n")
            else:
                conn.close()
                break
        except:
            continue

while True:
    conn, addr = server.accept()
    print(f"Connection established with {addr}")
    _thread.start_new_thread(clientthread, (conn, addr))

server.close()
