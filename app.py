import sqlite3
from flask import Flask, render_template, url_for, redirect
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
def Inyectar_Datos():
    DB = Get_DB()
    Productos = fun.Productos(DB)
    Componentes = fun.Componentes(DB)
    Componentes_Por_Producto = fun.Componentes_Por_Producto(DB)
    Stock = fun.Stock(DB)
    Fabricaciones = fun.Fabricaciones(DB)
    
    return dict(
        productosLista = Productos.Consultar(),
        productosTipos = Productos.Consultar_Tipos(),
        productoSiguiente = Productos.Consultar_Siguiente_ID(),
        productosFormateados = Productos.Consultar_Formateado(),

        componentesLista = Componentes.Consultar(),
        componenteSiguiente = Componentes.Consultar_Siguiente_ID(),
        componentesFormateados = Componentes.Consultar_Formateado(),
        componentesUnidades = fun.UNIDADES,
        
        componentesPorProductoLista = Componentes_Por_Producto.Consultar(),
        componentesPorProductoSiguiente = Componentes_Por_Producto.Consultar_Siguiente_ID(),
        
        stockLista = Stock.Consultar(),

        fabricacionesLista = Fabricaciones.Consultar(),
        fabricacionSiguiente = Fabricaciones.Consultar_Siguiente_ID(),
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

with APP.app_context():
    Init_DB()

if __name__ == '__main__':
    # APP.config['SECRET_KEY'] = 'bdpq'
    APP.run(debug=True)