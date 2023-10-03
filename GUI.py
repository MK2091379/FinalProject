import tkinter as tk
from tkinter import filedialog
from tkinter import ttk
import time
import pickle
from Sending import file_to_binary, HuffmanCodec, aes_encryption, binary_to_dna, write_to_file
from Receiving import binary_to_file, aes_decryption, dna_to_binary, read_from_file

def main():
    # Create a new Tkinter window
    window = tk.Tk()
    
    # Set the window size to 800x600
    window.geometry("200x200")
    
    # Set the window title
    window.title("My Encryption/Decryption App")
    
    # Set the background color to black
    window.configure(bg='black')

    # Create a button for encryption
    encrypt_button = tk.Button(window, text="Encrypt File", command=encrypt_file, bg='green', height = 2, width = 20)
    encrypt_button.pack(pady=10)

    # Create a button for decryption
    decrypt_button = tk.Button(window, text="Decrypt File", command=decrypt_file, bg='red', height = 2, width = 20)
    decrypt_button.pack(pady=10)

    # Create a progress bar
    #global progress
    #progress = ttk.Progressbar(window, length=100, mode='determinate')
    #progress.pack()

    # Run the Tkinter event loop
    window.mainloop()

def encrypt_file():
    # Open a file dialog and get the selected file path
    file_path = filedialog.askopenfilename()

    # Call your encryption functions here using the selected file path
    # For example:
    # Converting file to binary form
    binary_data = file_to_binary(file_path)
    
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
    
    # Update the progress bar in steps
    #for i in range(100):
    #    progress['value'] = i+1
    #    progress.update_idletasks()
    #    time.sleep(0.01)
    
    write_to_file(dna_data, 'encrypted_dna.txt')

def decrypt_file():
    # Open a file dialog and get the selected file path
    file_path = filedialog.askopenfilename()

    # Call your decryption functions here using the selected file path
    # For example:
    # Read the encrypted DNA data from a file
    encrypted_dna_data = read_from_file(file_path)
    
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
    
    # Update the progress bar in steps
    #for i in range(100):
    #    progress['value'] = i+1
    #    progress.update_idletasks()
    #    time.sleep(0.01)
        
    # Converting binary data to file
    binary_to_file(decoded_data,'result')
    
if __name__ == "__main__":
    main()