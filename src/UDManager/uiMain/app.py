# src/UDManager/uiMain/app.py

import tkinter as tk
from tkinter import messagebox
from src.UDManager.gestorAplicacion.eventos.evento import Evento
from src.UDManager.gestorAplicacion.inscripcion.joven import Joven
from src.UDManager.gestorAplicacion.reservas.instalacion import Instalacion
from src.UDManager.gestorAplicacion.reservas.reserva import Reserva
from src.UDManager.gestorAplicacion.pagos.cliente import Cliente
from src.UDManager.gestorAplicacion.pagos.boleta import Boleta
from src.UDManager.gestorAplicacion.torneo.torneo import Torneo
from src.UDManager.gestorAplicacion.inscripcion.tiendaEscuela import TiendaEscuela

tiendaEscuela = TiendaEscuela()
Instalacion.crearInstalaciones()

class Application(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Complejo Deportivo")
        self.geometry("1100x750")
        self.resizable(False, False)

        # Cargar base de datos (se implementa con pickle en BaseDatos)
        from src.UDManager.baseDatos.deserializador import Deserializador
        Deserializador.deserializar()

        # Se asumen listas globales; en una implementación real se cargarían desde BD
        self.clientes = Cliente.getListaClientes()
        self.instalaciones = Instalacion.listaInstalaciones
        self.torneos = Torneo.getTorneos()
        self.eventos = Evento.getEventos()
        self.pagos = Boleta.listaBoletas  # O la lista de pagos que uses
        # Se asignan demás listas según la estructura de BD
        self.arbitros = []
        self.medicos = []
        self.paramedicos = []
        self.foodtrucks = []
        self.formativos = []
        self.suscripciones = []

        # Zona 0: Título y descripción
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

        # Zona 2: Navegación y contenido
        self.tab_buttons_frame = tk.Frame(self, bd=2, relief="raised")
        self.tab_buttons_frame.pack(fill="x")
        self.tabs = {}
        self.create_tab_buttons()

        self.content_frame = tk.Frame(self)
        self.content_frame.pack(fill="both", expand=True)

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

    def create_clientes_tab(self):
        frame = tk.Frame(self.content_frame)
        lbl = tk.Label(frame, text="Gestión de Clientes", font=("Arial", 18))
        lbl.pack(pady=10)
        btn_crear = tk.Button(frame, text="Crear Cliente (sin suscripción)", command=self.crear_cliente)
        btn_crear.pack(pady=10)
        btn_ver = tk.Button(frame, text="Ver Clientes", command=self.ver_clientes)
        btn_ver.pack(pady=10)
        return frame

    def crear_cliente(self):
        # Se implementa la creación de clientes mediante un diálogo
        pass  # Se agrega la lógica real según el proyecto

    def ver_clientes(self):
        # Se implementa la visualización de clientes
        pass

    def create_instalaciones_tab(self):
        frame = tk.Frame(self.content_frame)
        lbl = tk.Label(frame, text="Instalaciones", font=("Arial", 18))
        lbl.pack(pady=10)
        btn_ver = tk.Button(frame, text="Ver Instalaciones", command=self.ver_instalaciones)
        btn_ver.pack(pady=10)
        return frame

    def ver_instalaciones(self):
        # Lógica para ver instalaciones
        pass

    def create_reservas_tab(self):
        frame = tk.Frame(self.content_frame)
        lbl = tk.Label(frame, text="Reservas", font=("Arial", 18))
        lbl.pack(pady=10)
        btn_crear = tk.Button(frame, text="Crear Reserva", command=self.crear_reserva)
        btn_crear.pack(pady=10)
        btn_ver = tk.Button(frame, text="Ver Reservas", command=self.ver_reservas)
        btn_ver.pack(pady=10)
        return frame

    def crear_reserva(self):
        # Lógica para crear reserva
        pass

    def ver_reservas(self):
        # Lógica para ver reservas
        pass

    def create_torneos_tab(self):
        frame = tk.Frame(self.content_frame)
        lbl = tk.Label(frame, text="Torneos", font=("Arial", 18))
        lbl.pack(pady=10)
        btn_crear = tk.Button(frame, text="Crear Torneo", command=self.crear_torneo)
        btn_crear.pack(pady=10)
        btn_ver = tk.Button(frame, text="Ver Fixture", command=self.ver_fixture)
        btn_ver.pack(pady=10)
        btn_equipos = tk.Button(frame, text="Ver Equipos", command=self.ver_equipos_torneo)
        btn_equipos.pack(pady=10)
        return frame

    def crear_torneo(self):
        # Lógica para crear torneo
        pass

    def ver_fixture(self):
        # Lógica para ver fixture
        pass

    def ver_equipos_torneo(self):
        # Lógica para ver equipos y jugadores de torneo
        pass

    def create_eventos_tab(self):
        frame = tk.Frame(self.content_frame)
        lbl = tk.Label(frame, text="Eventos", font=("Arial", 18))
        lbl.pack(pady=10)
        btn_crear = tk.Button(frame, text="Crear Evento", command=self.crear_evento)
        btn_crear.pack(pady=10)
        btn_ver = tk.Button(frame, text="Ver Eventos", command=self.ver_eventos)
        btn_ver.pack(pady=10)
        return frame

    def crear_evento(self):
        # Lógica para crear evento
        pass

    def ver_eventos(self):
        # Lógica para ver eventos
        pass

    def create_pagos_tab(self):
        frame = tk.Frame(self.content_frame)
        lbl = tk.Label(frame, text="Pagos", font=("Arial", 18))
        lbl.pack(pady=10)
        # Se añaden botones para las funcionalidades de pago
        btn_sus = tk.Button(frame, text="Pagar Suscripción", command=self.pagar_suscripcion)
        btn_sus.pack(pady=5)
        btn_cancel = tk.Button(frame, text="Cancelar Suscripción", command=self.cancelar_suscripcion)
        btn_cancel.pack(pady=5)
        btn_res = tk.Button(frame, text="Pagar Reserva", command=self.pagar_reserva)
        btn_res.pack(pady=5)
        btn_event = tk.Button(frame, text="Pagar Evento", command=self.pagar_evento)
        btn_event.pack(pady=5)
        btn_boleta = tk.Button(frame, text="Comprar Boleta (Evento/Torneo)", command=self.comprar_boleta)
        btn_boleta.pack(pady=5)
        btn_torneo = tk.Button(frame, text="Pagar Torneo", command=self.pagar_torneo)
        btn_torneo.pack(pady=5)
        return frame

    def pagar_suscripcion(self):
        # Lógica para pagar suscripción
        pass

    def cancelar_suscripcion(self):
        # Lógica para cancelar suscripción
        pass

    def pagar_reserva(self):
        # Lógica para pagar reserva
        pass

    def pagar_evento(self):
        messagebox.showinfo("Pago", "Funcionalidad de pago de eventos no implementada en este ejemplo.")

    def comprar_boleta(self):
        # Lógica para comprar boleta
        pass

    def pagar_torneo(self):
        # Lógica para pagar torneo
        pass

    def create_formativo_tab(self):
        frame = tk.Frame(self.content_frame)
        lbl = tk.Label(frame, text="Formativo", font=("Arial", 18))
        lbl.pack(pady=10)
        btn_inscribir = tk.Button(frame, text="Inscribir Joven", command=self.inscribir_joven)
        btn_inscribir.pack(pady=10)
        btn_ver = tk.Button(frame, text="Ver Inscripciones", command=self.ver_formativos)
        btn_ver.pack(pady=10)
        return frame

    def inscribir_joven(self):
        # Lógica para inscribir un joven
        pass

    def ver_formativos(self):
        # Lógica para ver inscripciones formativas
        pass

    def enterSystem(self):
        self.destroy()
        from src.UDManager.uiMain.app import Application
        app = Application()
        app.mainloop()

if __name__ == "__main__":
    app = Application()
    app.mainloop()
