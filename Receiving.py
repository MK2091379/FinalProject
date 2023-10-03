from Crypto.Cipher import AES
import numpy as np
import pickle


# Binary to File Conversion
def binary_to_file(binary_string, file_path):
    binary_data = np.array([int(binary_string[i:i+8], 2) for i in range(0, len(binary_string), 8)], dtype=np.uint8)
    extension_length = int.from_bytes(binary_data[:2], 'big')
    extension = binary_data[2:2+extension_length].tobytes().decode('utf-8')
    file_data = binary_data[2+extension_length:]

    with open(file_path + extension, 'wb') as file:
        file.write(file_data.tobytes())

# Convert DNA bases to binary
def dna_to_binary(dna_data):
    mapping = {'AT': '00', 'GC': '01', 'CG': '10', 'TA': '11'}
    binary_data = ''.join(mapping[dna_data[i:i+2]] for i in range(0, len(dna_data), 2))
    return binary_data

# AES decryption
def aes_decryption(cipher_text_binary, key):
    # Convert binary back to bytes
    cipher_text = bytes(int(cipher_text_binary[i:i+8], 2) for i in range(0, len(cipher_text_binary), 8))
    
    # Extract the initialization vector and the actual ciphertext
    iv = cipher_text[:AES.block_size]
    cipher_text = cipher_text[AES.block_size:]
    
    cipher = AES.new(key, AES.MODE_CFB, iv=iv)
    plain_text = cipher.decrypt(cipher_text)
    
    # Convert plain text bytes back to Huffman code
    huffman_code = ''.join(format(byte, '08b') for byte in plain_text)
    return huffman_code

# Read data from a file
def read_from_file(filename):
    with open(filename, 'r') as file:
        return file.read()

# Main function
def main():
    # Read the encrypted DNA data from a file
    encrypted_dna_data = read_from_file('encrypted_dna.txt')
    
    # Convert DNA bases to binary data
    binary_data = dna_to_binary(encrypted_dna_data)
    
    # Decrypt the data
    decrypted_data = aes_decryption(binary_data, b'This is a key123')
    
    # Load the Huffman codec from a file
    with open('huff_codec.pkl', 'rb') as f:
        codec = pickle.load(f)
        
    # Convert the binary data to bytes
    encoded_data = int(decrypted_data, 2).to_bytes((len(decrypted_data) + 7) // 8, 'big')

    # Decode the data
    decoded_data = codec.decode(encoded_data)
    
    # Converting binary data to file
    binary_to_file(decoded_data,'result')
    
if __name__ == "__main__":
    main()