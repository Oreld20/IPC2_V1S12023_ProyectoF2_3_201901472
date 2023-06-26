from flask import Flask, render_template, url_for, request
from markupsafe import escape #Este import es paraq ocultar los datos importantes ingresados en el url
from lista_enlazada import ListaEnlazada
from lista_doblecircular import ListaDoblementeEnlazadaCircular
from lista_doblenlazada import ListaDoblementeEnlazada
import xml.etree.ElementTree as ET
from clientes import Clientes
lista_clientes = ListaEnlazada()
lista_salas = ListaDoblementeEnlazada()
lista_Peliculas = ListaDoblementeEnlazadaCircular()
lista_Peliculas.CargarXML_Categorias()
lista_salas.CargarXML_salas(1)
objeto = Clientes("administrador","Oreld", "Ardon", "41445281", "eliotorel10@gmail.com", "201901472")
lista_clientes.add(objeto)
contador=1
voletos_comprados=[]



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
        if nodo_usuarios.correo == usuario and nodo_usuarios.contrasena == contrasena:
            if nodo_usuarios.rol == "administrador":
                nombre = nodo_usuarios.nombre
                return render_template('Opciones_Administrador.html',nombre=nombre )
            elif nodo_usuarios.rol == "cliente":
                nombre = nodo_usuarios.nombre
                return render_template('Opciones_Clientes.html',nombre=nombre)
        else:
            error = "Los datos ingresados no existen en el sistema"
            return render_template('Login.html',lista_c = lista_clientes, error = error)
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
    return render_template('Opciones_Clientes.html')


@app.route('/opciones_administrador', methods=['POST','GET'])
def opciones_administrador():
    if request.method == 'POST':
        opcion = request.form['boton']
        if opcion == "Cargar_los_XML":
            lista_clientes.CargarXML(1)
            lista_Peliculas.CargarXML_Categorias()
            lista_salas.CargarXML_salas(1)
            mensaje = "XML's Cargados con exito"
            return render_template('Opciones_Administrador.html',mensaje = mensaje)
    return render_template('Opciones_Administrador.html')


@app.route('/editar_clientes', methods=['POST','GET'])
def editar_clientes():
    if request.method== 'POST':
        opcion = request.form['correo']
        lista_clientes.eliminar_elemento_xml(opcion)
        lista_clientes.CargarXML(1)
        return render_template('Editar_Clientes.html', lista_c = lista_clientes)
    return render_template('Editar_Clientes.html', lista_c = lista_clientes)


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
        return render_template('Editar_Clientes.html', lista_c = lista_clientes)

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
        return render_template('Editar_Clientes.html', lista_c = lista_clientes)
    return render_template('nuevo_cliente.html')

@app.route('/editar_sala', methods = ['POST','GET'])
def editar_sala():
    if request.method=='POST':
        sala = request.form['sala']
        lista_salas.eliminar_sala_nombre(sala)
        lista_salas.CargarXML_salas(1)
        return render_template('editar_salas.html', lista_s = lista_salas)
    return render_template('editar_salas.html', lista_s = lista_salas)

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
        return render_template('editar_salas.html', lista_s = lista_salas)

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
        return render_template('editar_salas.html', lista_s = lista_salas)

    return render_template('nueva_sala.html')

@app.route('/listadopeliculas_cliente', methods = ['POST','GET'])
def listadopeliculas_cliente():
    lista_Peliculas.imprimir_Categoria()
    return render_template('listadopeliculas_cliente.html',lista_P=lista_Peliculas)

@app.route('/editar_peliculas', methods = ['POST','GET'])
def editar_peliculas():
    if request.method=='POST':
        titulo = request.form['titulo']
        lista_Peliculas.eliminar_pelicula_por_titulo(titulo)
        lista_Peliculas.CargarXML_Categorias()
        return render_template('editar_peliculas.html',lista_P=lista_Peliculas)

    return render_template('editar_peliculas.html',lista_P=lista_Peliculas)

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
        return render_template('editar_peliculas.html',lista_P=lista_Peliculas)
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
        return render_template('editar_peliculas.html',lista_P=lista_Peliculas)
    return render_template('nueva_pelicula.html')

@app.route('/editar_categorias', methods = ['POST','GET'])
def editar_categorias():
    return render_template('editar_categorias.html')

@app.route('/comprar_voletos', methods = ['POST','GET'])
def comprar_voletos():
    if request.method=='POST':
        titulo = request.form['titulo']
        sala = request.form['sala']
        voletos = request.form['voletos']
        total = lista_Peliculas.buscar_elemento(titulo)
        columnas = lista_salas.buscar_elemento(sala)
        asientos = int(columnas.asientos)/int(10)
        print(str(asientos))
        print(titulo)
        print(sala)
        print(voletos)
        print(total.dato.precio)
        precio = int(voletos)*int(total.dato.precio)
        
        return render_template('Terminacion_Voletos.html', titulo=titulo, sala=sala, voletos=voletos, precio=precio, asientos=asientos)


    return render_template('Compra_Voletos.html' ,lista_P=lista_Peliculas, lista_s = lista_salas)

@app.route('/terminacion_voletos', methods=['POST','GET'])
def terminacion_voletos():
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
        numero_boleto = f"#USACIPC2_201901472_{contador}"
        objeto = (f"Titulo: {titulo},  Sala: {sala},  No voletos: {voletos},  Monto total: {precio},  Nombre: {nombre},  Nit:  {nit},  Direccion: {direccion},  Datos: {datos},  Aseintos:  {asientos},  No voleto: {numero_boleto}")
        voletos_comprados.append(objeto)
        
        return render_template('historial_voletos.html', historial= voletos_comprados)        


    return render_template('Terminacion_Voletos.html')

@app.route('/historial_voletos', methods=['POST','GET'])
def historial_voletos():
    return render_template('historial_voletos.html', historial= voletos_comprados)

    
