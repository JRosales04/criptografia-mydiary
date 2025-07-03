
""""
Módulo para generar el par de claves y almacenarla
"""

import os

from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization

class GeneratePairKey:
    def __init__(self, password):
        # Contraseña para cifrar la clave privada con RSA
        self.password = password.encode('utf-8')
        self.private_key = self.generate_keys()
        self.public_key = self.private_key.public_key()

    def generate_keys(self):
        """Genera el par de claves para el sistema"""
        # Creamos la clave privada, a partir de la cual podremos obtener también la pública
        private_key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=2048,
        )
        return private_key

    def save_keys(self):
        """Crea la clave privada del sistema"""
        private_key_path = f"data/pks/pkv.pem"
        pk_directory_path = f"data/pks"
        # Verificar si los archivos de claves ya existen
        if os.path.exists(pk_directory_path):
            return
        else:
            if os.path.exists(private_key_path):
                return
            # Serializamos la clave privada
            pem_private_key = self.private_key.private_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PrivateFormat.PKCS8,
                encryption_algorithm=serialization.BestAvailableEncryption(self.password)
            )
            # Guardamos la clave privada en un archivo .pem
            if pem_private_key.splitlines()[0] == b'-----BEGIN ENCRYPTED PRIVATE KEY-----':
                with open(private_key_path, "wb") as archivo:
                    archivo.write(pem_private_key)
            print(f"Clave privada guardada: {pem_private_key}")
