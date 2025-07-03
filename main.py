
"""
Modulo main para la ejecución de la app
"""

import os

from src.app import App

# Ejemplo de uso
if __name__ == "__main__":
    # Creamos un directorio de datos
    dir = "data"
    if not os.path.exists(dir):
        os.makedirs(dir)
    # Iniciamos la aplicacion
    app = App()
    # Ajustamos el tamaño
    app.geometry("400x400")
    # La actualizamos permanentemente
    app.mainloop()
