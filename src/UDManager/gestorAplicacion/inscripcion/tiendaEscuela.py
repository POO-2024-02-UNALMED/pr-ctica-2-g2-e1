class TiendaEscuela:
    def __init__(self):
        self.articulos = []  # Lista de ArticuloTiendaEscuela

    def agregarArticulo(self, articulo):
        self.articulos.append(articulo)

    def eliminarArticulo(self, idArticulo):
        self.articulos = [art for art in self.articulos if art.idArticulo != idArticulo]

    def listarArticulos(self):
        return self.articulos

    def buscarArticuloPorId(self, idArticulo):
        for articulo in self.articulos:
            if articulo.idArticulo == idArticulo:
                return articulo
        return None
