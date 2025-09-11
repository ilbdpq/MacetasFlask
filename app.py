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

@APP.route('/')
def Index():
    return render_template('index.html')

@APP.route('/productos/', methods=['GET'])
def Productos_Consultar():
    print(fun.Productos_Tipos(Get_DB()))
    return render_template('/productos/productos.html', productos=fun.Productos_Tabla(Get_DB()), productosTipos=fun.Productos_Tipos(Get_DB()))

@APP.route('/productos/agregar', methods=['GET', 'POST'])
def Productos_Agregar():
    if request.method == 'POST':
        tipo = request.form['tipo_agregar']
        nombre = request.form['nombre_agregar']
        modelo = request.form['modelo_agregar']
        medidas = request.form['medidas_agregar']

        if not fun.Validar_Medidas(medidas):
            return render_template('/productos/productos.html', mensaje_agregar='Error: Las medidas deben tener el formato AxBxC, donde A, B y C son números entre 1 y 4 dígitos.')

        DB = Get_DB()
        DB.execute('INSERT INTO productos (tipo, nombre, modelo, medidas) VALUES (?, ?, ?, ?)', (tipo, nombre, modelo, medidas))
        DB.commit()

        return render_template('/productos/productos.html', mensaje_agregar='Producto agregado exitosamente.', productos=fun.Productos_Tabla(Get_DB()))

    return render_template('/productos/productos.html', productos=fun.Productos_Tabla(Get_DB()))

@APP.route('/productos/seleccionar', methods=['POST'])
def Productos_Seleccionar():
    id = request.form['id_seleccionar']
    DB = Get_DB()
    producto = DB.execute('SELECT * FROM productos WHERE id = ?', (id,)).fetchone()

    if producto is None:
        return render_template('/productos/productos.html', mensaje_modificar='Error: Producto no encontrado.', productos=fun.Productos_Tabla(Get_DB()))

    return render_template('/productos/productos.html', seleccionado=producto, productos=fun.Productos_Tabla(Get_DB()))

@APP.route('/productos/modificar', methods=['POST'])
def Productos_Modificar():
    id = request.form['id_modificar']
    tipo = request.form['tipo_modificar']
    nombre = request.form['nombre_modificar']
    modelo = request.form['modelo_modificar']
    medidas = request.form['medidas_modificar']

    if not fun.Validar_Medidas(medidas):
        return render_template('/productos/productos.html', mensaje_modificar='Error: Las medidas deben tener el formato AxBxC, donde A, B y C son números entre 1 y 4 dígitos.', productos=fun.Productos_Tabla(Get_DB()))

    DB = Get_DB()
    DB.execute('UPDATE productos SET tipo = ?, nombre = ?, modelo = ?, medidas = ? WHERE id = ?', (tipo, nombre, modelo, medidas, id))
    DB.commit()

    return render_template('/productos/productos.html', mensaje_modificar='Producto modificado exitosamente.', productos=fun.Productos_Tabla(Get_DB()))

@APP.route('/productos/eliminar', methods=['POST'])
def Productos_Eliminar():
    id = request.form['id_modificar']
    DB = Get_DB()
    DB.execute('UPDATE productos SET habilitado = 0 WHERE id = ?', (id,))
    DB.commit()

    return render_template('/productos/productos.html', mensaje_modificar='Producto eliminado exitosamente.', productos=fun.Productos_Tabla(Get_DB()))

if __name__ == '__main__':
    Init_DB()
    APP.run(debug=True)