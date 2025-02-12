class Boleta:
    listaBoletas = []
    ultimoId = 100000

    def __init__(self, tipoEvento, precio, cliente):
        self.id = Boleta.ultimoId
        Boleta.ultimoId += 1
        self.tipoEvento = tipoEvento
        self.precio = precio
        self.cliente = cliente
        self.pagada = False
        Boleta.listaBoletas.append(self)

    @classmethod
    def buscarBoleta(cls, id):
        for boleta in cls.listaBoletas:
            if boleta.id == id:
                return boleta
        return None

    def __str__(self):
        return (f"Boleta:\nID: {self.id}\nCliente: {self.cliente.nombre} {self.cliente.apellido}\n"
                f"Tipo de evento: {self.tipoEvento}\nPrecio: {self.precio}\nPagada: {self.pagada}")