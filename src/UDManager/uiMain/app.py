import pickle
import random
import tkinter
import tkinter as tk
from datetime import datetime, timedelta
from tkinter import messagebox
from src.UDManager.baseDatos.serializador import Serializador
from src.UDManager.gestorAplicacion.eventos.evento import Evento
from src.UDManager.gestorAplicacion.inscripcion.joven import Joven
from src.UDManager.gestorAplicacion.inscripcion.tiendaEscuela import TiendaEscuela
from src.UDManager.gestorAplicacion.inscripcion.articuloTiendaEscuela import ArticuloTiendaEscuela
from src.UDManager.gestorAplicacion.pagos.suscripcion import Suscripcion
from src.UDManager.gestorAplicacion.reservas.fechaReserva import FechaReserva
from src.UDManager.gestorAplicacion.reservas.instalacion import Instalacion
from src.UDManager.gestorAplicacion.reservas.reserva import Reserva
from src.UDManager.gestorAplicacion.pagos.cliente import Cliente
from src.UDManager.gestorAplicacion.torneo.equipo import Equipo
from src.UDManager.gestorAplicacion.torneo.torneo import Torneo
from src.UDManager.gestorAplicacion.entidades.trabajador import Trabajador

# Importa la clase FieldFrame desde su archivo
from src.UDManager.uiMain.fieldFrame import FieldFrame

TiendaEscuelaFormativo = TiendaEscuela()


class Application(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Complejo Deportivo")
        self.geometry("1100x750")
        self.resizable(False, False)
        self.clienteSelect = None
        self.calendario = None
        self.horaInicioEntry = None
        self.horaFinEntry = None
        self.instalacionSelect = None
        self.menuWin = None

        # Creación de la tienda para Deporte Formativo.
        self.crearTienda()

        # Cargar base de datos (usando pickle en BaseDatos)
        from src.UDManager.baseDatos.deserializador import Deserializador
        Deserializador.deserializar()

        # Lista Por defecto, en caso tal de que se encuentre vacia dps de deserializar
        if not Instalacion.listaInstalaciones:
            Instalacion.crearInstalaciones()

        # Listas globales
        self.clientes = Cliente.getListaClientes()
        self.instalaciones = Instalacion.listaInstalaciones
        self.torneos = Torneo.getTorneos()
        self.eventos = Evento.getEventos()
        self.arbitros = []
        self.medicos = []
        self.paramedicos = []
        self.foodtrucks = []
        self.formativos = []
        self.suscripciones = []
        self.participantesFields = []

        arbitros_disponibles = [
            Trabajador("Carlos", "Martínez", "Arbitro", 35),
            Trabajador("Ana", "González", "Arbitro", 40),
            Trabajador("Luis", "Fernández", "Arbitro", 32),
            Trabajador("Marta", "Pérez", "Arbitro", 45),
            Trabajador("Juan", "López", "Arbitro", 38),
            Trabajador("Claudia", "Rodríguez", "Arbitro", 30),
        ]

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
    #...
    def mostrarInstalaciones(self):
        for widget in self.contentFrame.winfo_children():
            widget.destroy()
        title = tk.Label(self.contentFrame, text="Gestión de Instalaciones", font=("Arial", 18), bg="white")
        title.pack(pady=10)

        formFrame = tk.Frame(self.contentFrame, bg="white")
        formFrame.pack(pady=10, fill="x")

        # FieldFrame para crear una nueva instalación
        criteria = ["Nombre", "Deporte", "Precio Hora"]
        fieldFrameInst = FieldFrame(formFrame, "Campo", criteria, "Valor")
        fieldFrameInst.pack(fill="both", expand=True, padx=10, pady=10)

        btnFrame = tk.Frame(formFrame, bg="white")
        btnFrame.pack(side="bottom", pady=10)

        def agregarInstalacion():
            missing = [crit for crit in criteria if not fieldFrameInst.getValue(crit).strip()]
            if missing:
                messagebox.showwarning("Campos Incompletos", "Faltan: " + ", ".join(missing))
            else:
                nombre = fieldFrameInst.getValue("Nombre")
                deporte = fieldFrameInst.getValue("Deporte")
                try:
                    precioHora = float(fieldFrameInst.getValue("Precio Hora"))
                except ValueError:
                    messagebox.showerror("Error", "El precio debe ser un valor numérico.")
                    return
                nuevaInst = Instalacion(nombre, deporte, precioHora)
                messagebox.showinfo("Éxito", f"Instalación '{nombre}' creada con ID {nuevaInst.id}.")
                for crit in criteria:
                    fieldFrameInst.setValue(crit, "")

        tk.Button(btnFrame, text="Agregar Instalación", command=agregarInstalacion).pack(side="left", padx=5)
        tk.Button(btnFrame, text="Ver Instalaciones", command=self.verInstalaciones).pack(side="left", padx=5)
        tk.Button(btnFrame, text="Editar Instalaciones", command=self.editarInstalaciones).pack(side="left", padx=5)

    def verInstalaciones(self):
        if not self.instalaciones:
            messagebox.showinfo("Instalaciones", "No hay instalaciones registradas.")
        else:
            info = "Lista de Instalaciones:\n"
            for inst in self.instalaciones:
                info += f"- {inst.nombre} (ID: {inst.id})\n"
            messagebox.showinfo("Instalaciones", info)

    def editarInstalaciones(self):
        editWin = tk.Toplevel(self)
        editWin.title("Editar Instalaciones")
        editWin.geometry("400x400")

        lbl = tk.Label(editWin, text="Seleccione una instalación para editar:", font=("Arial", 12))
        lbl.pack(pady=5)

        listbox = tk.Listbox(editWin)
        listbox.pack(fill="both", expand=True, padx=10, pady=5)
        for inst in self.instalaciones:
            listbox.insert(tk.END, f"{inst.id} - {inst.nombre}")

        formFrame = tk.Frame(editWin)
        formFrame.pack(fill="x", padx=10, pady=10)
        criteria = ["Nombre", "Deporte", "Precio Hora"]
        fieldFrameEdit = FieldFrame(formFrame, "Campo", criteria, "Valor")
        fieldFrameEdit.pack(fill="both", expand=True)

        def cargarInstalacion(event):
            selection = listbox.curselection()
            if selection:
                index = selection[0]
                inst = self.instalaciones[index]
                fieldFrameEdit.setValue("Nombre", inst.nombre)
                fieldFrameEdit.setValue("Deporte", inst.deporte)
                fieldFrameEdit.setValue("Precio Hora", str(inst.precioHora))

        listbox.bind("<<ListboxSelect>>", cargarInstalacion)

        btnFrameEdit = tk.Frame(editWin)
        btnFrameEdit.pack(pady=10)

        def guardarCambios():
            selection = listbox.curselection()
            if selection:
                index = selection[0]
                inst = self.instalaciones[index]
                inst.nombre = fieldFrameEdit.getValue("Nombre")
                inst.deporte = fieldFrameEdit.getValue("Deporte")
                try:
                    inst.precioHora = float(fieldFrameEdit.getValue("Precio Hora"))
                except ValueError:
                    messagebox.showerror("Error", "El precio debe ser un valor numérico.")
                    return
                messagebox.showinfo("Éxito", f"Instalación '{inst.nombre}' actualizada.")
                listbox.delete(index)
                listbox.insert(index, f"{inst.id} - {inst.nombre}")
            else:
                messagebox.showwarning("Selección", "Seleccione una instalación para editar.")

        def eliminarInstalacion():
            selection = listbox.curselection()
            if selection:
                index = selection[0]
                inst = self.instalaciones[index]
                if messagebox.askyesno("Confirmar", f"¿Está seguro de eliminar la instalación '{inst.nombre}'?"):
                    del self.instalaciones[index]
                    listbox.delete(index)
                    messagebox.showinfo("Eliminado", "Instalación eliminada.")
            else:
                messagebox.showwarning("Selección", "Seleccione una instalación para eliminar.")

        tk.Button(btnFrameEdit, text="Guardar Cambios", command=guardarCambios).pack(side="left", padx=5)
        tk.Button(btnFrameEdit, text="Eliminar Instalación", command=eliminarInstalacion).pack(side="left", padx=5)
    #...........

    def verReservas(self):
        if not Reserva.listaReservas:
            messagebox.showinfo("Reservas", "No hay reservas registradas.")
        else:
            info = "Lista de Reservas:\n"
            for reserva in Reserva.listaReservas:
                info += f"- {reserva}\n"
            messagebox.showinfo("Reservas", info)

    def editarReservas(self):
        editWin = tk.Toplevel(self)
        editWin.title("Editar Reservas")
        editWin.geometry("400x400")

        lbl = tk.Label(editWin, text="Seleccione una reserva para editar:", font=("Arial", 12))
        lbl.pack(pady=5)

        listbox = tk.Listbox(editWin)
        listbox.pack(fill="both", expand=True, padx=10, pady=5)
        for reserva in Reserva.listaReservas:
            listbox.insert(tk.END,
                           f"{reserva.ID} - {reserva.cliente.getNombreCompleto()} en {reserva.instalacion.nombre}")

        formFrame = tk.Frame(editWin)
        formFrame.pack(fill="x", padx=10, pady=10)
        criteria = ["ID Cliente", "ID Instalación", "Fecha Reserva", "Monto a Pagar"]
        fieldFrameEdit = FieldFrame(formFrame, "Campo", criteria, "Valor")
        fieldFrameEdit.pack(fill="both", expand=True)

        def cargarReserva(event):
            selection = listbox.curselection()
            if selection:
                index = selection[0]
                reserva = Reserva.listaReservas[index]
                fieldFrameEdit.setValue("ID Cliente", str(reserva.cliente.ID))
                fieldFrameEdit.setValue("ID Instalación", str(reserva.instalacion.id))
                fieldFrameEdit.setValue("Fecha Reserva", reserva.fechaReserva)
                fieldFrameEdit.setValue("Monto a Pagar", str(reserva.aPagar))

        listbox.bind("<<ListboxSelect>>", cargarReserva)

        btnFrameEdit = tk.Frame(editWin)
        btnFrameEdit.pack(pady=10)

        def guardarCambios():
            selection = listbox.curselection()
            if selection:
                index = selection[0]
                reserva = Reserva.listaReservas[index]
                try:
                    idCliente = int(fieldFrameEdit.getValue("ID Cliente"))
                    idInstalacion = int(fieldFrameEdit.getValue("ID Instalación"))
                    monto = float(fieldFrameEdit.getValue("Monto a Pagar"))
                except ValueError:
                    messagebox.showerror("Error", "Verifica que los campos numéricos sean correctos.")
                    return
                cliente = Cliente.obtenerCliente(idCliente)
                instalacion = Instalacion.obtenerInstalacion(idInstalacion)
                if cliente is None or instalacion is None:
                    messagebox.showerror("Error", "Cliente o Instalación no válidos.")
                    return
                reserva.cliente = cliente
                reserva.instalacion = instalacion
                reserva.fechaReserva = fieldFrameEdit.getValue("Fecha Reserva")
                reserva.aPagar = monto
                messagebox.showinfo("Éxito", f"Reserva {reserva.ID} actualizada.")
                listbox.delete(index)
                listbox.insert(index, f"{reserva.ID} - {cliente.getNombreCompleto()} en {instalacion.nombre}")
            else:
                messagebox.showwarning("Selección", "Seleccione una reserva para editar.")

        def eliminarReserva():
            selection = listbox.curselection()
            if selection:
                index = selection[0]
                reserva = Reserva.listaReservas[index]
                if messagebox.askyesno("Confirmar", f"¿Está seguro de eliminar la reserva {reserva.ID}?"):
                    del Reserva.listaReservas[index]
                    listbox.delete(index)
                    messagebox.showinfo("Eliminado", "Reserva eliminada.")
            else:
                messagebox.showwarning("Selección", "Seleccione una reserva para eliminar.")

        tk.Button(btnFrameEdit, text="Guardar Cambios", command=guardarCambios).pack(side="left", padx=5)
        tk.Button(btnFrameEdit, text="Eliminar Reserva", command=eliminarReserva).pack(side="left", padx=5)
    ####
    def mostrarReservas(self):
        # Limpia la zona de contenido
        for widget in self.contentFrame.winfo_children():
            widget.destroy()

        # Título para la sección
        title = tk.Label(self.contentFrame, text="Gestión de Reservas", font=("Arial", 18), bg="white")
        title.pack(pady=10)

        # Frame para el formulario de nueva reserva
        formFrame = tk.Frame(self.contentFrame, bg="white")
        formFrame.pack(pady=10, fill="x")

        # Mostrar la última reserva si existe
        if Reserva.listaReservas:
            ultimaReserva = Reserva.listaReservas[-1]  # Obtener la última reserva

            # Datos de la última reserva
            criteria = ["Cliente", "Instalación", "Fecha Reserva", "Hora Inicio", "Hora Fin", "Monto a Pagar"]
            values = [
                ultimaReserva.cliente,
                ultimaReserva.instalacion.nombre,
                ultimaReserva.fechaReserva.getInicioReserva().strftime("%Y-%m-%d"),  # Usar getInicioReserva()
                ultimaReserva.fechaReserva.getInicioReserva().strftime("%H:%M"),  # Hora de inicio
                ultimaReserva.fechaReserva.getFinReserva().strftime("%H:%M"),  # Hora de fin
                f"${ultimaReserva.aPagar:.2f}"  # Monto a pagar formateado (cambio aquí)
            ]

            # Crear un FieldFrame con los datos de la última reserva y marcar todos los campos como solo lectura
            fieldFrameReserva = FieldFrame(formFrame, "Campo", criteria, "Valor", values, ReadOnly=criteria)
            fieldFrameReserva.pack(fill="both", expand=True, padx=10, pady=10)

        # Botones para las reservas
        btnFrame = tk.Frame(formFrame, bg="white")
        btnFrame.pack(side="bottom", pady=10)

        tk.Button(btnFrame, text="Crear Reserva", command=self.mostrarMenuCreacionReserva).pack(side="left", padx=5)
        tk.Button(btnFrame, text="Ver Reservas", command=self.verReservas).pack(side="left", padx=5)
        # Listbox para mostrar las reservas
        listbox = tk.Listbox(formFrame, selectmode=tk.SINGLE, height=10, width=80)
        listbox.pack(padx=10, pady=10)

        # Mostrar todas las reservas en el Listbox
        for reserva in Reserva.listaReservas:
            listbox.insert(tk.END,
                           f"ID: {reserva.ID} - Cliente: {reserva.cliente} - Instalación: {reserva.instalacion.nombre} - Fecha: {reserva.fechaReserva.getInicioReserva().strftime('%Y-%m-%d %H:%M')}")

        # Frame para los botones
        btnFrame = tk.Frame(formFrame, bg="white")
        btnFrame.pack(side="bottom", pady=10)
        tk.Button(btnFrame, text="Eliminar Reserva", command=lambda: self.eliminarReserva(listbox)).pack(side="left",
                                                                                                         padx=5)

    def eliminarReserva(self, listbox):
        try:
            # Obtener la selección del listbox
            seleccion = listbox.curselection()
            if seleccion:
                index = seleccion[0]  # Obtener el índice de la reserva seleccionada
                reservaSeleccionada = Reserva.listaReservas[index]  # Obtener la reserva

                # Confirmación para eliminar
                confirmacion = messagebox.askyesno("Confirmar",
                                                   f"¿Está seguro de eliminar la reserva con ID {reservaSeleccionada.ID}?")

                if confirmacion:
                    # Eliminar la reserva de la lista
                    Reserva.listaReservas.remove(reservaSeleccionada)
                    messagebox.showinfo("Eliminado", "Reserva eliminada exitosamente.")
                    self.mostrarReservas()  # Actualizar la vista de reservas
            else:
                messagebox.showwarning("Selección", "Seleccione una reserva para eliminar.")
        except Exception as e:
            messagebox.showerror("Error", f"Hubo un error al eliminar la reserva: {str(e)}")

    def mostrarTorneos(self):
        for widget in self.contentFrame.winfo_children():
            widget.destroy()

        title = tk.Label(self.contentFrame, text="Gestion de Torneos", font=("Arial", 18), bg="white")
        title.pack(pady=10)

        # Mostrar los detalles del último torneo creado si existe
        if self.torneos:
            ultimo_torneo = self.torneos[-1]  # Obtener el último torneo
            criteria = ["Nombre del Torneo", "Equipos", "Deporte"]
            values = [
                ultimo_torneo.nombre,
                ", ".join([equipo.nombreEquipo for equipo in ultimo_torneo.equiposParticipantes]),
                ultimo_torneo.deporte
            ]
            fieldFrame = FieldFrame(self.contentFrame, "Campo", criteria, "Valor", values, ReadOnly=criteria)
            fieldFrame.pack(fill="x", padx=10, pady=5)  # Adjusted pady and fill

        # Frame for horizontal buttons
        btnFrame = tk.Frame(self.contentFrame, bg="white")
        btnFrame.pack(pady=10)

        # Create buttons in a horizontal row
        tk.Button(btnFrame, text="Crear Torneo", command=self.crearTorneo).pack(side="left", padx=5)
        tk.Button(btnFrame, text="Ver Torneos", command=self.verTorneos).pack(side="left", padx=5)
        tk.Button(btnFrame, text="Ver Equipos", command=self.verEquipos).pack(side="left", padx=5)
        tk.Button(btnFrame, text="Editar Equipos", command=self.editarEquipos).pack(side="left", padx=5)
        tk.Button(btnFrame, text="Valoración Médica", command=self.valoracionMedica).pack(side="left", padx=5)

        # Botón para Vender Boletas
        tk.Button(btnFrame, text="Vender Boletas", command=self.venderBoletas).pack(side="left",
                                                                                    padx=5)  # Aquí agregamos el botón

    def valoracionMedica(self):
        if not self.torneos:
            messagebox.showwarning("No hay torneos", "No hay torneos creados.")
            return

        ultimo_torneo = self.torneos[-1]  # Get the last tournament
        if not ultimo_torneo.equiposParticipantes:
            messagebox.showwarning("Sin Equipos", "No hay equipos en el torneo.")
            return

        # Randomly select a team from the tournament
        equipo_random = random.choice(ultimo_torneo.equiposParticipantes)

        # Determine the number of participants based on the sport
        if ultimo_torneo.deporte.lower() == "natacion":
            num_participantes = 2  # 2 participants per team for "Natación"
        else:
            num_participantes = 14  # 14 participants for other sports

        # Randomly select a participant number
        participante_random = random.randint(1, num_participantes)

        # Show the message
        messagebox.showinfo("Valoración Médica",
                            f"El jugador {participante_random} del equipo {equipo_random.nombreEquipo} ha fallado la valoración médica. Debe ser reemplazado.")


    def venderBoletas(self):
        # Create a new window to sell tickets
        boletasWin = tk.Toplevel(self)
        boletasWin.title("Vender Boletas")
        boletasWin.geometry("600x400")

        # Title
        title = tk.Label(boletasWin, text="Seleccionar Torneo", font=("Arial", 18), bg="white")
        title.pack(pady=10)

        # Dropdown to select a tournament
        torneos_nombres = [torneo.nombre for torneo in self.torneos]
        torneo_select = tk.StringVar(boletasWin)
        torneo_select.set(torneos_nombres[0])  # Set the first tournament as default

        torneo_menu = tk.OptionMenu(boletasWin, torneo_select, *torneos_nombres)
        torneo_menu.pack(pady=10)

        # Frame to select ticket quantity
        ticket_frame = tk.Frame(boletasWin)
        ticket_frame.pack(pady=10)

        # Function to display the number of tickets that can be sold based on the installation
        def mostrarCantidadBoletas():
            selected_tournament_name = torneo_select.get()
            selected_tournament = next(t for t in self.torneos if t.nombre == selected_tournament_name)

            # Generate ticket ID if not already generated
            selected_tournament.generar_ticket_id()  # Ensure ticket ID is generated once

            # Show the current ticket ID if it has been generated
            ticket_info = f"ID de Boletas: {selected_tournament.ticket_id}" if selected_tournament.ticket_id else "ID de boletas no generado"

            # Check the installation and set ticket limits
            if selected_tournament.instalacion in ["Cancha F11 1", "Cancha F11 2", "Coliseo"]:
                max_tickets = 20000
            else:
                max_tickets = 2000

            # Create a label and entry for the number of tickets
            label = tk.Label(ticket_frame, text=f"Cantidad de boletas (máximo {max_tickets}):", font=("Arial", 12))
            label.pack(pady=5)

            ticket_qty = tk.IntVar()
            ticket_entry = tk.Entry(ticket_frame, textvariable=ticket_qty)
            ticket_entry.pack(pady=5)

            def generarBoletas():
                try:
                    qty = ticket_qty.get()
                    if qty < 1 or qty > max_tickets:
                        messagebox.showerror("Error", f"Cantidad inválida. Debe ser entre 1 y {max_tickets}.")
                        return

                    # Generate a unique ticket ID
                    ticket_id = selected_tournament.ticket_id  # Use the already generated ticket ID

                    # Display success message with the ticket ID
                    messagebox.showinfo("Éxito", f"Boletas vendidas exitosamente. ID de boleta: {ticket_id}")
                    boletasWin.destroy()  # Close the window after selling tickets

                except ValueError:
                    messagebox.showerror("Error", "Por favor ingrese un número válido.")

            # Button to confirm and generate tickets
            confirm_button = tk.Button(boletasWin, text="Vender Boletas", command=generarBoletas)
            confirm_button.pack(pady=10)

        # Show the ticket options when a tournament is selected
        mostrarCantidadBoletas()

    def verTorneos(self):
        torneosWin = tk.Toplevel(self)
        torneosWin.title("Ver Torneos")
        torneosWin.geometry("600x400")

        title = tk.Label(torneosWin, text="Lista de Torneos", font=("Arial", 18), bg="white")
        title.pack(pady=10)

        canvas = tk.Canvas(torneosWin)
        scrollbar = tk.Scrollbar(torneosWin, orient="vertical", command=canvas.yview)
        canvas.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side="right", fill="y")
        canvas.pack(side="left", fill="both", expand=True)

        frame = tk.Frame(canvas)
        canvas.create_window((0, 0), window=frame, anchor="nw")

        if self.torneos:
            for torneo in self.torneos:
                # Asegurarnos de que ticket_id esté generado antes de acceder a él
                if torneo.ticket_id:
                    ticket_info = f"ID de Boletas: {torneo.ticket_id}"
                else:
                    ticket_info = "ID de boletas no generado"

                # Mostrar el ID de pago, si está disponible
                pago_info = f"ID de Pago: {torneo.pago_id}" if hasattr(torneo,
                                                                       'pago_id') and torneo.pago_id else "ID de pago no generado"

                tournament_text = f"Nombre: {torneo.nombre}\n" \
                                  f"Deporte: {torneo.deporte}\n" \
                                  f"Instalación: {torneo.instalacion}\n" \
                                  f"{ticket_info}\n{pago_info}"
                tournament_label = tk.Label(frame, text=tournament_text, font=("Arial", 12), anchor="w", justify="left")
                tournament_label.pack(pady=10, padx=10)
        else:
            no_tournament_label = tk.Label(frame, text="No hay torneos registrados.", font=("Arial", 12), anchor="w")
            no_tournament_label.pack(pady=10, padx=10)

        frame.update_idletasks()
        canvas.config(scrollregion=canvas.bbox("all"))

    def verEquipos(self):
        # Create a new window to display the list of teams
        equiposWin = tk.Toplevel(self)
        equiposWin.title("Ver Equipos")
        equiposWin.geometry("600x400")

        # Create a title for the new window
        title = tk.Label(equiposWin, text="Selecciona un Torneo", font=("Arial", 18), bg="white")
        title.pack(pady=10)

        # Dropdown to select a tournament
        torneos_nombres = [torneo.nombre for torneo in self.torneos]
        torneo_select = tk.StringVar(equiposWin)
        torneo_select.set(torneos_nombres[0])  # Set the first tournament as default

        torneo_menu = tk.OptionMenu(equiposWin, torneo_select, *torneos_nombres)
        torneo_menu.pack(pady=10)

        # Frame to display the teams of the selected tournament
        teams_frame = tk.Frame(equiposWin)
        teams_frame.pack(pady=10)

        # Function to display teams when a tournament is selected
        def mostrarEquipos():
            # Clear the previous teams displayed
            for widget in teams_frame.winfo_children():
                widget.destroy()

            selected_tournament_name = torneo_select.get()
            selected_tournament = next(t for t in self.torneos if t.nombre == selected_tournament_name)

            # Display the teams of the selected tournament
            for i, equipo in enumerate(selected_tournament.equiposParticipantes, 1):
                equipo_label = tk.Label(teams_frame, text=f"Equipo {i}: {equipo.nombreEquipo}", font=("Arial", 12))
                equipo_label.pack(pady=5)

        # Button to show teams for the selected tournament
        show_teams_button = tk.Button(equiposWin, text="Mostrar Equipos", command=mostrarEquipos)
        show_teams_button.pack(pady=10)

    def crearReserva(self):
        # Obtener la fecha desde el campo de texto
        fechaSeleccionada = self.fechaEntrada.get().strip()  # Obtener la fecha desde el campo de entrada

        # Validar el formato de la fecha (MM/DD/YY)
        try:
            fechaReserva = datetime.strptime(fechaSeleccionada, "%m/%d/%y")  # Convertimos la fecha
        except ValueError:
            messagebox.showerror("Error", "Formato de fecha incorrecto. Use MM/DD/YY.")
            return

        self.horaInicio = self.horaInicioEntry.get().strip()  # Eliminar espacios antes y después
        self.horaFin = self.horaFinEntry.get().strip()  # Eliminar espacios antes y después
        self.instalacionSeleccionada = next(
            inst for inst in self.instalaciones if inst.nombre == self.instalacionSelect.get())

        # Validar el formato de las horas (HH:MM)
        if len(self.horaInicio) != 5 or len(self.horaFin) != 5:
            messagebox.showerror("Error", "El formato de la hora debe ser HH:MM.")
            return

        if self.horaInicio[2] != ':' or self.horaFin[2] != ':':
            messagebox.showerror("Error", "El formato de la hora debe ser HH:MM.")
            return

        # Verificar que las horas y minutos sean numéricos
        horaInicioPartes = self.horaInicio.split(':')
        horaFinPartes = self.horaFin.split(':')

        if not (horaInicioPartes[0].isdigit() and horaInicioPartes[1].isdigit() and
                horaFinPartes[0].isdigit() and horaFinPartes[1].isdigit()):
            messagebox.showerror("Error", "La hora y los minutos deben ser números.")
            return

        try:
            fechaReserva = datetime.strptime(f"{fechaSeleccionada} {self.horaInicio}", "%m/%d/%y %H:%M")
            self.horaFin = datetime.strptime(f"{fechaSeleccionada} {self.horaFin}", "%m/%d/%y %H:%M")

            # Validar horas
            if fechaReserva >= self.horaFin:
                messagebox.showerror("Error", "La hora de inicio debe ser antes que la hora de fin.")
                return

            # Comprobar si la reserva es duplicada
            if self.esReservaDuplicada(self.instalacionSeleccionada, fechaReserva, self.horaFin):
                messagebox.showerror("Error", "Ya existe una reserva en este horario para esta instalación.")
                return

            # Crear la instancia de FechaReserva
            fechaReservaObj = FechaReserva(fechaReserva, self.horaFin)

            # Calcular el monto a pagar
            duracion = (self.horaFin - fechaReserva).seconds / 3600  # Duración en horas
            precioReserva = self.instalacionSeleccionada.precioHora * duracion

            # Crear la reserva y asignar un ID de pago único
            nuevaReserva = Reserva(self.clienteSeleccionado, self.instalacionSeleccionada, fechaReservaObj,
                                   precioReserva)
            messagebox.showinfo("Reserva creada",
                                f"Reserva con ID {nuevaReserva.ID} y ID de pago {nuevaReserva.ID_pago} creada exitosamente.")

            # Serializar la reserva después de crearla
            Serializador.serializar()

            self.menuWin.destroy()  # Cerrar la ventana de reserva
            self.mostrarReservas()  # Actualizar la vista de reservas

        except ValueError as e:
            print(f"Error: {e}")  # Muestra el error para depuración
            messagebox.showerror("Error", "Formato de hora incorrecto.")

    def esReservaDuplicada(self, instalacion, fechaInicio, fechaFin):
        """Verifica si ya existe una reserva para la misma instalación en el mismo rango horario"""
        for reserva in Reserva.listaReservas:
            if reserva.instalacion == instalacion:
                if (
                        fechaInicio >= reserva.fechaReserva.getInicioReserva() and fechaInicio < reserva.fechaReserva.getFinReserva()) or \
                        (
                                fechaFin > reserva.fechaReserva.getInicioReserva() and fechaFin <= reserva.fechaReserva.getFinReserva()):
                    return True
        return False

    def mostrarMenuCreacionReserva(self):
        self.menuWin = tk.Toplevel(self)
        self.menuWin.title("Crear Reserva")
        self.menuWin.geometry("700x700")

        labelCliente = tk.Label(self.menuWin, text="Selecciona un Cliente", font=("Arial", 12))
        labelCliente.pack(pady=5)
        clientes = [f"{cliente.ID} - {cliente.getNombreCompleto()}" for cliente in self.clientes]
        self.clienteSelect = tk.StringVar(self.menuWin)
        self.clienteSelect.set(clientes[0])
        clienteDropdown = tk.OptionMenu(self.menuWin, self.clienteSelect, *clientes)
        clienteDropdown.pack(pady=5)

        # Al seleccionar un cliente, lo asignamos a clienteSeleccionado
        self.clienteSeleccionado = self.clienteSelect.get()
        self.clienteSelect.trace_add("write", self.seleccionarCliente)

        labelFecha = tk.Label(self.menuWin, text="Selecciona una fecha (MM/DD/YY)", font=("Arial", 12))
        labelFecha.pack(pady=5)
        self.fechaEntrada = tk.Entry(self.menuWin)
        self.fechaEntrada.insert(0, "MM/DD/YY")  # Texto por defecto
        self.fechaEntrada.pack(pady=5)

        labelHoraInicio = tk.Label(self.menuWin, text="Hora de Inicio (HH:MM)", font=("Arial", 12))
        labelHoraInicio.pack(pady=5)
        self.horaInicioEntry = tk.Entry(self.menuWin)
        self.horaInicioEntry.pack(pady=5)

        labelHoraFin = tk.Label(self.menuWin, text="Hora de Fin (HH:MM)", font=("Arial", 12))
        labelHoraFin.pack(pady=5)
        self.horaFinEntry = tk.Entry(self.menuWin)
        self.horaFinEntry.pack(pady=5)

        labelInstalacion = tk.Label(self.menuWin, text="Selecciona una Instalación", font=("Arial", 12))
        labelInstalacion.pack(pady=5)
        instalaciones = [f"{inst.nombre}" for inst in self.instalaciones]
        self.instalacionSelect = tk.StringVar(self.menuWin)
        self.instalacionSelect.set(instalaciones[0])
        instalacionDropdown = tk.OptionMenu(self.menuWin, self.instalacionSelect, *instalaciones)
        instalacionDropdown.pack(pady=5)

        confirmarReservaBtn = tk.Button(self.menuWin, text="Aceptar", command=self.crearReserva)
        confirmarReservaBtn.pack(pady=20)

    def seleccionarCliente(self, *args):
        clienteSeleccionadoStr = self.clienteSelect.get()
        clienteID = clienteSeleccionadoStr.split(" - ")[0]
        self.clienteSeleccionado = next(cliente for cliente in self.clientes if str(cliente.ID) == clienteID)
        print(f"Cliente seleccionado: {self.clienteSeleccionado.getNombreCompleto()}")

    def crearReserva(self):
        fechaSeleccionada = self.fechaEntrada.get().strip()  # Obtener la fecha desde el campo de entrada

        # Validar el formato de la fecha (MM/DD/YY)
        try:
            fechaReserva = datetime.strptime(fechaSeleccionada, "%m/%d/%y")  # Convertimos la fecha
        except ValueError:
            messagebox.showerror("Error", "Formato de fecha incorrecto. Use MM/DD/YY.")
            return

        self.horaInicio = self.horaInicioEntry.get().strip()  # Eliminar espacios antes y después
        self.horaFin = self.horaFinEntry.get().strip()  # Eliminar espacios antes y después
        self.instalacionSeleccionada = next(
            inst for inst in self.instalaciones if inst.nombre == self.instalacionSelect.get())

        # Validar el formato de las horas (HH:MM)
        if len(self.horaInicio) != 5 or len(self.horaFin) != 5:
            messagebox.showerror("Error", "El formato de la hora debe ser HH:MM.")
            return

        if self.horaInicio[2] != ':' or self.horaFin[2] != ':':
            messagebox.showerror("Error", "El formato de la hora debe ser HH:MM.")
            return

        # Verificar que las horas y minutos sean numéricos
        horaInicioPartes = self.horaInicio.split(':')
        horaFinPartes = self.horaFin.split(':')

        if not (horaInicioPartes[0].isdigit() and horaInicioPartes[1].isdigit() and
                horaFinPartes[0].isdigit() and horaFinPartes[1].isdigit()):
            messagebox.showerror("Error", "La hora y los minutos deben ser números.")
            return

        try:
            fechaReserva = datetime.strptime(f"{fechaSeleccionada} {self.horaInicio}", "%m/%d/%y %H:%M")
            self.horaFin = datetime.strptime(f"{fechaSeleccionada} {self.horaFin}", "%m/%d/%y %H:%M")

            # Validar horas
            if fechaReserva >= self.horaFin:
                messagebox.showerror("Error", "La hora de inicio debe ser antes que la hora de fin.")
                return

            # Comprobar si la reserva es duplicada
            if self.esReservaDuplicada(self.instalacionSeleccionada, fechaReserva, self.horaFin):
                messagebox.showerror("Error", "Ya existe una reserva en este horario para esta instalación.")
                return

            # Crear la instancia de FechaReserva
            fechaReservaObj = FechaReserva(fechaReserva, self.horaFin)

            # Calcular el monto a pagar
            duracion = (self.horaFin - fechaReserva).seconds / 3600  # Duración en horas
            precioReserva = self.instalacionSeleccionada.precioHora * duracion

            # Crear la reserva y asignar un ID de pago único
            nuevaReserva = Reserva(self.clienteSeleccionado, self.instalacionSeleccionada, fechaReservaObj,
                                   precioReserva)
            messagebox.showinfo("Reserva creada",
                                f"Reserva con ID {nuevaReserva.ID} y ID de pago {nuevaReserva.ID_pago} creada exitosamente.")

            # Serializar la reserva después de crearla
            Serializador.serializar()

            self.menuWin.destroy()  # Cerrar la ventana de reserva
            self.mostrarReservas()  # Actualizar la vista de reservas

        except ValueError as e:
            print(f"Error: {e}")  # Muestra el error para depuración
            messagebox.showerror("Error", "Formato de hora incorrecto.")


    def crearTorneo(self):
        # Crear una nueva ventana para la creación del torneo
        torneoWin = tk.Toplevel(self)
        torneoWin.title("Crear Torneo")
        torneoWin.geometry("900x900")

        # Selección de cliente (desplegable)
        labelCliente = tk.Label(torneoWin, text="Selecciona un Cliente", font=("Arial", 12))
        labelCliente.pack(pady=5)
        clientes = [f"{cliente.ID} - {cliente.getNombreCompleto()}" for cliente in self.clientes]
        clienteSelect = tk.StringVar(torneoWin)
        clienteSelect.set(clientes[0])  # Establecer por defecto el primer cliente
        clienteDropdown = tk.OptionMenu(torneoWin, clienteSelect, *clientes)
        clienteDropdown.pack(pady=5)

        # Ingreso de nombre del torneo
        labelNombre = tk.Label(torneoWin, text="Nombre del Torneo", font=("Arial", 12))
        labelNombre.pack(pady=5)
        nombreTorneoEntry = tk.Entry(torneoWin)
        nombreTorneoEntry.pack(pady=5)

        # Selección de deporte
        labelDeporte = tk.Label(torneoWin, text="Selecciona un Deporte", font=("Arial", 12))
        labelDeporte.pack(pady=5)
        deportes = ["Futbol", "Baloncesto", "Natacion", "Voleibol"]
        deporteSelect = tk.StringVar(torneoWin)
        deporteSelect.set(deportes[0])  # Establecer por defecto el primer deporte
        deporteDropdown = tk.OptionMenu(torneoWin, deporteSelect, *deportes)
        deporteDropdown.pack(pady=5)

        # Función para filtrar las instalaciones según el deporte seleccionado
        def filtrarInstalaciones(instalacion, deporte):
            """Filtra las instalaciones según el deporte."""
            return instalacion.deporte.lower() == deporte.lower()

        # Actualizar instalaciones dependiendo del deporte seleccionado
        def actualizarInstalaciones(*args):
            """Actualiza las instalaciones en el desplegable según el deporte seleccionado"""
            deporteSeleccionado = deporteSelect.get()
            instalacionesFiltradas = [inst.nombre for inst in self.instalaciones if
                                      filtrarInstalaciones(inst, deporteSeleccionado)]
            instalacionSelect.set(instalacionesFiltradas[
                                      0] if instalacionesFiltradas else "")  # Establecer por defecto la primera instalación
            instalacionDropdown['menu'].delete(0, 'end')  # Limpiar el menú
            for instalacion in instalacionesFiltradas:
                instalacionDropdown['menu'].add_command(label=instalacion,
                                                        command=tk._setit(instalacionSelect, instalacion))

        # Llamar a la actualización de instalaciones cuando el deporte cambia
        deporteSelect.trace('w', actualizarInstalaciones)

        # Selección de instalación (basado en el deporte)
        labelInstalacion = tk.Label(torneoWin, text="Selecciona una Instalación", font=("Arial", 12))
        labelInstalacion.pack(pady=5)
        # Inicializar instalacionSelect
        instalacionSelect = tk.StringVar(torneoWin)
        instalacionDropdown = tk.OptionMenu(torneoWin, instalacionSelect, "")  # Vacío inicialmente
        instalacionDropdown.pack(pady=5)

        # Ingreso de los 5 equipos
        labelEquipos = tk.Label(torneoWin, text="Nombre de los 5 Equipos", font=("Arial", 12))
        labelEquipos.pack(pady=5)
        equipos = []
        for i in range(5):  # Limitamos a 5 equipos
            labelEquipo = tk.Label(torneoWin, text=f"Equipo {i + 1}", font=("Arial", 12))
            labelEquipo.pack(pady=5)
            equipoEntry = tk.Entry(torneoWin)
            equipoEntry.pack(pady=5)
            equipos.append(equipoEntry)

        # Fechas de inicio y fin con campos de texto
        labelFechaInicio = tk.Label(torneoWin, text="Fecha de Inicio (MM/DD/YY)", font=("Arial", 12))
        labelFechaInicio.pack(pady=5)
        fechaInicioEntry = tk.Entry(torneoWin)
        fechaInicioEntry.insert(0, "MM/DD/YY")  # Texto por defecto
        fechaInicioEntry.pack(pady=5)

        labelFechaFin = tk.Label(torneoWin, text="Fecha de Fin (MM/DD/YY)", font=("Arial", 12))
        labelFechaFin.pack(pady=5)
        fechaFinEntry = tk.Entry(torneoWin)
        fechaFinEntry.insert(0, "MM/DD/YY")  # Texto por defecto
        fechaFinEntry.pack(pady=5)

        # Botón Aceptar
        aceptarBtn = tk.Button(torneoWin, text="Aceptar",
                               command=lambda: self.onAceptar(clienteSelect, nombreTorneoEntry, deporteSelect,
                                                              instalacionSelect, fechaInicioEntry, fechaFinEntry,
                                                              equipos, torneoWin))
        aceptarBtn.pack(pady=20)

    def onAceptar(self, clienteSelect, nombreTorneoEntry, deporteSelect, instalacionSelect, fechaInicioEntry,
                  fechaFinEntry, equipos, torneoWin):
        clienteSeleccionado = next(cliente for cliente in self.clientes if
                                   f"{cliente.ID} - {cliente.getNombreCompleto()}" == clienteSelect.get())
        nombreTorneo = nombreTorneoEntry.get()
        deporte = deporteSelect.get()

        # Validar que se haya seleccionado una instalación
        try:
            instalacion = next(inst for inst in self.instalaciones if inst.nombre == instalacionSelect.get())
        except StopIteration:
            messagebox.showerror("Error", "La instalación seleccionada no es válida.")
            return

        # Validar fechas
        try:
            fechaInicio = datetime.strptime(fechaInicioEntry.get(), "%m/%d/%y")
            fechaFin = datetime.strptime(fechaFinEntry.get(), "%m/%d/%y")
            if (fechaFin - fechaInicio).days < 3:
                raise ValueError("La duración del torneo debe ser de al menos 3 días.")
        except ValueError as e:
            messagebox.showerror("Error", f"Fecha inválida: {e}")
            return

        # Comprobar si el torneo ya existe en la lista
        if any(torneo.nombre == nombreTorneo for torneo in self.torneos):
            messagebox.showerror("Error", "Ya existe un torneo con ese nombre.")
            return

        # Crear el torneo
        equiposParticipantes = [Equipo(equipo.get()) for equipo in equipos if equipo.get().strip()]
        torneo = Torneo(deporte, equiposParticipantes, fechaInicio, fechaFin, )
        torneo.instalacion = instalacion
        torneo.nombre = nombreTorneo  # Establecer el nombre del torneo

        # Imprimir los torneos para depuración
        print("Lista de torneos después de agregar el nuevo torneo:")
        for t in self.torneos:
            print(t.nombre)

        torneo.generar_pago_id()

        # Mostrar mensaje de éxito
        messagebox.showinfo("Torneo Creado",
                            f"Torneo '{nombreTorneo}' creado exitosamente con {len(equiposParticipantes)} equipos. ID de pago: {torneo.pago_id}")
        torneoWin.destroy()  # Cerramos la ventana de creación de torneo

    def editarEquipos(self):
        # Crear la ventana emergente para editar equipos
        editarWin = tk.Toplevel(self)
        editarWin.title("Editar Equipos")
        editarWin.geometry("800x800")

        # Selección de torneo (desplegable)
        labelTorneo = tk.Label(editarWin, text="Selecciona un Torneo", font=("Arial", 12))
        labelTorneo.pack(pady=5)

        torneos = [torneo.nombre for torneo in self.torneos]
        self.torneoSelect = tk.StringVar(editarWin)
        self.torneoSelect.set(torneos[0])  # Valor inicial
        torneoDropdown = tk.OptionMenu(editarWin, self.torneoSelect, *torneos)
        torneoDropdown.pack(pady=5)

        # Selección de equipo (desplegable)
        labelEquipo = tk.Label(editarWin, text="Selecciona un Equipo", font=("Arial", 12))
        labelEquipo.pack(pady=5)

        equipoSelect = tk.StringVar(editarWin)
        equipoDropdown = tk.OptionMenu(editarWin, equipoSelect, "")
        equipoDropdown.pack(pady=5)

        # Actualizar equipos según el torneo seleccionado
        def actualizarEquipos(*args):
            torneoSeleccionado = self.torneoSelect.get()
            torneo = next(t for t in self.torneos if t.nombre == torneoSeleccionado)
            equiposFiltrados = [equipo.nombreEquipo for equipo in torneo.equiposParticipantes]

            equipoSelect.set(equiposFiltrados[0] if equiposFiltrados else "")
            equipoDropdown['menu'].delete(0, 'end')
            for equipo in equiposFiltrados:
                equipoDropdown['menu'].add_command(label=equipo, command=tk._setit(equipoSelect, equipo))

        self.torneoSelect.trace_add('write', actualizarEquipos)

        # Función para mostrar los participantes
        def mostrarParticipantes(*args):
            # Limpiar los participantes previos (si los hay)
            if hasattr(self, 'participantesFrame') and self.participantesFrame is not None:
                for widget in self.participantesFrame.winfo_children():
                    widget.destroy()

            # Crear un Frame principal para centrar el contenido
            mainFrame = tk.Frame(editarWin)
            mainFrame.place(relx=0.5, rely=0.5, anchor='center')  # Centrar el Frame en la ventana

            # Crear un Canvas y agregar una barra de desplazamiento dentro del mainFrame
            self.canvas = tk.Canvas(mainFrame)
            self.scrollbar = tk.Scrollbar(mainFrame, orient="vertical", command=self.canvas.yview)
            self.canvas.configure(yscrollcommand=self.scrollbar.set)

            # Crear un Frame dentro del Canvas para los participantes
            self.participantesFrame = tk.Frame(self.canvas)

            # Colocar el Frame dentro del Canvas
            self.canvas.create_window((0, 0), window=self.participantesFrame, anchor="nw")
            self.canvas.pack(side="left", fill="both", expand=True)
            self.scrollbar.pack(side="right", fill="y")

            # Limpiar los participantes previos (si los hay)
            for widget in self.participantesFrame.winfo_children():
                widget.destroy()

            torneoSeleccionado = self.torneoSelect.get()
            torneo = next(t for t in self.torneos if t.nombre == torneoSeleccionado)
            equipoSeleccionado = equipoSelect.get()

            equipo = next(
                (equipo for equipo in torneo.equiposParticipantes if equipo.nombreEquipo == equipoSeleccionado), None)

            if equipo is None:
                messagebox.showerror("Error", "El equipo seleccionado no existe.")
                return

            if not hasattr(equipo, 'participantes'):
                equipo.participantes = []

            # Determinar cuántos participantes se necesitan
            num_participantes = 2 if torneo.deporte == "Natacion" else 12
            label = tk.Label(self.participantesFrame, text=f"Ingrese los {num_participantes} participantes del equipo",
                             font=("Arial", 12))
            label.pack(pady=10)

            self.participantesFields = []
            for i in range(num_participantes):
                label = tk.Label(self.participantesFrame, text=f"Participante {i + 1}", font=("Arial", 12))
                label.pack(pady=5)
                entry = tk.Entry(self.participantesFrame)
                entry.pack(pady=5)
                if i < len(equipo.participantes):
                    entry.insert(0, equipo.participantes[i])  # Mostrar participantes si están asignados
                self.participantesFields.append(entry)  # Agregar a la lista

            # Asegurarse de que la ventana se actualice correctamente
            self.participantesFrame.update_idletasks()

            # Configurar el Canvas para ajustarse a los nuevos elementos
            self.participantesFrame.update_idletasks()
            self.canvas.config(scrollregion=self.canvas.bbox("all"))

            # Centrar los participantes horizontalmente dentro del Canvas
            for widget in self.participantesFrame.winfo_children():
                widget.pack_configure(anchor='center')  # Centrar cada widget dentro del Frame

        # Botón para mostrar el FieldFrame de participantes
        mostrarBtn = tk.Button(editarWin, text="Mostrar Participantes", command=mostrarParticipantes)
        mostrarBtn.pack(pady=10)

        # Agregar botón para guardar los participantes
        def guardarParticipantes():
            torneoSeleccionado = self.torneoSelect.get()
            torneo = next(t for t in self.torneos if t.nombre == torneoSeleccionado)
            equipoSeleccionado = equipoSelect.get()

            equipo = next(equipo for equipo in torneo.equiposParticipantes if equipo.nombreEquipo == equipoSeleccionado)

            # Guardar los participantes en el equipo
            participantes = []
            for field in self.participantesFields:
                participantes.append(field.get().strip())

            if not all(participante for participante in participantes):
                messagebox.showwarning("Campos Incompletos", "Todos los participantes deben ser ingresados.")
                return

            equipo.participantes = participantes

            # Serializar los cambios
            from src.UDManager.baseDatos.serializador import Serializador
            Serializador.serializar()

            messagebox.showinfo("Éxito", "Participantes guardados y cambios serializados exitosamente.")

        # Botón para guardar los datos de los participantes
        guardarBtn = tk.Button(editarWin, text="Guardar Participantes", command=guardarParticipantes)
        guardarBtn.pack(pady=10)

    def guardarCambiosTorneo(self, torneoSelect, equipoSelect):
        # Obtener el torneo seleccionado
        torneoSeleccionado = torneoSelect.get()

        # Buscar el torneo en la lista de torneos
        torneo = next(t for t in self.torneos if t.nombre == torneoSeleccionado)

        # Obtener el equipo seleccionado
        equipoSeleccionado = equipoSelect.get()

        equipo = next(equipo for equipo in torneo.equiposParticipantes if equipo.nombreEquipo == equipoSeleccionado)

        # Asegúrate de obtener y almacenar los participantes si es necesario
        participantes = []
        for field in self.participantesFields:
            participantes.append(field.get().strip())

        if not all(participante for participante in participantes):
            messagebox.showwarning("Campos Incompletos", "Todos los participantes deben ser ingresados.")
            return

        # Guardar los participantes en el equipo
        equipo.participantes = participantes

        # Serializar los cambios
        from src.UDManager.baseDatos.serializador import Serializador
        Serializador.serializar()

        messagebox.showinfo("Éxito", "Participantes guardados y cambios serializados exitosamente.")

    def cargarEquipos(self):
        # Aseguramos que al cargar el equipo, el atributo 'participantes' esté presente
        for equipo in self.torneos:
            if not hasattr(equipo, 'participantes'):
                equipo.participantes = []  # Inicializamos participantes si no existe

    def cargarTorneos(self):
        try:
            with open("database.txt", "rb") as f:
                data = pickle.load(f)
                self.torneos = data.get("torneos", [])
        except FileNotFoundError:
            self.torneos = []  # Si no hay archivo, inicializamos una lista vacía


    #////////////////////EVENTOS/////////////////////////////////////////

    def mostrarEventos(self):
        for widget in self.contentFrame.winfo_children():
            widget.destroy()

        tk.Label(self.contentFrame,
                 text="Gestion de Eventos",
                 font=("Arial", 25, "bold"),
                 bg="white").pack(pady=10)

        formEvento = tk.Frame(self.contentFrame, width=400, height=600,borderwidth=3, relief="groove")
        formEvento.pack(anchor="w", pady=30, padx=50)
        formEvento.pack_propagate(False)

        clientesEncontrados = [f"{cliente.ID} - {cliente.getNombreCompleto()}" for cliente in self.clientes]
        self.clienteSelect = tk.StringVar(formEvento)
        self.clienteSelect.set(clientesEncontrados[0])

        self.clienteSeleccionado = self.clienteSelect.get()
        self.clienteSelect.trace_add("write", self.seleccionarCliente)

        self.tipoEvento = tk.StringVar(self.contentFrame)
        self.tipoEvento.set("Concierto")

        tk.Label(formEvento,
                 text="Creación de Evento",
                 font=("Arial", 20, "italic")).pack(pady=(10, 20))

        tk.Label(formEvento,
                 text="Eliga un Cliente",
                 font=("Arial", 12)).pack(pady=5, padx=40, anchor="w")

        tk.OptionMenu(formEvento,
                      self.clienteSelect,
                      *clientesEncontrados).pack(pady=5, padx=40, anchor="w")

        tk.Label(formEvento,
                 text="Nombre del evento",
                 font=("Arial", 12)).pack(pady=5, padx=40, anchor="w")

        self.eventoEntry = tk.Entry(formEvento,width=20)
        self.eventoEntry.pack(pady=5, padx=40, anchor="w")

        tk.Label(formEvento,
                 text="Tipo de Evento",
                 font=("Arial", 12)).pack(pady=5, padx=40, anchor="w")

        self.opcionTipoEvento = tk.OptionMenu(formEvento,
                                         self.tipoEvento,
                                         "Concierto",
                                         "Festival")

        self.opcionTipoEvento.pack(pady=5, padx=40, anchor="w")

        tk.Label(formEvento, text="Cantante", font=("Arial", 12)).pack(pady=5, padx=40, anchor="w")

        self.cantanteEntry = tk.Entry(formEvento, width=20)
        self.cantanteEntry.pack(pady=5, padx=40, anchor="w")

        tk.Button(formEvento,
                  text="Ir a Reserva",
                  width=20,
                  command=self.mostrarEventoReserva).pack(pady=(70,40), padx=60, anchor="se")

        tk.Button(formEvento,
                  text="Ver Eventos",
                  width=20,
                  command=self.mostrarListaEventos).pack(pady=5, padx=60, anchor="se")

        def toggle_entry(*args):
            if self.tipoEvento.get() == "Concierto":
                self.cantanteEntry.config(state="normal")
            else:
                self.cantanteEntry.config(state="disabled")

        self.tipoEvento.trace_add("write", toggle_entry)
        toggle_entry()

        self.eventoImagen = tkinter.PhotoImage(file="images/eventoImagen.png")
        tk.Label(self.contentFrame,image=self.eventoImagen).place(x=500,y=120)

    def mostrarListaEventos(self):
        winListaEventos = tk.Toplevel(self.contentFrame)
        winListaEventos.title("Lista Eventos")
        winListaEventos.geometry("400x400")
        winListaEventos.resizable(False, False)

        tk.Label(winListaEventos, text="Lista Eventos", font=("Arial", 15, "italic")).pack(pady=5, padx=40)

        listboxEventos = tk.Listbox(winListaEventos, width=50, height=10)
        listboxEventos.pack(pady=5)

        # Llenar el Listbox con los eventos
        listboxEventos.delete(0, tk.END)
        for evento in self.eventos:
            listboxEventos.insert(tk.END, evento)

        def eliminarEvento():
            seleccion = listboxEventos.curselection()
            if not seleccion:
                messagebox.showwarning("Atención", "Seleccione un evento para eliminar.")
                return

            indice = seleccion[0]
            evento_seleccionado = self.eventos[indice]

            confirmacion = messagebox.askyesno("Confirmación",
                                               f"¿Seguro que desea eliminar el evento {evento_seleccionado.nombre}?")

            if confirmacion:
                del Evento.eventos[indice]
                listboxEventos.delete(indice)
                messagebox.showinfo("Eliminado", "El evento ha sido eliminado con éxito.")
                Serializador.serializar()

        btnEliminar = tk.Button(winListaEventos, text="Eliminar Evento", command=eliminarEvento)
        btnEliminar.pack(pady=5)


    def mostrarEventoReserva(self):
        if (self.cantanteEntry.get().strip() == "" and self.tipoEvento.get() == "Concierto") or self.eventoEntry.get().strip() == "":
            tk.messagebox.showwarning("Error","Complete todos los campos")
        else:
            self.eventoPantalla = tk.Toplevel(self.contentFrame)
            self.eventoPantalla.title("Reserva de Evento")
            self.eventoPantalla.geometry("400x600")
            self.eventoPantalla.resizable(False, False)

            labelFechaEvento = tk.Label(self.eventoPantalla, text="Selecciona una fecha (MM/DD/YY)", font=("Arial", 12))
            labelFechaEvento.pack(pady=5)
            self.fechaEventoEntrada = tk.Entry(self.eventoPantalla)
            self.fechaEventoEntrada.insert(0, "MM/DD/YY")  # Texto por defecto
            self.fechaEventoEntrada.pack(pady=5)

            labelInicioEvento = tk.Label(self.eventoPantalla, text="Hora de Inicio (HH:MM)", font=("Arial", 12))
            labelInicioEvento.pack(pady=5)
            self.eventoInicioEntry = tk.Entry(self.eventoPantalla)
            self.eventoInicioEntry.pack(pady=5)

            labelFinEvento = tk.Label(self.eventoPantalla, text="Hora de Fin (HH:MM)", font=("Arial", 12))
            labelFinEvento.pack(pady=5)
            self.eventoFinEntry = tk.Entry(self.eventoPantalla)
            self.eventoFinEntry.pack(pady=5)

            labelInstalacionEvento = tk.Label(self.eventoPantalla, text="Selecciona una Instalación", font=("Arial", 12))
            labelInstalacionEvento.pack(pady=5)
            instalaciones = [f"{inst.nombre}" for inst in self.instalaciones]
            self.instalacionEvento = tk.StringVar(self.eventoPantalla)
            self.instalacionEvento.set(instalaciones[0])
            instalacionDropdown = tk.OptionMenu(self.eventoPantalla, self.instalacionEvento, *instalaciones)
            instalacionDropdown.pack(pady=5)

            tk.Button(self.eventoPantalla,
                      text="Completar Reserva",
                      width=20,
                      height=2,
                      relief="groove",
                      command=self.validarReservaEvento).pack(pady=70, padx=60, anchor="se")

    def validarReservaEvento(self):
        fechaSeleccionada = self.fechaEventoEntrada.get().strip()

        try:
            fechaReserva = datetime.strptime(fechaSeleccionada, "%m/%d/%y")
        except ValueError:
            messagebox.showerror("Error", "Formato de fecha incorrecto. Use MM/DD/YY.")
            return

        self.horaInicio = self.eventoInicioEntry.get().strip()
        self.horaFin = self.eventoFinEntry.get().strip()
        self.instalacionSeleccionada = next(
            inst for inst in self.instalaciones if inst.nombre == self.instalacionEvento.get())

        if len(self.horaInicio) != 5 or len(self.horaFin) != 5:
            messagebox.showerror("Error", "El formato de la hora debe ser HH:MM.")
            return

        if self.horaInicio[2] != ':' or self.horaFin[2] != ':':
            messagebox.showerror("Error", "El formato de la hora debe ser HH:MM.")
            return

        horaInicioPartes = self.horaInicio.split(':')
        horaFinPartes = self.horaFin.split(':')

        if not (horaInicioPartes[0].isdigit() and horaInicioPartes[1].isdigit() and
                horaFinPartes[0].isdigit() and horaFinPartes[1].isdigit()):
            messagebox.showerror("Error", "La hora y los minutos deben ser números.")
            return

        try:
            fechaReserva = datetime.strptime(f"{fechaSeleccionada} {self.horaInicio}", "%m/%d/%y %H:%M")
            self.horaFin = datetime.strptime(f"{fechaSeleccionada} {self.horaFin}", "%m/%d/%y %H:%M")

            if fechaReserva >= self.horaFin:
                messagebox.showerror("Error", "La hora de inicio debe ser antes que la hora de fin.")
                return

            if self.esReservaDuplicada(self.instalacionSeleccionada, fechaReserva, self.horaFin):
                messagebox.showerror("Error", "Ya existe una reserva en este horario para esta instalación.")
                return

            fechaReservaObj = FechaReserva(fechaReserva, self.horaFin)

            duracion = (self.horaFin - fechaReserva).seconds / 3600  # Duración en horas
            precioReserva = self.instalacionSeleccionada.precioHora * duracion

            nuevaReserva = Reserva(self.clienteSeleccionado, self.instalacionSeleccionada, fechaReservaObj,
                                   precioReserva)

            nuevoEvento = Evento(self.eventoEntry.get(),self.tipoEvento.get(),self.cantanteEntry.get(),nuevaReserva)

            messagebox.showinfo("Evento Creado",
                                f"Reserva con ID {nuevaReserva.ID} y ID de pago {nuevaReserva.ID_pago} creada exitosamente.")

            Serializador.serializar()

            self.eventoPantalla.destroy()
            self.mostrarEventos()

        except ValueError as e:
            print(f"Error: {e}")
            messagebox.showerror("Error", "Formato de hora incorrecto.")


    #///////////////////////////////PAGOS/////////////////////////////////////////////////

    def mostrarPagos(self):
        for widget in self.contentFrame.winfo_children():
            widget.destroy()

        title = tk.Label(self.contentFrame, text="Gestión de Pagos", font=("Arial", 25, "bold"), bg="white")
        title.pack(pady=10)

        botones1 = tk.Frame(self.contentFrame, bg="white", width=300, height=300, padx=40, pady=40)
        botones1.pack(padx=150, pady=(20, 5), anchor="ne")

        botones2 = tk.Frame(self.contentFrame, bg="white", width=300, height=300, padx=40, pady=40)
        botones2.pack(padx=150, pady=(5, 5), anchor="sw")

        self.img_pagos1 = tk.PhotoImage(file="images/img_pagos1.png", width=276, height=276)
        self.img_pagos2 = tk.PhotoImage(file="images/img_pagos2.png", width=276, height=276)

        tk.Button(botones1,
                  text="Pagar Suscripción",
                  width=25,
                  height=2,
                  relief="groove",
                  command=self.pagarSuscripcion,
                  overrelief="solid").pack(pady=15)
        tk.Button(botones1,
                  text="Cancelar Suscripción",
                  width=25,
                  height=2,
                  relief="groove",
                  command=self.menuCancelarSuscripcion,
                  overrelief="solid").pack(pady=15,
                                           padx=(10, 50),
                                           anchor="w")
        tk.Button(botones1,
                  text="Pagar Reserva",
                  width=25,
                  height=2,
                  relief="groove",
                  command=self.menuPagarReserva,
                  overrelief="solid").pack(pady=15)

        self.labelImg1 = tk.Label(self.contentFrame,image=self.img_pagos1, bg="white")
        self.labelImg1.place(x=200, y=110)

        tk.Button(botones2,
                  text="Pagar Formativo",
                  width=25,
                  height=2,
                  relief="groove",
                  overrelief="solid").pack(pady=15)

        tk.Button(botones2,
                  text="Comprar Boleta",
                  width=25,
                  height=2,
                  relief="groove",
                  command=self.menuComprarBoleta,
                  overrelief="solid").pack(pady=15,
                                           padx=(50, 10),
                                           anchor="e")
        tk.Button(botones2,
                  text="Pagar Torneo",
                  width=25,
                  height=2,
                  relief="groove",
                  overrelief="solid").pack(pady=15)

        self.labelImg2 = tk.Label(self.contentFrame, image=self.img_pagos2, bg="white")
        self.labelImg2.place(x=620, y=390)

#PAGAR SUSCRIPCION
    def pagarSuscripcion(self):
        self.winPagarSuscripcion = tk.Toplevel(self.contentFrame)
        self.winPagarSuscripcion.title("Pagar Suscripcion")
        self.winPagarSuscripcion.resizable(False, False)
        self.winPagarSuscripcion.geometry("500x400")

        tk.Label(self.winPagarSuscripcion,
                 text="Eliga un Cliente",
                 font=("Arial", 20, "bold")).pack(pady=15)

        self.listbox = tk.Listbox(self.winPagarSuscripcion,width=50)
        self.listbox.pack(padx=10,pady=15)

        for cliente in self.clientes:
            self.listbox.insert(tk.END, cliente)

        self.btnPagar = tk.Button(self.winPagarSuscripcion, text="Pagar Suscripción",
                                  command=self.abrirOpcionesSuscripcion)
        self.btnPagar.pack()

    def abrirOpcionesSuscripcion(self):
        seleccion = self.listbox.curselection()
        if not seleccion:
            messagebox.showwarning("Advertencia", "Seleccione un cliente primero.")
            return

        self.clienteSeleccionado = self.clientes[seleccion[0]]

        self.winOpciones = tk.Toplevel(self.winPagarSuscripcion)
        self.winOpciones.title("Seleccionar Suscripción")
        self.winOpciones.geometry("300x300")
        self.winOpciones.resizable(False, False)

        opciones = ["Rookie - $10,000", "ProPlayer - $20,000", "MVP - $30,000"]
        self.niveles = {"Rookie": 10000, "ProPlayer": 20000, "MVP": 30000}

        tk.Label(self.winOpciones, text="Seleccione una Suscripción",font=("Arial",12,"italic")).pack()
        self.listboxSuscripciones = tk.Listbox(self.winOpciones,width=30)
        self.listboxSuscripciones.pack(padx=10,pady=15)

        for opcion in opciones:
            self.listboxSuscripciones.insert(tk.END, opcion)

        self.btnConfirmar = tk.Button(self.winOpciones, text="Confirmar", command=self.confirmarPago)
        self.btnConfirmar.pack()

    def confirmarPago(self):
        seleccion = self.listboxSuscripciones.curselection()
        if not seleccion:
            messagebox.showwarning("Advertencia", "Seleccione una suscripción primero.")
            return

        opciones = list(self.niveles.keys())
        seleccionada = opciones[seleccion[0]]
        costo = self.niveles[seleccionada]

        respuesta = messagebox.askyesno("Confirmar Pago", f"¿Desea comprar la suscripción {seleccionada} por ${costo}?")

        if respuesta:
            self.clienteSeleccionado.suscripcion = Suscripcion(seleccionada, costo)
            messagebox.showinfo("Éxito", f"Suscripción {seleccionada} adquirida con éxito.")
            self.winOpciones.destroy()

        Serializador.serializar()

#CANCELAR SUSCRIPCION

    def menuCancelarSuscripcion(self):
        self.winCancelarSuscripcion = tk.Toplevel(self.contentFrame)
        self.winCancelarSuscripcion.title("Cancelar Suscripción")
        self.winCancelarSuscripcion.resizable(False, False)
        self.winCancelarSuscripcion.geometry("500x400")

        tk.Label(self.winCancelarSuscripcion, text="Seleccione un Cliente",font=("Arial",14,"italic")).pack()

        self.listbox = tk.Listbox(self.winCancelarSuscripcion,width=40)
        self.listbox.pack(padx=10,pady=15)

        for cliente in self.clientes:
            self.listbox.insert(tk.END, cliente)

        self.btnCancelar = tk.Button(self.winCancelarSuscripcion, text="Cancelar Suscripción",
                                     command=self.cancelarSuscripcion)
        self.btnCancelar.pack()

    def cancelarSuscripcion(self):
        seleccion = self.listbox.curselection()
        if not seleccion:
            messagebox.showwarning("Advertencia", "Seleccione un cliente primero.")
            return

        clienteSeleccionado = self.clientes[seleccion[0]]

        if clienteSeleccionado.suscripcion.nivel == "Ninguno":
            messagebox.showwarning("Advertencia", "Este cliente no tiene una suscripción activa para cancelar.")
            return

        respuesta = messagebox.askyesno("Confirmar Cancelación", "¿Está seguro de que desea cancelar la suscripción?")

        if respuesta:
            clienteSeleccionado.suscripcion = Suscripcion("Ninguno", 0)
            messagebox.showinfo("Éxito", "La suscripción ha sido cancelada.")

        Serializador.serializar()

#PAGAR RESERVA

    def menuPagarReserva(self):
        self.winPagarReserva = tk.Toplevel(self.contentFrame)
        self.winPagarReserva.title("Pagar Reserva")
        self.winPagarReserva.geometry("600x400")
        self.winPagarReserva.resizable(False, False)

        tk.Label(self.winPagarReserva, text="Pagar Reserva", font=("Arial", 20, "bold")).pack(pady=10)

        self.listbox = tk.Listbox(self.winPagarReserva,width=60)
        self.listbox.pack(fill="both", padx=10, pady=5)

        self.actualizarLista()

        btn_pagar = tk.Button(self.winPagarReserva, text="Pagar", command=self.pagarReserva)
        btn_pagar.pack(pady=10)

    def actualizarLista(self):
        self.listbox.delete(0, tk.END)
        for reserva in Reserva.listaReservas:
            if not reserva.pagada:  # Solo mostrar reservas no pagadas
                self.listbox.insert(tk.END,
                                    f"ID: {reserva.ID} - Cliente: {reserva.cliente} - Instalación: {reserva.instalacion.nombre} - Fecha: {reserva.fechaReserva.getInicioReserva().strftime('%Y-%m-%d %H:%M')}")

    def pagarReserva(self):
        seleccion = self.listbox.curselection()
        if seleccion:
            index = seleccion[0]
            reservas_no_pagadas = [reserva for reserva in Reserva.listaReservas if not reserva.pagada]
            reserva_seleccionada = reservas_no_pagadas[index]

            confirmacion = messagebox.askyesno("Confirmar Pago",
                                               f"Desea pagar la reserva con ID_pago: {reserva_seleccionada.ID_pago}\nMonto a Pagar: {reserva_seleccionada.aPagar}?")

            if confirmacion:
                reserva_seleccionada.pagada = True  # Marcar como pagada
                self.actualizar_lista()  # Actualizar la lista para ocultar la reserva pagada

    def pagarFormativo(self):

        pass

#COMPRAR BOLETA

    def menuComprarBoleta(self):
        self.winComprarBoleta = tk.Toplevel(self.contentFrame)
        self.winComprarBoleta.geometry("600x500")
        self.winComprarBoleta.resizable(False, False)
        self.winComprarBoleta.title("Comprar Boleta")

        tk.Label(self.winComprarBoleta, text="Seleccione un evento", font=("Arial", 14)).pack(pady=10)

        self.listbox = tk.Listbox(self.winComprarBoleta,width=80)
        self.listbox.pack()
        for evento in self.eventos:
            self.listbox.insert(tk.END, evento)

        tk.Button(self.winComprarBoleta, text="Comprar Boleta", command=self.comprarBoleta).pack(pady=(25,5))
        tk.Button(self.winComprarBoleta, text="Ver Boletas", command=self.verBoletas).pack(pady=5)

    def comprarBoleta(self):
        seleccion = self.listbox.curselection()
        if not seleccion:
            messagebox.showwarning("Advertencia", "Seleccione un evento primero")
            return
        evento = self.eventos[seleccion[0]]

        if messagebox.askyesno("Confirmar", f"¿Desea comprar una boleta para {evento.nombre}?"):
            boleta = evento.agregar_boleta()
            messagebox.showinfo("Boleta Comprada", str(boleta))

        Serializador.serializar()

    def verBoletas(self):
        seleccion = self.listbox.curselection()
        if not seleccion:
            messagebox.showwarning("Advertencia", "Seleccione un evento primero")
            return
        evento = self.eventos[seleccion[0]]

        win_boletas = tk.Toplevel(self.winComprarBoleta)
        win_boletas.title("Boletas Compradas")
        win_boletas.geometry("300x300")

        tk.Label(win_boletas, text=f"Boletas para {evento.nombre} ID: {evento.ID}", font=("Arial", 12)).pack(pady=10)
        listbox_boletas = tk.Listbox(win_boletas)
        listbox_boletas.pack()

        for boleta in evento.boletas:
            listbox_boletas.insert(tk.END, str(boleta))



    def pagarTorneo(self):
        pass

    ###FORMATIVO/////////////////////////////////////////////////////////////////////////////////////
    #///////////////////////////////////////////////////////////////////////////////////
    #//////////////////////////////////////////////////////////////////////////////////////////////////

    def crearTienda(self):
        """Crea la tienda y precarga 5 artículos por cada deporte."""
        self.tiendaEscuela = TiendaEscuela()
        # Artículos para Fútbol
        self.tiendaEscuela.agregarArticulo(ArticuloTiendaEscuela(1, "Balón de Fútbol", 10, 15000, "Fútbol"))
        self.tiendaEscuela.agregarArticulo(ArticuloTiendaEscuela(2, "Camiseta de Fútbol", 5, 18000, "Fútbol"))
        self.tiendaEscuela.agregarArticulo(ArticuloTiendaEscuela(3, "Botines de Fútbol", 8, 25000, "Fútbol"))
        self.tiendaEscuela.agregarArticulo(ArticuloTiendaEscuela(4, "Medias de Fútbol", 15, 12000, "Fútbol"))
        self.tiendaEscuela.agregarArticulo(ArticuloTiendaEscuela(5, "Guantes de Portero", 3, 30000, "Fútbol"))
        # Artículos para Baloncesto
        self.tiendaEscuela.agregarArticulo(ArticuloTiendaEscuela(6, "Balón de Baloncesto", 10, 16000, "Baloncesto"))
        self.tiendaEscuela.agregarArticulo(
            ArticuloTiendaEscuela(7, "Camiseta de Baloncesto", 5, 19000, "Baloncesto"))
        self.tiendaEscuela.agregarArticulo(
            ArticuloTiendaEscuela(8, "Zapatillas de Baloncesto", 8, 28000, "Baloncesto"))
        self.tiendaEscuela.agregarArticulo(
            ArticuloTiendaEscuela(9, "Pantalones Deportivos", 12, 13000, "Baloncesto"))
        self.tiendaEscuela.agregarArticulo(ArticuloTiendaEscuela(10, "Muñequeras", 20, 11000, "Baloncesto"))
        # Artículos para Natación
        self.tiendaEscuela.agregarArticulo(ArticuloTiendaEscuela(11, "Gorro de Natación", 15, 10000, "Natación"))
        self.tiendaEscuela.agregarArticulo(ArticuloTiendaEscuela(12, "Gafas de Natación", 10, 20000, "Natación"))
        self.tiendaEscuela.agregarArticulo(ArticuloTiendaEscuela(13, "Traje de Baño", 7, 25000, "Natación"))
        self.tiendaEscuela.agregarArticulo(ArticuloTiendaEscuela(14, "Flotador", 12, 12000, "Natación"))
        self.tiendaEscuela.agregarArticulo(ArticuloTiendaEscuela(15, "Toalla Deportiva", 20, 15000, "Natación"))
        # Artículos para Tenis
        self.tiendaEscuela.agregarArticulo(ArticuloTiendaEscuela(16, "Raqueta de Tenis", 6, 30000, "Tenis"))
        self.tiendaEscuela.agregarArticulo(
            ArticuloTiendaEscuela(17, "Pelotas de Tenis (Paquete)", 10, 17000, "Tenis"))
        self.tiendaEscuela.agregarArticulo(ArticuloTiendaEscuela(18, "Camiseta de Tenis", 8, 20000, "Tenis"))
        self.tiendaEscuela.agregarArticulo(ArticuloTiendaEscuela(19, "Pantalón Corto", 12, 14000, "Tenis"))
        self.tiendaEscuela.agregarArticulo(ArticuloTiendaEscuela(20, "Muñequeras de Tenis", 20, 11000, "Tenis"))

    def UltimoDiaDelMes(self, fecha):
        if fecha.month == 12:
            return 31
        proximoMes = fecha.replace(month=fecha.month + 1, day=1)
        return (proximoMes - timedelta(days=1)).day

    def mostrarFormativo(self):
        """Pantalla inicial de Deporte Formativo con dos opciones:
           1. Inscribir Joven.
           2. Seleccionar Joven para Tienda."""
        for widget in self.contentFrame.winfo_children():
            widget.destroy()

        title = tk.Label(self.contentFrame, text="Deporte Formativo", font=("Arial", 20), bg="white")
        title.pack(pady=20)

        # --- FRAME CON LA IMAGEN Y EL ÚLTIMO JOVEN INSCRITO (CENTRADO) ---
        infoFrame = tk.Frame(self.contentFrame, bg="white")
        infoFrame.pack(pady=10, fill="x")  # Lo colocamos arriba, antes de los botones

        # Cargar la imagen "image4.png"
        try:
            self.imagen = tk.PhotoImage(file="image4.png")
            # Creamos un label para la imagen y lo centramos con pack
            tk.Label(infoFrame, image=self.imagen, bg="white").pack(pady=5)
        except Exception as e:
            tk.Label(infoFrame, text="(No se pudo cargar la imagen)", bg="white").pack(pady=5)

        # Buscar el último joven inscrito (que tenga asignado un horario)
        last_inscrito = None
        for j in Joven.listaJovenes:
            if j.horario:
                last_inscrito = j

        if last_inscrito:
            info_text = f"Último Joven Inscrito: {last_inscrito.getNombreCompleto()} - Horario: {last_inscrito.horario}"
        else:
            info_text = "No hay jóvenes inscritos."

        tk.Label(infoFrame, text=info_text, font=("Arial", 12), bg="white").pack(pady=5)

        # --- FRAME DE BOTONES ---
        btnFrame = tk.Frame(self.contentFrame, bg="white")
        btnFrame.pack(pady=20)  # Esto quedará debajo de infoFrame

        tk.Button(btnFrame, text="Inscribir Joven", font=("Arial", 14),
                  command=self.inscribirJoven).pack(side="left", padx=20)
        tk.Button(btnFrame, text="Seleccionar Joven para Tienda", font=("Arial", 14),
                  command=self.seleccionarJovenParaTienda).pack(side="left", padx=20)

    def inscribirJoven(self):
        """Interfaz para inscribir un joven. Se recogen los datos mediante un FieldFrame,
           se selecciona el deporte y se asigna un horario, generando las fechas.
           Luego, se formaliza la inscripción (aún sin pago) mediante el método Formalizar."""
        for widget in self.contentFrame.winfo_children():
            widget.destroy()

        title = tk.Label(self.contentFrame, text="Área Formativa", font=("Arial", 18), bg="white")
        title.pack(pady=10)

        formFrame = tk.Frame(self.contentFrame, bg="white")
        formFrame.pack(pady=10, fill="x")

        criteria = ["nombre", "apellido", "edad", "experienciaJoven", "eps",
                    "nombreAcudiente", "telefonoAcudiente", "cedulaAcudiente"]
        self.horariosDisponibles = {
            "Lunes-Miércoles 8-10": [0, 2],
            "Lunes-Miércoles 10-12": [0, 2],
            "Martes-Jueves 8-10": [1, 3],
            "Martes-Jueves 10-12": [1, 3],
            "Viernes 14-16": [4]
        }
        fieldFrame = FieldFrame(formFrame, "Campo", criteria, "Valor")
        fieldFrame.pack(fill="both", expand=True, padx=10, pady=10)

        tk.Label(formFrame, text="Deporte:", font=("Arial", 12), bg="white").pack(pady=5)
        deportes = ["Fútbol", "Baloncesto", "Natación", "Tenis"]
        self.deporteVar = tk.StringVar()
        self.deporteVar.set(deportes[0])
        opMenuDeporte = tk.OptionMenu(formFrame, self.deporteVar, *deportes)
        opMenuDeporte.pack()

        btnFrame = tk.Frame(formFrame, bg="white")
        btnFrame.pack(side="bottom", pady=10)

        tk.Button(btnFrame, text="Crear Joven", command=lambda: self.crearJoven(fieldFrame)).pack(side="left",
                                                                                                  padx=5)
        tk.Button(btnFrame, text="Mostrar Jóvenes", command=self.mostrarInscripciones).pack(side="left", padx=5)
        tk.Button(btnFrame, text="Formalizar Inscripción", command=self.Formalizar).pack(side="left", padx=5)
        tk.Button(btnFrame, text="Borrar Joven", command=self.borrarJoven).pack(side="left", padx=5)
        tk.Button(btnFrame, text="Volver", command=self.mostrarFormativo).pack(side="left", padx=5)

    def borrarJoven(self):
        """Abre una ventana para borrar un joven seleccionado de la lista global."""
        borrarWin = tk.Toplevel(self.contentFrame)
        borrarWin.title("Borrar Jóvenes")

        tk.Label(borrarWin, text="Seleccione un Joven para borrar:", font=("Arial", 12)).pack(pady=5)

        listaBox = tk.Listbox(borrarWin, width=100, height=20)
        listaBox.pack(padx=10, pady=10, fill="both", expand=True)

        for j in Joven.listaJovenes:
            listaBox.insert(tk.END, f"{j.getNombreCompleto()} (ID: {j.id})")

        def borrarSeleccionado():
            selected = listaBox.curselection()
            if not selected:
                messagebox.showwarning("Borrar", "Seleccione un joven para borrar.")
                return
            index = selected[0]
            confirm = messagebox.askyesno("Confirmar", "¿Está seguro de borrar el joven seleccionado?")
            if confirm:
                del Joven.listaJovenes[index]
                listaBox.delete(index)
                messagebox.showinfo("Borrar", "Joven borrado correctamente.")

        tk.Button(borrarWin, text="Borrar", command=borrarSeleccionado).pack(pady=5)
        tk.Button(borrarWin, text="Cerrar", command=borrarWin.destroy).pack(pady=5)

    def Formalizar(self):
        """Formaliza la inscripción de un joven:
           - Se selecciona un joven sin inscripción formal (no pagada).
           - Se asigna un horario y se generan las fechas.
           - Se asigna la tarifa base (según experiencia) a baseInscripcion.
           - El valor total de inscripción es: baseInscripcion + totalCompras.
           inscripcionPagada permanece False (pendiente de pago)."""
        inscripcionWindow = tk.Toplevel(self.contentFrame)
        inscripcionWindow.title("Formalizar inscripción de Joven")

        tk.Label(inscripcionWindow, text="Seleccione un Joven", font=("Arial", 12)).pack(pady=5)

        jovenesNoFormales = [j for j in Joven.listaJovenes if not j.inscripcionPagada]
        if not jovenesNoFormales:
            messagebox.showinfo("Aviso", "No hay jóvenes disponibles para formalización.")
            inscripcionWindow.destroy()
            return

        self.jovenesLabels = [f"{j.getNombreCompleto()} (ID: {j.id})" for j in jovenesNoFormales]
        self.jovenesRefs = jovenesNoFormales

        jovenVar = tk.StringVar()
        jovenVar.set(self.jovenesLabels[0])
        tk.OptionMenu(inscripcionWindow, jovenVar, *self.jovenesLabels).pack()

        tk.Label(inscripcionWindow, text="Seleccione un Horario", font=("Arial", 12)).pack(pady=5)
        horarioVar = tk.StringVar()
        horarioVar.set(list(self.horariosDisponibles.keys())[0])
        tk.OptionMenu(inscripcionWindow, horarioVar, *self.horariosDisponibles.keys()).pack()

        def confirmar():
            etiquetaSeleccionada = jovenVar.get()
            indice = self.jovenesLabels.index(etiquetaSeleccionada)
            joven = self.jovenesRefs[indice]

            joven.horario = horarioVar.get()
            diasValidos = self.horariosDisponibles[joven.horario]
            fechas = []
            hoy = datetime.today()
            ultimoDiaMes = self.UltimoDiaDelMes(hoy)
            for dia in range(1, ultimoDiaMes + 1):
                fecha = hoy.replace(day=dia)
                if fecha.weekday() in diasValidos:
                    fechas.append(fecha.strftime("%d/%m/%y"))
            joven.fechas = fechas

            # Asigna la tarifa base según la experiencia (una sola vez)
            self.asignarBaseInscripcion(joven)

            messagebox.showinfo("Inscripción Registrada",
                                f"Joven {joven.getNombreCompleto()} formalizado.\n"
                                f"Tarifa base: {joven.baseInscripcion}.\n"
                                f"Valor actual de inscripción (base + compras): {joven.baseInscripcion + joven.totalCompras}.")
            from src.UDManager.baseDatos.serializador import Serializador
            Serializador.serializar()
            inscripcionWindow.destroy()

        tk.Button(inscripcionWindow, text="Inscribir", command=confirmar).pack(pady=10)

    def asignarBaseInscripcion(self, joven):
        """Asigna la tarifa base al joven según su experiencia, y la guarda en baseInscripcion.
           - Experiencia < 6 meses: 50,000
           - 6 a menos de 12 meses: 45,000
           - ≥ 12 meses: 40,000"""
        try:
            exp = int(joven.experienciaJoven)
        except:
            exp = 0
        if exp < 6:
            joven.baseInscripcion = 50000
        elif exp < 12:
            joven.baseInscripcion = 45000
        else:
            joven.baseInscripcion = 40000

    def crearJoven(self, fieldFrame):
        valores = [fieldFrame.getValue(c).strip() for c in
                   ["nombre", "apellido", "edad", "experienciaJoven", "eps",
                    "nombreAcudiente", "telefonoAcudiente", "cedulaAcudiente"]]
        if "" in valores:
            messagebox.showwarning("Campos Incompletos", "Todos los campos son obligatorios.")
            return
        try:
            edad = int(valores[2])
            experiencia = int(valores[3])
        except ValueError:
            messagebox.showerror("Error", "Edad y Experiencia deben ser números.")
            return
        deporteSeleccionado = self.deporteVar.get()
        nuevoId = max([int(j.id) for j in Joven.listaJovenes if isinstance(j.id, int)], default=0) + 1
        nuevoJoven = Joven(
            valores[0],
            valores[1],
            nuevoId,
            edad,
            experiencia,
            valores[4],
            valores[5],
            valores[6],
            ""
        )
        nuevoJoven.deporte = deporteSeleccionado
        messagebox.showinfo("Éxito",
                            f"Joven {nuevoJoven.getNombreCompleto()} creado correctamente con ID {nuevoJoven.id}.\n"
                            "Ahora puede inscribirlo en un horario.")

    def mostrarInscripciones(self):
        listaWin = tk.Toplevel(self.contentFrame)
        listaWin.title("Listado de Jóvenes")
        listaBox = tk.Listbox(listaWin, width=100, height=20)
        listaBox.pack(padx=10, pady=10, fill="both", expand=True)

        for j in Joven.listaJovenes:
            estado = "Inscripción Pagada" if j.inscripcionPagada else "Inscripción no Pagada"
            fechasStr = ", ".join(j.fechas) if hasattr(j, "fechas") and j.fechas else "Sin fechas"
            inscripcionValor = f"${j.baseInscripcion + j.totalCompras}" if hasattr(j,
                                                                                   "baseInscripcion") else "No calculado"
            listaBox.insert(tk.END,
                            f"{j.getNombreCompleto()} (ID: {j.id}) - {j.deporte} - {estado} - Inscripción: {inscripcionValor} - {fechasStr}")

        def mostrarDetalles():
            selected = listaBox.curselection()
            if not selected:
                messagebox.showwarning("Detalles", "Seleccione un joven para ver los detalles.")
                return
            index = selected[0]
            joven = Joven.listaJovenes[index]
            tarifa_base = joven.baseInscripcion if hasattr(joven, "baseInscripcion") else "No asignada"
            total_compras = joven.totalCompras
            valor_total = joven.baseInscripcion + joven.totalCompras if hasattr(joven,
                                                                                "baseInscripcion") else "No calculado"
            messagebox.showinfo("Inscripción Registrada",
                                f"Joven {joven.getNombreCompleto()} formalizado.\n"
                                f"Tarifa base: {tarifa_base}.\n"
                                f"Total Compras: {total_compras}.\n"
                                f"Valor actual de inscripción: {valor_total}")

        tk.Button(listaWin, text="Detalles", command=mostrarDetalles).pack(pady=5)
        tk.Button(listaWin, text="Cerrar", command=listaWin.destroy).pack(pady=5)

    def seleccionarJovenParaTienda(self):
        selWindow = tk.Toplevel(self.contentFrame)
        selWindow.title("Seleccionar Joven para Tienda")
        inscriptos = [j for j in Joven.listaJovenes if j.horario]
        if not inscriptos:
            messagebox.showinfo("Seleccion", "No hay jóvenes inscritos.")
            selWindow.destroy()
            return
        self.jovenesTiendaLabels = [f"{j.getNombreCompleto()} (ID: {j.id}) - {j.deporte}" for j in inscriptos]
        self.jovenesTiendaRefs = inscriptos
        tk.Label(selWindow, text="Seleccione un Joven:", font=("Arial", 12)).pack(pady=5)
        jovenVar = tk.StringVar()
        jovenVar.set(self.jovenesTiendaLabels[0])
        tk.OptionMenu(selWindow, jovenVar, *self.jovenesTiendaLabels).pack()
        tk.Button(selWindow, text="Usar Tienda",
                  command=lambda: self.mostrarTiendaParaJoven(jovenVar, selWindow)).pack(
            pady=10)

    def mostrarTiendaParaJoven(self, jovenVar, parentWindow):
        etiqueta = jovenVar.get()
        indice = self.jovenesTiendaLabels.index(etiqueta)
        joven = self.jovenesTiendaRefs[indice]
        parentWindow.destroy()
        deporte = joven.deporte
        articulosFiltrados = [art for art in self.tiendaEscuela.listarArticulos() if art.tipoArticulo == deporte]
        if not articulosFiltrados:
            messagebox.showinfo("Tienda", "No hay artículos para este deporte.")
            return
        tiendaWindow = tk.Toplevel(self.contentFrame)
        tiendaWindow.title("Tienda para " + joven.getNombreCompleto())
        tk.Label(tiendaWindow, text=f"Artículos de {deporte}", font=("Arial", 14)).pack(pady=5)
        listbox = tk.Listbox(tiendaWindow, width=80)
        for art in articulosFiltrados:
            listbox.insert(tk.END, str(art))
        listbox.pack(padx=10, pady=10)
        if not hasattr(joven, "totalCompras"):
            joven.totalCompras = 0

        def comprarArticulo():
            selected = listbox.curselection()
            if not selected:
                messagebox.showwarning("Tienda", "Seleccione un artículo para comprar.")
                return
            index = selected[0]
            articulo = articulosFiltrados[index]
            if articulo.stockArticulo > 0:
                articulo.stockArticulo -= 1
                joven.totalCompras += articulo.precio
                messagebox.showinfo("Compra", f"Se ha agregado el artículo {articulo.nombreArticulo} por ${articulo.precio}.")
                listbox.delete(index)
                listbox.insert(index, str(articulo))
            else:
                messagebox.showinfo("Compra", "El artículo está agotado.")

        tk.Button(tiendaWindow, text="Comprar", command=comprarArticulo).pack(pady=5)

        def finalizar():
            valor_actual = joven.baseInscripcion + joven.totalCompras if hasattr(joven,
                                                                                 "baseInscripcion") else "No calculado"
            messagebox.showinfo("Total Compras", f"El total de inscripción hasta ahora es: ${valor_actual}")
            tiendaWindow.destroy()

        tk.Button(tiendaWindow, text="Finalizar", command=finalizar).pack(pady=5)

    #-------

    def salir(self):
        from src.UDManager.baseDatos.serializador import Serializador
        Serializador.serializar()
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