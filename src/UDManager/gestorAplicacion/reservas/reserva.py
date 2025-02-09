from gestorAplicacion.pagos.cliente import Cliente

class Reserva:
    listaReservas = []

    def __init__(self, cliente=None, instalacion=None, fechaReserva=None, aPagar=0,
                 equipo1=None, equipo2=None, grupoFormativo=None, arbitro=None, horaReservada=None):
        self.id = len(Reserva.listaReservas) + 1
        self.cliente = cliente
        self.instalacion = instalacion
        self.fechaReserva = fechaReserva
        self.aPagar = aPagar
        self.pagada = False
        self.equipo1 = equipo1
        self.equipo2 = equipo2
        self.grupoFormativo = grupoFormativo
        self.arbitro = arbitro
        Reserva.listaReservas.append(self)

    @classmethod
    def buscarReserva(cls, id):
        for reserva in cls.listaReservas:
            if reserva.id == id:
                return reserva
        return None

    def setPagada(self):
        self.pagada = True

    def __str__(self):
        if self.cliente and self.instalacion:
            descuento = (self.cliente.suscripcion.tipoSuscripcion.descuento
                         if (self.cliente and self.cliente.suscripcion) else 0)
            totalConDesc = self.aPagar - self.aPagar * descuento
            return (f"Reserva:\nID: {self.id}\nCliente: {self.cliente.nombre} {self.cliente.apellido}\n"
                    f"Instalación: {self.instalacion.nombre}\nTotal básico: {self.aPagar}\n"
                    f"Total con descuento: {totalConDesc}\nPagada: {self.pagada}")
        else:
            return f"Reserva ID: {self.id}"
