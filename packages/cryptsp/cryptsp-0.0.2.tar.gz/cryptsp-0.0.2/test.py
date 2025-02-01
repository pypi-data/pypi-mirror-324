import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from src.cryptsp import CryptoManager


def example_usage():
    # Initialize the crypto manager
    crypto = CryptoManager()

    # Generate a random key
    key = crypto.generate_key()

    # Example data
    data = "Hello, World!"

    # AES encryption/decryption
    encrypted = crypto.encrypt_aes(data, key)
    decrypted = crypto.decrypt_aes(encrypted, key)
    print(f"AES: {decrypted.decode()}")

    # ChaCha20 encryption/decryption
    encrypted = crypto.encrypt_chacha20(data, key)
    decrypted = crypto.decrypt_chacha20(encrypted, key)
    print(f"ChaCha20: {decrypted.decode()}")

    # RSA encryption/decryption
    private_key, public_key = crypto.generate_rsa_keypair()
    encrypted = crypto.encrypt_rsa(data, public_key)
    decrypted = crypto.decrypt_rsa(encrypted, private_key)
    print(f"RSA: {decrypted.decode()}")

    # Digital signature
    signature = crypto.sign_data(data, private_key)
    is_valid = crypto.verify_signature(data, signature, public_key)
    print(f"Signature valid: {is_valid}")

if __name__ == "__main__":
    example_usage()
