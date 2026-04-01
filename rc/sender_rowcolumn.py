import socket
import math

def encrypt(text, key):
    col = len(key)
    row = math.ceil(len(text) / col)
    text += 'X' * (row * col - len(text))

    matrix = [list(text[i*col:(i+1)*col]) for i in range(row)]
    key_order = sorted(list(enumerate(key)), key=lambda x: x[1])

    cipher = ''
    for k, _ in key_order:
        for r in range(row):
            cipher += matrix[r][k]
    return cipher

ip = input("Enter receiver IP address: ")
port = int(input("Enter receiver port number: "))
key = input("Enter Row Column key: ")
pt = input("\nEnter message to send: ")

ct = encrypt(pt, key)

s = socket.socket()
print("\nThe sender is connecting to receiver on port", port, "...")
s.connect((ip, port))
print("The sender is connected to receiver on port", port)

print("\n[RECEIVER]: Welcome to Row Column Cipher By 23BCE1454")
print("The sender is sending the message :", pt)
print("The encrypted message is :", ct)

s.send((ct + "|" + key).encode())
print("The message is sent")

s.close()
