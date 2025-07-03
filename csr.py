
"""
Script de creación de CSR (Request de certificado)
"""

import os

from src.constants import CONTRASEÑA_SISTEMA

from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives import hashes
from cryptography.x509 import NameOID
from cryptography import x509

# Función para extraer la clave privada
def load_private_key():
    try:
        with open(f"data/pks/pkv.pem", 'rb') as key_file:
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

if __name__ == "__main__":
    # Creamos un directorio para almacenar el CSR
    dir = "data/reqx509"
    if not os.path.exists(dir):
        os.makedirs(dir)
    # Creamos la solicitud de certificado (CSR)
    csr = x509.CertificateSigningRequestBuilder().subject_name(x509.Name([
        x509.NameAttribute(NameOID.COUNTRY_NAME, "ES"),
        x509.NameAttribute(NameOID.STATE_OR_PROVINCE_NAME, "MADRID"),
        x509.NameAttribute(NameOID.ORGANIZATION_NAME, "UC3M"),
        x509.NameAttribute(NameOID.COMMON_NAME, "MyDiary.com"),
        x509.NameAttribute(NameOID.EMAIL_ADDRESS, "100500450@uc3m.es"),
    ])
    ).sign(load_private_key(), hashes.SHA256())
    # Guardamos la CSR en un archivo
    with open("data/reqx509/Areq.pem", "wb") as csr_file:
        csr_file.write(csr.public_bytes(serialization.Encoding.PEM))
    # Print de depuración
    print("CSR generado y guardado en 'data/reqx509/Areq.pem'")