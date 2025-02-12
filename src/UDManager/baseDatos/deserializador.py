import pickle
import os

class Deserializador:
    @staticmethod
    def deserializar(filePath="database.pkl"):
        if os.path.exists(filePath):
            try:
                with open(filePath, "rb") as f:
                    data = pickle.load(f)
                return data
            except Exception as e:
                print("Error en deserializacion:", e)
                return None
        else:
            return None
