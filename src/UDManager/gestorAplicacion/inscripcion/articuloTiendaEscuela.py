# src/UDManager/gestorAplicacion/inscripcion/articuloTiendaEscuela.py

class ArticuloTiendaEscuela:
    def __init__(self, idArticulo, nombreArticulo, stockArticulo, precio, tipoArticulo):
        self.idArticulo = idArticulo
        self.nombreArticulo = nombreArticulo
        self.stockArticulo = stockArticulo
        self.precio = precio
        self.tipoArticulo = tipoArticulo

    def __str__(self):
        return f"Articulo {self.idArticulo}: {self.nombreArticulo} - Stock: {self.stockArticulo} - Precio: {self.precio}"
