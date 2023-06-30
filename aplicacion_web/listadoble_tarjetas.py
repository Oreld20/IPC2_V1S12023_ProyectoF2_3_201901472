from nodo_doblenlace import Nodo
import xml.etree.ElementTree as ET
from tarjetas import Tarjetas

class ListaDoblementeEnlazada_tarjetas:
    def __init__(self):
        self.primero = None
        self.ultimo = None

    def reiniciar(self):
        self.primero = None
        self.ultimo = None

    def esta_vacia(self):
        return self.primero is None


    def insertar_final(self, dato):
        nuevo_nodo = Nodo(dato)
        if self.esta_vacia():
            self.primero = nuevo_nodo
            self.ultimo = nuevo_nodo
        else:
            nuevo_nodo.anterior = self.ultimo
            self.ultimo.siguiente = nuevo_nodo
            self.ultimo = nuevo_nodo

    def imprimir_lista(self):
        if self.esta_vacia():
            print("La lista está vacía.")
        else:
            actual = self.primero
            while actual is not None:
                actual.dato.imprimir()
                actual = actual.siguiente
    
    def __iter__(self):
        actual = self.primero
        while actual is not None:
            yield actual.dato
            actual = actual.siguiente

    
    def buscar_elemento(self, target):
        current_node = self.primero
        while current_node is not None:
            if current_node.dato.titular == target:
                return current_node.dato
            current_node = current_node.siguiente
        return None
    
    def cargar_desde_xml(self):
        self.primero = None
        self.ultimo = None
        tree = ET.parse(r'C:\Users\eliot\OneDrive\Documentos\MyEspacio_De_Trabajo\proyecto-ipc2\aplicacion_web\tarjetas.XML')
        root = tree.getroot()

        for tarjeta_xml in root.findall("tarjeta"):
            tipo = tarjeta_xml.find("tipo").text
            numero = tarjeta_xml.find("numero").text
            titular = tarjeta_xml.find("titular").text
            fecha_expiracion = tarjeta_xml.find("fecha_expiracion").text

            tarjeta = Tarjetas(tipo, numero, titular, fecha_expiracion)
            self.insertar_final(tarjeta)


    def eliminar_tarjetas_por_titular(self, titular):
        tree = ET.parse(r'C:\Users\eliot\OneDrive\Documentos\MyEspacio_De_Trabajo\proyecto-ipc2\aplicacion_web\tarjetas.XML')
        root = tree.getroot()

        tarjetas = root.findall("tarjeta")

        for tarjeta in tarjetas:
            titular_xml = tarjeta.find("titular").text
            if titular_xml == titular:
                root.remove(tarjeta)

        tree.write(r'C:\Users\eliot\OneDrive\Documentos\MyEspacio_De_Trabajo\proyecto-ipc2\aplicacion_web\tarjetas.XML')


    def editar_tarjeta_por_titular(self, titular, nuevo_titular, nuevo_tipo, nuevo_numero, nueva_fecha):
        tree = ET.parse(r'C:\Users\eliot\OneDrive\Documentos\MyEspacio_De_Trabajo\proyecto-ipc2\aplicacion_web\tarjetas.XML')
        root = tree.getroot()

        tarjetas = root.findall("tarjeta")

        for tarjeta in tarjetas:
            titular_xml = tarjeta.find("titular").text
            if titular_xml == titular:
                tipo_xml = tarjeta.find("tipo")
                tipo_xml.text = nuevo_tipo

                numero_xml = tarjeta.find("numero")
                numero_xml.text = nuevo_numero

                fecha_xml = tarjeta.find("fecha_expiracion")
                fecha_xml.text = nueva_fecha

                titular_xml = tarjeta.find("titular")
                titular_xml.text = nuevo_titular

        tree.write(r'C:\Users\eliot\OneDrive\Documentos\MyEspacio_De_Trabajo\proyecto-ipc2\aplicacion_web\tarjetas.XML')
        
    

    def agregar_tarjeta_a_xml(self, tipo, numero, titular, fecha_expiracion):
        tree = ET.parse(r'C:\Users\eliot\OneDrive\Documentos\MyEspacio_De_Trabajo\proyecto-ipc2\aplicacion_web\tarjetas.XML')
        root = tree.getroot()

        tarjetas = root.findall("tarjeta")

        nueva_tarjeta = ET.Element("tarjeta")

        tipo_xml = ET.SubElement(nueva_tarjeta, "tipo")
        tipo_xml.text = tipo

        numero_xml = ET.SubElement(nueva_tarjeta, "numero")
        numero_xml.text = numero

        titular_xml = ET.SubElement(nueva_tarjeta, "titular")
        titular_xml.text = titular

        fecha_expiracion_xml = ET.SubElement(nueva_tarjeta, "fecha_expiracion")
        fecha_expiracion_xml.text = fecha_expiracion

        root.append(nueva_tarjeta)

        tree.write(r'C:\Users\eliot\OneDrive\Documentos\MyEspacio_De_Trabajo\proyecto-ipc2\aplicacion_web\tarjetas.XML')

    
    
