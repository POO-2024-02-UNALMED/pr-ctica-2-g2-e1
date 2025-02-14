# src/UDManager/baseDatos/serializador.py

import src.UDManager.gestorAplicacion.eventos.evento as ev
import src.UDManager.gestorAplicacion.inscripcion.grupoFormativo as gf
import src.UDManager.gestorAplicacion.pagos.cliente as cl
import src.UDManager.gestorAplicacion.reservas.reserva as res
import src.UDManager.gestorAplicacion.torneo.torneo as tor
import pickle

class Serializador:
    @staticmethod
    def serializar():
        # Se serializan los datos de cada módulo en archivos separados.
        # Se puede implementar según la lógica del proyecto.
        with open("database.txt", "wb") as f:
            pickle.dump({
                "clientes": cl.Cliente.getListaClientes(),
                "reservas": res.Reserva.getListaReservas(),
                "torneos": tor.Torneo.getTorneos(),
                "grupoFormativos": gf.GrupoFormativo.getGrupoFormativos(),
                "eventos": ev.Evento.getEventos()
            }, f)
