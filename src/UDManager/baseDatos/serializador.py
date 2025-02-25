# src/UDManager/baseDatos/serializador.py

import src.UDManager.gestorAplicacion.eventos.evento as ev
import src.UDManager.gestorAplicacion.inscripcion.grupoFormativo as gf
import src.UDManager.gestorAplicacion.pagos.cliente as cl
import src.UDManager.gestorAplicacion.reservas.reserva as res
import src.UDManager.gestorAplicacion.reservas.instalacion as inst
import src.UDManager.gestorAplicacion.torneo.torneo as tor
from src.UDManager.gestorAplicacion.inscripcion.joven import Joven
import pickle
import os

class Serializador:
    @staticmethod
    def serializar():
        db_path = os.path.join(os.path.dirname(__file__), "..", "baseDatos", "database.txt")
        try:
            with open(db_path, "wb") as f:
                pickle.dump({
                    "clientes": cl.Cliente.getListaClientes(),
                    "reservas": res.Reserva.getListaReservas(),
                    "instalaciones": inst.Instalacion.getListaInstalaciones(),
                    "torneos": tor.Torneo.getTorneos(),
                    "grupoFormativos": gf.GrupoFormativo.getGrupoFormativos(),
                    "eventos": ev.Evento.getEventos(),
                    "jovenes": Joven.listaJovenes

                }, f)
                print("Serialización exitosa")
        except Exception as e:
            print("Error durante la serialización:", e)
