# src/UDManager/baseDatos/serializador.py

import src.UDManager.gestorAplicacion.eventos.evento as ev
import src.UDManager.gestorAplicacion.inscripcion.grupoFormativo as gf
import src.UDManager.gestorAplicacion.pagos.cliente as cl
import src.UDManager.gestorAplicacion.reservas.reserva as res
import src.UDManager.gestorAplicacion.reservas.instalacion as inst
import src.UDManager.gestorAplicacion.torneo.torneo as tor
import pickle

class Serializador:
    @staticmethod
    def serializar():
        # Se serializan los datos de cada módulo en archivos separados.
        # Se puede implementar según la lógica del proyecto.
        try:
            with open("database.txt", "wb") as f:
                pickle.dump({
                    "clientes": cl.Cliente.getListaClientes(),
                    "reservas": res.Reserva.getListaReservas(),
                    "instalaciones": inst.Instalacion.getListaInstalaciones(),
                    "torneos": tor.Torneo.getTorneos(),
                    "grupoFormativos": gf.GrupoFormativo.getGrupoFormativos(),
                    "eventos": ev.Evento.getEventos()
                }, f)
                print("Serialización exitosa")
        except Exception as e:
            print("Error durante la serialización:", e)
