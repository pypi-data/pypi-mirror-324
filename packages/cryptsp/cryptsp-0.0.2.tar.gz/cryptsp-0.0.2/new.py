from Crypto.Cipher import AES, ChaCha20_Poly1305, Salsa20
from Crypto.Util.Padding import pad, unpad
from Crypto.PublicKey import RSA, ECC
from Crypto.Cipher import PKCS1_OAEP
from Crypto.Signature import pss, DSS
from Crypto.Hash import SHA256, SHA512, HMAC
from Crypto.Protocol.KDF import PBKDF2, scrypt, HKDF
from Crypto.Random import get_random_bytes
from base64 import b64encode, b64decode
import hashlib
import os
import json
from typing import Union, Dict, Tuple, Optional
from dataclasses import dataclass
from jwt import encode as jwt_encode, decode as jwt_decode, ExpiredSignatureError
from bcrypt import hashpw, gensalt, checkpw
from argon2 import PasswordHasher

class CryptoException(Exception):
    """Base exception class for cryptography operations."""
    pass

@dataclass
class EncryptedData:
    """Container for encrypted data and metadata."""
    algorithm: str
    ciphertext: bytes
    iv: Optional[bytes] = None
    tag: Optional[bytes] = None
    nonce: Optional[bytes] = None

    def to_dict(self) -> Dict:
        """Convert to dictionary format for serialization."""
        return {
            'algorithm': self.algorithm,
            'ciphertext': b64encode(self.ciphertext).decode('utf-8'),
            'iv': b64encode(self.iv).decode('utf-8') if self.iv else None,
            'tag': b64encode(self.tag).decode('utf-8') if self.tag else None,
            'nonce': b64encode(self.nonce).decode('utf-8') if self.nonce else None
        }

    @classmethod
    def from_dict(cls, data: Dict) -> 'EncryptedData':
        """Create instance from dictionary."""
        return cls(
            algorithm=data['algorithm'],
            ciphertext=b64decode(data['ciphertext']),
            iv=b64decode(data['iv']) if data.get('iv') else None,
            tag=b64decode(data['tag']) if data.get('tag') else None,
            nonce=b64decode(data['nonce']) if data.get('nonce') else None
        )

class CryptoManager:
    """Main class for cryptographic operations."""
    
    def __init__(self, default_key_size: int = 32):
        """Initialize with default key size in bytes."""
        self.default_key_size = default_key_size
        self.ph = PasswordHasher()  # For Argon2

    def generate_key(self, size: Optional[int] = None) -> bytes:
        """Generate a secure random key."""
        return os.urandom(size or self.default_key_size)

    def derive_key(self, password: str, salt: bytes = None, iterations: int = 100000, 
                   algorithm: str = 'PBKDF2') -> Tuple[bytes, bytes]:
        """Derive a key from a password using PBKDF2 or Argon2."""
        if salt is None:
            salt = os.urandom(16)
        
        if algorithm == 'PBKDF2':
            key = PBKDF2(password.encode(), salt, dkLen=32, count=iterations)
        elif algorithm == 'Argon2':
            key = self.ph.hash(password.encode(), salt=salt).encode()
            key = hashlib.sha256(key).digest()  # Derive a 32-byte key
        else:
            raise CryptoException(f"Unsupported key derivation algorithm: {algorithm}")
        
        return key, salt

    def encrypt_aes(self, data: Union[str, bytes], key: bytes, mode: str = 'GCM') -> EncryptedData:
        """Encrypt data using AES with specified mode."""
        if isinstance(data, str):
            data = data.encode()

        if mode == 'GCM':
            cipher = AES.new(key, AES.MODE_GCM)
            ciphertext, tag = cipher.encrypt_and_digest(data)
            return EncryptedData('AES-GCM', ciphertext, nonce=cipher.nonce, tag=tag)
        elif mode == 'CBC':
            cipher = AES.new(key, AES.MODE_CBC)
            ciphertext = cipher.encrypt(pad(data, AES.block_size))
            return EncryptedData('AES-CBC', ciphertext, iv=cipher.iv)
        elif mode == 'CTR':
            cipher = AES.new(key, AES.MODE_CTR)
            ciphertext = cipher.encrypt(data)
            return EncryptedData('AES-CTR', ciphertext, nonce=cipher.nonce)
        else:
            raise CryptoException(f"Unsupported AES mode: {mode}")

    def decrypt_aes(self, encrypted_data: EncryptedData, key: bytes) -> bytes:
        """Decrypt AES-encrypted data."""
        if encrypted_data.algorithm == 'AES-GCM':
            cipher = AES.new(key, AES.MODE_GCM, nonce=encrypted_data.nonce)
            return cipher.decrypt_and_verify(encrypted_data.ciphertext, encrypted_data.tag)
        elif encrypted_data.algorithm == 'AES-CBC':
            cipher = AES.new(key, AES.MODE_CBC, iv=encrypted_data.iv)
            return unpad(cipher.decrypt(encrypted_data.ciphertext), AES.block_size)
        elif encrypted_data.algorithm == 'AES-CTR':
            cipher = AES.new(key, AES.MODE_CTR, nonce=encrypted_data.nonce)
            return cipher.decrypt(encrypted_data.ciphertext)
        else:
            raise CryptoException(f"Unsupported algorithm: {encrypted_data.algorithm}")

    def encrypt_chacha20(self, data: Union[str, bytes], key: bytes) -> EncryptedData:
        """Encrypt data using ChaCha20-Poly1305."""
        if isinstance(data, str):
            data = data.encode()
        
        cipher = ChaCha20_Poly1305.new(key=key)
        ciphertext, tag = cipher.encrypt_and_digest(data)
        return EncryptedData('CHACHA20', ciphertext, nonce=cipher.nonce, tag=tag)

    def decrypt_chacha20(self, encrypted_data: EncryptedData, key: bytes) -> bytes:
        """Decrypt ChaCha20-Poly1305 encrypted data."""
        cipher = ChaCha20_Poly1305.new(key=key, nonce=encrypted_data.nonce)
        return cipher.decrypt_and_verify(encrypted_data.ciphertext, encrypted_data.tag)

    def encrypt_salsa20(self, data: Union[str, bytes], key: bytes) -> EncryptedData:
        """Encrypt data using Salsa20."""
        if isinstance(data, str):
            data = data.encode()
        
        nonce = get_random_bytes(8)  # Salsa20 uses an 8-byte nonce
        cipher = Salsa20.new(key=key, nonce=nonce)
        ciphertext = cipher.encrypt(data)
        return EncryptedData('SALSA20', ciphertext, nonce=nonce)

    def decrypt_salsa20(self, encrypted_data: EncryptedData, key: bytes) -> bytes:
        """Decrypt Salsa20 encrypted data."""
        cipher = Salsa20.new(key=key, nonce=encrypted_data.nonce)
        return cipher.decrypt(encrypted_data.ciphertext)

    def generate_ecc_keypair(self, curve: str = 'P-256') -> Tuple[ECC.EccKey, ECC.EccKey]:
        """Generate ECC key pair."""
        key = ECC.generate(curve=curve)
        return key, key.public_key()

    def generate_rsa_keypair(self, key_size: int = 2048) -> Tuple[RSA.RsaKey, RSA.RsaKey]:
        """Generate RSA key pair."""
        key = RSA.generate(key_size)
        return key, key.publickey()

    def encrypt_rsa(self, data: Union[str, bytes], public_key: RSA.RsaKey) -> bytes:
        """Encrypt data using RSA."""
        if isinstance(data, str):
            data = data.encode()
        cipher = PKCS1_OAEP.new(public_key)
        return cipher.encrypt(data)

    def decrypt_rsa(self, encrypted_data: bytes, private_key: RSA.RsaKey) -> bytes:
        """Decrypt RSA-encrypted data."""
        cipher = PKCS1_OAEP.new(private_key)
        return cipher.decrypt(encrypted_data)

    def encrypt_ecies(self, data: Union[str, bytes], public_key: ECC.EccKey) -> EncryptedData:
        """Encrypt data using ECIES (Elliptic Curve Integrated Encryption Scheme)."""
        if isinstance(data, str):
            data = data.encode()
        
        # Generate an ephemeral ECC key
        ephemeral_key = ECC.generate(curve='P-256')
        shared_key = ephemeral_key.d * public_key.pointQ  # ECDH shared secret
        shared_key = hashlib.sha256(shared_key.x.to_bytes(32, 'big')).digest()  # Derive symmetric key
        
        # Encrypt data using AES-GCM
        cipher = AES.new(shared_key, AES.MODE_GCM)
        ciphertext, tag = cipher.encrypt_and_digest(data)
        
        # Serialize ephemeral public key
        ephemeral_pubkey = ephemeral_key.public_key().export_key(format='DER')
        
        return EncryptedData('ECIES', ciphertext, nonce=cipher.nonce, tag=tag, iv=ephemeral_pubkey)

    def decrypt_ecies(self, encrypted_data: EncryptedData, private_key: ECC.EccKey) -> bytes:
        """Decrypt ECIES encrypted data."""
        # Deserialize ephemeral public key
        ephemeral_pubkey = ECC.import_key(encrypted_data.iv)
        
        # Compute shared secret
        shared_key = private_key.d * ephemeral_pubkey.pointQ
        shared_key = hashlib.sha256(shared_key.x.to_bytes(32, 'big')).digest()  # Derive symmetric key
        
        # Decrypt data using AES-GCM
        cipher = AES.new(shared_key, AES.MODE_GCM, nonce=encrypted_data.nonce)
        return cipher.decrypt_and_verify(encrypted_data.ciphertext, encrypted_data.tag)

    def create_hmac(self, data: Union[str, bytes], key: bytes, hash_algo: str = 'SHA256') -> bytes:
        """Create HMAC for data authentication."""
        if isinstance(data, str):
            data = data.encode()
            
        if hash_algo == 'SHA256':
            h = HMAC.new(key, digestmod=SHA256)
        elif hash_algo == 'SHA512':
            h = HMAC.new(key, digestmod=SHA512)
        else:
            raise CryptoException(f"Unsupported hash algorithm: {hash_algo}")
            
        h.update(data)
        return h.digest()

    def verify_hmac(self, data: Union[str, bytes], hmac: bytes, key: bytes, 
                    hash_algo: str = 'SHA256') -> bool:
        """Verify HMAC."""
        calculated_hmac = self.create_hmac(data, key, hash_algo)
        return hmac == calculated_hmac

    def sign_data(self, data: Union[str, bytes], private_key: Union[RSA.RsaKey, ECC.EccKey]) -> bytes:
        """Sign data using RSA or ECC private key."""
        if isinstance(data, str):
            data = data.encode()
        
        h = SHA256.new(data)
        if isinstance(private_key, RSA.RsaKey):
            signer = pss.new(private_key)
        else:  # ECC
            signer = DSS.new(private_key, 'fips-186-3')
        return signer.sign(h)

    def verify_signature(self, data: Union[str, bytes], signature: bytes, 
                        public_key: Union[RSA.RsaKey, ECC.EccKey]) -> bool:
        """Verify signature using RSA or ECC public key."""
        if isinstance(data, str):
            data = data.encode()
            
        h = SHA256.new(data)
        try:
            if isinstance(public_key, RSA.RsaKey):
                verifier = pss.new(public_key)
                verifier.verify(h, signature)
            else:  # ECC
                verifier = DSS.new(public_key, 'fips-186-3')
                verifier.verify(h, signature)
            return True
        except (ValueError, TypeError):
            return False

    def encrypt_file(self, file_path: str, key: bytes, algorithm: str = 'AES-GCM') -> str:
        """Encrypt a file and save the encrypted version."""
        with open(file_path, 'rb') as f:
            data = f.read()
            
        if algorithm.startswith('AES'):
            encrypted_data = self.encrypt_aes(data, key, mode=algorithm.split('-')[1])
        elif algorithm == 'CHACHA20':
            encrypted_data = self.encrypt_chacha20(data, key)
        else:
            raise CryptoException(f"Unsupported algorithm: {algorithm}")

        output_path = f"{file_path}.encrypted"
        with open(output_path, 'w') as f:
            json.dump(encrypted_data.to_dict(), f)
            
        return output_path

    def decrypt_file(self, encrypted_file_path: str, key: bytes) -> str:
        """Decrypt an encrypted file and save the decrypted version."""
        with open(encrypted_file_path, 'r') as f:
            encrypted_data = EncryptedData.from_dict(json.load(f))

        if encrypted_data.algorithm.startswith('AES'):
            decrypted_data = self.decrypt_aes(encrypted_data, key)
        elif encrypted_data.algorithm == 'CHACHA20':
            decrypted_data = self.decrypt_chacha20(encrypted_data, key)
        else:
            raise CryptoException(f"Unsupported algorithm: {encrypted_data.algorithm}")

        output_path = encrypted_file_path.replace('.encrypted', '.decrypted')
        with open(output_path, 'wb') as f:
            f.write(decrypted_data)
            
        return output_path

# Example usage of all methods
manager = CryptoManager()
key = manager.generate_key()

# AES-GCM
encrypted_data = manager.encrypt_aes("Hello, AES-GCM!", key, mode='GCM')
decrypted_data = manager.decrypt_aes(encrypted_data, key)
print("Decrypted (AES-GCM):", decrypted_data.decode())

# AES-CBC
encrypted_data = manager.encrypt_aes("Hello, AES-CBC!", key, mode='CBC')
decrypted_data = manager.decrypt_aes(encrypted_data, key)
print("Decrypted (AES-CBC):", decrypted_data.decode())

# AES-CTR
encrypted_data = manager.encrypt_aes("Hello, AES-CTR!", key, mode='CTR')
decrypted_data = manager.decrypt_aes(encrypted_data, key)
print(decrypted_data.decode())  # Output: Hello, AES-CTR!

# ChaCha20
encrypted_data = manager.encrypt_chacha20("Hello, ChaCha20!", key)
decrypted_data = manager.decrypt_chacha20(encrypted_data, key)
print("Decrypted (ChaCha20):", decrypted_data.decode())

# Salsa20
encrypted_data = manager.encrypt_salsa20("Hello, Salsa20!", key)
decrypted_data = manager.decrypt_salsa20(encrypted_data, key)
print(decrypted_data.decode())  # Output: Hello, Salsa20!

# ECIES
private_key, public_key = manager.generate_ecc_keypair()
encrypted_data = manager.encrypt_ecies("Hello, ECIES!", public_key)
decrypted_data = manager.decrypt_ecies(encrypted_data, private_key)
print(decrypted_data.decode())  # Output: Hello, ECIES!

# Argon2
key, salt = manager.derive_key("my_password", algorithm='Argon2')
print(f"Derived key: {b64encode(key).decode()}")

data_to_encrypt = "Hello, Argon2!"
encrypted_data = manager.encrypt_aes(data_to_encrypt, key, mode='GCM')
decrypted_data = manager.decrypt_aes(encrypted_data, key)
print("Decrypted Data:", decrypted_data.decode())

# RSA
private_key, public_key = manager.generate_rsa_keypair()
encrypted_data = manager.encrypt_rsa("Hello, RSA!", public_key)
decrypted_data = manager.decrypt_rsa(encrypted_data, private_key)
print("Decrypted (RSA):", decrypted_data.decode())

# PBKDF2
key, salt = manager.derive_key("my_password", algorithm='PBKDF2')
print(f"Derived key (PBKDF2): {b64encode(key).decode()}")

# HMAC
data = "Hello, HMAC!"
hmac = manager.create_hmac(data, key, hash_algo='SHA256')
is_valid = manager.verify_hmac(data, hmac, key, hash_algo='SHA256')
print("HMAC Valid:", is_valid)

# Digital Signatures (RSA)
data = "Hello, Signature!"
signature = manager.sign_data(data, private_key)
is_valid = manager.verify_signature(data, signature, public_key)
print("Signature Valid (RSA):", is_valid)

# Digital Signatures (ECC)
data = "Hello, ECC Signature!"
signature = manager.sign_data(data, private_key)
is_valid = manager.verify_signature(data, signature, public_key)
print("Signature Valid (ECC):", is_valid)


file_path = "/Users/srivatsapalepu/cryptsp/example.txt"
encrypted_file = manager.encrypt_file(file_path, key, algorithm='AES-GCM')
decrypted_file = manager.decrypt_file(encrypted_file, key)

with open(decrypted_file, "r") as f:
    print("Decrypted File Content:", f.read())
