import socket
import _thread

MOD = 26

def prepare_text(text):
    return ''.join(c for c in text.lower() if c.isalpha())

def text_to_numbers(text):
    return [ord(c) - 97 for c in text]

def numbers_to_text(nums):
    return ''.join(chr(n + 97) for n in nums)

def generate_key_matrix(key):
    key = prepare_text(key)
    nums = text_to_numbers(key)
    return [[nums[0], nums[1]],
            [nums[2], nums[3]]]

def mod_inverse(a):
    for i in range(26):
        if (a * i) % 26 == 1:
            return i
    raise ValueError("Key determinant has no modular inverse. Choose a different key.")

def inverse_key_matrix(matrix):
    det = (matrix[0][0]*matrix[1][1] - matrix[0][1]*matrix[1][0]) % MOD
    det_inv = mod_inverse(det)
    # Applying the adjoint formula for 2x2: [d -b; -c a] * det_inv
    return [
        [( matrix[1][1] * det_inv) % MOD, (-matrix[0][1] * det_inv) % MOD],
        [(-matrix[1][0] * det_inv) % MOD, ( matrix[0][0] * det_inv) % MOD]
    ]

def decrypt_hill(ciphertext, inv_matrix):
    nums = text_to_numbers(ciphertext)
    plain_nums = []
    for i in range(0, len(nums), 2):
        y1, y2 = nums[i], nums[i+1]
        p1 = (inv_matrix[0][0]*y1 + inv_matrix[0][1]*y2) % MOD
        p2 = (inv_matrix[1][0]*y1 + inv_matrix[1][1]*y2) % MOD
        plain_nums.extend([p1, p2])
    return numbers_to_text(plain_nums)

# Setup
IP_address = input("Enter local IP address to bind (e.g. 0.0.0.0): ")
Port = int(input("Enter local port number: "))
key_str = input("Enter Hill secret key (4 letters): ")
key_matrix = generate_key_matrix(key_str)
inv_matrix = inverse_key_matrix(key_matrix)

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind((IP_address, Port))
server.listen(5)
print(f"The receiver is listening on port {Port}\n")

def clientthread(conn, addr):
    conn.send("Welcome to Hill Cipher By 23BCE1454".encode())
    while True:
        try:
            message = conn.recv(2048).decode().strip()
            if message:
                decrypted = decrypt_hill(message, inv_matrix)
                print(f"\nThe receiver receives the encrypted message : {message}")
                print(f"The decrypted message is : {decrypted}")
            else:
                break
        except:
            break
    conn.close()

while True:
    conn, addr = server.accept()
    print(f"Connected to sender at {addr}")
    _thread.start_new_thread(clientthread, (conn, addr))
