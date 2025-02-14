import tkinter as tk
from tkinter import messagebox, simpledialog
import pickle
import random
from datetime import datetime, timedelta
from src.UDManager.gestorAplicacion.eventos.evento import Evento
from src.UDManager.gestorAplicacion.inscripcion.joven import Joven
from src.UDManager.gestorAplicacion.reservas.instalacion import Instalacion
from src.UDManager.gestorAplicacion.reservas.reserva import Reserva
from src.UDManager.gestorAplicacion.pagos.cliente import Cliente
from src.UDManager.gestorAplicacion.pagos.boleta import Boleta
from src.UDManager.gestorAplicacion.torneo.torneo import Torneo
from src.UDManager.gestorAplicacion.inscripcion.tiendaEscuela import TiendaEscuela

# Componente genérico para mostrar listas de atributo-valor de forma estática.
# Este componente hereda de Frame y coloca dos columnas de Labels:
# una para el nombre del criterio y otra para su valor.
class FieldFrame(tk.Frame):
    def __init__(self, master, tituloCriterios, criterios, tituloValores, valores, habilitado=None, **kwargs):
        """
        Crea un FieldFrame para mostrar criterios y sus valores (no editables).
        :param master: contenedor padre.
        :param tituloCriterios: título de la columna de criterios.
        :param criterios: lista con los nombres de los criterios.
        :param tituloValores: título de la columna de valores.
        :param valores: lista con los valores a mostrar (si es None, se deja en blanco).
        :param habilitado: (no utilizado en esta versión, todos son no editables).
        """
        super().__init__(master, **kwargs)
        # Cabecera con los títulos de ambas columnas
        tk.Label(self, text=tituloCriterios, font=("Arial", 12, "bold")).grid(row=0, column=0, padx=5, pady=5)
        tk.Label(self, text=tituloValores, font=("Arial", 12, "bold")).grid(row=0, column=1, padx=5, pady=5)
        # Crear una fila por cada criterio
        for i, criterio in enumerate(criterios, start=1):
            tk.Label(self, text=criterio, anchor="w").grid(row=i, column=0, padx=5, pady=2, sticky="w")
            value = ""
            if valores and i-1 < len(valores):
                value = valores[i-1]
            tk.Label(self, text=value, anchor="w").grid(row=i, column=1, padx=5, pady=2, sticky="w")
        self.columnconfigure(1, weight=1)

    def getValue(self, criterio):
        # En esta versión no se puede editar, así que se retorna None.
        return None

# Instancia global para la tienda
tiendaEscuela = TiendaEscuela()
Instalacion.crearInstalaciones()

class Application(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Complejo Deportivo")
        self.geometry("1100x750")
        self.resizable(False, False)

        # Cargar base de datos (se utiliza pickle mediante Deserializador)
        from src.UDManager.baseDatos.deserializador import Deserializador
        Deserializador.deserializar()

        # Se obtienen las listas desde las clases modelo
        self.clientes = Cliente.getListaClientes()
        self.instalaciones = Instalacion.listaInstalaciones
        self.torneos = Torneo.getTorneos()
        self.eventos = Evento.getEventos()
        self.pagos = Boleta.listaBoletas  # Se usa la lista de boletas
        self.arbitros = []
        self.medicos = []
        self.paramedicos = []
        self.foodtrucks = []
        self.formativos = []
        self.suscripciones = []

        # Zona 0: Título y descripción de la aplicación
        title_frame = tk.Frame(self, bd=2, relief="ridge", bg="#ecf0f1")
        title_frame.pack(fill="x")
        title_label = tk.Label(title_frame, text="Complejo Deportivo", font=("Arial", 24, "bold"), bg="#ecf0f1", fg="#2c3e50")
        title_label.pack(side="left", padx=10, pady=5)
        desc_label = tk.Label(title_frame, text="Utilice el menú para gestionar las funcionalidades del sistema", font=("Arial", 12), bg="#ecf0f1", fg="#2c3e50")
        desc_label.pack(side="left", padx=10, pady=5)

        # Zona 1: Menú superior
        menubar = tk.Menu(self)
        fileMenu = tk.Menu(menubar, tearoff=0)
        fileMenu.add_command(label="Guardar", command=self.save_db)
        fileMenu.add_command(label="Cargar", command=lambda: messagebox.showinfo("BD", "Funcionalidad de carga implementada en inicio.py"))
        fileMenu.add_separator()
        fileMenu.add_command(label="Salir", command=self.quit)
        menubar.add_cascade(label="Archivo", menu=fileMenu)
        self.config(menu=menubar)

        # Zona 2: Botones de navegación y área de contenido
        self.tab_buttons_frame = tk.Frame(self, bd=2, relief="raised")
        self.tab_buttons_frame.pack(fill="x")
        self.tabs = {}
        self.create_tab_buttons()

        self.content_frame = tk.Frame(self)
        self.content_frame.pack(fill="both", expand=True)

        # Crear pestañas utilizando FieldFrame en la parte superior de cada una
        self.tabs["Clientes"] = self.create_clientes_tab()
        self.tabs["Instalaciones"] = self.create_instalaciones_tab()
        self.tabs["Reservas"] = self.create_reservas_tab()
        self.tabs["Torneos"] = self.create_torneos_tab()
        self.tabs["Eventos"] = self.create_eventos_tab()
        self.tabs["Pagos"] = self.create_pagos_tab()
        self.tabs["Formativo"] = self.create_formativo_tab()

        self.show_tab("Clientes")

    def create_tab_buttons(self):
        botones = ["Clientes", "Instalaciones", "Reservas", "Torneos", "Eventos", "Pagos", "Formativo"]
        for b in botones:
            btn = tk.Button(self.tab_buttons_frame, text=b, command=lambda name=b: self.show_tab(name))
            btn.pack(side="left", padx=2, pady=2)

    def show_tab(self, tab_name):
        for frame in self.content_frame.winfo_children():
            frame.pack_forget()
        self.tabs[tab_name].pack(fill="both", expand=True)

    def save_db(self):
        from src.UDManager.baseDatos.serializador import Serializador
        Serializador.serializar()
        messagebox.showinfo("BD", "Base de datos guardada correctamente.")

    # ---------------------------- TAB CLIENTES ----------------------------
    def create_clientes_tab(self):
        frame = tk.Frame(self.content_frame)
        # Se muestra el título del proceso y su descripción
        field = FieldFrame(frame, "Criterio", ["Proceso", "Descripción"], "Valor",
                            ["Gestión de Clientes", "Permite crear y visualizar clientes"])
        field.pack(fill="x", padx=5, pady=5)
        btn_crear = tk.Button(frame, text="Crear Cliente (sin suscripción)", command=lambda: messagebox.showinfo("Crear Cliente", "Función Crear Cliente no implementada."))
        btn_crear.pack(pady=10)
        btn_ver = tk.Button(frame, text="Ver Clientes", command=lambda: messagebox.showinfo("Ver Clientes", "Función Ver Clientes no implementada."))
        btn_ver.pack(pady=10)
        return frame

    # ---------------------------- TAB INSTALACIONES ----------------------------
    def create_instalaciones_tab(self):
        frame = tk.Frame(self.content_frame)
        field = FieldFrame(frame, "Criterio", ["Proceso", "Descripción"], "Valor",
                            ["Gestión de Instalaciones", "Visualiza las instalaciones disponibles"])
        field.pack(fill="x", padx=5, pady=5)
        btn_ver = tk.Button(frame, text="Ver Instalaciones", command=lambda: messagebox.showinfo("Instalaciones", "Función Ver Instalaciones no implementada."))
        btn_ver.pack(pady=10)
        return frame

    # ---------------------------- TAB RESERVAS ----------------------------
    def create_reservas_tab(self):
        frame = tk.Frame(self.content_frame)
        field = FieldFrame(frame, "Criterio", ["Proceso", "Descripción"], "Valor",
                            ["Gestión de Reservas", "Permite crear y consultar reservas"])
        field.pack(fill="x", padx=5, pady=5)
        btn_crear = tk.Button(frame, text="Crear Reserva", command=lambda: messagebox.showinfo("Crear Reserva", "Función Crear Reserva no implementada."))
        btn_crear.pack(pady=10)
        btn_ver = tk.Button(frame, text="Ver Reservas", command=lambda: messagebox.showinfo("Ver Reservas", "Función Ver Reservas no implementada."))
        btn_ver.pack(pady=10)
        return frame

    # ---------------------------- TAB TORNEOS ----------------------------
    def create_torneos_tab(self):
        frame = tk.Frame(self.content_frame)
        field = FieldFrame(frame, "Criterio", ["Proceso", "Descripción"], "Valor",
                            ["Gestión de Torneos", "Crea torneos y muestra el fixture"])
        field.pack(fill="x", padx=5, pady=5)
        btn_crear = tk.Button(frame, text="Crear Torneo", command=lambda: messagebox.showinfo("Crear Torneo", "Función Crear Torneo no implementada."))
        btn_crear.pack(pady=10)
        btn_ver = tk.Button(frame, text="Ver Fixture", command=lambda: messagebox.showinfo("Ver Fixture", "Función Ver Fixture no implementada."))
        btn_ver.pack(pady=10)
        btn_equipos = tk.Button(frame, text="Ver Equipos", command=lambda: messagebox.showinfo("Ver Equipos", "Función Ver Equipos no implementada."))
        btn_equipos.pack(pady=10)
        return frame

    # ---------------------------- TAB EVENTOS ----------------------------
    def create_eventos_tab(self):
        frame = tk.Frame(self.content_frame)
        field = FieldFrame(frame, "Criterio", ["Proceso", "Descripción"], "Valor",
                            ["Gestión de Eventos", "Permite crear y consultar eventos"])
        field.pack(fill="x", padx=5, pady=5)
        btn_crear = tk.Button(frame, text="Crear Evento", command=lambda: messagebox.showinfo("Crear Evento", "Función Crear Evento no implementada."))
        btn_crear.pack(pady=10)
        btn_ver = tk.Button(frame, text="Ver Eventos", command=lambda: messagebox.showinfo("Ver Eventos", "Función Ver Eventos no implementada."))
        btn_ver.pack(pady=10)
        return frame

    # ---------------------------- TAB PAGOS ----------------------------
    def create_pagos_tab(self):
        frame = tk.Frame(self.content_frame)
        field = FieldFrame(frame, "Criterio", ["Proceso", "Descripción"], "Valor",
                            ["Gestión de Pagos", "Realiza pagos de suscripciones, reservas, etc."])
        field.pack(fill="x", padx=5, pady=5)
        btn_sus = tk.Button(frame, text="Pagar Suscripción", command=lambda: messagebox.showinfo("Pagar Suscripción", "Función Pagar Suscripción no implementada."))
        btn_sus.pack(pady=5)
        btn_cancel = tk.Button(frame, text="Cancelar Suscripción", command=lambda: messagebox.showinfo("Cancelar Suscripción", "Función Cancelar Suscripción no implementada."))
        btn_cancel.pack(pady=5)
        btn_res = tk.Button(frame, text="Pagar Reserva", command=lambda: messagebox.showinfo("Pagar Reserva", "Función Pagar Reserva no implementada."))
        btn_res.pack(pady=5)
        btn_event = tk.Button(frame, text="Pagar Evento", command=lambda: messagebox.showinfo("Pagar Evento", "Función Pagar Evento no implementada."))
        btn_event.pack(pady=5)
        btn_boleta = tk.Button(frame, text="Comprar Boleta (Evento/Torneo)", command=lambda: messagebox.showinfo("Comprar Boleta", "Función Comprar Boleta no implementada."))
        btn_boleta.pack(pady=5)
        btn_torneo = tk.Button(frame, text="Pagar Torneo", command=lambda: messagebox.showinfo("Pagar Torneo", "Función Pagar Torneo no implementada."))
        btn_torneo.pack(pady=5)
        return frame

    # ---------------------------- TAB FORMATIVO ----------------------------
    def create_formativo_tab(self):
        frame = tk.Frame(self.content_frame)
        field = FieldFrame(frame, "Criterio", ["Proceso", "Descripción"], "Valor",
                            ["Gestión Formativa", "Permite inscribir y consultar jóvenes"])
        field.pack(fill="x", padx=5, pady=5)
        btn_inscribir = tk.Button(frame, text="Inscribir Joven", command=lambda: messagebox.showinfo("Inscribir Joven", "Función Inscribir Joven no implementada."))
        btn_inscribir.pack(pady=10)
        btn_ver = tk.Button(frame, text="Ver Inscripciones", command=lambda: messagebox.showinfo("Ver Inscripciones", "Función Ver Inscripciones no implementada."))
        btn_ver.pack(pady=10)
        return frame

    def enterSystem(self):
        self.destroy()
        from src.UDManager.uiMain.app import Application
        app = Application()
        app.mainloop()

    def on_resize(self, event):
        from PIL import Image, ImageTk
        new_w = self.winfo_width()
        new_h = self.winfo_height()
        scale = min(new_w / self.BASE_WIDTH, new_h / self.BASE_HEIGHT)

        # Redimensionar las imágenes del botón utilizando Pillow
        btn_files = ["image1.png", "image2.png", "image3.png", "image4.png", "image5.png"]
        new_image_list = []
        for i, file in enumerate(btn_files):
            try:
                pil_img = Image.open(file)
            except Exception as e:
                print(f"Error al abrir {file}: {e}")
                pil_img = Image.new("RGB", (200, 150), "white")
            orig_size = pil_img.size
            new_size = (max(1, int(orig_size[0] * scale)), max(1, int(orig_size[1] * scale)))
            resized = pil_img.resize(new_size, Image.LANCZOS)
            new_image_list.append(ImageTk.PhotoImage(resized))
        self.imageList = new_image_list
        self.enterButton.config(image=self.imageList[self.currentImageIndex])
        self.enterButton.image = self.imageList[self.currentImageIndex]

        # Redimensionar las imágenes de los desarrolladores
        dev_index = self.currentResumeIndex
        dev_files = [f"dev{dev_index+1}_{i}.png" for i in range(1, 5)]
        new_dev_images = []
        for i, file in enumerate(dev_files):
            try:
                pil_img = Image.open(file)
            except Exception as e:
                print(f"Error al abrir {file}: {e}")
                pil_img = Image.new("RGB", (100, 100), "white")
            orig_size = pil_img.size
            new_size = (max(1, int(orig_size[0] * scale)), max(1, int(orig_size[1] * scale)))
            resized = pil_img.resize(new_size, Image.LANCZOS)
            new_dev_images.append(ImageTk.PhotoImage(resized))
        self.devImages = new_dev_images
        self.photoLabel1.config(image=self.devImages[0])
        self.photoLabel1.image = self.devImages[0]
        self.photoLabel2.config(image=self.devImages[1])
        self.photoLabel2.image = self.devImages[1]
        self.photoLabel3.config(image=self.devImages[2])
        self.photoLabel3.image = self.devImages[2]
        self.photoLabel4.config(image=self.devImages[3])
        self.photoLabel4.image = self.devImages[3]

if __name__ == "__main__":
    app = Application()
    app.mainloop()
