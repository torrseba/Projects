
'''
- You may use this program to verify that your assembly program produces the same hash values
- You do not need include assert statements inside of your assembly program. They are included
  in this file to improved readability by providing details on the expected size of inputs 
  and outputs
'''

BLOCK_SIZE = 8
HALF_BLOCK_SIZE = BLOCK_SIZE // 2
HALF_BLOCK_BIT_SIZE = HALF_BLOCK_SIZE * 8
CIPHER_ROUNDS = 4


def pad_message(message: bytes) -> bytes:
    if len(message) % 8 == 0:
        return message

    message += 0x80.to_bytes(1, "little", signed=False)
    if len(message) % 8 == 0:
        return message

    total_zero_bytes = (BLOCK_SIZE - (len(message) % BLOCK_SIZE))
    message += b'\0' * total_zero_bytes
    assert len(message) % BLOCK_SIZE == 0
    return message


def blue_hen_prf(block: bytes, right: bytes) -> bytes:
    assert len(block) == BLOCK_SIZE
    assert len(right) == HALF_BLOCK_SIZE
    block_low = int.from_bytes(block[HALF_BLOCK_SIZE:], byteorder='little', signed=False)
    block_high = int.from_bytes(block[:HALF_BLOCK_SIZE], byteorder='little', signed=False)
    right = int.from_bytes(right, byteorder='little', signed=False)

    out = (right + block_low) & 0xFFFFFFFF
    out = (((out << 8) & 0xFFFFFFFF) | ((out >> (HALF_BLOCK_BIT_SIZE - 8)) & 0xFFFFFFFF)) & 0xFFFFFFFF
    out = (out + block_high) & 0xFFFFFFFF
    out = (((out >> 3) & 0xFFFFFFFF) | ((out << (HALF_BLOCK_BIT_SIZE - 3)) & 0xFFFFFFFF)) & 0xFFFFFFFF
    return out.to_bytes(HALF_BLOCK_SIZE, byteorder='little', signed=False)


def blue_hen_compression_function(h: bytes, block: bytes) -> bytes:
    assert len(h) == BLOCK_SIZE
    assert len(block) == BLOCK_SIZE
    left = h[:HALF_BLOCK_SIZE]
    right = h[HALF_BLOCK_SIZE:]
    for i in range(CIPHER_ROUNDS):
        next_left = right
        next_right = blue_hen_prf(block, right)
        next_right = bytes(x ^ y for x, y in zip(left, next_right))
        left, right = next_left, next_right

    output = left + right
    assert len(output) == BLOCK_SIZE
    return output


def blue_hen_hash(message: bytes) -> bytes:
    iv = b'BLUE_HEN'
    h = iv
    padded_message = pad_message(message)
    for i in range(0, len(padded_message), BLOCK_SIZE):
        block = padded_message[i:i+BLOCK_SIZE]
        compressed_block = blue_hen_compression_function(h, block)
        h = bytes(x ^ y for x, y in zip(h, compressed_block))
    assert len(h) == BLOCK_SIZE
    return h[::-1]


def main():
    message = input("Enter a message: ").encode('ascii')
    #message_hash = blue_hen_hash(message)
    message_hash = blue_hen_hash(b'HELLO!\x8b')
    print(message_hash.hex().upper())


if __name__ == '__main__':
    main()
   
