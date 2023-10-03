import os
from Crypto.Cipher import AES
from dahuffman import HuffmanCodec
from Crypto.Random import get_random_bytes
import numpy as np
import pickle

# File to Binary Conversion
def file_to_binary(file_path):
    _, file_extension = os.path.splitext(file_path)
    binary_extension = file_extension.encode('utf-8')
    binary_extension_length = len(binary_extension).to_bytes(2, 'big')

    def read_file_in_chunks(file, chunk_size=8192):
        while True:
            data = file.read(chunk_size)
            if not data:
                break
            yield data

    with open(file_path, 'rb') as file:
        binary_data = binary_extension_length + binary_extension
        for chunk in read_file_in_chunks(file):
            binary_data += chunk

    return ''.join(format(byte, '08b') for byte in np.frombuffer(binary_data, dtype=np.uint8))

# Convert binary to DNA bases
def binary_to_dna(binary_data):
    mapping = {'00': 'AT', '01': 'GC', '10': 'CG', '11': 'TA'}
    dna_data = ''.join(mapping[binary_data[i:i+2]] for i in range(0, len(binary_data), 2))
    return dna_data

# AES encryption
BLOCK_SIZE = 16

def aes_encryption(huffman_code, key):
    # Convert Huffman code to bytes
    plain_text = bytes(int(huffman_code[i:i+8], 2) for i in range(0, len(huffman_code), 8))
    
    # Generate a random initialization vector
    iv = get_random_bytes(AES.block_size)
    
    cipher = AES.new(key, AES.MODE_CFB, iv=iv)
    cipher_text = cipher.encrypt(plain_text)
    
    # Convert cipher text to binary
    cipher_text_binary = ''.join(format(byte, '08b') for byte in iv + cipher_text)
    return cipher_text_binary

# Write data to a file
def write_to_file(data, filename):
    with open(filename, 'w') as file:
        file.write(data)

# Main function
def main():
    # Converting file to binary form
    binary_data = file_to_binary('test.png')
    
    # Create a HuffmanCodec object from the data
    codec = HuffmanCodec.from_data(binary_data)
    # Encode the data
    encoded_data = codec.encode(binary_data)
    encoded_data = ''.join(format(byte, '08b') for byte in encoded_data)
    # Save the Huffman codec to a file
    with open('huff_codec.pkl', 'wb') as f:
        pickle.dump(codec, f)
    
    #Encrypt data    
    encrypted_data = aes_encryption(encoded_data, b'This is a key123')
    
    # Convert data to dna beses form
    dna_data = binary_to_dna(encrypted_data)
    
    # Write the encrypted DNA data to a file
    write_to_file(dna_data, 'encrypted_dna.txt')

if __name__ == "__main__":
    main()