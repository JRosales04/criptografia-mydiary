
"""
Modulo register_authenticate para la clase Register_Authenticate
"""

import base64
import json
import re

from pathlib import Path

from src.constants import CARACTERES_ESPECIALES, CONTRASEÑA_SISTEMA
from src.key import Key
from src.generate_pair_key import GeneratePairKey

class Register_Authenticate():
    def __init__(self):
        # Inicializamos el fichero de almacenamiento de usuarios
        self.filename = "data/usuarios.json"
        self.inicializar_json()
        self.crear_directorio("data/notes")
        self.crear_directorio("data/pks")
        self.crear_directorio("data/signs")
        self.crear_claves_sistema(CONTRASEÑA_SISTEMA)

    def inicializar_json(self):
        """Crea el archivo JSON con la información de los usuarios registrados"""
        # Comprobamos que el JSON no esté creado
        try:
            with open(self.filename, 'x') as file:
                # Creamos el JSON y le añadimos una lista vacía
                json.dump([], file, indent=4, sort_keys=True)
        # Si el archivo existe, no hacemos nada
        except FileExistsError:
            pass

    def crear_directorio(self, name):
        """Crea un directorio en la raíz del proyecto"""
        notes_dir = Path(f"{name}")
        if not notes_dir.exists():
            notes_dir.mkdir()

    def obtener_usuarios_registrados(self):
        """Actualiza el registro volcando el contenido del JSON"""
        with open(self.filename, 'r') as file:
            return json.load(file)

    def guardar_usuarios_registrados(self, lista):
        """Vuelca el contenido pasado por parámetro en el archivo JSON"""
        with open(self.filename, 'w') as file:
            json.dump(lista, file, indent=4, sort_keys=True)

    def crear_usuario(self, username, password):
        """Devuelve un diccionario con el nuevo registro del usuario"""
        # Obtenemos el password_token a partir de la contraseña
        pwdtoken_instance = Key(password)
        # Obtenemos el salt
        salt, pwd_token = pwdtoken_instance.derivate_pwdtoken()
        # Codificamos salt y key en Base64
        pwdtoken_base64 = base64.b64encode(pwd_token).decode('utf-8')
        salt_base64 = base64.b64encode(salt).decode('utf-8')
        print(f"Usuario registrado como: username={username}, salt_pwd={salt_base64}, pwd_token={pwdtoken_base64}")
        # Devolvemos un diccionario para serializarlo a JSON
        return {'nombre_usuario':username, 'salt_pwd':salt_base64, 'pwd_token':pwdtoken_base64}

    def comprobar_formato_contraseña(self, password):
        """Devuelve 0 si el formato de la contraseña es correcto; y un número negativo en función
        del error correspondiente. Establecemos como formato correcto una contraseña que contenga
        mínimo 8 caracteres, de los cuales se incluyan al menos una mayúscula, un número y un
        carácter especial"""
        # Verificar si el tamaño es correcto
        if len(password) < 8:
            return False
        # Verificar si contiene al menos una mayúscula
        if not re.search(r'[A-Z]', password):
            return False
        # Verificar si contiene al menos un número
        if not re.search(r'[0-9]', password):
            return False
        # Verificar si contiene al menos un carácter especial
        if not re.search(r'[{}]'.format(re.escape(CARACTERES_ESPECIALES)), password):
            return False
        return True

    def registrar_usuario(self, username, password):
        """Comprueba si el usuario entrante no está registrado, y añade sus datos en el archivo JSON"""
        # Actualizamos el registro de usuarios
        registro = self.obtener_usuarios_registrados()
        # Verificamos si el nombre de usuario no se repite
        for user in registro:
            if user['nombre_usuario'] == username:
                return False
        # Creamos el nuevo usuario registrado
        usuario = self.crear_usuario(username, password)
        registro.append(usuario)
        # Guardamos los datos actualizados en el archivo JSON
        self.guardar_usuarios_registrados(registro)
        print("Usuario guardado en el JSON")
        return True

    def autenticar_usuario(self, username, password):
        """Comprueba si el usuario entrante está registrado, y compara las contraseñas para darle
        acceso"""
        # Actualizamos el registro de usuarios
        registro = self.obtener_usuarios_registrados()
        # Verificamos si el usuario existe
        for user in registro:
            if user['nombre_usuario'] == username:
                key = Key(password)
                print(f"Inicio de sesión del usuario {username} con key={key}")
                return key.authenticate(user)
        print("Usuario no encontrado")
        return False

    def crear_claves_sistema(self, password):
        """Crea un par de claves para el sistema"""
        pk = GeneratePairKey(password)
        pk.save_keys()