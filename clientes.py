from typing import Any


class Clientes:
    def __init__(self, rol, nombre, apellido, telefono, correo, contrasena):

        self.rol = rol
        self.nombre = nombre
        self.apellido = apellido
        self.telefono = telefono
        self.correo = correo
        self.contrasena = contrasena

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
    