import sqlite3
from flask import Flask, render_template, url_for, redirect, session
from flask import request
from flask import g
import datetime

import funciones as fun

APP = Flask(__name__)
DATABASE = 'database.db'

def Get_DB():
    DB = getattr(g, '_database', None)

    if DB is None:
        DB = g._database = sqlite3.connect(DATABASE)

    return DB

@APP.teardown_appcontext
def Close_DB(exception):
    DB = getattr(g, '_database', None)

    if DB is not None:
        DB.close()

def Init_DB():
    with APP.app_context():
        DB = Get_DB()

        with APP.open_resource('schema.sql', mode='r', encoding='UTF-8') as f:
            DB.cursor().executescript(f.read())

        DB.commit()

@APP.context_processor
def Inyectar_Datos():
    DB = Get_DB()
    Usuario = fun.Usuario(DB)
    
    return dict(
        roles = Usuario.getRoles(),
        usuarios = Usuario.getAll(),
        usuario_siguiente = Usuario.getNext()
    )
    
'''
Página principal
'''
@APP.route('/')
def Index():
    try:
        session['sesion']

    except KeyError:
        return redirect(url_for('Template_Login'))

    else:
        return render_template('index.html')

'''
Login
'''
@APP.route('/login')
def Template_Login():
    return render_template('/login.html')

@APP.route('/login/', methods=['POST'])
def Login():
    username = request.form['username']
    password = request.form['password']

    Usuario = fun.Usuario(Get_DB())
    if Usuario.getRole(username, password) == 'Administrador':
        session['sesion'] = 'admin'
        session.permanent = True
        return redirect(url_for('Index'))

    else:
        return redirect(url_for('Template_Login'))

'''
Usuarios
'''
@APP.route('/usuarios/', methods=['GET'])
def Template_Usuarios():    
    try:
        mensajes = session['mensajes']

    except KeyError:
        mensajes = []
        
    return render_template('/usuarios.html', mensajes=mensajes)

@APP.route('/usuarios/modificar/', methods=['POST'])
def Modificar_Usuario():
    id = request.form['id']
    username = request.form['username']
    password = request.form['password']
    nombres = request.form['nombres']
    rol = request.form['rol']

    Usuario = fun.Usuario(Get_DB())
    session['mensajes'] += [fun.Tiempo(), Usuario.set(id=id, username=username, password=password, nombres=nombres, rol=rol)]
    return redirect(url_for('Template_Usuarios'))
        
@APP.route('/usuarios/eliminar/', methods=['POST'])
def Eliminar_Usuario():
    id = request.form['id']

    Usuario = fun.Usuario(Get_DB())
    session['mensajes'] += [fun.Tiempo(), Usuario.delete(id=id)]

    return redirect(url_for('Template_Usuarios'))

'''
Productos
'''
@APP.route('/productos/', methods=['GET'])
def Productos_Consultar():
    return render_template('/productos.html')

@APP.route('/productos/agregar', methods=['GET', 'POST'])
def Productos_Agregar():
    if request.method == 'POST':
        id = request.form['id_agregar']
        tipo = request.form['tipo_agregar']
        nombre = request.form['nombre_agregar']
        modelo = request.form['modelo_agregar']
        medidas = request.form['medidas_agregar']

        Productos = fun.Productos(Get_DB())
        Stock = fun.Stock(Get_DB())

        return render_template('/productos.html', mensajes=[Productos.Agregar(tipo, nombre, modelo, medidas), Stock.Agregar(id, 'Producto', 0)])

    return render_template('/productos.html')

@APP.route('/productos/modificar', methods=['POST'])
def Productos_Modificar():
    id = request.form['id_modificar']
    tipo = request.form['tipo_modificar']
    nombre = request.form['nombre_modificar']
    modelo = request.form['modelo_modificar']
    medidas = request.form['medidas_modificar']

    Productos = fun.Productos(Get_DB())

    return render_template('/productos.html', mensajes=[Productos.Modificar(id, tipo, nombre, modelo, medidas)])

@APP.route('/productos/eliminar', methods=['POST'])
def Productos_Eliminar():
    id = request.form['id_eliminar']
    
    Productos = fun.Productos(Get_DB())

    return render_template('/productos.html', mensajes=[Productos.Eliminar(id)])

'''
Componentes
'''
@APP.route('/componentes/', methods=['GET'])
def Componentes_Consultar():
    return render_template('/componentes.html')

@APP.route('/componentes/agregar', methods=['POST'])
def Componentes_Agregar():
    if request.method == 'POST':
        id = request.form['id_agregar']
        nombre = request.form['nombre_agregar']
        unidad = request.form['unidad_agregar']

        Componentes = fun.Componentes(Get_DB())
        Stock = fun.Stock(Get_DB())

        return render_template('/componentes.html', mensajes=[Componentes.Agregar(nombre, unidad), Stock.Agregar(id, 'Componente', 0)])

    return render_template('/componentes.html')

@APP.route('/componentes/modificar', methods=['POST'])
def Componentes_Modificar():
    id = request.form['id_modificar']
    nombre = request.form['nombre_modificar']
    unidad = request.form['unidad_modificar']

    Componentes = fun.Componentes(Get_DB())

    return render_template('/componentes.html', mensajes=[Componentes.Modificar(id, nombre, unidad)])

@APP.route('/componentes/eliminar', methods=['POST'])
def Componentes_Eliminar():
    id = request.form['id_eliminar']
    
    Componentes = fun.Componentes(Get_DB())

    return render_template('/componentes.html', mensajes=[Componentes.Eliminar(id)])

@APP.route('/componentes/por-producto/agregar', methods=['POST'])
def Componentes_Por_Producto_Agregar():
    id_producto = request.form['id_producto']
    id_componente = request.form['id_componente']
    cantidad = request.form['cantidad']
    
    Componentes_Por_Producto = fun.Componentes_Por_Producto(Get_DB())
    return render_template('/componentes.html', mensajes=[Componentes_Por_Producto.Agregar(id_producto, id_componente, cantidad)])

@APP.route('/componentes/por-producto/modificar', methods=['POST'])
def Componentes_Por_Producto_Modificar():
    id = request.form['id_modificar']
    id_producto = request.form['id_producto']
    id_componente = request.form['id_componente']
    cantidad = request.form['cantidad']
    
    Componentes_Por_Producto = fun.Componentes_Por_Producto(Get_DB())
    return render_template('/componentes.html', mensajes=[Componentes_Por_Producto.Modificar(id, id_producto, id_componente, cantidad)])

@APP.route('/componentes/por-producto/eliminar', methods=['POST'])
def Componentes_Por_Producto_Eliminar():
    id = request.form['id_eliminar']
    
    Componentes_Por_Producto = fun.Componentes_Por_Producto(Get_DB())
    return render_template('/componentes.html', mensajes=[Componentes_Por_Producto.Eliminar(id)])

'''
Stock
'''
@APP.route('/stock/', methods=['GET'])
def Stock_Consultar():
    return render_template('/stock.html')

@APP.route('/stock/modificar', methods=['POST'])
def Stock_Modificar():
    id = request.form['id_modificar']
    cantidad = request.form['cantidad_modificar']

    Stock = fun.Stock(Get_DB())

    return render_template('/stock.html', mensajes=[Stock.Modificar(id, cantidad)])

'''
Fabricaciones
'''
@APP.route('/fabricaciones/', methods=['GET'])
def Fabricaciones_Consultar():
    return render_template('/fabricaciones.html')

@APP.route('/fabricaciones/agregar', methods=['POST'])
def Fabricaciones_Agregar():
    if request.method == 'POST':
        fecha = request.form['agregar_fecha']
        productos = request.form.getlist('agregar_producto')
        cantidades = request.form.getlist('agregar_cantidad')
        costos = request.form.getlist('agregar_costo')
        ventas = request.form.getlist('agregar_venta')

        Fabricaciones = fun.Fabricaciones(Get_DB())
        Stock = fun.Stock(Get_DB())

        # BUG: El Stock se agrega aunque falle la Fabricación
        # TODO: El Stock de los Componentes debería disminuir

        return render_template('/fabricaciones.html', mensajes=[Fabricaciones.Agregar(fecha, productos, cantidades, costos, ventas), Stock.Agregar_Fabricacion(productos, cantidades)])

    return render_template('/fabricaciones.html')

'''
FACTURAS
'''

@APP.route('/facturas/', methods=['GET'])
def Facturas_Consultar():
    return render_template('/facturas_2.html')

@APP.route('/facturas/agregar', methods=['POST'])
def Facturas_Agregar():
    if request.method == 'POST':
        fecha = request.form['agregar_fecha']
        cliente = request.form['agregar_cliente']
        productos = request.form.getlist('agregar_producto')
        cantidades = request.form.getlist('agregar_cantidad')
        precios = request.form.getlist('agregar_precio')

        Facturas = fun.Facturas(Get_DB())
        Stock = fun.Stock(Get_DB())

        # TODO: El Stock debería disminuir

        return render_template('/facturas.html', mensajes=[Facturas.Agregar(fecha, cliente, productos, cantidades, precios), Stock.Facturar(productos, cantidades)])

    return render_template('/facturas.html')

with APP.app_context():
    Init_DB()

if __name__ == '__main__':
    APP.config['SECRET_KEY'] = 'bdpq'
    APP.config['PERMANENT_SESSION_LIFETIME'] =  datetime.timedelta(minutes=30)
    APP.run(debug=True)