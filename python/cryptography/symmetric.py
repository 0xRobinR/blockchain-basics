from Crypto.Cipher import AES
import os

def pad(data):
    length = 16 - (len(data) % 16)
    return data + bytes([length]) * length

def unpad(data):
    return data[:-data[-1]]

def encrypt(key, data):
    cipher = AES.new(key, AES.MODE_ECB)
    return cipher.encrypt(pad(data))

def decrypt(key, enc_data):
    cipher = AES.new(key, AES.MODE_ECB)
    return unpad(cipher.decrypt(enc_data))

key = b'this-key-is-a-custom-key'
data = b"blockchain is a way, that keeps centralization away"
print(f"Original Data: {data}")

enc_data = encrypt(key, data)
print(f"Encrypted Data: {enc_data}")

dec_data = decrypt(key, enc_data)
print(f"Decrypted Data: {dec_data}")
