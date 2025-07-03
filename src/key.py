
import os
import base64

from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives.kdf.scrypt import Scrypt
from cryptography.hazmat.primitives import hashes

class Key():
    def __init__(self, password):
        # Convertimos la contraseña a bytes
        self.password = password.encode('utf-8')
        # Salt para generar el password token
        self.salt_pwd = os.urandom(16)
        # Salt para generar la clave
        self.salt_key = os.urandom(16)

    def derivate_pwdtoken(self):
        """Genera una clave a partir de la contraseña"""
        kdf = Scrypt(salt=self.salt_pwd, length=32, n=2 ** 14, r=8, p=1)
        # Derivamos la clave usando la contraseña en formato bytes
        pwd_token = kdf.derive(self.password)
        return self.salt_pwd, pwd_token

    def authenticate(self, user: dict):
        """Verifica la contraseña del usuario"""
        salt_json = user["salt_pwd"]
        key_json = user["pwd_token"]
        # Convertimos el salt y la clave desde base64 si son cadenas
        if isinstance(salt_json, str):
            salt = base64.b64decode(salt_json)
        else:
            salt = salt_json
        if isinstance(key_json, str):
            key_token = base64.b64decode(key_json)
        else:
            key_token = key_json
        # Preparamos el KDF con el salt almacenado (longitud de 32 bytes)
        kdf = Scrypt(salt=salt, length=32, n=2 ** 14, r=8, p=1)
        # Verificamos la contraseña, que debe estar en bytes
        try:
            # Verificamos si la clave derivada coincide (kdf.verify())
            kdf.verify(self.password, key_token)
            return True
        except Exception as e:
            return False
        
    def generate_key(self):
        """Genera una clave cada vez que queramos cifrar, usando self.salt_key"""
        kdf = PBKDF2HMAC(algorithm=hashes.SHA256(), length=32, salt=self.salt_key, iterations=480000)
        key = kdf.derive(self.password)
        return self.salt_key, key