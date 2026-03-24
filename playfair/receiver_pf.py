import socket
import _thread

alphabet_list = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 
                 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']

def generate_key_matrix(word, alphabet):
    key_letters = []
    for char in word:
        if char not in key_letters and char in alphabet:
            key_letters.append(char)
    comp = key_letters + [c for c in alphabet if c not in key_letters]
    return [comp[i:i+5] for i in range(0, 25, 5)]

def search_element(matrix, element):
    for i in range(5):
        for j in range(5):
            if matrix[i][j] == element: 
                return i, j
    return 0, 0

def decrypt_playfair(matrix, ciphertext):
    res = ""
    for i in range(0, len(ciphertext), 2):
        r1, c1 = search_element(matrix, ciphertext[i])
        r2, c2 = search_element(matrix, ciphertext[i+1])
        if r1 == r2:
            res += matrix[r1][(c1 - 1) % 5] + matrix[r2][(c2 - 1) % 5]
        elif c1 == c2:
            res += matrix[(r1 - 1) % 5][c1] + matrix[(r2 - 1) % 5][c2]
        else:
            res += matrix[r1][c2] + matrix[r2][c1]
    return res

# Binding Setup
IP_address = input("Enter local IP to bind (e.g., 0.0.0.0): ")
Port = int(input("Enter receiver port number: "))
key_str = input("Enter Playfair secret key: ").lower().replace('j', 'i')
matrix = generate_key_matrix(key_str, alphabet_list)

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind((IP_address, Port))
server.listen(5)

print(f"\nThe receiver is listening on port {Port}...")

def clientthread(conn, addr):
    conn.send("Welcome to PlayFair Cipher System".encode())
    while True:
        try:
            message = conn.recv(2048).decode().strip()
            if message:
                decrypted = decrypt_playfair(matrix, message)
                print(f"\nThe receiver receives the encrypted message : {message}")
                print(f"The decrypted message is : {decrypted}")
            else:
                break
        except:
            break
    conn.close()

while True:
    conn, addr = server.accept()
    print(f"Connected to sender: {addr}")
    _thread.start_new_thread(clientthread, (conn, addr))
