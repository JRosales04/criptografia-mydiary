
"""
Módulo que maneja la lógica de las notas
"""

import random
from datetime import datetime

class Nota():
    def __init__(self, titulo, contenido, autor):
        # Declaramos los atributos de la nota
        self.titulo = titulo
        self.contenido = contenido
        self.fecha = datetime.now().strftime("%Y-%m-%d")
        self.hora = datetime.now().strftime("%H:%M:%S")
        self.autor = autor
        self.background = self.generar_color_fondo()

    def formato_json(self):
        """Devuelve una instancia de la nota en formato JSON"""
        return {
            "titulo": self.titulo,
            "contenido": self.contenido,
            "fecha": self.fecha,
            "hora": self.hora,
            "autor": self.autor,
            "background": self.background,
        }

    def generar_color_fondo(self):
        """Generar componentes de color RGB aleatorios en el rango de 128 a 255 (colores claros)"""
        # Generamos las componentes RGB
        rojo = random.randint(128, 255)
        verde = random.randint(128, 255)
        azul = random.randint(128, 255)
        # Convertimos el formato a hexadecimal
        color_hexadecimal = "#{:02x}{:02x}{:02x}".format(rojo, verde, azul)
        # Devolvemos el color en hexadecimal
        return color_hexadecimal
