
"""
Modulo que maneja la app (manager de Tkinter)
"""

import tkinter as tk
from src.screens import Home, InicioSesion, Registro, BlocNotas
from src.register_authenticate import Register_Authenticate

class App(tk.Tk):
    """Clase generadora de la interfaz"""
    def __init__(self, *args, **kwargs):
        """Método constructor de la clase; hereda de la clase tk.Tk"""
        super().__init__(*args, **kwargs)
        # Título de la ventana
        self.title("MyDiary.com")
        # Deshabilitamos el redimensionamiento de la ventana
        self.resizable(False, False)
        # Inicializamos una instancia para el registro del usuario
        self.user_manager = Register_Authenticate()
        # Creamos un contenedor principal para la interfaz
        container = tk.Frame(self)
        container.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        # Diccionario de frames (pantallas)
        self.frames = {}
        # Inicializamos las pantallas generales antes de que el usuario inicie sesión
        for F in (Home, InicioSesion, Registro):
            # Añadimos estas pantallas al diccionario de frames
            frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky=tk.NSEW)
        self.show_frame(Home)

    def show_frame(self, container, username=None, password=None):
        """Muestra la pantalla seleccionada, limpiando los campos si es necesario,
        y gestionando BlocNotas en función del usuario registrado"""
        # Buscamos la pantalla que vamos a mostrar según el container
        if container == Registro:
            # Limpiar los campos de Registro si se navega a dicha pantalla
            frame_registro = self.frames[Registro]
            frame_registro.username_entry.delete(0, tk.END)
            frame_registro.password_entry.delete(0, tk.END)
        elif container == InicioSesion:
            # Limpiar los campos de InicioSesion si se navega a dicha pantalla
            frame_inicio_sesion = self.frames[InicioSesion]
            frame_inicio_sesion.username_entry.delete(0, tk.END)
            frame_inicio_sesion.password_entry.delete(0, tk.END)
        elif container == BlocNotas and username and password:
            # Gestionamos la pantalla de BlocNotas en función del usuario
            # Primero verificamos si existe una instancia de BlocNotas para el usuario actual
            if username not in self.frames:
                # Si no existe, creamos una nueva instancia de BlocNotas para este usuario
                frame_bloc_notas = BlocNotas(self.frames[InicioSesion].master, self, username, password)
                # Almacenamos la instancia usando el username como clave
                self.frames[username] = frame_bloc_notas
                frame_bloc_notas.grid(row=0, column=0, sticky=tk.NSEW)
                # Cargamos las notas del usuario registrado
                frame_bloc_notas.cargar_notas()
            # En caso de que exista, cambiamos el container al frame específico del usuario
            container = username
        # Mostramos la pantalla solicitada
        frame = self.frames[container]
        frame.tkraise()