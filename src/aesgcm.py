
"""
Modulo que maneja el cifrado por el algoritmo AES-GCM
"""

import os
import json
import base64

from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from src.key import Key
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes

class AES():

    def __init__(self, username, password):
        # Declaramos los atributos que vamos a usar
        self.usuario = username
        self.password = password
        # Generamos el nonce (numero aleatorio de 12 bytes)
        self.nonce = os.urandom(12)
        # Generar la clave para el cifrado-autenticado con AES-GCM
        self.salt, self.key = Key(password).generate_key()

    def encrypt(self, lista_notas):
        """Método de cifrado: devuelve un diccionario serializable a JSON que contiene
        el mensaje cifrado, el nonce, el salt y el tag"""
        print(f"Datos en claro: {lista_notas}")
        cifrado = Cipher(algorithms.AES(self.key), modes.GCM(self.nonce))
        cifrador = cifrado.encryptor()
        contenido_str = json.dumps(lista_notas)
        texto_cifrado = cifrador.update(contenido_str.encode()) + cifrador.finalize()
        print(f"Datos cifrados: {texto_cifrado}")
        return {
            "texto_cifrado": base64.b64encode(texto_cifrado).decode('utf-8'),
            "nonce": base64.b64encode(self.nonce).decode('utf-8'),
            "salt": base64.b64encode(self.salt).decode('utf-8'),
            "tag": base64.b64encode(cifrador.tag).decode('utf-8')
        }

    def decrypt(self):
        """Método de descifrado: obtiene el diccionario de cifrado y devuelve los datos
        en claro (la lista con las notas)"""
        datos_decrypt = self.extraer_datos_json()
        if isinstance(datos_decrypt, dict):
            texto_cifrado = base64.b64decode(datos_decrypt['texto_cifrado'])
            print(f"Datos cifrados: {texto_cifrado}")
            nonce = base64.b64decode(datos_decrypt['nonce'])
            salt = base64.b64decode(datos_decrypt['salt'])
            tag = base64.b64decode(datos_decrypt['tag'])
            # Se vuelve a generar la clave con la contraseña
            kdf = PBKDF2HMAC(algorithm=hashes.SHA256(), length=32, salt=salt, iterations=480000)
            key_descifrar = kdf.derive(self.password.encode('utf-8'))
            descifrador = Cipher(algorithms.AES(key_descifrar), modes.GCM(nonce, tag)).decryptor()
            texto_bytes = descifrador.update(texto_cifrado) + descifrador.finalize()
            print(f"Datos en claro: {texto_bytes.decode('utf-8')}")
            return json.loads(texto_bytes.decode('utf-8'))
        return datos_decrypt

    def extraer_datos_json(self):
        """Metodo auxiliar para extraer los datos del JSON correspondiente al usuario"""
        try:
            with open(f"data/notes/{self.usuario}.json", 'r') as file:
                data = json.load(file)
                return data
        except FileNotFoundError:
            return []
