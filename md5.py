import math
import struct

def left_rotate(x, c):
    """32-bit left rotation."""
    return ((x << c) | (x >> (32 - c))) & 0xFFFFFFFF

# Shift values for the 64 steps
S = [
    7, 12, 17, 22, 7, 12, 17, 22, 7, 12, 17, 22, 7, 12, 17, 22,
    5, 9, 14, 20, 5, 9, 14, 20, 5, 9, 14, 20, 5, 9, 14, 20,
    4, 11, 16, 23, 4, 11, 16, 23, 4, 11, 16, 23, 4, 11, 16, 23,
    6, 10, 15, 21, 6, 10, 15, 21, 6, 10, 15, 21, 6, 10, 15, 21
]

# Constants derived from the sine function
K = [int(abs(math.sin(i + 1)) * (2**32)) & 0xFFFFFFFF for i in range(64)]

def md5_roundwise(message):
    print(f"Number of characters in the input: {len(message)}")
    
    # Pre-processing: Padding
    msg_bytes = bytearray(message.encode())
    original_length_bits = (8 * len(msg_bytes)) & 0xFFFFFFFFFFFFFFFF
    
    # 1. Append a single '1' bit (0x80)
    msg_bytes.append(0x80)
  
    while (len(msg_bytes) % 64) != 56:
        msg_bytes.append(0x00)
  
    msg_bytes += struct.pack('<Q', original_length_bits)

    A0, B0, C0, D0 = 0x67452301, 0xEFCDAB89, 0x98BADCFE, 0x10325476

    block_count = 1
    for block_index in range(0, len(msg_bytes), 64):
        print(f"\n--- Processing Block {block_count} ---")
        block = msg_bytes[block_index : block_index + 64]
        M = list(struct.unpack('<16I', block))
        
        A, B, C, D = A0, B0, C0, D0

        for i in range(64):
            if 0 <= i <= 15:
                F = (B & C) | (~B & D)
                g = i
            elif 16 <= i <= 31:
                F = (D & B) | (~D & C)
                g = (5 * i + 1) % 16
            elif 32 <= i <= 47:
                F = B ^ C ^ D
                g = (3 * i + 5) % 16
            else:
                F = C ^ (B | ~D)
                g = (7 * i) % 16
            temp = (A + F + K[i] + M[g]) & 0xFFFFFFFF
            A = D
            D = C
            C = B
            B = (B + left_rotate(temp, S[i])) & 0xFFFFFFFF

            if (i + 1) % 16 == 0:
                print(f"Round {(i // 16) + 1} Result: A={hex(A)}, B={hex(B)}, C={hex(C)}, D={hex(D)}")

        A0 = (A0 + A) & 0xFFFFFFFF
        B0 = (B0 + B) & 0xFFFFFFFF
        C0 = (C0 + C) & 0xFFFFFFFF
        D0 = (D0 + D) & 0xFFFFFFFF
        block_count += 1

    final_hash = struct.pack('<4I', A0, B0, C0, D0).hex()
    print(f"\nFinal Hash Value: {final_hash}")

if __name__ == "__main__":
    user_input = input("Enter message: ")
    md5_roundwise(user_input)
