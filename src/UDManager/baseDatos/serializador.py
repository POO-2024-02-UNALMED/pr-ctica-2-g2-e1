import pickle

class Serializador:
    @staticmethod
    def serializar(data, filePath="database.pkl"):
        try:
            with open(filePath, "wb") as f:
                pickle.dump(data, f)
            return True
        except Exception as e:
            print("Error en serializacion:", e)
            return False
