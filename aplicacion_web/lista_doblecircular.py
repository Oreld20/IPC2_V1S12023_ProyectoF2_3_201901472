from nodo_doblecircular import Nodo
import xml.etree.ElementTree as ET
from peliculas import Pelicula
class ListaDoblementeEnlazadaCircular:
    def __init__(self):
        self.primero = None
        self.ultimo = None

    def esta_vacia(self):
        return self.primero is None

    def insertar_inicio(self, dato):
        nuevo_nodo = Nodo(dato)
        if self.esta_vacia():
            nuevo_nodo.siguiente = nuevo_nodo
            nuevo_nodo.anterior = nuevo_nodo
            self.primero = nuevo_nodo
        else:
            ultimo = self.primero.anterior
            nuevo_nodo.siguiente = self.primero
            nuevo_nodo.anterior = ultimo
            self.primero.anterior = nuevo_nodo
            ultimo.siguiente = nuevo_nodo
            self.primero = nuevo_nodo

    def insertar_final(self, dato):
        nuevo_nodo = Nodo(dato)
        if self.esta_vacia():
            nuevo_nodo.siguiente = nuevo_nodo
            nuevo_nodo.anterior = nuevo_nodo
            self.primero = nuevo_nodo
        else:
            ultimo = self.primero.anterior
            nuevo_nodo.siguiente = self.primero
            nuevo_nodo.anterior = ultimo
            self.primero.anterior = nuevo_nodo
            ultimo.siguiente = nuevo_nodo

    def imprimir_Categoria(self):
        if self.esta_vacia():
            print("La lista está vacía.")
        else:
            actual = self.primero
            actual.dato.imprimir_categoria()
            while True:
                actual = actual.siguiente
                actual.dato.imprimir_categoria()
                if actual == self.primero:
                    break

    def imprimir_pelicula(self):
        if self.esta_vacia():
            print("La lista está vacía.")
        else:
            actual = self.primero
            actual.dato.imprimir_pelicula()
            while True:
                actual = actual.siguiente
                actual.dato.imprimir_pelicula()
                if actual == self.primero:
                    break


    def CargarXML_Categorias(self):
        self.primero = None
        self.ultimo = None
        
        tree = ET.parse(r'C:\Users\eliot\OneDrive\Documentos\MyEspacio_De_Trabajo\proyecto-ipc2\aplicacion_web\categorias_peliculas.XML')
        root = tree.getroot()
        for categoria in root.findall("categoria"):
            nombre = categoria.find('nombre').text
            name = nombre.strip()
            pelicula = categoria.find('peliculas')

            for peli in pelicula.findall('pelicula'):
                titulo = peli.find('titulo').text
                director = peli.find('director').text
                anio = peli.find('anio').text
                fecha = peli.find('fecha').text
                hora = peli.find('hora').text
                try:
                    imagen = peli.find('imagen').text
                    precio = peli.find('precio').text
                except Exception as e:
                    print(e)
                image = imagen.strip()
                price = precio.strip()
                objeto = Pelicula(name, titulo, director, anio, fecha, hora, image, price)
                self.insertar_final(objeto)



    def buscar_elemento(self, dato):
        if self is None:
            return False

        actual = self.primero
        while True:
            if actual.dato.titulo == dato:
                return actual.dato
            actual = actual.siguiente
            if actual == self.primero:
                break

        return False
    

    def verificar_nodos_repetidos(self):
        valores = set()  # Conjunto para almacenar los valores de los nodos

        nodo_actual = self.primero
        while nodo_actual is not None:
            if nodo_actual.dato in valores:
                return False

            valores.add(nodo_actual.dato)
            nodo_actual = nodo_actual.siguiente

            if nodo_actual == self.primero:
                break

        return True
    

    def eliminar_elemento(self, elemento):
        if self.primero is None:
            return  # La lista está vacía, no hay nada que eliminar

        if self.primero == self.ultimo and self.primero.dato.titulo == elemento:
            self.primero = None
            self.ultimo = None
            return

        nodo_actual = self.primero
        while nodo_actual is not None:
            if nodo_actual.dato.titulo == elemento:
                if nodo_actual == self.primero:
                    self.primero = nodo_actual.siguiente
                    self.primero.anterior = self.ultimo
                    self.ultimo.siguiente = self.primero
                elif nodo_actual == self.ultimo:
                    self.ultimo = nodo_actual.anterior
                    self.ultimo.siguiente = self.primero
                    self.primero.anterior = self.ultimo
                else:
                    nodo_actual.anterior.siguiente = nodo_actual.siguiente
                    nodo_actual.siguiente.anterior = nodo_actual.anterior
                return
            nodo_actual = nodo_actual.siguiente


    def eliminar_pelicula_por_titulo(self, titulo):
        tree = ET.parse(r'C:\Users\eliot\OneDrive\Documentos\MyEspacio_De_Trabajo\proyecto-ipc2\aplicacion_web\categorias_peliculas.XML')
        root = tree.getroot()
        for categoria in root.findall('categoria'):
            peliculas = categoria.find('peliculas')
            for pelicula in peliculas.findall('pelicula'):
                titulo_pelicula = pelicula.find('titulo').text
                if titulo_pelicula == titulo:
                    peliculas.remove(pelicula)
                    self.CargarXML_Categorias()

        tree.write(r'C:\Users\eliot\OneDrive\Documentos\MyEspacio_De_Trabajo\proyecto-ipc2\aplicacion_web\categorias_peliculas.XML')


    def editar_pelicula_por_titulo(self, titulo, nuevo_titulo,  nuevo_director, nuevo_anio, nueno_fecha, nuevo_hora, nuevo_imagen, nuevo_precio):
        tree = ET.parse(r'C:\Users\eliot\OneDrive\Documentos\MyEspacio_De_Trabajo\proyecto-ipc2\aplicacion_web\categorias_peliculas.XML')
        root = tree.getroot()

        # Buscar la película por su título
        for pelicula in root.iter('pelicula'):
            titulo_pelicula = pelicula.find('titulo').text
            if titulo_pelicula == titulo:
                # Editar los elementos director y anio de la película
                pelicula.find('titulo').text = nuevo_titulo
                pelicula.find('director').text = nuevo_director
                pelicula.find('anio').text = nuevo_anio
                pelicula.find('fecha').text = nueno_fecha
                pelicula.find('hora').text = nuevo_hora
                pelicula.find('imagen').text = nuevo_imagen
                pelicula.find('precio').text = nuevo_precio
                categoria = root.find('categoria').text

        # Guardar los cambios en el archivo XML
        nuevo_dato= Pelicula(categoria, nuevo_titulo, nuevo_director, nuevo_anio, nueno_fecha, nuevo_hora, nuevo_imagen, nuevo_precio)
        self.editar_elemento(titulo, nuevo_dato)
        tree.write(r'C:\Users\eliot\OneDrive\Documentos\MyEspacio_De_Trabajo\proyecto-ipc2\aplicacion_web\categorias_peliculas.XML')



    def añadir_pelicula(self, categoria, titulo, director, anio, fecha, hora, imagen, precio):
        tree = ET.parse(r'C:\Users\eliot\OneDrive\Documentos\MyEspacio_De_Trabajo\proyecto-ipc2\aplicacion_web\categorias_peliculas.XML')
        root = tree.getroot()

        # Buscar la categoría específica
        for categoria_element in root.findall('categoria'):
            nombre_categoria = categoria_element.find('nombre').text
            if nombre_categoria == categoria:
                peliculas = categoria_element.find('peliculas')
                
                # Crear el elemento de la nueva película
                pelicula_nueva = ET.Element('pelicula')
                
                titulo_element = ET.Element('titulo')
                titulo_element.text = titulo
                pelicula_nueva.append(titulo_element)
                
                director_element = ET.Element('director')
                director_element.text = director
                pelicula_nueva.append(director_element)
                
                anio_element = ET.Element('anio')
                anio_element.text = anio
                pelicula_nueva.append(anio_element)
                
                fecha_element = ET.Element('fecha')
                fecha_element.text = fecha
                pelicula_nueva.append(fecha_element)
                
                hora_element = ET.Element('hora')
                hora_element.text = hora
                pelicula_nueva.append(hora_element)

                imagen_element = ET.Element('imagen')
                imagen_element.text = imagen
                pelicula_nueva.append(imagen_element)

                precio_element = ET.Element('precio')
                precio_element.text = precio
                pelicula_nueva.append(precio_element)
                
                # Añadir la nueva película a la lista de películas
                peliculas.append(pelicula_nueva)
                self.CargarXML_Categorias()

        # Guardar los cambios en el archivo XML
        tree.write(r'C:\Users\eliot\OneDrive\Documentos\MyEspacio_De_Trabajo\proyecto-ipc2\aplicacion_web\categorias_peliculas.XML')


    def buscar_elemento(self, titulo):
        if self.primero is None:
            return None

        actual = self.primero
        while True:
            if actual.dato.titulo == titulo:
                return actual

            actual = actual.siguiente
            if actual == self.primero:
                break

        return None
    
    def editar_elemento(self, titulo, nueva_info):
        nodo = self.buscar_elemento(titulo)
        if nodo is not None:
            nodo.dato = nueva_info
            print("Elemento editado con éxito.")
        else:
            print("No se encontró el elemento en la lista.")


    def agregar_categoria_xml(self, nombre_categoria):
        # Cargar el archivo XML
        tree = ET.parse(r'C:\Users\eliot\OneDrive\Documentos\MyEspacio_De_Trabajo\proyecto-ipc2\aplicacion_web\categorias_peliculas.XML')
        root = tree.getroot()

        # Crear el nuevo elemento de categoría
        nueva_categoria = ET.Element('categoria')

        # Crear el elemento 'nombre' dentro de la nueva categoría
        nombre = ET.Element('nombre')
        nombre.text = nombre_categoria
        nueva_categoria.append(nombre)

        # Crear el elemento 'peliculas' dentro de la nueva categoría
        peliculas = ET.Element('peliculas')
        nueva_categoria.append(peliculas)

        # Agregar la nueva categoría al elemento raíz
        root.append(nueva_categoria)

        # Guardar los cambios en el archivo XML
        tree.write(r'C:\Users\eliot\OneDrive\Documentos\MyEspacio_De_Trabajo\proyecto-ipc2\aplicacion_web\categorias_peliculas.XML')


    def editar_categoria_xml(self, nombre_categoria_existente, nuevo_nombre_categoria):
        # Cargar el archivo XML
        tree = ET.parse(r'C:\Users\eliot\OneDrive\Documentos\MyEspacio_De_Trabajo\proyecto-ipc2\aplicacion_web\categorias_peliculas.XML')
        root = tree.getroot()

        # Buscar la categoría existente por el nombre
        for categoria in root.findall('categoria'):
            nombre = categoria.find('nombre').text
            if nombre == nombre_categoria_existente:
                # Actualizar el nombre de la categoría
                categoria.find('nombre').text = nuevo_nombre_categoria

        # Guardar los cambios en el archivo XML
        tree.write(r'C:\Users\eliot\OneDrive\Documentos\MyEspacio_De_Trabajo\proyecto-ipc2\aplicacion_web\categorias_peliculas.XML')


    def eliminar_categoria_xml(self, nombre_categoria):
        # Cargar el archivo XML
        tree = ET.parse(r'C:\Users\eliot\OneDrive\Documentos\MyEspacio_De_Trabajo\proyecto-ipc2\aplicacion_web\categorias_peliculas.XML')
        root = tree.getroot()

        # Buscar y eliminar la categoría por el nombre
        for categoria in root.findall('categoria'):
            nombre = categoria.find('nombre').text
            if nombre == nombre_categoria:
                root.remove(categoria)

        # Guardar los cambios en el archivo XML
        tree.write(r'C:\Users\eliot\OneDrive\Documentos\MyEspacio_De_Trabajo\proyecto-ipc2\aplicacion_web\categorias_peliculas.XML')


    def __iter__(self):
        node = self.primero
        while True:
            yield node.dato
            node = node.siguiente
            if node == self.primero:
                break

    def reiniciar(self):
        self.primero = None
        self.ultimo = None


    def asociar_lista_doble_circular(self, titular, dato_favorito):
        nodo_actual = self.primero
        while nodo_actual is not None:
            if nodo_actual.dato.nombre == titular:
                nodo_actual.dato.append_favoritos(dato_favorito)
                break
            nodo_actual = nodo_actual.siguiente


    def recorrer_lista_doble_circular(self, titular):
        nodo_actual = self.primero
        while nodo_actual is not None:
            if nodo_actual.dato.nombre == titular:
                lista_doble_circular = nodo_actual.dato.lista_favoritos
                if lista_doble_circular is not None:
                    return lista_doble_circular
                else:
                    print("El cliente no tiene una lista doblemente enlazada circular asociada.")
                break
            nodo_actual = nodo_actual.siguiente
    
            
        
            
        







            