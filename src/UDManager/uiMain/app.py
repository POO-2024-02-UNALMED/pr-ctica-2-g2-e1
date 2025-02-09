import tkinter as tk
from tkinter import messagebox
from uiMain.dataManager import DataManager
from gestorAplicacion.eventos.evento import Evento
from gestorAplicacion.inscripcion.joven import Joven
from gestorAplicacion.reservas.instalacion import Instalacion
from gestorAplicacion.reservas.reserva import Reserva
from gestorAplicacion.pagos.cliente import Cliente
from gestorAplicacion.pagos.boleta import Boleta
from gestorAplicacion.torneo.torneo import Torneo
from uiMain import globalInstances


class Application(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Sistema de Gestión")
        self.geometry("900x700")

        # Menú de Archivo
        menubar = tk.Menu(self)
        fileMenu = tk.Menu(menubar, tearoff=0)
        fileMenu.add_command(label="Guardar", command=DataManager.saveData)
        fileMenu.add_command(label="Cargar", command=DataManager.loadData)
        fileMenu.add_separator()
        fileMenu.add_command(label="Salir", command=self.quit)
        menubar.add_cascade(label="Archivo", menu=fileMenu)
        self.config(menu=menubar)

        # Frame de navegación
        navFrame = tk.Frame(self)
        navFrame.pack(side=tk.TOP, fill=tk.X)

        buttons = [
            ("Eventos", self.showEventos),
            ("Jóvenes", self.showJovenes),
            ("Tienda", self.showTienda),
            ("Reservas", self.showReservas),
            ("Instalaciones", self.showInstalaciones),
            ("Torneos", self.showTorneos),
            ("Clientes", self.showClientes),
            ("Boletas", self.showBoletas)
        ]
        for (text, command) in buttons:
            btn = tk.Button(navFrame, text=text, command=command)
            btn.pack(side=tk.LEFT, padx=2, pady=2)

        # Contenedor para los frames
        self.container = tk.Frame(self)
        self.container.pack(fill=tk.BOTH, expand=True)

        self.frames = {}
        self.frames["eventos"] = self.createEventosFrame(self.container)
        self.frames["jovenes"] = self.createJovenesFrame(self.container)
        self.frames["tienda"] = self.createTiendaFrame(self.container)
        self.frames["reservas"] = self.createReservasFrame(self.container)
        self.frames["instalaciones"] = self.createInstalacionesFrame(self.container)
        self.frames["torneos"] = self.createTorneosFrame(self.container)
        self.frames["clientes"] = self.createClientesFrame(self.container)
        self.frames["boletas"] = self.createBoletasFrame(self.container)

        self.currentFrame = None
        self.showFrame("eventos")

    def showFrame(self, name):
        if self.currentFrame:
            self.currentFrame.pack_forget()
        frame = self.frames[name]
        frame.pack(fill=tk.BOTH, expand=True)
        self.currentFrame = frame

    def showEventos(self):
        self.showFrame("eventos")

    def showJovenes(self):
        self.showFrame("jovenes")

    def showTienda(self):
        self.showFrame("tienda")

    def showReservas(self):
        self.showFrame("reservas")

    def showInstalaciones(self):
        self.showFrame("instalaciones")

    def showTorneos(self):
        self.showFrame("torneos")

    def showClientes(self):
        self.showFrame("clientes")

    def showBoletas(self):
        self.showFrame("boletas")

    def createEventosFrame(self, parent):
        frame = tk.Frame(parent)
        self.eventosListbox = tk.Listbox(frame, width=100)
        self.eventosListbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        btnFrame = tk.Frame(frame)
        btnFrame.pack(side=tk.RIGHT, fill=tk.Y)
        tk.Button(btnFrame, text="Agregar Evento", command=self.addEvento).pack(pady=5)
        tk.Button(btnFrame, text="Refrescar", command=self.refreshEventos).pack(pady=5)
        return frame

    def refreshEventos(self):
        self.eventosListbox.delete(0, tk.END)
        for evento in Evento.eventos:
            self.eventosListbox.insert(tk.END, str(evento))

    def addEvento(self):
        win = tk.Toplevel(self)
        win.title("Agregar Evento")
        labels = ["Nombre Evento", "Tipo Evento", "Personaje Principal", "Género Musical"]
        entries = {}
        for i, label in enumerate(labels):
            tk.Label(win, text=label+":").grid(row=i, column=0)
            entry = tk.Entry(win)
            entry.grid(row=i, column=1)
            entries[label] = entry

        def saveEvento():
            evento = Evento()
            evento.nombreEvento = entries["Nombre Evento"].get()
            evento.tipoEvento = entries["Tipo Evento"].get()
            evento.personajePrincipal = entries["Personaje Principal"].get()
            evento.generoMusical = entries["Género Musical"].get()
            Evento.eventos.append(evento)
            self.refreshEventos()
            win.destroy()

        tk.Button(win, text="Guardar", command=saveEvento).grid(row=len(labels), column=0, columnspan=2)

    def createJovenesFrame(self, parent):
        frame = tk.Frame(parent)
        self.jovenesListbox = tk.Listbox(frame, width=100)
        self.jovenesListbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        btnFrame = tk.Frame(frame)
        btnFrame.pack(side=tk.RIGHT, fill=tk.Y)
        tk.Button(btnFrame, text="Agregar Joven", command=self.addJoven).pack(pady=5)
        tk.Button(btnFrame, text="Refrescar", command=self.refreshJovenes).pack(pady=5)
        return frame

    def refreshJovenes(self):
        self.jovenesListbox.delete(0, tk.END)
        for joven in Joven.listaJovenes:
            self.jovenesListbox.insert(tk.END, str(joven))

    def addJoven(self):
        win = tk.Toplevel(self)
        win.title("Agregar Joven")
        labels = ["Nombre", "Apellido", "Edad", "Experiencia", "EPS", "Nombre Acudiente", "Teléfono Acudiente", "Cédula Acudiente"]
        entries = {}
        for i, label in enumerate(labels):
            tk.Label(win, text=label+":").grid(row=i, column=0)
            entry = tk.Entry(win)
            entry.grid(row=i, column=1)
            entries[label] = entry

        def saveJoven():
            try:
                Joven(
                    nombre=entries["Nombre"].get(),
                    apellido=entries["Apellido"].get(),
                    edad=int(entries["Edad"].get()),
                    experienciaJoven=int(entries["Experiencia"].get()),
                    eps=entries["EPS"].get(),
                    nombreAcudiente=entries["Nombre Acudiente"].get(),
                    telefonoAcudiente=entries["Teléfono Acudiente"].get(),
                    cedulaAcudiente=entries["Cédula Acudiente"].get()
                )
                self.refreshJovenes()
                win.destroy()
            except Exception as e:
                messagebox.showerror("Error", f"Error: {e}")

        tk.Button(win, text="Guardar", command=saveJoven).grid(row=len(labels), column=0, columnspan=2)

    def createTiendaFrame(self, parent):
        frame = tk.Frame(parent)
        self.tiendaListbox = tk.Listbox(frame, width=100)
        self.tiendaListbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        btnFrame = tk.Frame(frame)
        btnFrame.pack(side=tk.RIGHT, fill=tk.Y)
        tk.Button(btnFrame, text="Agregar Artículo", command=self.addArticulo).pack(pady=5)
        tk.Button(btnFrame, text="Refrescar", command=self.refreshTienda).pack(pady=5)
        return frame

    def refreshTienda(self):
        self.tiendaListbox.delete(0, tk.END)
        for art in globalInstances.tiendaEscuela.listarArticulos():
            self.tiendaListbox.insert(tk.END, str(art))

    def addArticulo(self):
        win = tk.Toplevel(self)
        win.title("Agregar Artículo")
        labels = ["ID Artículo", "Nombre Artículo", "Stock", "Precio", "Tipo Artículo"]
        entries = {}
        for i, label in enumerate(labels):
            tk.Label(win, text=label+":").grid(row=i, column=0)
            entry = tk.Entry(win)
            entry.grid(row=i, column=1)
            entries[label] = entry

        def saveArticulo():
            try:
                from gestorAplicacion.inscripcion.articuloTiendaEscuela import ArticuloTiendaEscuela
                art = ArticuloTiendaEscuela(
                    idArticulo=int(entries["ID Artículo"].get()),
                    nombreArticulo=entries["Nombre Artículo"].get(),
                    stockArticulo=int(entries["Stock"].get()),
                    precio=float(entries["Precio"].get()),
                    tipoArticulo=entries["Tipo Artículo"].get()
                )
                globalInstances.tiendaEscuela.agregarArticulo(art)
                self.refreshTienda()
                win.destroy()
            except Exception as e:
                messagebox.showerror("Error", f"Error: {e}")

        tk.Button(win, text="Guardar", command=saveArticulo).grid(row=len(labels), column=0, columnspan=2)

    def createReservasFrame(self, parent):
        frame = tk.Frame(parent)
        self.reservasListbox = tk.Listbox(frame, width=100)
        self.reservasListbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        btnFrame = tk.Frame(frame)
        btnFrame.pack(side=tk.RIGHT, fill=tk.Y)
        tk.Button(btnFrame, text="Agregar Reserva", command=self.addReserva).pack(pady=5)
        tk.Button(btnFrame, text="Refrescar", command=self.refreshReservas).pack(pady=5)
        return frame

    def refreshReservas(self):
        self.reservasListbox.delete(0, tk.END)
        for reserva in Reserva.listaReservas:
            self.reservasListbox.insert(tk.END, str(reserva))

    def addReserva(self):
        win = tk.Toplevel(self)
        win.title("Agregar Reserva")
        labels = ["ID Cliente", "ID Instalación", "A Pagar"]
        entries = {}
        for i, label in enumerate(labels):
            tk.Label(win, text=label+":").grid(row=i, column=0)
            entry = tk.Entry(win)
            entry.grid(row=i, column=1)
            entries[label] = entry

        def saveReserva():
            try:
                idCliente = int(entries["ID Cliente"].get())
                idInstalacion = int(entries["ID Instalación"].get())
                aPagar = int(entries["A Pagar"].get())
                cliente = Cliente.obtenerCliente(idCliente)
                instalacion = Instalacion.obtenerInstalacion(idInstalacion)
                if not cliente or not instalacion:
                    messagebox.showerror("Error", "Cliente o Instalación no encontrado.")
                    return
                Reserva(cliente=cliente, instalacion=instalacion, fechaReserva=None, aPagar=aPagar)
                self.refreshReservas()
                win.destroy()
            except Exception as e:
                messagebox.showerror("Error", f"Error: {e}")

        tk.Button(win, text="Guardar", command=saveReserva).grid(row=len(labels), column=0, columnspan=2)

    def createInstalacionesFrame(self, parent):
        frame = tk.Frame(parent)
        self.instalacionesListbox = tk.Listbox(frame, width=100)
        self.instalacionesListbox.pack(fill=tk.BOTH, expand=True)
        btnFrame = tk.Frame(frame)
        btnFrame.pack(side=tk.RIGHT, fill=tk.Y)
        tk.Button(btnFrame, text="Refrescar", command=self.refreshInstalaciones).pack(pady=5)
        return frame

    def refreshInstalaciones(self):
        self.instalacionesListbox.delete(0, tk.END)
        for inst in Instalacion.listaInstalaciones:
            self.instalacionesListbox.insert(tk.END, str(inst))

    def createTorneosFrame(self, parent):
        frame = tk.Frame(parent)
        self.torneosListbox = tk.Listbox(frame, width=100)
        self.torneosListbox.pack(fill=tk.BOTH, expand=True)
        btnFrame = tk.Frame(frame)
        btnFrame.pack(side=tk.RIGHT, fill=tk.Y)
        tk.Button(btnFrame, text="Refrescar", command=self.refreshTorneos).pack(pady=5)
        return frame

    def refreshTorneos(self):
        self.torneosListbox.delete(0, tk.END)
        for torneo in Torneo.torneos:
            self.torneosListbox.insert(tk.END, str(torneo))

    def createClientesFrame(self, parent):
        frame = tk.Frame(parent)
        self.clientesListbox = tk.Listbox(frame, width=100)
        self.clientesListbox.pack(fill=tk.BOTH, expand=True)
        btnFrame = tk.Frame(frame)
        btnFrame.pack(side=tk.RIGHT, fill=tk.Y)
        tk.Button(btnFrame, text="Refrescar", command=self.refreshClientes).pack(pady=5)
        return frame

    def refreshClientes(self):
        self.clientesListbox.delete(0, tk.END)
        for cliente in Cliente.listaClientes:
            self.clientesListbox.insert(tk.END, str(cliente))

    def createBoletasFrame(self, parent):
        frame = tk.Frame(parent)
        self.boletasListbox = tk.Listbox(frame, width=100)
        self.boletasListbox.pack(fill=tk.BOTH, expand=True)
        btnFrame = tk.Frame(frame)
        btnFrame.pack(side=tk.RIGHT, fill=tk.Y)
        tk.Button(btnFrame, text="Refrescar", command=self.refreshBoletas).pack(pady=5)
        return frame

    def refreshBoletas(self):
        self.boletasListbox.delete(0, tk.END)
        for boleta in Boleta.listaBoletas:
            self.boletasListbox.insert(tk.END, str(boleta))

if __name__ == "__main__":
    app = Application()
    app.mainloop()
