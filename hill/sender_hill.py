import socket
import select
import sys
import re

MOD = 26

def prepare_text(text):
    text = text.lower()
    return re.sub(r'[^a-z]', '', text)

def pad_text(text):
    if len(text) % 2 != 0:
        text += 'x'
    return text

def text_to_numbers(text):
    return [ord(c) - 97 for c in text]

def numbers_to_text(nums):
    return ''.join(chr(n + 97) for n in nums)

def generate_key_matrix(key):
    key = prepare_text(key)
    if len(key) != 4:
        raise ValueError("Key must be exactly 4 letters for 2x2 Hill Cipher")
    nums = text_to_numbers(key)
    return [[nums[0], nums[1]],
            [nums[2], nums[3]]]

def encrypt_hill(plaintext, key_matrix):
    nums = text_to_numbers(plaintext)
    cipher_nums = []
    for i in range(0, len(nums), 2):
        x1, x2 = nums[i], nums[i+1]
        c1 = (key_matrix[0][0]*x1 + key_matrix[0][1]*x2) % MOD
        c2 = (key_matrix[1][0]*x1 + key_matrix[1][1]*x2) % MOD
        cipher_nums.extend([c1, c2])
    return numbers_to_text(cipher_nums)

# Connection Setup
IP_address = input("Enter receiver IP address: ")
Port = int(input("Enter receiver port number: "))
key_str = input("Enter Hill secret key (4 letters): ")
key_matrix = generate_key_matrix(key_str)

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
            clean_text = prepare_text(text)
            padded_text = pad_text(clean_text)
            encrypted = encrypt_hill(padded_text, key_matrix)
            print(f"The sender is sending the message : {text}")
            print(f"The encrypted message is : {encrypted}")
            server.send(encrypted.encode())
            print("The message is sent\n")
