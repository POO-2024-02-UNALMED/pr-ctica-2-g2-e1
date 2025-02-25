class ErrorAplicacion(Exception):
    """Clase base para las excepciones de la aplicación."""
    def __init__(self, mensaje):
        super().__init__(f"Manejo de errores de la Aplicación: {mensaje}")

#////////////////////////PAGOS////////////////////////////////////////////////////

class ErrorSeleccion(ErrorAplicacion):
    """Error relacionado con la selección de clientes o suscripciones."""
    pass

class ClienteNoSeleccionado(ErrorSeleccion):
    """Error cuando no se selecciona un cliente al intentar pagar una suscripción."""
    def __init__(self):
        super().__init__("Debe seleccionar un cliente antes de continuar.")

class SuscripcionNoSeleccionada(ErrorSeleccion):
    """Error cuando no se selecciona una suscripción antes de confirmar el pago."""
    def __init__(self):
        super().__init__("Debe seleccionar una suscripción antes de confirmar el pago.")

class NoHayReservasPendientes(ErrorSeleccion):
    """Error cuando no hay reservas pendientes de pago."""
    def __init__(self):
        super().__init__("No hay reservas pendientes de pago.")

class ReservaNoSeleccionada(ErrorSeleccion):
    """Error cuando el usuario intenta pagar sin seleccionar una reserva."""
    def __init__(self):
        super().__init__("Debe seleccionar una reserva antes de proceder con el pago.")


#///////////////////////////EVENTOS EXCEPCIONES/////////////////////////////////////////////


class ErrorEventos(ErrorAplicacion):
    """Clase base para las excepciones relacionadas con eventos."""
    def __init__(self, mensaje):
        super().__init__(f"Error en Eventos: {mensaje}")

class DatosEventoIncompletos(ErrorEventos):
    """Error cuando faltan datos para la creación de un evento."""
    def __init__(self):
        super().__init__("Todos los campos del evento deben estar completos.")

class FormatoFechaIncorrecto(ErrorEventos):
    """Error cuando la fecha no tiene el formato correcto."""
    def __init__(self):
        super().__init__("Formato de fecha incorrecto. Use MM/DD/YY.")

class FormatoHoraIncorrecto(ErrorEventos):
    """Error cuando la hora no tiene el formato correcto."""
    def __init__(self):
        super().__init__("El formato de la hora debe ser HH:MM.")

class HoraInicioMayorQueFin(ErrorEventos):
    """Error cuando la hora de inicio es mayor o igual que la hora de fin."""
    def __init__(self):
        super().__init__("La hora de inicio debe ser antes que la hora de fin.")
