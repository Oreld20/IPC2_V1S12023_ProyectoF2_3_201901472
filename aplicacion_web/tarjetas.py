class Tarjetas:
    def __init__(self, tipo, numero, titular, expiracion):
        self.tipo = tipo
        self.numero = numero
        self.titular = titular
        self.expiracion = expiracion

    def imprimir(self):
        print(f"tipo: {self.tipo}, numero: {self.numero}, titular: {self.titular}, expiracion: {self.expiracion}")
              