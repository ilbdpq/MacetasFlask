import sqlite3
from flask import Flask, render_template, url_for, redirect, session, send_from_directory
from flask import request
from flask import g
import datetime
import os

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
    Producto = fun.Producto(DB)
    Componente = fun.Componente(DB)
    Componente_Por_Producto = fun.Componente_Por_Producto(DB)
    Stock = fun.Stock(DB)
    Fabricacion = fun.Fabricacion(DB)
    Factura = fun.Factura(DB)
    Informe = fun.Informe(DB)
    
    return dict(
        titulo = 'Macetas S.A.',
        fechaHoy = fun.FechaHoy(),
        fechaAnterior = fun.FechaAnterior(),
        fechaSiguiente = fun.FechaSiguiente(),
        
        roles = Usuario.getRoles(),
        usuarios = Usuario.getAll(),
        usuario_siguiente = Usuario.getNext(),

        productos_habilitados = Producto.getEnabled(),
        producto_siguiente = Producto.getNext(),
        productos_lista = Producto.getList(),

        unidades = Componente.getUnidades(),
        componentes_habilitados = Componente.getEnabled(),
        componente_siguiente = Componente.getNext(),
        componentes_lista = Componente.getList(),
        componentes_por_producto_habilitados = Componente_Por_Producto.getEnabled(),
        componente_por_producto_siguiente = Componente_Por_Producto.getNext(),

        stock = Stock.getAll(),

        fabricaciones = Fabricacion.getAll(),
        fabricacion_siguiente = Fabricacion.getNext(),

        facturas = Factura.getAll(),
        factura_siguiente = Factura.getNext(),

        informe_fabricaciones_producto = Informe.Fabricaciones_Producto(),
        informe_ventas_producto = Informe.Ventas_Producto(),
        informe_registros = Informe.Registros(),
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
        if session['sesion'] == 'Administrador':
            return render_template('index.html')

        else:
            return redirect(url_for('Template_Login'))

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
        session['sesion'] = 'Administrador'
        session['mensajes'] = []
        session.permanent = True
        return redirect(url_for('Index'))

    else:
        return redirect(url_for('Template_Login'))

@APP.route('/logout', methods=['POST'])
def Logout():
    session.pop('sesion', None)
    return redirect(url_for('Template_Login'))

'''
Usuarios
'''
@APP.route('/usuarios/', methods=['GET'])
def Template_Usuarios():    
    try:
        session['mensajes']

    except KeyError:
        session['mensajes'] = []
        
    return render_template('/usuarios.html', mensajes=session['mensajes'])

@APP.route('/usuarios/modificar/', methods=['POST'])
def Modificar_Usuario():
    id = request.form['id']
    username = request.form['username']
    password = request.form['password']
    nombres = request.form['nombres']
    rol = request.form['rol']

    Usuario = fun.Usuario(Get_DB())
    session['mensajes'] = [fun.Tiempo(), Usuario.set(id=id, username=username, password=password, nombres=nombres, rol=rol)]
    return redirect(url_for('Template_Usuarios'))
        
@APP.route('/usuarios/eliminar/', methods=['POST'])
def Eliminar_Usuario():
    id = request.form['id']

    Usuario = fun.Usuario(Get_DB())
    session['mensajes'] = [fun.Tiempo(), Usuario.delete(id=id)]

    return redirect(url_for('Template_Usuarios'))

@APP.route('/usuarios/agregar/', methods=['POST'])
def Agregar_Usuario():
    username = request.form['username']
    password = request.form['password']
    nombres = request.form['nombres']
    rol = request.form['rol']

    Usuario = fun.Usuario(Get_DB())
    session['mensajes'] = [fun.Tiempo(), Usuario.add(username=username, password=password, nombres=nombres, rol=rol)]

    return redirect(url_for('Template_Usuarios'))

'''
Productos
'''
@APP.route('/productos/', methods=['GET'])
def Template_Productos():    
    try:
        session['mensajes']

    except KeyError:
        session['mensajes'] = []
        
    return render_template('/productos.html', mensajes=session['mensajes'])

@APP.route('/productos/modificar/', methods=['POST'])
def Modificar_Producto():
    id = request.form['id']
    tipo = request.form['tipo']
    nombre = request.form['nombre']
    modelo = request.form['modelo']
    estilo = request.form['estilo']
    medidas = request.form['medidas']
    precio_venta = request.form['precio_venta']

    Producto = fun.Producto(Get_DB())
    session['mensajes'] = [fun.Tiempo(), Producto.set(id, tipo, nombre, modelo, estilo, medidas, precio_venta)]

    return redirect(url_for('Template_Productos'))

@APP.route('/productos/eliminar/', methods=['POST'])
def Eliminar_Producto():
    id = request.form['id']

    Producto = fun.Producto(Get_DB())
    session['mensajes'] = [fun.Tiempo(), Producto.delete(id=id)]
    
    return redirect(url_for('Template_Productos'))

@APP.route('/productos/agregar/', methods=['POST'])
def Agregar_Producto():
    tipo = request.form['tipo']
    nombre = request.form['nombre']
    modelo = request.form['modelo']
    estilo = request.form['estilo']
    medidas = request.form['medidas']
    precio_venta = request.form['precio_venta']

    Producto = fun.Producto(Get_DB())
    session['mensajes'] = [fun.Tiempo(), Producto.add(tipo, nombre, modelo, estilo, medidas, precio_venta)]

    return redirect(url_for('Template_Productos'))

'''
Componentes
'''
@APP.route('/componentes/', methods=['GET'])
def Template_Componentes():    
    try:
        session['mensajes']

    except KeyError:
        session['mensajes'] = []
        
    return render_template('/componentes.html', mensajes=session['mensajes'])

@APP.route('/componentes/modificar/', methods=['POST'])
def Modificar_Componente():
    id = request.form['id']
    nombre = request.form['nombre']
    unidad = request.form['unidad']
    precio_costo = request.form['precio_costo']

    Componente = fun.Componente(Get_DB())
    session['mensajes'] = [fun.Tiempo(), Componente.set(id, nombre, unidad, precio_costo)]

    return redirect(url_for('Template_Componentes'))

@APP.route('/componentes/eliminar/', methods=['POST'])
def Eliminar_Componente():
    id = request.form['id']

    Componente = fun.Componente(Get_DB())
    session['mensajes'] = [fun.Tiempo(), Componente.delete(id)]

    return redirect(url_for('Template_Componentes'))

@APP.route('/componentes/agregar/', methods=['POST'])
def Agregar_Componente():
    nombre = request.form['nombre']
    unidad = request.form['unidad']
    precio_costo = request.form['precio_costo']

    Componente = fun.Componente(Get_DB())
    session['mensajes'] = [fun.Tiempo(), Componente.add(nombre, unidad, precio_costo)]

    return redirect(url_for('Template_Componentes'))

@APP.route('/componentes/por-producto/modificar/', methods=['POST'])
def Modificar_Componente_Por_Producto():
    id = request.form['id']
    id_producto = request.form['id_producto']
    id_componente = request.form['id_componente']
    cantidad = request.form['cantidad']

    Componente_Por_Producto = fun.Componente_Por_Producto(Get_DB())
    session['mensajes'] = [fun.Tiempo(), Componente_Por_Producto.set(id, id_producto, id_componente, cantidad)]

    return redirect(url_for('Template_Componentes'))

@APP.route('/componentes/por-producto/eliminar/', methods=['POST'])
def Eliminar_Componente_Por_Producto():
    id = request.form['id']

    Componente_Por_Producto = fun.Componente_Por_Producto(Get_DB())
    session['mensajes'] = [fun.Tiempo(), Componente_Por_Producto.delete(id)]

    return redirect(url_for('Template_Componentes'))

@APP.route('/componentes/por-producto/agregar/', methods=['POST'])
def Agregar_Componente_Por_Producto():
    id_producto = request.form['id_producto']
    id_componente = request.form['id_componente']
    cantidad = request.form['cantidad']

    Componente_Por_Producto = fun.Componente_Por_Producto(Get_DB())
    session['mensajes'] = [fun.Tiempo(), Componente_Por_Producto.add(id_producto, id_componente, cantidad)]

    return redirect(url_for('Template_Componentes'))

'''
Stock
'''
@APP.route('/stock/', methods=['GET'])
def Template_Stock():
    try:
        session['mensajes']

    except KeyError:
        session['mensajes'] = []
        
    return render_template('/stock.html', mensajes=session['mensajes'])

@APP.route('/stock/modificar/', methods=['POST'])
def Modificar_Stock():
    id = request.form['id']
    cantidad = request.form['cantidad']

    Stock = fun.Stock(Get_DB())
    session['mensajes'] = [fun.Tiempo(), Stock.set(id, cantidad)]

    return redirect(url_for('Template_Stock'))

@APP.route('/stock/agregar/', methods=['POST'])
def Agregar_Stock():
    item = request.form['item']
    cantidad = request.form['cantidad']

    tipo_item, id_item = item.split(',')

    Stock = fun.Stock(Get_DB())
    session['mensajes'] = [fun.Tiempo(), Stock.add(tipo_item, id_item, cantidad)]

    return redirect(url_for('Template_Stock'))

'''
Fabricaciones
'''
@APP.route('/fabricaciones/', methods=['GET'])
def Template_Fabricaciones():
    try:
        session['mensajes']

    except KeyError:
        session['mensajes'] = []
        
    return render_template('/fabricaciones.html', mensajes=session['mensajes'])

@APP.route('/fabricaciones/agregar/', methods=['POST'])
def Agregar_Fabricacion():
    fecha = request.form['fecha']
    id_productos = request.form.getlist('id_producto')
    cantidades = request.form.getlist('cantidad')
    
    Fabricacion = fun.Fabricacion(Get_DB())
    session['mensajes'] = [fun.Tiempo(), Fabricacion.add(fecha, id_productos, cantidades)]
    
    return redirect(url_for('Template_Fabricaciones'))

'''
Facturas
'''

@APP.route('/facturas/', methods=['GET'])
def Template_Facturas():
    try:
        session['mensajes']

    except KeyError:
        session['mensajes'] = []
        
    return render_template('/facturas.html', mensajes=session['mensajes'])

@APP.route('/facturas/agregar/', methods=['POST'])
def Agregar_Factura():
    fecha = request.form['fecha']
    cliente = request.form['cliente']
    id_productos = request.form.getlist('id_producto')
    cantidades = request.form.getlist('cantidad')
    
    Factura = fun.Factura(Get_DB())
    session['mensajes'] = [fun.Tiempo(), Factura.add(fecha, cliente, id_productos, cantidades)]
    
    return redirect(url_for('Template_Facturas'))

@APP.route('/informes/general/', methods=['GET'])
def Template_Informes_General():
    return render_template('/informes_general.html')

@APP.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(APP.root_path, 'static'), 'favicon.ico', mimetype='image/vnd.microsoft.icon')

with APP.app_context():
    Init_DB()

if __name__ == '__main__':
    APP.config['SECRET_KEY'] = 'bdpq'
    APP.config['PERMANENT_SESSION_LIFETIME'] =  datetime.timedelta(minutes=30)
    APP.run(debug=True)