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

# Importa la clase FieldFrame desde su archivo
from src.UDManager.uiMain.fieldFrame import FieldFrame

TiendaEscuela = TiendaEscuela()
Instalacion.crearInstalaciones()

class Application(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Complejo Deportivo")
        self.geometry("1100x750")
        self.resizable(False, False)

        # Cargar base de datos (usando pickle en BaseDatos)
        from src.UDManager.baseDatos.deserializador import Deserializador
        Deserializador.deserializar()

        # Listas globales
        self.clientes = Cliente.getListaClientes()
        self.instalaciones = Instalacion.listaInstalaciones
        self.torneos = Torneo.getTorneos()
        self.eventos = Evento.getEventos()
        self.pagos = Boleta.listaBoletas
        self.arbitros = []
        self.medicos = []
        self.paramedicos = []
        self.foodtrucks = []
        self.formativos = []
        self.suscripciones = []

        # ZONA 0: Título y descripción
        titleFrame = tk.Frame(self, bd=2, relief="ridge", bg="#ecf0f1")
        titleFrame.pack(fill="x")
        titleLabel = tk.Label(titleFrame, text="Complejo Deportivo",
                              font=("Arial", 24, "bold"),
                              bg="#ecf0f1", fg="#2c3e50")
        titleLabel.pack(side="left", padx=10, pady=5)
        descLabel = tk.Label(titleFrame,
                             text="Utilice el menú para gestionar las funcionalidades del sistema",
                             font=("Arial", 12),
                             bg="#ecf0f1", fg="#2c3e50")
        descLabel.pack(side="left", padx=10, pady=5)

        # ZONA 1: Menú Superior
        menubar = tk.Menu(self)
        fileMenu = tk.Menu(menubar, tearoff=0)
        fileMenu.add_command(label="Aplicacion", command=self.infoAplicacion)
        # Se han quitado las opciones de Guardar y Cargar
        fileMenu.add_separator()
        fileMenu.add_command(label="Salir", command=self.salir)
        menubar.add_cascade(label="Archivo", menu=fileMenu)

        procesosMenu = tk.Menu(menubar, tearoff=0)
        procesosMenu.add_command(label="Clientes", command=self.mostrarClientes)
        procesosMenu.add_command(label="Instalaciones", command=self.mostrarInstalaciones)
        procesosMenu.add_command(label="Reservas", command=self.mostrarReservas)
        procesosMenu.add_command(label="Torneos", command=self.mostrarTorneos)
        procesosMenu.add_command(label="Eventos", command=self.mostrarEventos)
        procesosMenu.add_command(label="Pagos", command=self.mostrarPagos)
        procesosMenu.add_command(label="Formativo", command=self.mostrarFormativo)
        menubar.add_cascade(label="Procesos y Consultas", menu=procesosMenu)

        ayudaMenu = tk.Menu(menubar, tearoff=0)
        ayudaMenu.add_command(label="Acerca de", command=self.acercaDe)
        menubar.add_cascade(label="Ayuda", menu=ayudaMenu)

        self.config(menu=menubar)

        # ZONA 2: Contenido Principal
        self.contentFrame = tk.Frame(self, bg="white")
        self.contentFrame.pack(fill="both", expand=True)
        self.mostrarInicio()

    def infoAplicacion(self):
        msg = ("Esta aplicacion permite gestionar clientes, instalaciones, reservas, "
               "torneos, eventos, pagos y procesos formativos en el Complejo Deportivo.")
        messagebox.showinfo("Informacion de la Aplicacion", msg)

    def acercaDe(self):
        # Muestra los nombres de los desarrolladores
        devs = ("Los desarrolladores de este programa son:\n\n"
            "Fabián Andrés Hurtado Arango\n"
            "Christian Bustos Betancur\n"
            "José Mauricio Toscano Aguas\n"
            "Jesús Daniel Pérez Petro")

        messagebox.showinfo("Acerca de", devs)

    def mostrarInicio(self):
        for widget in self.contentFrame.winfo_children():
            widget.destroy()
        lbl = tk.Label(self.contentFrame,
                       text="Bienvenido al Sistema\n\nUse el menu 'Procesos y Consultas' para acceder a cada modulo.",
                       font=("Arial", 16), bg="white", fg="#2c3e50")
        lbl.pack(expand=True)

    def mostrarClientes(self):
        for widget in self.contentFrame.winfo_children():
            widget.destroy()
        title = tk.Label(self.contentFrame, text="Gestion de Clientes", font=("Arial", 18), bg="white")
        title.pack(pady=10)
        formFrame = tk.Frame(self.contentFrame, bg="white")
        formFrame.pack(pady=10, fill="x")
        criteria = ["Nombre", "Apellido", "Edad"]
        readOnly = []
        fieldFrame = FieldFrame(formFrame, "Criterio", criteria, "Valor", None, readOnly)
        fieldFrame.pack(fill="both", expand=True, padx=10, pady=10)
        btnFrame = tk.Frame(formFrame, bg="white")
        btnFrame.pack(side="bottom", pady=10)

        def onAceptar():
            missing = []
            for crit in criteria:
                if not fieldFrame.getValue(crit).strip():
                    missing.append(crit)
            if missing:
                messagebox.showwarning("Campos Incompletos", "Faltan: " + ", ".join(missing))
            else:
                nombre = fieldFrame.getValue("Nombre")
                apellido = fieldFrame.getValue("Apellido")
                try:
                    edad = int(fieldFrame.getValue("Edad"))
                except ValueError:
                    edad = 0
                # El cliente se crea y se guarda en la lista global automáticamente
                nuevoCliente = Cliente(nombre=nombre, apellido=apellido, edad=edad)
                messagebox.showinfo("Exito", f"Cliente '{nuevoCliente.getNombreCompleto()}' creado con ID {nuevoCliente.ID}.")
                for crit in criteria:
                    fieldFrame.setValue(crit, "")

        def onBorrar():
            for crit in criteria:
                fieldFrame.setValue(crit, "")

        tk.Button(btnFrame, text="Aceptar", command=onAceptar).pack(side="left", padx=5)
        tk.Button(btnFrame, text="Borrar", command=onBorrar).pack(side="left", padx=5)
        # Se agrega botón para ver clientes...
        tk.Button(self.contentFrame, text="Ver Clientes", command=self.verClientes).pack(pady=10)
        # Y se agrega un botón para editar clientes
        tk.Button(self.contentFrame, text="Editar Clientes", command=self.editarClientes).pack(pady=10)

    def verClientes(self):
        if not self.clientes:
            messagebox.showinfo("Clientes", "No hay clientes registrados.")
        else:
            info = "Lista de Clientes:\n"
            for c in self.clientes:
                info += f"- {c.getNombreCompleto()} (ID: {c.ID})\n"
            messagebox.showinfo("Clientes", info)

    def editarClientes(self):
        # Ventana para editar o eliminar clientes
        editWin = tk.Toplevel(self)
        editWin.title("Editar Clientes")
        editWin.geometry("400x400")

        lbl = tk.Label(editWin, text="Seleccione un cliente para editar:", font=("Arial", 12))
        lbl.pack(pady=5)

        listbox = tk.Listbox(editWin)
        listbox.pack(fill="both", expand=True, padx=10, pady=5)
        for client in self.clientes:
            listbox.insert(tk.END, f"{client.ID} - {client.getNombreCompleto()}")

        # Frame para el formulario de edición
        formFrame = tk.Frame(editWin)
        formFrame.pack(fill="x", padx=10, pady=10)
        criteria = ["Nombre", "Apellido", "Edad"]
        fieldFrameEdit = FieldFrame(formFrame, "Criterio", criteria, "Valor")
        fieldFrameEdit.pack(fill="both", expand=True)

        def loadSelectedClient(event):
            selection = listbox.curselection()
            if selection:
                index = selection[0]
                client = self.clientes[index]
                fieldFrameEdit.setValue("Nombre", client.nombre)
                fieldFrameEdit.setValue("Apellido", client.apellido)
                fieldFrameEdit.setValue("Edad", str(client.edad))
            else:
                for crit in criteria:
                    fieldFrameEdit.setValue(crit, "")

        listbox.bind("<<ListboxSelect>>", loadSelectedClient)

        btnFrameEdit = tk.Frame(editWin)
        btnFrameEdit.pack(pady=10)

        def guardarCambios():
            selection = listbox.curselection()
            if selection:
                index = selection[0]
                client = self.clientes[index]
                client.nombre = fieldFrameEdit.getValue("Nombre")
                client.apellido = fieldFrameEdit.getValue("Apellido")
                try:
                    client.edad = int(fieldFrameEdit.getValue("Edad"))
                except ValueError:
                    client.edad = 0
                messagebox.showinfo("Exito", f"Cliente '{client.getNombreCompleto()}' actualizado.")
                # Actualizar la lista
                listbox.delete(index)
                listbox.insert(index, f"{client.ID} - {client.getNombreCompleto()}")
            else:
                messagebox.showwarning("Seleccion", "Seleccione un cliente para editar.")

        def eliminarCliente():
            selection = listbox.curselection()
            if selection:
                index = selection[0]
                client = self.clientes[index]
                if messagebox.askyesno("Confirmar", f"¿Está seguro de eliminar a {client.getNombreCompleto()}?"):
                    del self.clientes[index]
                    listbox.delete(index)
                    messagebox.showinfo("Eliminado", "Cliente eliminado.")
            else:
                messagebox.showwarning("Seleccion", "Seleccione un cliente para eliminar.")

        tk.Button(btnFrameEdit, text="Guardar Cambios", command=guardarCambios).pack(side="left", padx=5)
        tk.Button(btnFrameEdit, text="Eliminar Cliente", command=eliminarCliente).pack(side="left", padx=5)

    def mostrarInstalaciones(self):
        for widget in self.contentFrame.winfo_children():
            widget.destroy()
        title = tk.Label(self.contentFrame, text="Gestion de Instalaciones", font=("Arial", 18), bg="white")
        title.pack(pady=10)
        tk.Button(self.contentFrame, text="Ver Instalaciones", command=self.verInstalaciones).pack(pady=10)

    def verInstalaciones(self):
        if not self.instalaciones:
            messagebox.showinfo("Instalaciones", "No hay instalaciones registradas.")
        else:
            info = "Lista de Instalaciones:\n"
            for inst in self.instalaciones:
                info += f"- {inst.getNombre()} (ID: {inst.getId()})\n"
            messagebox.showinfo("Instalaciones", info)

    def mostrarReservas(self):
        for widget in self.contentFrame.winfo_children():
            widget.destroy()
        title = tk.Label(self.contentFrame, text="Gestion de Reservas", font=("Arial", 18), bg="white")
        title.pack(pady=10)
        tk.Button(self.contentFrame, text="Crear Reserva", command=self.crearReserva).pack(pady=10)
        tk.Button(self.contentFrame, text="Ver Reservas", command=self.verReservas).pack(pady=10)

    def crearReserva(self):
        pass

    def verReservas(self):
        pass

    def mostrarTorneos(self):
        for widget in self.contentFrame.winfo_children():
            widget.destroy()
        title = tk.Label(self.contentFrame, text="Gestion de Torneos", font=("Arial", 18), bg="white")
        title.pack(pady=10)
        tk.Button(self.contentFrame, text="Crear Torneo", command=self.crearTorneo).pack(pady=10)
        tk.Button(self.contentFrame, text="Ver Fixture", command=self.verFixture).pack(pady=10)
        tk.Button(self.contentFrame, text="Ver Equipos", command=self.verEquiposTorneo).pack(pady=10)

    def crearTorneo(self):
        pass

    def verFixture(self):
        pass

    def verEquiposTorneo(self):
        pass

    def mostrarEventos(self):
        for widget in self.contentFrame.winfo_children():
            widget.destroy()
        title = tk.Label(self.contentFrame, text="Gestion de Eventos", font=("Arial", 18), bg="white")
        title.pack(pady=10)
        tk.Button(self.contentFrame, text="Crear Evento", command=self.crearEvento).pack(pady=10)
        tk.Button(self.contentFrame, text="Ver Eventos", command=self.verEventos).pack(pady=10)

    def crearEvento(self):
        pass

    def verEventos(self):
        pass

    def mostrarPagos(self):
        for widget in self.contentFrame.winfo_children():
            widget.destroy()
        title = tk.Label(self.contentFrame, text="Gestion de Pagos", font=("Arial", 18), bg="white")
        title.pack(pady=10)
        tk.Button(self.contentFrame, text="Pagar Suscripcion", command=self.pagarSuscripcion).pack(pady=5)
        tk.Button(self.contentFrame, text="Cancelar Suscripcion", command=self.cancelarSuscripcion).pack(pady=5)
        tk.Button(self.contentFrame, text="Pagar Reserva", command=self.pagarReserva).pack(pady=5)
        tk.Button(self.contentFrame, text="Pagar Evento", command=self.pagarEvento).pack(pady=5)
        tk.Button(self.contentFrame, text="Comprar Boleta (Evento/Torneo)", command=self.comprarBoleta).pack(pady=5)
        tk.Button(self.contentFrame, text="Pagar Torneo", command=self.pagarTorneo).pack(pady=5)

    def pagarSuscripcion(self):
        pass

    def cancelarSuscripcion(self):
        pass

    def pagarReserva(self):
        pass

    def pagarEvento(self):
        messagebox.showinfo("Pago", "Funcionalidad de pago de eventos no implementada en este ejemplo.")

    def comprarBoleta(self):
        pass

    def pagarTorneo(self):
        pass

    def mostrarFormativo(self):
        for widget in self.contentFrame.winfo_children():
            widget.destroy()
        title = tk.Label(self.contentFrame, text="Area Formativa", font=("Arial", 18), bg="white")
        title.pack(pady=10)
        tk.Button(self.contentFrame, text="Inscribir Joven", command=self.inscribirJoven).pack(pady=10)
        tk.Button(self.contentFrame, text="Ver Inscripciones", command=self.verFormativos).pack(pady=10)

    def inscribirJoven(self):
        pass

    def verFormativos(self):
        pass

    def salir(self):
        self.destroy()
        from src.UDManager.uiMain.inicio import InicioWindow
        inicioWindow = InicioWindow()
        inicioWindow.mainloop()

    def enterSystem(self):
        self.destroy()
        from src.UDManager.uiMain.app import Application
        app = Application()
        app.mainloop()

if __name__ == "__main__":
    app = Application()
    app.mainloop()
