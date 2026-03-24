import socket
import select
import sys
import re

alphabet_list = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 
                 'u', 'v', 'w', 'x', 'y', 'z']

def prepare_text(text):
    # Convert to lower, replace j with i, and remove everything except a-z
    text = text.lower().replace('j', 'i')
    return re.sub(r'[^a-z]', '', text)

def fill_letter(text):
    res = ""
    i = 0
    while i < len(text):
        res += text[i]
        # If there's a next character and it's the same as current
        if i + 1 < len(text):
            if text[i] == text[i+1]:
                res += 'x'
                i += 1 
            else:
                res += text[i+1]
                i += 2
        else:
            i += 1
    # If odd length after splitting duplicates, add padding
    if len(res) % 2 != 0:
        res += 'z'
    return res

def group_characters(text):
    return [text[i:i+2] for i in range(0, len(text), 2)]

def generate_key_matrix(word, alphabet):
    key_letters = []
    # Filter key for unique chars only
    for char in word:
        if char not in key_letters and char in alphabet:
            key_letters.append(char)
    complementary = key_letters + [c for c in alphabet if c not in key_letters]
    return [complementary[i:i+5] for i in range(0, 25, 5)]

def search_element(matrix, element):
    for i in range(5):
        for j in range(5):
            if matrix[i][j] == element:
                return i, j
    return 0, 0

def encrypt_playfair_cipher(matrix, plaintext_list):
    cipher_text = []
    for pair in plaintext_list:
        r1, c1 = search_element(matrix, pair[0])
        r2, c2 = search_element(matrix, pair[1])
        if r1 == r2: # Same Row
            cipher_text.append(matrix[r1][(c1 + 1) % 5] + matrix[r2][(c2 + 1) % 5])
        elif c1 == c2: # Same Column
            cipher_text.append(matrix[(r1 + 1) % 5][c1] + matrix[(r2 + 1) % 5][c2])
        else: # Rectangle
            cipher_text.append(matrix[r1][c2] + matrix[r2][c1])
    return "".join(cipher_text)

# Connection Setup
IP_address = input("Enter receiver IP address: ")
Port = int(input("Enter receiver port number: "))
key_str = input("Enter Playfair secret key: ").lower().replace('j', 'i')
matrix = generate_key_matrix(key_str, alphabet_list)

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
            # Pre-processing
            clean_text = prepare_text(text)
            filled_text = fill_letter(clean_text)
            plaintext_list = group_characters(filled_text)
            encrypted = encrypt_playfair_cipher(matrix, plaintext_list)
            print(f"The sender is sending the message : {text}")
            print(f"The encrypted message is : {encrypted}")
            server.send(encrypted.encode())
            print("The message is sent\n")
