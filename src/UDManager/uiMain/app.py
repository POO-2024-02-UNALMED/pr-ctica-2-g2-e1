import pickle
import random
import tkinter
import tkinter as tk
from datetime import datetime, timedelta
from tkinter import messagebox

from tkcalendar import Calendar

from src.UDManager.baseDatos.serializador import Serializador
from src.UDManager.gestorAplicacion.eventos.evento import Evento
from src.UDManager.gestorAplicacion.inscripcion.joven import Joven
from src.UDManager.gestorAplicacion.reservas.fechaReserva import FechaReserva
from src.UDManager.gestorAplicacion.reservas.instalacion import Instalacion
from src.UDManager.gestorAplicacion.reservas.reserva import Reserva
from src.UDManager.gestorAplicacion.pagos.cliente import Cliente
from src.UDManager.gestorAplicacion.pagos.boleta import Boleta
from src.UDManager.gestorAplicacion.torneo.equipo import Equipo
from src.UDManager.gestorAplicacion.torneo.torneo import Torneo
from src.UDManager.gestorAplicacion.inscripcion.tiendaEscuela import TiendaEscuela

# Importa la clase FieldFrame desde su archivo
from src.UDManager.uiMain.fieldFrame import FieldFrame

TiendaEscuela = TiendaEscuela()


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
                ultimaReserva.cliente.getNombreCompleto(),
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
                           f"ID: {reserva.ID} - Cliente: {reserva.cliente.getNombreCompleto()} - Instalación: {reserva.instalacion.nombre} - Fecha: {reserva.fechaReserva.getInicioReserva().strftime('%Y-%m-%d %H:%M')}")

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
        tk.Button(self.contentFrame, text="Crear Torneo", command=self.crearTorneo).pack(pady=10)
        tk.Button(self.contentFrame, text="Ver Fixture", command=self.verFixture).pack(pady=10)
        tk.Button(self.contentFrame, text="Ver Equipos", command=self.verEquiposTorneo).pack(pady=10)
        tk.Button(self.contentFrame, text= "Editar Equipos", command=self.editarEquipos).pack(pady=5)

    def crearReserva(self):
        print("El método crearReserva ha sido llamado.")  # Confirmamos la ejecución del método
        self.clienteSeleccionado = next(cliente for cliente in self.clientes if
                                        f"{cliente.ID} - {cliente.getNombreCompleto()}" == self.clienteSelect.get())
        self.fechaSeleccionada = self.calendario.get_date()  # Obtener la fecha del calendario (en formato string)
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
            # Convertir la fecha seleccionada y las horas a formato datetime
            print(
                f"Fecha seleccionada: {self.fechaSeleccionada} | Hora inicio: {self.horaInicio} | Hora fin: {self.horaFin}")

            fechaReserva = datetime.strptime(f"{self.fechaSeleccionada} {self.horaInicio}", "%m/%d/%y %H:%M")
            self.horaFin = datetime.strptime(f"{self.fechaSeleccionada} {self.horaFin}", "%m/%d/%y %H:%M")

            # Verificar las fechas convertidas
            print(f"Fecha de reserva: {fechaReserva} | Hora fin: {self.horaFin}")

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
        # Crear una nueva ventana de creación de reserva
        self.menuWin = tk.Toplevel(self)
        self.menuWin.title("Crear Reserva")
        self.menuWin.geometry("700x700")

        # Campo para seleccionar cliente
        labelCliente = tk.Label(self.menuWin, text="Selecciona un Cliente", font=("Arial", 12))
        labelCliente.pack(pady=5)
        clientes = [f"{cliente.ID} - {cliente.getNombreCompleto()}" for cliente in self.clientes]
        self.clienteSelect = tk.StringVar(self.menuWin)
        self.clienteSelect.set(clientes[0])  # Establecer por defecto el primer cliente
        clienteDropdown = tk.OptionMenu(self.menuWin, self.clienteSelect, *clientes)
        clienteDropdown.pack(pady=5)

        # Campo para seleccionar la fecha de la reserva usando un calendario
        labelFecha = tk.Label(self.menuWin, text="Selecciona una fecha", font=("Arial", 12))
        labelFecha.pack(pady=5)
        from tkcalendar import Calendar
        self.calendario = Calendar(self.menuWin)
        self.calendario.pack(pady=5)

        # Campos para seleccionar horas de inicio y fin de la reserva
        labelHoraInicio = tk.Label(self.menuWin, text="Hora de Inicio (HH:MM)", font=("Arial", 12))
        labelHoraInicio.pack(pady=5)
        self.horaInicioEntry = tk.Entry(self.menuWin)  # Asignar a self
        self.horaInicioEntry.pack(pady=5)

        labelHoraFin = tk.Label(self.menuWin, text="Hora de Fin (HH:MM)", font=("Arial", 12))
        labelHoraFin.pack(pady=5)
        self.horaFinEntry = tk.Entry(self.menuWin)  # Asignar a self
        self.horaFinEntry.pack(pady=5)

        # Campo para seleccionar instalación
        labelInstalacion = tk.Label(self.menuWin, text="Selecciona una Instalación", font=("Arial", 12))
        labelInstalacion.pack(pady=5)
        instalaciones = [f"{inst.nombre}" for inst in self.instalaciones]
        self.instalacionSelect = tk.StringVar(self.menuWin)
        self.instalacionSelect.set(instalaciones[0])  # Establecer por defecto la primera instalación
        instalacionDropdown = tk.OptionMenu(self.menuWin, self.instalacionSelect, *instalaciones)
        instalacionDropdown.pack(pady=5)

        # Botón para confirmar la reserva
        confirmarReservaBtn = tk.Button(self.menuWin, text="Aceptar", command=self.crearReserva)
        confirmarReservaBtn.pack(pady=20)
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

    def crearTorneo(self):
        # Crear una nueva ventana para la creación del torneo
        torneoWin = tk.Toplevel(self)
        torneoWin.title("Crear Torneo")
        torneoWin.geometry("600x600")

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
        deportes = ["Futbol", "Baloncesto", "Natación", "Voleibol"]
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

        # Fechas de inicio y fin con calendarios
        labelFechaInicio = tk.Label(torneoWin, text="Fecha de Inicio", font=("Arial", 12))
        labelFechaInicio.pack(pady=5)

        # Usamos el calendario para la fecha de inicio
        calendarioInicio = Calendar(torneoWin, selectmode="day", date_pattern="yyyy-mm-dd")
        calendarioInicio.pack(pady=5, side="left", padx=5)

        labelFechaFin = tk.Label(torneoWin, text="Fecha de Fin", font=("Arial", 12))
        labelFechaFin.pack(pady=5)

        # Usamos el calendario para la fecha de fin
        calendarioFin = Calendar(torneoWin, selectmode="day", date_pattern="yyyy-mm-dd")
        calendarioFin.pack(pady=5, side="left", padx=5)

        # Botón Aceptar
        aceptarBtn = tk.Button(torneoWin, text="Aceptar",
                               command=lambda: self.onAceptar(clienteSelect, nombreTorneoEntry, deporteSelect,
                                                              instalacionSelect, calendarioInicio, calendarioFin,
                                                              equipos,torneoWin))
        aceptarBtn.pack(pady=20)

    def onAceptar(self, clienteSelect, nombreTorneoEntry, deporteSelect, instalacionSelect, calendarioInicio,
                  calendarioFin, equipos, torneoWin):
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
            fechaInicio = datetime.strptime(calendarioInicio.get_date(), "%Y-%m-%d")
            fechaFin = datetime.strptime(calendarioFin.get_date(), "%Y-%m-%d")
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
        torneo = Torneo(deporte, equiposParticipantes)
        torneo.instalacion = instalacion
        torneo.nombre = nombreTorneo  # Establecer el nombre del torneo

        # Verificar si ya existe el torneo en la lista antes de agregarlo
        if not any(t.nombre == torneo.nombre for t in self.torneos):
            self.torneos.append(torneo)  # Solo lo agregamos si no existe
            self.serializarTorneos()  # Serializamos los torneos para persistirlos

        # Imprimir los torneos para depuración
        print("Lista de torneos después de agregar el nuevo torneo:")
        for t in self.torneos:
            print(t.nombre)

        # Mostrar mensaje de éxito
        messagebox.showinfo("Torneo Creado",
                            f"Torneo '{nombreTorneo}' creado exitosamente con {len(equiposParticipantes)} equipos.")
        torneoWin.destroy()  # Cerramos la ventana de creación de torneo

    def editarEquipos(self):
        # Crear una nueva ventana para editar los equipos
        editarWin = tk.Toplevel(self)
        editarWin.title("Editar Equipos")
        editarWin.geometry("600x600")

        # Selección de torneo (desplegable)
        labelTorneo = tk.Label(editarWin, text="Selecciona un Torneo", font=("Arial", 12))
        labelTorneo.pack(pady=5)

        # Cargar torneos desde la lista
        torneos = [torneo.nombre for torneo in self.torneos]
        if not torneos:
            messagebox.showerror("Error", "No hay torneos disponibles")
            return

        torneoSelect = tk.StringVar(editarWin)
        torneoSelect.set(torneos[0])  # Establecer por defecto el primer torneo
        torneoDropdown = tk.OptionMenu(editarWin, torneoSelect, *torneos)
        torneoDropdown.pack(pady=5)

        # Selección de equipo (desplegable) - Inicialmente vacío
        labelEquipo = tk.Label(editarWin, text="Selecciona un Equipo", font=("Arial", 12))
        labelEquipo.pack(pady=5)
        equipoSelect = tk.StringVar(editarWin)
        equipoDropdown = tk.OptionMenu(editarWin, equipoSelect, "")  # Vacío inicialmente
        equipoDropdown.pack(pady=5)

        # Función para actualizar los equipos después de seleccionar un torneo
        def actualizarEquipos(*args):
            """Actualiza los equipos basados en el torneo seleccionado."""
            torneoSeleccionado = torneoSelect.get()
            torneo = next(t for t in self.torneos if t.nombre == torneoSeleccionado)  # Obtener el torneo
            equiposFiltrados = [equipo.nombreEquipo for equipo in
                                torneo.equiposParticipantes]  # Filtrar equipos usando el atributo correcto
            if equiposFiltrados:
                equipoSelect.set(equiposFiltrados[0])  # Establecer el primer equipo por defecto
                equipoDropdown['menu'].delete(0, 'end')  # Limpiar el menú de equipos
                for equipo in equiposFiltrados:
                    equipoDropdown['menu'].add_command(label=equipo, command=tk._setit(equipoSelect, equipo))
            else:
                messagebox.showerror("Error", "Este torneo no tiene equipos.")

        # Llamar a la actualización de equipos cuando el torneo cambia
        torneoSelect.trace('w', actualizarEquipos)

        # Llamar a la función de actualización al iniciar para el primer torneo
        actualizarEquipos()

    def serializarTorneos(self):
        """Serializa la lista de torneos para persistirla en un archivo."""
        with open('torneos.pkl', 'wb') as f:
            pickle.dump(self.torneos, f)

    def cargarTorneos(self):
        """Cargar torneos desde el archivo serializado."""
        try:
            with open('torneos.pkl', 'rb') as f:
                self.torneos = pickle.load(f)
        except FileNotFoundError:
            self.torneos = []  # Si no hay archivo, inicializamos una lista vacía

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
                  overrelief="solid").pack(pady=15)
        tk.Button(botones1,
                  text="Cancelar Suscripción",
                  width=25,
                  height=2,
                  relief="groove",
                  overrelief="solid").pack(pady=15,
                                            padx=(10, 50),
                                            anchor="w")
        tk.Button(botones1,
                  text="Pagar Reserva",
                  width=25,
                  height=2,
                  relief="groove",
                  command=self.pagarReserva,
                  overrelief="solid").pack(pady=15)

        self.labelImg1 = tk.Label(self.contentFrame,image=self.img_pagos1, bg="white")
        self.labelImg1.place(x=200, y=110)

        tk.Button(botones2,
                  text="Pagar Evento",
                  width=25,
                  height=2,
                  relief="groove",
                  overrelief="solid").pack(pady=15)
        tk.Button(botones2,
                  text="Comprar Boleta",
                  width=25,
                  height=2,
                  relief="groove",
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

    def pagarSuscripcion(self):
        pass

    def cancelarSuscripcion(self):
        pass

    def pagarReserva(self):
        pass

    def pagarEvento(self):

        pass

    def comprarBoleta(self):
        pass

    def pagarTorneo(self):
        pass

###FORMATIVO
    
    def UltimoDiaDelMes(self, fecha):
        if fecha.month == 12:
            return 31
        proximoMes = fecha.replace(month=fecha.month + 1, day=1)
        return (proximoMes - timedelta(days=1)).day

    def mostrarFormativo(self):
        # Limpia el contentFrame
        for widget in self.contentFrame.winfo_children():
            widget.destroy()

        title = tk.Label(self.contentFrame, text="Área Formativa", font=("Arial", 18), bg="white")
        title.pack(pady=10)

        formFrame = tk.Frame(self.contentFrame, bg="white")
        formFrame.pack(pady=10, fill="x")

        # Campos que pedimos al usuario
        criteria = ["nombre", "apellido", "edad", "experienciaJoven", "eps",
                    "nombreAcudiente", "telefonoAcudiente", "cedulaAcudiente"]

        # Definimos los horarios disponibles (diasemana: 0 = lunes, 6 = domingo)
        self.horariosDisponibles = {
            "Lunes-Miércoles 8-10": [0, 2],
            "Lunes-Miércoles 10-12": [0, 2],
            "Martes-Jueves 8-10": [1, 3],
            "Martes-Jueves 10-12": [1, 3],
            "Viernes 14-16": [4]
        }

        #FieldFrame para los campos de texto
        fieldFrame = FieldFrame(formFrame, "Campo", criteria, "Valor")
        fieldFrame.pack(fill="both", expand=True, padx=10, pady=10)

        # OptionMenu para "deporte"
        tk.Label(formFrame, text="Deporte:", font=("Arial", 12), bg="white").pack(pady=5)
        deportes = ["Fútbol", "Baloncesto", "Natación", "Tenis"]
        self.deporteVar = tk.StringVar()
        self.deporteVar.set(deportes[0])  # Valor inicial
        opMenuDeporte = tk.OptionMenu(formFrame, self.deporteVar, *deportes)
        opMenuDeporte.pack()

        btnFrame = tk.Frame(formFrame, bg="white")
        btnFrame.pack(side="bottom", pady=10)

        tk.Button(btnFrame, text="Crear Joven", command=lambda: self.crearJoven(fieldFrame)).pack(side="left", padx=5)
        tk.Button(btnFrame, text="Inscribir Joven", command=self.inscribirJoven).pack(side="left", padx=5)
        tk.Button(btnFrame, text="Ver Jovenes", command=self.mostrarInscripciones).pack(side="left", padx=5)

    def crearJoven(self, fieldFrame):
        # Obtenemos los valores del FieldFrame (sin "deporte")
        valores = [fieldFrame.getValue(c).strip() for c in
                   ["nombre", "apellido", "edad", "experienciaJoven", "eps",
                    "nombreAcudiente", "telefonoAcudiente", "cedulaAcudiente"]]

        # Verificamos campos vacíos
        if "" in valores:
            messagebox.showwarning("Campos Incompletos", "Todos los campos son obligatorios.")
            return

        # Convertimos a int los campos "edad" y "experienciaJoven"
        try:
            edad = int(valores[2])
            experiencia = int(valores[3])
        except ValueError:
            messagebox.showerror("Error", "Edad y Experiencia deben ser números.")
            return

        # Obtenemos el deporte seleccionado en el OptionMenu
        deporteSeleccionado = self.deporteVar.get()

        # Calculamos un nuevo ID
        nuevoId = max([int(j.id) for j in Joven.listaJovenes if isinstance(j.id, int)], default=0) + 1

        # Creamos el objeto Joven
        nuevoJoven = Joven(
            valores[0],  # nombre
            valores[1],  # apellido
            nuevoId,
            edad,
            experiencia,
            valores[4],  # eps
            valores[5],  # nombreAcudiente
            valores[6],  # telefonoAcudiente
            valores[7]  # cedulaAcudiente
        )
        # Asignamos el deporte que viene del OptionMenu
        nuevoJoven.deporte = deporteSeleccionado

        messagebox.showinfo("Éxito",
                            f"Joven {nuevoJoven.getNombreCompleto()} creado correctamente con ID {nuevoJoven.id}. "
                            "Ahora puede inscribirlo en un horario.")

    def inscribirJoven(self):
        # Ventana emergente para inscribir
        inscripcionWindow = tk.Toplevel(self.contentFrame)
        inscripcionWindow.title("Inscribir Joven")

        tk.Label(inscripcionWindow, text="Seleccione un Joven", font=("Arial", 12)).pack(pady=5)

        # Construccion de  la lista de jóvenes no inscritos
        jovenesNoInscritos = [j for j in Joven.listaJovenes if not j.inscripcionPagada]
        if not jovenesNoInscritos:
            messagebox.showinfo("Aviso", "No hay jóvenes disponibles para inscripción.")
            inscripcionWindow.destroy()
            return

        #creacion de listas paralelas para OptionMenu
        self.jovenesLabels = [f"{j.getNombreCompleto()} (ID: {j.id})" for j in jovenesNoInscritos]
        self.jovenesRefs = jovenesNoInscritos

        jovenVar = tk.StringVar()
        jovenVar.set(self.jovenesLabels[0])  # Primera opción por defecto
        jovenMenu = tk.OptionMenu(inscripcionWindow, jovenVar, *self.jovenesLabels)
        jovenMenu.pack()

        tk.Label(inscripcionWindow, text="Seleccione un Horario", font=("Arial", 12)).pack(pady=5)
        horarioVar = tk.StringVar()
        horarioVar.set(list(self.horariosDisponibles.keys())[0])
        horarioMenu = tk.OptionMenu(inscripcionWindow, horarioVar, *self.horariosDisponibles.keys())
        horarioMenu.pack()

        def confirmar():
            etiquetaSeleccionada = jovenVar.get()
            indice = self.jovenesLabels.index(etiquetaSeleccionada)
            joven = self.jovenesRefs[indice]

            joven.inscripcionPagada = True
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

            messagebox.showinfo("Inscripción Exitosa",
                                f"Joven {joven.getNombreCompleto()} inscrito en {joven.deporte} "
                                f"en las fechas {', '.join(fechas)} en el horario {joven.horario}.")

            from src.UDManager.baseDatos.serializador import Serializador
            Serializador.serializar()
            inscripcionWindow.destroy()

        tk.Button(inscripcionWindow, text="Inscribir", command=confirmar).pack(pady=10)

    def mostrarInscripciones(self):
        inscripciones = []
        for j in Joven.listaJovenes:
            estado = "Inscrito" if j.inscripcionPagada else "No Inscrito"
            fechasStr = ", ".join(j.fechas) if hasattr(j, "fechas") and j.fechas else "Sin fechas"
            inscripciones.append(f"{j.getNombreCompleto()} (ID: {j.id}) - {j.deporte} - {estado} - {fechasStr}")

        if inscripciones:
            messagebox.showinfo("Inscripciones", "\n".join(inscripciones))
        else:
            messagebox.showinfo("Inscripciones", "No hay jóvenes registrados.")


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