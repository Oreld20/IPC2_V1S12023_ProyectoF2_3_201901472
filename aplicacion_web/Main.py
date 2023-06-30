from flask import Flask, render_template, url_for, request, redirect, jsonify
from markupsafe import escape #Este import es paraq ocultar los datos importantes ingresados en el url
from lista_enlazada import ListaEnlazada
from lista_doblecircular import ListaDoblementeEnlazadaCircular
from lista_doblenlazada import ListaDoblementeEnlazada
import xml.etree.ElementTree as ET
from listadoble_tarjetas import ListaDoblementeEnlazada_tarjetas
import json
import xmltodict
import requests
from boletos import Boletos
from tarjetas import Tarjetas
from clientes import Clientes
from salas import Salas
from peliculas import Pelicula
from tarjetas import Tarjetas
lista_clientes = ListaEnlazada()
lista_salas = ListaDoblementeEnlazada()
lista_Peliculas = ListaDoblementeEnlazadaCircular()
lista_Peliculas.CargarXML_Categorias()
objeto = Clientes("administrador","Oreld", "Ardon", "41445281", "eliotorel10@gmail.com", "201901472")
lista_clientes.add(objeto)
lista_tarjetas = ListaDoblementeEnlazada_tarjetas()
lista_clientes_json = ListaEnlazada()
lista_salas_json= ListaDoblementeEnlazada()
lista_peliculas_json = ListaDoblementeEnlazadaCircular()
lista_tarjetas_json= ListaDoblementeEnlazada_tarjetas()
lista_boletos = []

contador_global = 0

def incrementar_contador():
    global contador_global
    contador_global += 1

def obtener_contador():
    global contador_global
    return contador_global

app = Flask(__name__)

@app.route('/')
def main():
    url_for('login')
    url_for('peliculas')
    url_for('main')
    url_for('registro')
    url_for('opciones_clientes')
    url_for('opciones_administrador')
    return render_template('Menu.html',lista_P = lista_Peliculas )


@app.route('/login', methods=['POST','GET'])
def login():
    if request.method == 'POST':
        usuario = request.form['usuario']
        contrasena = request.form['contraseña']
        nodo_usuarios=lista_clientes.getNodo(usuario)
        try:
        
            if nodo_usuarios.correo == usuario and nodo_usuarios.contrasena == contrasena:
                if nodo_usuarios.rol == "administrador":
                    nombre = nodo_usuarios.nombre
                    return render_template('Opciones_Administrador.html')
                elif nodo_usuarios.rol == "cliente":
                    nombre = nodo_usuarios.nombre
                    return render_template('Opciones_Clientes.html', nombre=nombre)
            else:
                error = "Los datos ingresados no existen en el sistema"
                return render_template('Login.html',lista_c = lista_clientes, error = error)
        except Exception as e:
                    print(e)
    return render_template('Login.html',lista_c = lista_clientes)


@app.route('/registro', methods=['POST','GET'])
def registro():
    if request.method=='POST':
        rol = "cliente"
        nombre = request.form['nombre']
        apellido = request.form['apellido']
        telefono = request.form['telefono']
        email = request.form['email']
        password= request.form['contraseña']
        lista_clientes.nuevo_registroXML(rol,nombre,apellido, telefono, email, password)
        lista_clientes.CargarXML(1)
        mensaje = "cliente creado con exito"
        return render_template('Register.html', mensaje=mensaje)
    return render_template('Register.html')


@app.route('/Peliculas')
def peliculas():
    return render_template('Listado_Peliculas.html',lista_P=lista_Peliculas)


@app.route('/opciones_clientes')
def opciones_clientes():
    nombre = request.args.get('nombre')
    return render_template('Opciones_Clientes.html', nombre=nombre)


@app.route('/opciones_administrador', methods=['POST','GET'])
def opciones_administrador():
    if request.method == 'POST':
        opcion = request.form['boton']
        if opcion == "Cargar_los_XML":
            try:
                lista_clientes.CargarXML(1)
                lista_Peliculas.CargarXML_Categorias()
                lista_salas.CargarXML_salas(1)
                lista_tarjetas.cargar_desde_xml()
                lista_clientes_json.reiniciar()
                lista_salas_json.reiniciar()
                lista_peliculas_json.reiniciar()
                lista_tarjetas_json.reiniciar()

                response = requests.get('http://localhost:5700/json_usuarios')
                clientes_api = response.json()
                objeto_json = json.loads(clientes_api)
                usuarios = objeto_json["usuarios"]["usuario"]
                for usuario in usuarios:
                    rol = usuario["rol"]
                    nombre= usuario["nombre"]
                    apellido= usuario["apellido"]
                    telefono= usuario["telefono"]
                    correo= usuario["correo"]
                    contrasena= usuario["contrasena"]
                    objeto =Clientes(rol, nombre, apellido, telefono, correo, contrasena)
                    lista_clientes_json.add(objeto)


                response = requests.get('http://localhost:5700/json_salas')
                salas_api = response.json()
                salas_json = json.loads(salas_api)
                json_salas = salas_json["cines"]["cine"]["salas"]["sala"]
                for sala_json in json_salas:
                    sala = sala_json["numero"]
                    asientos = sala_json["asientos"]
                    sala_objeto = Salas(sala, asientos)
                    lista_salas_json.insertar_final(sala_objeto)

                
                response = requests.get('http://localhost:5700/categorias_peliculas')
                peliculas_api = response.json()
                peliculas_json = json.loads(peliculas_api)
                categorias_json = peliculas_json["categorias"]["categoria"]
                for categoria_json in categorias_json:
                    categoria = categoria_json["nombre"]
                    peliculas_json = categoria_json["peliculas"]["pelicula"]
                    for pelicula_json in peliculas_json:
                        titulo = pelicula_json["titulo"]
                        director = pelicula_json["director"]
                        anio = pelicula_json["anio"]
                        fecha = pelicula_json["fecha"]
                        hora = pelicula_json["hora"]
                        imagen = pelicula_json["imagen"]
                        precio = pelicula_json["precio"]
                        pelicula_objeto = Pelicula(categoria, titulo, director, anio, fecha, hora, imagen, precio)
                        lista_peliculas_json.insertar_final(pelicula_objeto)

                response = requests.get('http://localhost:5700/json_tarjetas')
                tarjetas_api = response.json()
                tarjetas_jsonn = json.loads(tarjetas_api)
                tarjetas_json = tarjetas_jsonn["tarjetas"]["tarjeta"]
                for tarjeta_json in tarjetas_json:
                    tipo = tarjeta_json["tipo"]
                    numero = tarjeta_json["numero"]
                    titular = tarjeta_json["titular"]
                    expiracion = tarjeta_json["fecha_expiracion"]
                    tarjeta_objeto = Tarjetas(tipo, numero, titular, expiracion)
                    lista_tarjetas_json.insertar_final(tarjeta_objeto)

                mensaje = "XML's Cargados con exito"
                return render_template('Opciones_Administrador.html',mensaje = mensaje)
            except Exception as e:
                print(e)
    return render_template('Opciones_Administrador.html')


@app.route('/editar_clientes', methods=['POST','GET'])
def editar_clientes():
    if request.method== 'POST':
        opcion = request.form['correo']
        lista_clientes.eliminar_elemento_xml(opcion)
        lista_clientes.CargarXML(1)
        return render_template('Editar_Clientes.html', lista_c = lista_clientes, lista_cj=lista_clientes_json )
    return render_template('Editar_Clientes.html', lista_c = lista_clientes, lista_cj = lista_clientes_json)


@app.route('/edicion_clientes', methods=['POST','GET'])
def edicion_clientes():
    correo = request.args.get('correo')
    print(correo)
    if request.method=='POST':
        viejo_email = request.form['viejo']
        rol =request.form['rol']
        nombre = request.form['nombre']
        apellido= request.form['apellido']
        telefono= request.form['telefono']
        email= request.form['email']
        password= request.form['password']
        lista_clientes.editar_usuario(viejo_email, rol, nombre, apellido, telefono, email, password)
        lista_clientes.CargarXML(1)
        return render_template('Editar_Clientes.html', lista_c = lista_clientes , lista_cj=lista_clientes_json)

    return render_template('Edicion_Clientes.html', lista_c = lista_clientes,correo=correo)

@app.route('/nuevo_cliente', methods = ['POST','GET'])
def nuevo_cliente():
    if request.method=='POST':
        rol = request.form['rol']
        nombre = request.form['nombre']
        apellido = request.form['apellido']
        telefono = request.form['telefono']
        email = request.form['email']
        password= request.form['contraseña']
        lista_clientes.nuevo_registroXML(rol,nombre,apellido, telefono, email, password)
        lista_clientes.CargarXML(1)
        return render_template('Editar_Clientes.html', lista_c = lista_clientes, lista_cj=lista_clientes_json)
    return render_template('nuevo_cliente.html')

@app.route('/editar_sala', methods = ['POST','GET'])
def editar_sala():
    if request.method=='POST':
        sala = request.form['sala']
        lista_salas.eliminar_sala_nombre(sala)
        lista_salas.CargarXML_salas(1)
        return render_template('editar_salas.html', lista_s = lista_salas, lista_sj=lista_salas_json)
    return render_template('editar_salas.html', lista_s = lista_salas, lista_sj=lista_salas_json)

@app.route('/edicion_salas', methods = ['POST','GET'])
def edicion_salas():
    sala = request.args.get('sala')
    print(sala)
    if request.method=='POST':
        numero = request.form['numero']
        lugar = request.form['sala']
        asientos = request.form['asientos']
        lista_salas.editar_sala(numero, lugar, asientos)
        lista_salas.CargarXML_salas(1)
        return render_template('editar_salas.html', lista_s = lista_salas, lista_sj=lista_salas_json)

    return render_template('Edicion_Salas.html', lista_s = lista_salas, sala=sala)

@app.route('/nueva_sala', methods = ['POST','GET'])
def nueva_sala():
    if request.method=='POST':
        numero = request.form['numero']
        asientos = request.form['asientos']
        print(numero)
        print(asientos)
        lista_salas.crear_nueva_sala(numero, asientos)
        lista_salas.CargarXML_salas(1)
        return render_template('editar_salas.html', lista_s = lista_salas, lista_sj=lista_salas_json)

    return render_template('nueva_sala.html')

@app.route('/listadopeliculas_cliente', methods = ['POST','GET'])
def listadopeliculas_cliente():
    nombre = request.args.get('nombre')
    if request.method=='POST':
        name = request.form['nombre']
        favorito = request.form['favorito']
        print(favorito)
        print(name)
        pelicula=lista_Peliculas.buscar_elemento(favorito).dato
        lista_clientes.asociar_lista_circular(name, pelicula)
        lista_clientes.recorrer_lista_circular(name)
        return render_template('listadopeliculas_cliente.html',lista_P=lista_Peliculas, nombre=name)
        
    return render_template('listadopeliculas_cliente.html',lista_P=lista_Peliculas, nombre=nombre)

@app.route('/editar_peliculas', methods = ['POST','GET'])
def editar_peliculas():
    if request.method=='POST':
        titulo = request.form['titulo']
        lista_Peliculas.eliminar_pelicula_por_titulo(titulo)
        lista_Peliculas.CargarXML_Categorias()
        return render_template('editar_peliculas.html', lista_P=lista_Peliculas, lista_pelj = lista_peliculas_json)

    return render_template('editar_peliculas.html', lista_P=lista_Peliculas, lista_pelj = lista_peliculas_json)

@app.route('/Edicion_Peliculas', methods = ['POST','GET'])
def Edicion_Peliculas():
    nombre = request.args.get('nombre')
    if request.method=='POST':
        anterior = request.form['anterior']
        titulo = request.form['titulo']
        director = request.form['director']
        año = request.form['año']
        fecha = request.form['fecha']
        hora = request.form['hora']
        imagen = request.form['imagen']
        precio = request.form['precio']
        lista_Peliculas.editar_pelicula_por_titulo(anterior,titulo, director, año, fecha,hora, imagen, precio)
        lista_Peliculas.CargarXML_Categorias()
        return render_template('editar_peliculas.html',lista_P=lista_Peliculas, lista_pelj = lista_peliculas_json)
    return render_template('Edicion_Peliculas.html', nombre=nombre, lista_P=lista_Peliculas)

@app.route('/nueva_pelicula', methods = ['POST','GET'])
def nueva_pelicula():
    if request.method=='POST':
        categoria = request.form['categoria']
        titulo = request.form['titulo']
        director = request.form['director']
        año = request.form['año']
        fecha = request.form['fecha']
        hora = request.form['hora']
        imagen = request.form['imagen']
        precio = request.form['precio']

        lista_Peliculas.añadir_pelicula(categoria, titulo, director, año, fecha, hora, imagen, precio)
        lista_Peliculas.CargarXML_Categorias()
        return render_template('editar_peliculas.html',lista_P=lista_Peliculas, lista_pelj = lista_peliculas_json)
    return render_template('nueva_pelicula.html')

@app.route('/editar_categorias', methods = ['POST','GET'])
def editar_categorias():
    if request.method=='POST':
        print("se estan recibiendo datos")
    
    lista_p=retorno_categorias()

    return render_template('editar_categorias.html', lista_p =lista_p)

@app.route('/comprar_voletos', methods = ['POST','GET'])
def comprar_voletos():
    nombre = request.args.get('nombre')
    if request.method=='POST':
        titulo = request.form['titulo']
        sala = request.form['sala']
        voletos = request.form['voletos']
        total = lista_Peliculas.buscar_elemento(titulo)
        columnas = lista_salas.buscar_elemento(sala)
        asientos = int(columnas.asientos)/int(10)
        precio = int(voletos)*int(total.dato.precio)
        ubicacion = lista_salas.buscar_elemento(sala)
        if (int(ubicacion.asientos) > int(voletos)):
            return render_template('Terminacion_Voletos.html', titulo=titulo, sala=sala, voletos=voletos, precio=precio, asientos=asientos, nombre=nombre)
        else:
            mensaje ="cantidad de voletos ingresada no valida"
            return render_template('Compra_Voletos.html' ,lista_P=lista_Peliculas, lista_s = lista_salas, nombre=nombre, mensaje =mensaje)
        
    return render_template('Compra_Voletos.html' ,lista_P=lista_Peliculas, lista_s = lista_salas, nombre=nombre)

@app.route('/terminacion_voletos', methods=['POST','GET'])
def terminacion_voletos():
    nombre = request.args.get('nombre')
    if request.method=='POST':
        titulo = request.form['titulo']
        voletos = request.form['voletos']
        sala = request.form['sala']
        precio = request.form['precio']
        nombre = request.form['nombre']
        nit = request.form['nit']
        direccion = request.form['direccion']
        datos = request.form['datos']
        asientos = request.form['asientos']
        name = nombre
        lugares = int(lista_salas.buscar_elemento(sala).asientos)/10
        numero_boleto = f"#USACIPC2_201901472_{obtener_contador()}"

        if(str(datos) == "Tarjeta"):
            print("slecciono tarjeta")
            tarjetas=lista_tarjetas.buscar_elemento(nombre).tipo
            #Buscar si el cliente tiene una tarjeta registrada
            if (tarjetas):
                print("si tuene una tarjeta asociada")
                decision = comprar_asientos(nombre , sala, asientos)    
                if (decision):
                    #Los asientos seleccionados son unicos
                    objeto = Boletos(titulo, sala, voletos, precio, nombre, nit, direccion, datos, asientos, numero_boleto)
                    lista_clientes.asociar_lista_nativa(nombre, objeto)
                    lista_boletos.append(objeto)
                    incrementar_contador()
                    mensaje="Se registro la compra con exito"
                    return render_template('Opciones_Clientes.html', nombre=name, mensaje= mensaje)
                else:
                    #alguno de los asientos seleccionados ya esta ocupado
                    print("hay datos repetidos")
                    mensaje = "Alguno de los asientos ya esta ocupado"
                    return render_template('Terminacion_Voletos.html', titulo=titulo, sala=sala, voletos=voletos, precio=precio, asientos=lugares, nombre=name, mensaje=mensaje)
                        
            else:
                print("No tiene registrada una tarjeta y selecciono una")
                mensaje = "No tiene registrada una tarjeta y selecciono una"
                return render_template('Terminacion_Voletos.html', titulo=titulo, sala=sala, voletos=voletos, precio=precio, asientos=asientos, nombre=name, mensaje=mensaje)

        elif(str(datos)=="Efectivo"):
            print("Selecciono Efectivo")
            decision = comprar_asientos(nombre , sala, asientos) 
            if (decision):
                objeto = Boletos(titulo, sala, voletos, precio, nombre, nit, direccion, datos, asientos, numero_boleto)
                lista_clientes.asociar_lista_nativa(nombre, objeto)
                lista_boletos.append(objeto)
                incrementar_contador()
                mensaje="Se registro la compra con exito"
                return render_template('Opciones_Clientes.html', nombre=name, mensaje= mensaje)
            else:
                print("hay datos repetidos")
                mensaje = "Alguno de los asientos ya esta ocupado"
                return render_template('Terminacion_Voletos.html', titulo=titulo, sala=sala, voletos=voletos, precio=precio, asientos=lugares, nombre=name, mensaje=mensaje)
                        
                       

       
        
    return render_template('Terminacion_Voletos.html', nombre = nombre)

@app.route('/historial_voletos', methods=['POST','GET'])
def historial_voletos():
    nombre = request.args.get('nombre')
    lista_p=lista_clientes.recorrer_lista_nativa(nombre)
    print(lista_p)

    return render_template('historial_voletos.html', lista_p=lista_p, nombre=nombre)

@app.route('/peliculas_favoritas', methods=['POST','GET'])
def peliculas_favoritas():
    nombre = request.args.get('nombre')
    lista_favorito = lista_clientes.recorrer_lista_circular(nombre)
    if(lista_favorito is None):
        return render_template('peliculas_favoritas.html', nombre=nombre)
    else:
        return render_template('peliculas_favoritas.html', lista_f=lista_favorito, nombre=nombre)

@app.route('/editar_tarjetas', methods=['POST','GET'])
def editar_tarjetas():
    if request.method=='POST':
        titular = request.form['titular']
        print(titular)
        lista_tarjetas.eliminar_tarjetas_por_titular(titular)
        lista_tarjetas.cargar_desde_xml()
        return render_template('editar_tarjetas.html', lista_t=lista_tarjetas, lista_tj=lista_tarjetas_json)
        

    return render_template('editar_tarjetas.html', lista_t=lista_tarjetas, lista_tj=lista_tarjetas_json)


@app.route('/nueva_tarjeta', methods=['POST','GET'])
def nueva_tarjeta():
    nombre = request.args.get('nombre')
    if request.method=='POST':
        tipo = request.form['tipo']
        numero = request.form['numero']
        titular = request.form['titular']
        expiracion = request.form['expiracion']
        lista_tarjetas.agregar_tarjeta_a_xml(tipo, numero ,titular, expiracion)
        lista_tarjetas.cargar_desde_xml()
    return render_template('nueva_tarjeta.html', nombre=nombre)

@app.route('/nueva_tarjeta_administrador', methods=['POST','GET'])
def nueva_tarjeta_administrador():
    if request.method=='POST':
        tipo = request.form['tipo']
        numero = request.form['numero']
        titular = request.form['titular']
        expiracion = request.form['expiracion']
        lista_tarjetas.agregar_tarjeta_a_xml(tipo, numero ,titular, expiracion)
        lista_tarjetas.cargar_desde_xml()
        return render_template('editar_tarjetas.html', lista_t=lista_tarjetas, lista_tj=lista_tarjetas_json)
    return render_template('nueva_tarjeta_administrador.html')


@app.route('/edicion_tarjetas', methods=['POST','GET'])
def edicion_tarjetas():
    nombre = request.args.get('nombre')
    if request.method=='POST':
        tipo = request.form['tipo']
        numero = request.form['numero']
        titular = request.form['titular']
        expiracion = request.form['expiracion']
        anterior = request.form['anterior']
        lista_tarjetas.editar_tarjeta_por_titular(anterior, titular, tipo, numero, expiracion)
        lista_tarjetas.cargar_desde_xml()
        return render_template('editar_tarjetas.html', lista_t=lista_tarjetas, lista_tj=lista_tarjetas_json)


    return render_template('Edicion_Tarjetas.html', lista_t=lista_tarjetas, nombre=nombre)


@app.route('/tu-endpoint', methods=['GET'])
def tu_funcion():
    # Realizar la solicitud a la API
    response = requests.get('https://api.example.com/data')
    # Verificar el código de respuesta
    if response.status_code == 200:
        # Extraer los datos JSON de la respuesta
        json_data = response.json()
        # Devolver una respuesta JSON utilizando jsonify de Flask
        return jsonify(json_data)
    else:
        # Si la solicitud no fue exitosa, devolver un mensaje de error
        return jsonify({'mensaje': 'Error al obtener los datos de la API'})
    
@app.route('/cancelar_voletos', methods=['POST','GET'])
def cancelar_voletos():
    if request.method=='POST':
        asientos = request.form['asientos']
        sala = request.form['sala']
        No_voleto = request.form['voleto']
        nombre = request.form['nombre']
        lista=lista_clientes.recorrer_lista_nativa(nombre)
        eliminar_asientos_Diccionario(nombre, sala, asientos)
        eliminar_boleto_por_No_voleto(No_voleto, lista)
        eliminar_boleto_por_No_voleto(No_voleto, lista_boletos)
        return render_template('Cancelar_Voletos.html', lisra_vl = lista_boletos)

    return render_template('Cancelar_Voletos.html', lisra_vl = lista_boletos)
    
    
def comprar_asientos(nombre, sala, asientos):
    asientos = asientos.split(",")
    salas = lista_clientes.recorrer_lista_voletos_guardados(nombre)
    if sala in salas:
        asientos_comprados = salas[sala]
        for asiento in asientos:
            if asiento in asientos_comprados:
                return False  # El asiento ya ha sido comprado
            else:
                asientos_comprados.add(asiento)
    else:
        salas[sala] = set(asientos)
    return True  # Los asientos se han comprado correctamente


def eliminar_asientos_Diccionario(nombre, sala, asientos):
    asientos = asientos.split(",")
    salas = lista_clientes.recorrer_lista_voletos_guardados(nombre)
    if sala in salas:
        asientos_comprados = salas[sala]
        for asiento in asientos:
            if asiento.strip() in asientos_comprados:
                asientos_comprados.remove(asiento.strip())


def eliminar_boleto_por_No_voleto(No_voleto, lista_boleto):
    for boleto in lista_boleto:
        if boleto.No_voleto == No_voleto:
            lista_boleto.remove(boleto)
            return True

    return False 

def retorno_categorias():
    print("Metodo para obtener solo las categorias")
    peliculas = lista_Peliculas
    categorias_unicas = set()
    for pelicula in peliculas:
        categorias_unicas.add(pelicula.categoria)

    for categoria in categorias_unicas:
        print(categoria)
        return editar_categorias

    

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)








    
