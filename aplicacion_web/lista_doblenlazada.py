from nodo_doblenlace import Nodo
import xml.etree.ElementTree as ET
from salas import Salas
class ListaDoblementeEnlazada:
    def __init__(self):
        self.primero = None
        self.ultimo = None

    def reiniciar(self):
        self.primero = None
        self.ultimo = None

    def esta_vacia(self):
        return self.primero is None

    def insertar_inicio(self, dato):
        nuevo_nodo = Nodo(dato)
        if self.esta_vacia():
            self.primero = nuevo_nodo
            self.ultimo = nuevo_nodo
        else:
            nuevo_nodo.siguiente = self.primero
            self.primero.anterior = nuevo_nodo
            self.primero = nuevo_nodo

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

    def imprimir_lista_reversa(self):
        if self.esta_vacia():
            print("La lista está vacía.")
        else:
            actual = self.ultimo
            while actual is not None:
                print(actual.dato)
                actual = actual.anterior


    def CargarXML_salas(self,operacion):
        if operacion == 1:
            self.primero= None
        tree = ET.parse(r'C:\Users\eliot\OneDrive\Documentos\MyEspacio_De_Trabajo\proyecto-ipc2\aplicacion_web\salas.XML')
        root = tree.getroot()
        cine = root.find('cine')

        for indice, sala in enumerate(cine.findall("salas/sala")):
            numero = sala.find('numero').text
            asientos = sala.find('asientos').text
            objeto = Salas(numero, asientos)
            if operacion == 1:
                if self.verificar_nodos_repetidos():
                    self.insertar_final(objeto)
            elif operacion == 2:
                self.modify(objeto, indice)

    def modify(self, nuevo_dato, posicion):
        if self.primero is None or posicion < 0:
            return  False

        nodo_actual = self.primero
        indice = 0
        while nodo_actual is not None:
            if indice == posicion:
                nodo_actual.dato = nuevo_dato
                return
            nodo_actual = nodo_actual.siguiente
            indice += 1


    def buscar_elemento(self, target):
        current_node = self.primero
        while current_node is not None:
            if current_node.dato.sala == target:
                return current_node.dato
            current_node = current_node.siguiente
        return None
    
    def verificar_nodos_repetidos(self):
        valores = set()

        nodo_actual = self.primero
        while nodo_actual is not None:
            if nodo_actual.dato in valores:
                return False

            valores.add(nodo_actual.dato)
            nodo_actual = nodo_actual.siguiente

        return True
    
    def eliminar_elemento(self, elemento):
        if self.primero is None:
            return  # La lista está vacía, no hay nada que eliminar

        if self.primero.dato.sala == elemento:
            if self.primero == self.ultimo:
                self.primero = None
                self.ultimo = None
            else:
                self.primero = self.primero.siguiente
                self.primero.anterior = None
            return

        if self.ultimo.dato.sala == elemento:
            self.ultimo = self.ultimo.anterior
            self.ultimo.siguiente = None
            return

        nodo_actual = self.primero.siguiente
        while nodo_actual is not None:
            if nodo_actual.dato.sala == elemento:
                nodo_actual.anterior.siguiente = nodo_actual.siguiente
                nodo_actual.siguiente.anterior = nodo_actual.anterior
                return
            nodo_actual = nodo_actual.siguiente

            
    def editar_sala(self, numero_sala, nuevo_numero, nuevos_asientos):
        # Parsear el archivo XML
        tree = ET.parse(r'C:\Users\eliot\OneDrive\Documentos\MyEspacio_De_Trabajo\proyecto-ipc2\aplicacion_web\salas.XML')
        root = tree.getroot()

        for sala in root.iter('sala'):
            numero = sala.find('numero').text
            if numero == numero_sala:
                nuevo_numero_element = sala.find('numero')
                nuevo_numero_element.text = nuevo_numero
                nuevos_asientos_element = sala.find('asientos')
                nuevos_asientos_element.text = nuevos_asientos

            tree.write(r'C:\Users\eliot\OneDrive\Documentos\MyEspacio_De_Trabajo\proyecto-ipc2\aplicacion_web\salas.XML')
            self.CargarXML_salas(1)


    def crear_nueva_sala(self, numero_sala, asientos):
        # Parsear el archivo XML
        tree = ET.parse(r'C:\Users\eliot\OneDrive\Documentos\MyEspacio_De_Trabajo\proyecto-ipc2\aplicacion_web\salas.XML')
        root = tree.getroot()

        nueva_sala = ET.SubElement(root.find('cine').find('salas'), 'sala')

        numero = ET.SubElement(nueva_sala, 'numero')
        numero.text = numero_sala

        asientos_elem = ET.SubElement(nueva_sala, 'asientos')
        asientos_elem.text = asientos

        tree.write(r'C:\Users\eliot\OneDrive\Documentos\MyEspacio_De_Trabajo\proyecto-ipc2\aplicacion_web\salas.XML')
        self.CargarXML_salas(1)

    def eliminar_sala_nombre(self, nombre):
        tree = ET.parse(r'C:\Users\eliot\OneDrive\Documentos\MyEspacio_De_Trabajo\proyecto-ipc2\aplicacion_web\salas.XML')
        root = tree.getroot()
        for cine in root.findall('cine'):
            salas = cine.find('salas')
            for sala in salas.findall('sala'):
                numero = sala.find('numero').text
                if numero == nombre:
                    salas.remove(sala)
                    self.CargarXML_salas(1)
                                                
        tree.write(r'C:\Users\eliot\OneDrive\Documentos\MyEspacio_De_Trabajo\proyecto-ipc2\aplicacion_web\salas.XML')

    def __iter__(self):
        actual = self.primero
        while actual is not None:
            yield actual.dato
            actual = actual.siguiente
            
              

            

         
        