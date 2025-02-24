# src/UDManager/uiMain/dataManager.py

import pickle

class DataManager:
    @staticmethod
    def saveData():
        try:
            with open("../baseDatos/database.txt", "wb") as f:
                pickle.dump("datos guardados", f)
            print("Datos guardados correctamente.")
        except Exception as e:
            print("Error al guardar datos:", e)

    @staticmethod
    def loadData():
        try:
            with open("../baseDatos/database.txt", "rb") as f:
                data = pickle.load(f)
            print("Datos cargados correctamente.")
            return data
        except Exception as e:
            print("Error al cargar datos:", e)
            return None
