import socket

def rail_encrypt(text, key):
    if key == 1:
        return text
    rail = [['\n' for _ in range(len(text))] for _ in range(key)]
    dir_down = False
    row, col = 0, 0

    for ch in text:
        if row == 0 or row == key - 1:
            dir_down = not dir_down
        rail[row][col] = ch
        col += 1
        row += 1 if dir_down else -1

    return "".join(ch for row in rail for ch in row if ch != '\n')

ip = input("Enter receiver IP address: ")
port = int(input("Enter receiver port number: "))
key = int(input("Enter Rail Fence key: "))
pt = input("\nEnter message to send: ")

ct = rail_encrypt(pt, key)

s = socket.socket()
print("\nThe sender is connecting to receiver on port", port, "...")
s.connect((ip, port))
print("The sender is connected to receiver on port", port)

print("\n[RECEIVER]: Welcome to Rail Fence Cipher By 23BCE1454")
print("The sender is sending the message :", pt)
print("The encrypted message is :", ct)

s.send((ct + "|" + str(key)).encode())
print("The message is sent")

s.close()
