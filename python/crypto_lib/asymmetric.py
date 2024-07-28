import random
from sympy import isprime
from crypto_lib.sha256 import sha256

def generate_large_prime(bits):
    while True:
        prime_candidate = random.getrandbits(bits)
        if isprime(prime_candidate):
            return prime_candidate

def egcd(a, b):
    if a == 0:
        return b, 0, 1
    g, y, x = egcd(b % a, a)
    return g, x - (b // a) * y, y

def modinv(a, m):
    _, x, _ = egcd(a, m)
    return x % m

def generate_keys(bits=1024):
    p = generate_large_prime(bits)
    q = generate_large_prime(bits)

    n = p * q
    phi = (p - 1) * (q - 1)
    e = 65537
    d = modinv(e, phi)
    public_key = (e, n)
    private_key = (d, n)
    return public_key, private_key

def encrypt(public_key, plaintext):
    e, n = public_key
    plaintext_bytes = plaintext.encode('utf-8')
    plaintext_int = int.from_bytes(plaintext_bytes, byteorder='big')
    ciphertext_int = pow(plaintext_int, e, n)
    return ciphertext_int

def decrypt(private_key, ciphertext):
    d, n = private_key
    plaintext_int = pow(ciphertext, d, n)
    plaintext_bytes = plaintext_int.to_bytes((plaintext_int.bit_length() + 7) // 8, byteorder='big')
    return plaintext_bytes.decode('utf-8')

def create_signature(private_key, message):
    d, n = private_key
    message_hash = int.from_bytes(sha256(message.encode('utf-8')), byteorder='big')
    signature = pow(message_hash, d, n)
    return signature

def verify_signature(public_key, message, signature):
    e, n = public_key
    message_hash = int.from_bytes(sha256(message.encode('utf-8')), byteorder='big')
    signature_hash = pow(signature, e, n)
    return message_hash == signature_hash

def main():
    public_key, private_key = generate_keys(bits=512)
    print(public_key)
    print()
    print(private_key)
    print()

    message = "Hello, this is a secret message!"
    ciphertext = encrypt(public_key, message)
    print("Encrypted:", ciphertext)
    decrypted_message = decrypt(private_key, ciphertext)
    print("Decrypted:", decrypted_message)
    signature = create_signature(private_key, message)
    print("Signature:", signature)
    is_valid = verify_signature(public_key, message, signature)
    print("Signature valid:", is_valid)

if __name__ == "__main__":
    main()
