from typing import Any
from lista_doblecircular import ListaDoblementeEnlazadaCircular
class Clientes:
    def __init__(self, rol, nombre, apellido, telefono, correo, contrasena):

        self.rol = rol
        self.nombre = nombre
        self.apellido = apellido
        self.telefono = telefono
        self.correo = correo
        self.contrasena = contrasena
        self.lista_voletos_guardados = {}
        self.lista_favoritos = ListaDoblementeEnlazadaCircular()
        self.lista_nativa = []

    def imprimir(self):
        print(f"rol: {self.rol}, nombre: {self.nombre}, apellido: {self.apellido}, telefono: {self.telefono}, correo: {self.correo}, contrasena: {self.contrasena}")
              
    def get_rol(self):
        return self.rol
    
    def get_nombre(self):
        return self.nombre
    
    def get_apellido(self):
        return self.apellido
    
    def get_telefono(self):
        return self.telefono
    
    def get_correo(self):
        return self.correo
    
    def get_contrasena(self):
        return self.contrasena
    
    def get_listaVoletos(self):
        return self.lista_nativa
    
    def append_listaVoletos(self, voleto):
        self.lista_nativa.append(voleto)

    def append_favoritos(self, pelicula):
        self.lista_favoritos.insertar_final(pelicula)
    