# src/UDManager/gestorAplicacion/inscripcion/tiendaEscuela.py

class TiendaEscuela:
    def __init__(self):
        self.articulos = []

    def agregarArticulo(self, articulo):
        self.articulos.append(articulo)

    def eliminarArticulo(self, idArticulo):
        self.articulos = [art for art in self.articulos if art.getIdArticulo() != idArticulo]

    def listarArticulos(self):
        return self.articulos

    def buscarArticuloPorId(self, id):
        for articulo in self.articulos:
            if articulo.getIdArticulo() == id:
                return articulo
        return None
