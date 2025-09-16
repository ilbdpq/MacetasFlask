import sqlite3
from flask import Flask, render_template, url_for
from flask import request
from flask import g

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
def Inyectar_Productos():
    DB = Get_DB()
    Productos = fun.Productos(DB)
    Componentes = fun.Componentes(DB)
    
    return dict(
        productosLista = Productos.Consultar(),
        productosTipos = Productos.Consultar_Tipos(),
        productoSiguiente = Productos.Consultar_Siguiente_ID(),
        productosFormateados = Productos.Consultar_Formateado(),

        componentesLista = Componentes.Consultar(),
        componenteSiguiente = Componentes.Consultar_Siguiente_ID()
    )

'''
Página principal
'''
@APP.route('/')
def Index():
    return render_template('index.html')

'''
Productos
'''
@APP.route('/productos/', methods=['GET'])
def Productos_Consultar():
    return render_template('/productos.html')

@APP.route('/productos/agregar', methods=['GET', 'POST'])
def Productos_Agregar():
    if request.method == 'POST':
        tipo = request.form['tipo_agregar']
        nombre = request.form['nombre_agregar']
        modelo = request.form['modelo_agregar']
        medidas = request.form['medidas_agregar']

        Productos = fun.Productos(Get_DB())

        return render_template('/productos.html', mensaje=Productos.Agregar(tipo, nombre, modelo, medidas))

    return render_template('/productos.html')

@APP.route('/productos/modificar', methods=['POST'])
def Productos_Modificar():
    id = request.form['id_modificar']
    tipo = request.form['tipo_modificar']
    nombre = request.form['nombre_modificar']
    modelo = request.form['modelo_modificar']
    medidas = request.form['medidas_modificar']

    Productos = fun.Productos(Get_DB())

    return render_template('/productos.html', mensaje=Productos.Modificar(id, tipo, nombre, modelo, medidas))

@APP.route('/productos/eliminar', methods=['POST'])
def Productos_Eliminar():
    id = request.form['id_eliminar']
    
    Productos = fun.Productos(Get_DB())

    return render_template('/productos.html', mensaje=Productos.Eliminar(id))

'''
Componentes
'''
@APP.route('/componentes/', methods=['GET'])
def Componentes_Consultar():
    return render_template('/componentes.html')

@APP.route('/componentes/agregar', methods=['POST'])
def Componentes_Agregar():
    if request.method == 'POST':
        producto = request.form['producto_agregar']
        nombre = request.form['nombre_agregar']
        medidas = request.form['medidas_agregar']
        cantidad = request.form['cantidad_agregar']

        Componentes = fun.Componentes(Get_DB())

        return render_template('/componentes.html', mensaje=Componentes.Agregar(producto, nombre, medidas, cantidad))

    return render_template('/componentes.html')

@APP.route('/componentes/modificar', methods=['POST'])
def Componentes_Modificar():
    id = request.form['id_modificar']
    producto = request.form['producto_modificar']
    nombre = request.form['nombre_modificar']
    medidas = request.form['medidas_modificar']
    cantidad = request.form['cantidad_modificar']

    Componentes = fun.Componentes(Get_DB())

    return render_template('/componentes.html', mensaje=Componentes.Modificar(id, producto, nombre, medidas, cantidad))

with APP.app_context():
    Init_DB()

if __name__ == '__main__':
    APP.config['SECRET_KEY'] = 'bdpq'
    APP.run(debug=True)