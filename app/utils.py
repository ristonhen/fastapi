import secrets
import string
import base64
from passlib.context import CryptContext
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash(password: str):
    return pwd_context.hash(password)

def verify(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def encrypt(plaintext: str, key: str) -> str:
    cipher = AES.new(key.encode(), AES.MODE_CBC)
    ciphertext = cipher.encrypt(pad(plaintext.encode(), AES.block_size))
    iv = base64.b64encode(cipher.iv).decode('utf-8')
    encrypted_data = base64.b64encode(ciphertext).decode('utf-8')
    return f"{iv}:{encrypted_data}"

def decrypt(ciphertext: str, key: str) -> str:
    iv, encrypted_data = ciphertext.split(':')
    iv = base64.b64decode(iv)
    
    encrypted_data = base64.b64decode(encrypted_data)
    cipher = AES.new(key.encode(), AES.MODE_CBC, iv)
    decrypted_data = unpad(cipher.decrypt(encrypted_data), AES.block_size)
    return decrypted_data.decode('utf-8')

def generate_reset_token(length=16):
    characters = string.ascii_letters + string.digits
    reset_token = ''.join(secrets.choice(characters) for _ in range(length))
    return reset_token