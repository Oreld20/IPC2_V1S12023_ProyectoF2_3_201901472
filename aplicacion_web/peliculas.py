
class Pelicula:
    def __init__(self, categoria, titulo, director, anio, fecha, hora, imagen, precio):
        self.categoria = categoria
        self.titulo = titulo
        self.director = director
        self.anio = anio
        self.fecha = fecha
        self.hora = hora
        self.imagen = imagen
        self.precio = precio

    def imprimir_categoria(self):
        print(f"categoria: {self.categoria}, titulo: {self.titulo}, director: {self.director}, anio: {self.anio}, fecha: {self.fecha}, hora: {self.hora}, imagen: {self.imagen}, precio: {self.precio}")

    def imprimir_pelicula(self):
        print(f"titulo: {self.titulo}, director: {self.director}")

