import socket
import math

def decrypt(cipher, key):
    col = len(key)
    row = math.ceil(len(cipher) / col)
    key_order = sorted(list(enumerate(key)), key=lambda x: x[1])

    matrix = [['' for _ in range(col)] for _ in range(row)]
    idx = 0

    for k, _ in key_order:
        for r in range(row):
            if idx < len(cipher):
                matrix[r][k] = cipher[idx]
                idx += 1

    return ''.join(matrix[r][c] for r in range(row) for c in range(col) if matrix[r][c] != 'X')

ip = input("Enter sender IP address: ")
port = int(input("Enter sender port number: "))
key = input("Enter Row Column key: ")

s = socket.socket()
print("\nThe receiver is connecting to sender on port", port, "...")
s.bind((ip, port))
s.listen(1)
print("The receiver is connected to sender on port", port)

c, a = s.accept()
print("\nConnected to sender")

data = c.recv(1024).decode()
ct, k = data.split("|")

print("\nThe receiver receives the encrypted message :", ct)
pt = decrypt(ct, k)
print("The decrypted message is :", pt)

c.close()
s.close()
