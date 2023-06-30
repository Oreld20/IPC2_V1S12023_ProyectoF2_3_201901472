class Salas:
    def __init__(self, sala, asientos):
        self.sala = sala
        self.asientos = asientos
    
    def imprimir(self):
        print(f"sala: {self.sala} asientos: {self.asientos}")