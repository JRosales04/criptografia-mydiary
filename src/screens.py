
import json
import tkinter as tk

from pathlib import Path
from tkinter import messagebox

from src.constants import BACKGROUND, BOTON
from src.aesgcm import AES
from src.note import Nota
from src.register_authenticate import Register_Authenticate
from src.sign_validation import Sign

# Pantalla Home (pantalla inicial de la APP)
class Home(tk.Frame):
    def __init__(self, parent, controller):
        """ Metodo constructor de la clase """
        super().__init__(parent)
        # Gestión de interfaz de Tkinter
        self.controller = controller
        self.configure(background=BACKGROUND)
        # Instancia de registro y autenticación de usuarios
        self.user_manager = Register_Authenticate()
        # Carga de objetos en la pantalla
        self.init_widgets()

    def init_widgets(self):
        """Inicializa los widgets en la pantalla"""
        # Frame principal para alinear elementos verticalmente
        main_frame = tk.Frame(self, bg=BACKGROUND)
        main_frame.pack(expand=True)
        # Título de la pantalla
        title_label = tk.Label(
            main_frame,
            text="MyDiary.com",
            font=("Arial", 30),
            bg=BACKGROUND,
            fg="black")
        title_label.pack(pady=15)
        # Frame para centrar los botones
        button_frame = tk.Frame(main_frame, bg=BACKGROUND)
        button_frame.pack()
        # Botón de Inicio de Sesión
        login_button = tk.Button(
            button_frame,
            text="Iniciar Sesión",
            command=self.iniciar_sesion,
            font=("Arial", 10),
            width=10,
            padx=7,
            pady=7,
            bg=BOTON,
            fg="black",
            relief="solid",
            bd=0
        )
        login_button.pack(pady=7)
        # Botón de Registrarse
        register_button = tk.Button(
            button_frame,
            text="Registrarse",
            command=self.registrarse,
            font=("Arial", 10),
            width=10,
            padx=7,
            pady=7,
            bg=BOTON,
            fg="black",
            relief="solid",
            bd=0
        )
        register_button.pack(pady=7)
        # Botón de Salir
        exit_button = tk.Button(
            button_frame,
            text="Salir",
            command=self.salir,
            font=("Arial", 10),
            width=10,
            padx=7,
            pady=7,
            bg=BOTON,
            fg="black",
            relief="solid",
            bd=0
        )
        exit_button.pack(pady=7)

    def iniciar_sesion(self):
        """ Lógica para el botón de iniciar sesión """
        self.controller.show_frame(InicioSesion)

    def registrarse(self):
        self.controller.show_frame(Registro)

    def salir(self):
        """ Lógica para salir de la aplicación """
        self.controller.quit()
        print("Saliendo de la aplicación...")

# Pantalla Registro (pantalla de registro de usuario)
class Registro(tk.Frame):
    def __init__(self, parent, controller):
        """ Metodo constructor de la clase """
        super().__init__(parent)
        # Gestión de interfaz de Tkinter
        self.configure(background=BACKGROUND)
        self.controller = controller
        # Instancia de registro y autenticación de usuarios
        self.user_manager = Register_Authenticate()
        # Carga de objetos en la pantalla
        self.init_widgets()

    def init_widgets(self):
        """Inicializa los widgets en la pantalla"""
        # Frame principal para alinear elementos verticalmente
        main_frame = tk.Frame(self, bg=BACKGROUND)
        main_frame.pack(expand=True)
        # Título de la pantalla
        title_label = tk.Label(
            main_frame,
            text="Registrarse",
            font=("Arial", 30),
            bg=BACKGROUND
        )
        title_label.pack(pady=5)
        # Frame para centrar los botones y campos de entrada
        button_frame = tk.Frame(main_frame, bg=BACKGROUND)
        button_frame.pack(pady=7)
        # Campo de entrada para el nombre de usuario
        self.username_label = tk.Label(
            button_frame,
            text="Nombre de usuario:",
            font=("Arial", 10),
            bg=BACKGROUND
        )
        self.username_label.pack(pady=2)
        # Etiqueta para escribir el nombre de usuario
        self.username_entry = tk.Entry(button_frame)
        self.username_entry.pack(pady=2)
        # Campo de entrada para la contraseña
        self.password_label = tk.Label(
            button_frame,
            text="Contraseña:",
            font=("Arial", 10),
            bg=BACKGROUND
        )
        self.password_label.pack(pady=2)
        # Etiqueta para escribir la contraseña
        self.password_entry = tk.Entry(button_frame, show="*")
        self.password_entry.pack(pady=2)
        # Botón para registrar
        register_button = tk.Button(
            button_frame,
            text="Registrar",
            command=self.registrar_usuario,
            font=("Arial", 10),
            width=10,
            padx=7,
            pady=7,
            bg=BOTON,
            fg="black",
            relief="solid",
            bd=0
        )
        register_button.pack(pady=15, padx=10)
        # Botón para volver al inicio
        back_button = tk.Button(
            button_frame,
            text="Volver al Inicio",
            command=lambda: self.controller.show_frame(Home),
            font=("Arial", 10),
            width=10,
            padx=7,
            pady=7,
            bg=BOTON,
            fg="black",
            relief="solid",
            bd=0
        )
        back_button.pack(pady=5, padx=10)

    def registrar_usuario(self):
        """Método para registrar un nuevo usuario"""
        # Obtenemos el username y la contraseña
        username = self.username_entry.get()
        password = self.password_entry.get()
        # Comprobamos que no sean strings vacíos
        if username and password:
            # Comprbamos el formato de la contraseña
            if not self.user_manager.comprobar_formato_contraseña(password):
                # Ventana de advertencia en caso de que la contraseña no presente un formato correcto
                messagebox.showinfo("Advertencia",
                                    "La contraseña no tiene un formato válido: mínimo 8 caracteres de los cuales incluyan al menos una mayúscula, un número y un carácter especial")
                self.controller.show_frame(Home)
            else:
                # Intentamos registrar el usuario
                if self.user_manager.registrar_usuario(username, password):
                    # Creamos su archivo JSON
                    self.crear_json_usuario(username)
                    # Ventana de éxito en caso de que el usuario se haya registrado correctamente
                    messagebox.showinfo("Éxito", "Usuario registrado exitosamente.")
                    self.controller.show_frame(Home)
                else:
                    # Ventana de error en caso de que el nombre de usuario se repita
                    messagebox.showerror("Error", "El nombre de usuario ya está en uso.")
        else:
            # Ventana de advertencia si los datos son strings vacíos
            messagebox.showwarning("Advertencia", "Por favor, ingresa un nombre de usuario y una contraseña.")

    def crear_json_usuario(self, username):
        """Crea un archivo JSON para el nuevo usuario registrado"""
        # Declaramos la ruta donde se creará el archivo JSON
        ruta = (str(Path.home()) + ("/PycharmProjects/PROYECTO.CRIPTOGRAFIA/data/notes/"))
        user_file = ruta + f"{username}.json"
        # Inicializamos una lista vacía donde almacenar los objetos Nota del usuario
        datos_usuario = []
        try:
            # Creamos y guardamos el archivo JSON
            with open(user_file, "w", encoding="utf-8") as file:
                json.dump(datos_usuario, file, ensure_ascii=False, indent=4)
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo crear el archivo JSON: {e}")

# Pantalla InicioSesion (pantalla de autenticado de usuario)
class InicioSesion(tk.Frame):
    def __init__(self, parent, controller):
        """ Método constructor de la clase """
        super().__init__(parent)
        # Gestión de interfaz de Tkinter
        self.configure(background=BACKGROUND)
        self.controller = controller
        # Instancia de registro y autenticación de usuario
        self.user_manager = Register_Authenticate()
        # Carga de objetos en la pantalla
        self.init_widgets()

    def init_widgets(self):
        """Inicializa los widgets en la pantalla"""
        # Frame principal para alinear elementos verticalmente
        main_frame = tk.Frame(self, bg=BACKGROUND)
        main_frame.pack(expand=True)
        # Título de la pantalla
        title_label = tk.Label(
            main_frame,
            text="Iniciar Sesión",
            font=("Arial", 30),
            bg=BACKGROUND)
        title_label.pack(pady=5)
        # Frame para centrar los botones y campos de entrada
        button_frame = tk.Frame(main_frame, bg=BACKGROUND)
        button_frame.pack(pady=7)
        # Campo de entrada para el nombre de usuario
        self.username_label = tk.Label(
            button_frame,
            text="Nombre de usuario:",
            font=("Arial", 10),
            bg=BACKGROUND
        )
        self.username_label.pack(pady=2)
        # Etiqueta para escribir el nombre de usuario
        self.username_entry = tk.Entry(button_frame)
        self.username_entry.pack(pady=2)
        # Campo de entrada para la contraseña
        self.password_label = tk.Label(
            button_frame,
            text="Contraseña:",
            font=("Arial", 10),
            bg=BACKGROUND
        )
        self.password_label.pack(pady=2)
        # Etiqueta para escribir la contraseña
        self.password_entry = tk.Entry(button_frame, show="*")
        self.password_entry.pack(pady=2)
        # Botón de inicio de sesión
        login_button = tk.Button(
            button_frame,
            text="Iniciar Sesión",
            command=self.iniciar_sesion,
            font = ("Arial", 10),
            width = 10,
            padx = 7,
            pady = 7,
            bg = BOTON,
            fg = "black",
            relief = "solid",
            bd = 0
        )
        login_button.pack(pady=15, padx=10)
        # Botón para volver al inicio
        back_button = tk.Button(
            button_frame,
            text="Volver al Inicio",
            command=lambda: self.controller.show_frame(Home),
            font=("Arial", 10),
            width=10,
            padx=7,
            pady=7,
            bg=BOTON,
            fg="black",
            relief="solid",
            bd=0
        )
        back_button.pack(pady=5, padx=10)

    def iniciar_sesion(self):
        """Método para iniciar sesión"""
        username = self.username_entry.get()
        password = self.password_entry.get()
        if self.user_manager.autenticar_usuario(username, password):
            messagebox.showinfo("Éxito", f"¡Bienvenido/a {username.upper()}!")
            self.controller.show_frame(BlocNotas, username, password)
        else:
            messagebox.showerror("Error", "Acceso denegado. Nombre de usuario o contraseña incorrectos.")

class BlocNotas(tk.Frame):
    def __init__(self, parent, controller, username, password):
        super().__init__(parent)
        # Gestion de interfaz en Tkinter
        self.configure(background=BACKGROUND)
        self.controller = controller
        # Atributos de la clase
        self.username = username
        # Instancia de AES
        self.aes = AES(username, password)
        # Instancia de firma y verificación de firmas
        self.sign = Sign(username)
        self.sign.validate_certificate()
        # Gestión del guardado de notas
        self.file = f"data/notes/{self.username}.json"
        self.notas = []
        # Carga de objetos en la pantalla
        self.cargar_notas()
        self.init_widgets()

    def init_widgets(self):
        main_frame = tk.Frame(self, bg=BACKGROUND)
        main_frame.pack(expand=True, fill=tk.BOTH)
        # Título de la pantalla
        titulo = tk.Label(
            main_frame,
            text=f"Bloc de Notas de {self.username.upper()}",
            font=("Arial", 15),
            bg=BACKGROUND
        )
        titulo.pack(pady=10)
        # Frame de notas y barra de desplazamiento
        notas_frame = tk.Frame(main_frame)
        notas_frame.pack(expand=True, fill=tk.BOTH)
        # Crear un canvas para la barra de desplazamiento
        self.canvas = tk.Canvas(
            notas_frame,
            bg=BACKGROUND
        )
        self.scrollbar = tk.Scrollbar(
            notas_frame,
            orient="vertical",
            command=self.canvas.yview
        )
        # Frame scrollable
        self.scrollable_frame = tk.Frame(self.canvas, bg=BACKGROUND)
        # Configurar el canvas
        self.scrollable_frame.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))
        # Calcular el ancho del canvas y centrar el scrollable_frame
        self.canvas.create_window((self.canvas.winfo_width() // 2, 0), window=self.scrollable_frame, anchor="n")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        # Empaquetar el canvas y la barra de desplazamiento
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        # Botones
        button_frame = tk.Frame(main_frame, bg=BACKGROUND)
        button_frame.pack(pady=5)
        btn_crear_nota = tk.Button(
            button_frame,
            text="Nueva Nota",
            command=self.crear_nota,
            font=("Arial", 10),
            bg=BACKGROUND,
            fg="black",
            relief="solid",
            bd=0
        )
        btn_crear_nota.grid(row=0, column=0, padx=10)
        btn_cerrar_sesion = tk.Button(
            button_frame,
            text="Cerrar Sesión",
            command=self.cerrar_sesion,
            font=("Arial", 10),
            bg=BACKGROUND,
            fg="black",
            relief="solid",
            bd=0
        )
        btn_cerrar_sesion.grid(row=0, column=1, padx=10)
        # Mostramos las notas
        self.mostrar_notas()

    def guardar_notas(self):
        cifrado = self.aes.encrypt(self.notas)
        with open(self.file, "w", encoding="utf-8") as file:
            json.dump(cifrado, file, ensure_ascii=False, indent=4)

    def cargar_notas(self):
        self.notas = self.aes.decrypt()
        if self.notas is None:
            self.notas = []

    def crear_nota(self):
        # Abrimos una ventana nueva
        ventana_nueva_nota = tk.Toplevel(self)
        # Añadimos el espacio de texto para el título
        ventana_nueva_nota.title("Nueva Nota")
        tk.Label(ventana_nueva_nota, text="Título:").pack(pady=5)
        titulo_entry = tk.Entry(ventana_nueva_nota, width=50)
        titulo_entry.pack(pady=5)
        # Añadimos el espacio de texto para el contenido
        tk.Label(ventana_nueva_nota, text="Contenido:").pack(pady=5)
        contenido_text = tk.Text(ventana_nueva_nota, height=10, width=50)
        contenido_text.pack(pady=5)
        # Asignamos un botón para guardar la nota
        boton_guardar_nota = tk.Button(
            ventana_nueva_nota,
            text="Guardar Nota",
            command=lambda: self.almacenar_nota(titulo_entry.get(), contenido_text.get("1.0", tk.END), ventana_nueva_nota),
            font = ("Arial", 10),
            bg = BACKGROUND,
            fg = "black",
            relief = "solid",
            bd = 0
        )
        boton_guardar_nota.pack(pady=10)

    def almacenar_nota(self, titulo, contenido, ventana_nueva_nota):
        # Comprobamos que los contenidos de la nota no estén vacíos
        if titulo.strip() and contenido.strip():
            # Creamos la instancia de Nota
            nueva_nota = Nota(titulo, contenido, self.username)
            # Firmamos y verificamos la nueva nota
            self.firmar_verificar_nota(nueva_nota)
            # Añadimos la nota en formato json a la lista de notas del usuario
            self.notas.append(nueva_nota.formato_json())
            # Guardamos las notas en el JSON
            self.guardar_notas()
            # Mostramos las notas por la interfaz
            self.mostrar_notas()
            # Cerramos la ventana de nueva nota
            ventana_nueva_nota.destroy()
        else:
            # Mensaje de advertencia en caso de que el contenido esté vacío
            messagebox.showwarning("Advertencia", "El título y el contenido no pueden estar vacíos.")

    def mostrar_notas(self):
        """Muestra cada nota en la pantalla"""
        # Limpiamos el contenido previo en el frame de notas
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()
        # Mostramos cada nota en el frame
        for idx, nota in enumerate(self.notas):
            # Frame de la nota con grid
            nota_frame = tk.Frame(self.scrollable_frame, bg=nota["background"], padx=10, pady=10)
            nota_frame.grid(row=idx, column=0, padx=5, pady=5, sticky="nsew")
            # Título de la nota
            titulo_label = tk.Label(nota_frame, text=nota["titulo"], bg=nota["background"], font=("Arial", 14),
                                    wraplength=350, justify="center", anchor="center")
            titulo_label.grid(row=0, column=0, columnspan=3, sticky="ew", pady=(0, 5))
            # Contenido de la nota
            contenido_label = tk.Label(nota_frame, text=nota["contenido"], bg=nota["background"], wraplength=350,
                                       justify="center", anchor="center")
            contenido_label.grid(row=1, column=0, columnspan=3, sticky="ew", pady=(0, 5))
            # Fecha de la nota
            fecha_label = tk.Label(nota_frame, text=nota["fecha"], bg=nota["background"], font=("Arial", 8),
                                   anchor="center")
            fecha_label.grid(row=2, column=0, sticky="nsew")
            # Hora de la nota
            hora_label = tk.Label(nota_frame, text=nota["hora"], bg=nota["background"], font=("Arial", 8),
                                  anchor="center")
            hora_label.grid(row=2, column=1, sticky="nsew")
            # Autor de la nota
            autor_label = tk.Label(nota_frame, text=nota["autor"].upper(), bg=nota["background"], font=("Arial", 8),
                                   anchor="center")
            autor_label.grid(row=2, column=2, sticky="nsew")
            nota_frame.grid_columnconfigure(0, weight=1)
            nota_frame.grid_columnconfigure(1, weight=1)
            nota_frame.grid_columnconfigure(2, weight=1)

    def firmar_verificar_nota(self, nota):
        """Gestión del firmado y verificacion de notas a partir de la clave privada del sistema"""
        # Obtenemos la nota en formato legible
        message = json.dumps(nota.formato_json()).encode('utf-8')
        # Firmamos la nota
        sign = self.sign.sign(message)
        print(f"Nota firmada: {sign}")
        # Verificamos la firma con la clave publica del sistema
        self.sign.validate_sign(message, sign)
        print(f"Nota verificada: {sign}")
        return True

    def cerrar_sesion(self):
        messagebox.showinfo("Sesión", "Sesión cerrada exitósamente")
        print(f"Cerrando sesión de {self.username}...")
        self.controller.show_frame(Home)
