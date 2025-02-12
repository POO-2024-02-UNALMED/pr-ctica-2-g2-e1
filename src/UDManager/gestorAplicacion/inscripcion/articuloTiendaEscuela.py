class ArticuloTiendaEscuela:
    def __init__(self, idArticulo=0, nombreArticulo="", stockArticulo=0, precio=0.0, tipoArticulo=""):
        self.idArticulo = idArticulo
        self.nombreArticulo = nombreArticulo
        self.stockArticulo = stockArticulo
        self.precio = precio
        self.tipoArticulo = tipoArticulo

    def __str__(self):
        return (f"Articulo: {self.nombreArticulo} (ID: {self.idArticulo}) - Stock: {self.stockArticulo} - "
                f"Precio: {self.precio} - Tipo: {self.tipoArticulo}")
