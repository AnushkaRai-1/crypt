import socket

def rail_decrypt(cipher, key):
    if key == 1:
        return cipher

    rail = [['\n' for _ in range(len(cipher))] for _ in range(key)]
    dir_down = None
    row, col = 0, 0

    for _ in cipher:
        if row == 0:
            dir_down = True
        if row == key - 1:
            dir_down = False
        rail[row][col] = '*'
        col += 1
        row += 1 if dir_down else -1

    index = 0
    for i in range(key):
        for j in range(len(cipher)):
            if rail[i][j] == '*' and index < len(cipher):
                rail[i][j] = cipher[index]
                index += 1

    result = []
    row, col = 0, 0
    for _ in cipher:
        if row == 0:
            dir_down = True
        if row == key - 1:
            dir_down = False
        result.append(rail[row][col])
        col += 1
        row += 1 if dir_down else -1

    return "".join(result)

ip = input("Enter sender IP address: ")
port = int(input("Enter sender port number: "))
key = int(input("Enter Rail Fence key: "))

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
pt = rail_decrypt(ct, int(k))
print("The decrypted message is :", pt)

c.close()
s.close()
