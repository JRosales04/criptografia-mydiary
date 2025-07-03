
""""
Módulo para la gestión de firma
"""

import base64
import json
import os

from cryptography import x509
from src.constants import CONTRASEÑA_SISTEMA
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding

class Sign:

    def __init__(self, user):
        self.user = user
        self.private_key = self.load_private_key()
        self.filename = f"data/signs/{self.user}.json"

    def load_private_key(self):
        path = f"data/pks/pkv.pem"
        try:
            with open(path, 'rb') as key_file:
                private_key = serialization.load_pem_private_key(
                    data=key_file.read(),
                    password=CONTRASEÑA_SISTEMA.encode("utf-8"),
                )
                return private_key
        except ValueError as e:
            raise ValueError(
                    "Error: No se pudo descifrar o decodificar los datos PEM. Revisa la contraseña.") from e
        except TypeError as e:
            raise TypeError("Error: Contraseña incorrecta o clave no estaba cifrada.") from e
        except Exception as e:
            raise Exception("Error inesperado al cargar la clave privada.") from e

    def sign(self, message):
        # Creamos la firma
        signature = self.private_key.sign(
            message,
            padding.PSS(
                mgf=padding.MGF1(hashes.SHA256()),
                salt_length=padding.PSS.MAX_LENGTH
            ),
            hashes.SHA256()
        )
        # Convertir la firma a Base64 para almacenamiento en JSON
        signature_base64 = base64.b64encode(signature).decode('utf-8')
        note_signature = {"signature": signature_base64}
        # Si no existe el archivo, lo creamos y firmamos
        if not os.path.exists(self.filename):
            # Inicializamos el formato JSON
            data = [note_signature]
        # Si ya existe el archivo, añadimos la nueva firma
        else:
            with open(self.filename, 'r') as file:
                data = json.load(file)
                data.append(note_signature)
        # Guardamos en un archivo JSON
        with open(self.filename, 'w') as file:
            json.dump(data, file, indent=4, sort_keys=True)
        return signature_base64

    def validate_sign(self, message, sign):
        """Metodo para validar la firma de una nota"""
        # Cargamos el certificado de clave pública del sistema
        with open("data/pks/Acert.pem", "rb") as cert_file:
            certificado_A = x509.load_pem_x509_certificate(cert_file.read())
        # Extraemos la clave publica del certificado
        A_cert_pku = certificado_A.public_key()
        # Verificamos la firma
        A_cert_pku.verify(
            base64.b64decode(sign),
            message,
            padding.PSS(
                mgf=padding.MGF1(hashes.SHA256()),
                salt_length=padding.PSS.MAX_LENGTH
            ),
            hashes.SHA256()
        )
        print(f"La firma de la nota {message} es válida.")

    def validate_certificate(self):
        """Metodo para validar la firma del certificado de clave pública del sistema"""
        # Cargamos el certificado del sistema (A)
        with open("data/pks/Acert.pem", "rb") as cert_file:
            certificado_A = x509.load_pem_x509_certificate(cert_file.read())
        # Cargamos el certificado de la entidad de certificación (AC1, autoridad que firmó el certificado anterior)
        with open("openssl/AC1/ac1cert.pem", "rb") as cert_file:
            certificado_ac1 = x509.load_pem_x509_certificate(cert_file.read())
        # Verificamos que el emisor del certificado de A es AC1
        if certificado_A.issuer == certificado_ac1.subject:
            # Verificamos la firma del certificado con la clave publica de AC1
            certificado_ac1.public_key().verify(
                certificado_A.signature,
                certificado_A.tbs_certificate_bytes,
                padding.PKCS1v15(),
                    certificado_A.signature_hash_algorithm
            )
        print("El certificado del sistema ha sido verificado.")
        certificado_ac1.public_key().verify(
            certificado_ac1.signature,
            certificado_ac1.tbs_certificate_bytes,
            padding.PKCS1v15(),
            certificado_ac1.signature_hash_algorithm
        )
        print("El certificado de la entidad de certificación ha sido verificado.")
