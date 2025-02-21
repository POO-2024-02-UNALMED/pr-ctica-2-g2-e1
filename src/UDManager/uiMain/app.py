import tkinter as tk
from datetime import datetime
from tkinter import messagebox

from src.UDManager.baseDatos.serializador import Serializador
from src.UDManager.gestorAplicacion.eventos.evento import Evento
from src.UDManager.gestorAplicacion.inscripcion.joven import Joven
from src.UDManager.gestorAplicacion.reservas.fechaReserva import FechaReserva
from src.UDManager.gestorAplicacion.reservas.instalacion import Instalacion
from src.UDManager.gestorAplicacion.reservas.reserva import Reserva
from src.UDManager.gestorAplicacion.pagos.cliente import Cliente
from src.UDManager.gestorAplicacion.pagos.boleta import Boleta
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