import re
import sqlite3
import datetime

Mensajes = {
    'USUARIO_EXITO_AGREGAR'                   : 'Usuario agregado exitosamente.',
    'USUARIO_EXITO_MODIFICAR'                 : 'Usuario modificado exitosamente.',
    'USUARIO_EXITO_ELIMINAR'                  : 'Usuario eliminado exitosamente.',
    'USUARIO_ERROR_USERNAME_DUPLICADO'        : 'Error: Usuario duplicado.',
    'USUARIO_ERROR_USERNAME'                  : 'Error: El nombre de usuario solo puede contener letras.',
    'USUARIO_ERROR_PASSWORD'                  : 'Error: La contraseña solo puede contener letras y números.',
    'USUARIO_ERROR_NOMBRES'                   : 'Error: Los nombres solo pueden contener letras, números, espacios y guiones.',
    
    'PRODUCTO_EXITO_AGREGAR'                  : 'Producto agregado exitosamente.',
    'PRODUCTO_EXITO_MODIFICAR'                : 'Producto modificado exitosamente.',
    'PRODUCTO_EXITO_ELIMINAR'                 : 'Producto eliminado exitosamente.',
    'PRODUCTO_ERROR_TIPO'                     : 'Error: El tipo solo puede contener letras, números, espacios y guiones.',
    'PRODUCTO_ERROR_NOMBRE'                   : 'Error: El nombre solo puede contener letras, números, espacios y guiones.',
    'PRODUCTO_ERROR_MODELO'                   : 'Error: El modelo solo puede contener letras, números, espacios y guiones.',
    'PRODUCTO_ERROR_DUPLICADO'                : 'Error: Ya existe un producto con ese nombre y modelo.',
    'PRODUCTO_ERROR_MEDIDAS'                  : 'Error: Las medidas deben tener el formato AxBxC, donde A, B y C son números entre 1 y 4 dígitos.',
    'PRODUCTO_ERROR_PRECIO'                   : 'Error: El precio de venta debe ser un número positivo.',
    
    'COMPONENTE_EXITO_AGREGAR'                : 'Componente agregado exitosamente.',
    'COMPONENTE_EXITO_MODIFICAR'              : 'Componente modificado exitosamente.',
    'COMPONENTE_EXITO_ELIMINAR'               : 'Componente eliminado exitosamente.',
    'COMPONENTE_ERROR_NOMBRE'                 : 'Error: El nombre solo puede contener letras, números, espacios y guiones.',
    'COMPONENTE_ERROR_DUPLICADO'              : 'Error: Ya existe un componente con ese nombre.',
    'COMPONENTE_ERROR_UNIDAD'                 : 'Error: Las medidas deben ser "m3" o "kg".',
    'COMPONENTE_ERROR_CANTIDAD'               : 'Error: La cantidad debe ser un número entero.',
    'COMPONENTE_ERROR_NOENCONTRADO'           : 'Error: Componente no encontrado.',
    
    'COMPONENTE-POR-PRODUCTO_EXITO_AGREGAR'   : 'Componente por producto agregado exitosamente.',
    'COMPONENTE-POR-PRODUCTO_EXITO_MODIFICAR' : 'Componente por producto modificado exitosamente.',
    'COMPONENTE-POR-PRODUCTO_EXITO_ELIMINAR'  : 'Componente por producto eliminado exitosamente.',
    'COMPONENTE-POR-PRODUCTO_ERROR_CANTIDAD'  : 'Error: La cantidad debe ser un número positivo.',

    'STOCK_EXITO_MODIFICAR'                   : 'Stock modificado exitosamente.',
    'STOCK_ERROR_ITEM'                        : 'Error: El ítem no existe o ya tiene stock inicializado.',
    'STOCK_ERROR_CANTIDAD'                    : 'Error: La cantidad debe ser cero o un número positivo.',

    'FABRICACION_EXITO_AGREGAR'               : 'Fabricación agregada exitosamente.',
    'FABRICACION_EXITO_MODIFICAR'             : 'Fabricación modificada exitosamente.',
    'FABRICACION_ERROR_FECHA'                 : 'Error: La fecha no puede ser anterior a ayer ni posterior a mañana',
    'FABRICACION_ERROR_PRODUCTO_DUPLICADO'    : 'Error: No se pueden agregar productos duplicados en la misma fabricación.',
    'FABRICACION_ERROR_STOCK'                 : 'Error: Stock de componentes insuficiente',

    'FACTURA_EXITO_AGREGAR'                   : 'Factura agregada exitosamente.',
    'FACTURA_ERROR_PRODUCTO_DUPLICADO'        : 'Error: No se pueden agregar productos duplicados en la misma factura.',
    'FACTURA_ERROR_CANTIDAD'                  : 'Error: La cantidad debe ser un número positivo.',
    'FACTURA_ERROR_FECHA'                     : 'Error: La fecha no puede ser anterior a ayer ni posterior a mañana',
    'FACTURA_ERROR_CLIENTE'                   : 'Error: El cliente solo puede contener letras, números, espacios y guiones.',
    'FACTURA_ERROR_STOCK'                     : 'Error: Stock de productos insuficiente',
}

UNIDADES = {
    'kg' : 'Kilogramo(s)',
    'l' : 'Litro(s)',
    'cm' : 'Centímetro(s)',
    'u' : 'Unidad(es)'
}

def Tiempo():
    return datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

def FechaHoy():
    return datetime.datetime.now().strftime('%Y-%m-%d')

def FechaAnterior():
    return (datetime.datetime.now() - datetime.timedelta(days=1)).strftime('%Y-%m-%d')

def FechaSiguiente():
    return (datetime.datetime.now() + datetime.timedelta(days=1)).strftime('%Y-%m-%d')

def Validar_Username(username):
    # Solo letras
    patron = r'^[a-zA-Z]+$'

    if re.match(patron, username):
        return True

    return False

def Validar_Password(password):
    # Solo letras y números
    patron = r'^[a-zA-Z0-9]+$'

    if re.match(patron, password):
        return True

    return False

def Validar_Medidas(medidas):
    # 1 a 4 dígitos x 1 a 4 dígitos x 1 a 4 dígitos (10x20x30)
    patron = r'^\d{1,4}x\d{1,4}x\d{1,4}$'

    if re.match(patron, medidas):
        return True

    return False

def Validar_Texto(texto):
    # Solo letras, números, espacios y guiones
    patron = r'^[a-zA-Z0-9áéíóúÁÉÍÓÚñÑüÜ\s-]+$'

    if re.match(patron, texto):
        return True

    return False

def Validar_Unidad(unidad):
    if unidad in UNIDADES.keys():
        return True
    
    return False

def Validar_Numero(numero, minimo=1):
    try:
        valor = float(numero)
        
        if valor >= minimo:
            return True
        
        return False
    
    except ValueError:
        return False

def Validar_Duplicado(DB, tabla, columna, valor):
    consulta = f'SELECT COUNT(*) FROM {tabla} WHERE {columna} = ? AND habilitado != 0'
    resultado = DB.execute(consulta, (valor,)).fetchone()[0]
    
    if resultado > 0:
        return False
    
    return True

def Validar_Item(DB, tipo_item, id_item):
    if tipo_item not in ['Producto', 'Componente']:
        return False
    
    tabla = 'productos' if tipo_item == 'Producto' else 'componentes'
    consulta = f'SELECT COUNT(*) FROM {tabla} WHERE id = ? AND habilitado != 0'
    resultado = DB.execute(consulta, (id_item,)).fetchone()[0]
    
    if resultado == 0:
        return False
    
    return True

def Validar_Stock(DB, tipo_item, id_item):
    consulta = 'SELECT COUNT(*) FROM stock WHERE tipo_item = ? AND id_item = ?'
    resultado = DB.execute(consulta, (tipo_item, id_item)).fetchone()[0]
    
    if resultado == 0:
        return True
    
    return False

def Validar_Fecha(fecha):
    if datetime.datetime.strptime(FechaAnterior(), '%Y-%m-%d') < datetime.datetime.strptime(fecha, '%Y-%m-%d') < datetime.datetime.strptime(FechaSiguiente(), '%Y-%m-%d'):
        return True
    else:
        return False

def Validar_Fabricacion_Stock(DB, CUR, id_productos, cantidades):
    componentes_necesarios = {}
    
    for id_producto, cantidad in zip(id_productos, cantidades):
        query = CUR.execute(
            '''
            SELECT
                cp.id_componente,
                cp.cantidad * ? AS cantidad_necesaria,
                s.cantidad AS cantidad_disponible
            FROM componentes_por_producto cp
            JOIN stock s ON
            	s.id_item = cp.id_componente
            	AND s.tipo_item = 'Componente'
            WHERE cp.id_producto = ?
            ''', (float(cantidad), int(id_producto))).fetchall()

        componentes_necesarios[int(id_producto)] = {row[0] : [row[1], row[2]] for row in query}

    # componentes_necesarios = {
    #     id_producto : {
    #         id_componente : [cantidad_necesaria, cantidad_disponible]
    #     }
    # }

    # Acumuladores por componente
    necesario_total = {}
    disponible_por_componente = {}

    # Recorrer productos y componentes
    for producto in componentes_necesarios.values():
        for id_componente, (necesaria, disponible) in producto.items():
            necesario_total[id_componente] = necesario_total.get(id_componente, 0) + necesaria
            disponible_por_componente[id_componente] = disponible

    # Verificar si hay suficiente disponibilidad
    for id_componente in necesario_total:
        if disponible_por_componente[id_componente] < necesario_total[id_componente]:
            return False

    return True

def Validar_Factura_Stock(DB, CUR, id_productos, cantidades):
    query = CUR.execute(
        'SELECT cantidad FROM stock WHERE tipo_item = "Producto" AND id_item IN ({0})'.format(', '.join('?' for _ in id_productos)),
        (tuple(id_productos))).fetchall()
    cantidades_actuales = [columna[0] for columna in query]

    for id_producto, cantidad, cantidad_actual in zip(id_productos, cantidades, cantidades_actuales):
        if float(cantidad) > cantidad_actual:
            return False

    return True

class Usuario:
    '''
    usuarios
        id INTEGER PRIMARY KEY AUTOINCREMENT
        username TEXT UNIQUE NOT NULL
        password TEXT NOT NULL
        nombres TEXT NOT NULL
        rol TEXT NOT NULL
    '''

    def __init__(self, DB):
        self.DB = DB
        self.CUR = self.DB.cursor()

    def getAll(self):
        self.CUR.execute('SELECT * FROM usuarios')
        query = self.CUR.fetchall()
        usuarios = {}

        for id, username, password, nombres, rol in query:
            usuario = {
                'username' : username,
                'password' : password,
                'nombres' : nombres,
                'rol' : rol
            }
            usuarios[id] = usuario
        
        return usuarios

    def getRoles(self):
        return ['Administrador', 'Gerente', 'Encargado', 'Operario']

    def getRole(self, username, password):
        self.CUR.execute('''SELECT rol FROM usuarios WHERE username = ? AND password = ?''',
                         (username, password))
        return self.CUR.fetchone()[0]

    def getNext(self):
        try:
            id = self.DB.execute('SELECT seq + 1 FROM sqlite_sequence WHERE name = "usuarios"').fetchone()[0]

        except TypeError:
            return 1
        
        return id

    def get(self, username):
        self.CUR.execute('SELECT FROM usuarios WHERE username = ?',
                         (username))
        
        return self.CUR.fetchone()

    def add(self, username, password, nombres, rol):
        if not Validar_Username(username):
            return Mensajes['USUARIO_ERROR_USERNAME']

        if not Validar_Password(password):
            return Mensajes['USUARIO_ERROR_PASSWORD']

        if not Validar_Texto(nombres):
            return Mensajes['USUARIO_ERROR_NOMBRES']        
        
        try:
            self.CUR.execute('''INSERT INTO usuarios (username, password, nombres, rol)
                             VALUES (?, ?, ?, ?)''', (username, password, nombres, rol))
            self.DB.commit()

            return Mensajes['USUARIO_EXITO_AGREGAR']

        except sqlite3.IntegrityError:
            return Mensajes['USUARIO_ERROR_USERNAME_DUPLICADO']

    def set(self, id, username, password, nombres, rol):
        if not Validar_Username(username):
            return Mensajes['USUARIO_ERROR_USERNAME']

        if not Validar_Password(password):
            return Mensajes['USUARIO_ERROR_PASSWORD']

        if not Validar_Texto(nombres):
            return Mensajes['USUARIO_ERROR_NOMBRES'] 
        
        try:
            self.CUR.execute('''UPDATE usuarios SET password = ?, nombres = ?, rol = ? WHERE id = ?''',
                             (password, nombres, rol, id))
            self.DB.commit()

            return Mensajes['USUARIO_EXITO_MODIFICAR']

        except sqlite3.IntegrityError:
            return Mensajes['USUARIO_ERROR_USERNAME']

    def delete(self, id):
        self.CUR.execute('''DELETE FROM usuarios WHERE id = ?''',
                         (id,))
        self.DB.commit()

        return Mensajes['USUARIO_EXITO_ELIMINAR']

class Producto:
    '''
    productos
        id INTEGER PRIMARY KEY AUTOINCREMENT
        tipo TEXT NOT NULL
        nombre TEXT NOT NULL
        modelo TEXT NOT NULL
        estilo TEXT NOT NULL
        medidas TEXT NOT NULL -- Largo x Ancho x Alto
        precio_venta REAL NOT NULL
        habilitado INTEGER NOT NULL DEFAULT 1
    '''

    def __init__(self, DB):
        self.DB = DB
        self.CUR = self.DB.cursor()
        
    def getAll(self):
        self.CUR.execute('SELECT id, tipo, nombre, modelo, estilo, medidas, printf("%.2f", precio_venta), habilitado FROM productos')
        query = self.CUR.fetchall()
        productos = {}

        for id, tipo, nombre, modelo, estilo, medidas, precio_venta, habilitado in query:
            producto = {
                'tipo' : tipo,
                'nombre' : nombre,
                'modelo' : modelo,
                'estilo' : estilo,
                'medidas' : medidas,
                'precio_venta' : float(precio_venta),
                'habilitado' : habilitado
            }
            productos[id] = producto

        return productos

    def getEnabled(self):
        self.CUR.execute('SELECT id, tipo, nombre, modelo, estilo, medidas, printf("%.2f", precio_venta) FROM productos WHERE habilitado == 1')
        query = self.CUR.fetchall()
        productos = {}

        for id, tipo, nombre, modelo, estilo, medidas, precio_venta in query:
            producto = {
                'tipo' : tipo,
                'nombre' : nombre,
                'modelo' : modelo,
                'estilo' : estilo,
                'medidas' : medidas,
                'precio_venta' : float(precio_venta)
            }
            productos[id] = producto

        return productos

    def getDisabled(self):
        self.CUR.execute('SELECT id, tipo, nombre, modelo, estilo, medidas, printf("%.2f", precio_venta) FROM productos WHERE habilitado == 0')
        query = self.CUR.fetchall()
        productos = {}

        for id, tipo, nombre, modelo, estilo, medidas, precio_venta in query:
            producto = {
                'tipo' : tipo,
                'nombre' : nombre,
                'modelo' : modelo,
                'estilo' : estilo,
                'medidas' : medidas,
                'precio_venta' : float(precio_venta)
            }
            productos[id] = producto

        return productos

    def getNext(self):
        try:
            id = self.DB.execute('SELECT seq + 1 FROM sqlite_sequence WHERE name = "productos"').fetchone()[0]

        except TypeError:
            return 1
        
        return id


    def getList(self):
        self.CUR.execute("SELECT id, tipo || ' ' || nombre || ' ' || modelo FROM productos WHERE habilitado = 1")
        query = self.CUR.fetchall()
        productos = {}

        for id, texto in query:
            productos[id] = texto

        return productos

    def set(self, id, tipo, nombre, modelo, estilo, medidas, precio_venta):
        self.CUR.execute('UPDATE productos SET tipo = ?, nombre = ?, modelo = ?, estilo = ?, medidas = ?, precio_venta = ? WHERE id = ?',
                             (tipo, nombre, modelo, estilo, medidas, precio_venta, id))
        self.DB.commit()

        return Mensajes['PRODUCTO_EXITO_MODIFICAR']

    def add(self, tipo, nombre, modelo, estilo, medidas, precio_venta):
        if not Validar_Texto(nombre):
            return Mensajes['PRODUCTO_ERROR_NOMBRE']

        if not Validar_Texto(tipo):
            return Mensajes['PRODUCTO_ERROR_TIPO']

        if not Validar_Texto(modelo):
            return Mensajes['PRODUCTO_ERROR_MODELO']

        if not Validar_Medidas(medidas):
            return Mensajes['PRODUCTO_ERROR_MEDIDAS']

        if not Validar_Numero(precio_venta, minimo=0):
            return Mensajes['PRODUCTO_ERROR_PRECIO']
        
        self.CUR.execute('INSERT INTO productos (tipo, nombre, modelo, estilo, medidas, precio_venta) VALUES (?,?,?,?,?,?)',
                         (tipo, nombre, modelo, estilo, medidas, precio_venta))
        self.DB.commit()

        return Mensajes['PRODUCTO_EXITO_AGREGAR']

    def delete(self, id):
        self.CUR.execute('UPDATE productos SET habilitado = 0 WHERE id = ?',
                         (id,))
        self.DB.commit()

        return Mensajes['PRODUCTO_EXITO_ELIMINAR']


class Componente:
    '''
    componentes
        id INTEGER PRIMARY KEY AUTOINCREMENT
        nombre TEXT NOT NULL
        unidad TEXT NOT NULL
        precio_costo REAL NOT NULL
        habilitado INTEGER NOT NULL DEFAULT 1
    '''
    
    def __init__(self, DB):
        self.DB = DB
        self.CUR = self.DB.cursor()

    def getUnidades(self):
        unidades = {
            'kg' : 'Kilogramo(s)',
            'l' : 'Litro(s)',
            'cm' : 'Centímetro(s)',
            'u' : 'Unidad(es)'
        }

        return unidades
    
    def getAll(self):
        self.CUR.execute('SELECT id, nombre, unidad, printf("%.2f", precio_costo), habilitado FROM componentes')
        query = self.CUR.fetchall()
        componentes = {}

        for id, nombre, unidad, precio_costo, habilitado in query:
            componente = {
                'nombre' : nombre,
                'unidad' : unidad,
                'precio_costo' : float(precio_costo),
                'habilitado' : habilitado
            }
            componentes[id] = componente

        return componentes

    def getEnabled(self):
        self.CUR.execute('SELECT id, nombre, unidad, printf("%.2f", precio_costo) FROM componentes WHERE habilitado == 1')
        query = self.CUR.fetchall()
        componentes = {}

        for id, nombre, unidad, precio_costo in query:
            componente = {
                'nombre' : nombre,
                'unidad' : unidad,
                'precio_costo' : float(precio_costo)
            }
            componentes[id] = componente

        return componentes

    def getDisabled(self):
        self.CUR.execute('SELECT id, nombre, unidad, printf("%.2f", precio_costo) FROM componentes WHERE habilitado == 0')
        query = self.CUR.fetchall()
        componentes = {}

        for id, nombre, unidad, precio_costo in query:
            componente = {
                'nombre' : nombre,
                'unidad' : unidad,
                'precio_costo' : float(precio_costo)
            }
            componentes[id] = componente

        return componentes

    def getNext(self):
        try:
            id = self.DB.execute('SELECT seq + 1 FROM sqlite_sequence WHERE name = "componentes"').fetchone()[0]

        except TypeError:
            return 1
        
        return id

    def getList(self):
        self.CUR.execute("SELECT id, nombre || ' (' || unidad || ')' FROM componentes WHERE habilitado = 1")
        query = self.CUR.fetchall()
        componentes = {}

        for id, texto in query:
            componentes[id] = texto

        return componentes

    def set(self, id, nombre, unidad, precio_costo):
        self.CUR.execute('UPDATE componentes SET nombre = ?, unidad = ?, precio_costo = ? WHERE id = ?',
                             (nombre, unidad, precio_costo, id))
        self.DB.commit()

        return Mensajes['COMPONENTE_EXITO_MODIFICAR']
        
    def add(self, nombre, unidad, precio_costo):
        self.CUR.execute('INSERT INTO componentes (nombre, unidad, precio_costo) VALUES (?,?,?)',
                         (nombre, unidad, precio_costo))
        self.DB.commit()

        return Mensajes['COMPONENTE_EXITO_AGREGAR']

    def delete(self, id):
        self.CUR.execute('UPDATE componentes SET habilitado = 0 WHERE id = ?',
                         (id,))
        self.DB.commit()

        return Mensajes['COMPONENTE_EXITO_ELIMINAR']
    
class Componente_Por_Producto:
    '''
    componentes_por_producto
        id INTEGER PRIMARY KEY AUTOINCREMENT
        id_producto INTEGER NOT NULL
        id_componente INTEGER NOT NULL
        cantidad REAL NOT NULL
        habilitado INTEGER NOT NULL DEFAULT 1
    '''
    
    def __init__(self, DB):
        self.DB = DB
        self.CUR = self.DB.cursor()

    def getEnabled(self):
        self.CUR.execute('SELECT id, id_producto, id_componente, cantidad FROM componentes_por_producto WHERE habilitado = 1')
        query = self.CUR.fetchall()
        componentes_por_producto = {}

        for id, id_producto, id_componente, cantidad in query:
            componente = {
                'id_producto' : int(id_producto),
                'id_componente' : int(id_componente),
                'cantidad' : float(cantidad)
            }
            componentes_por_producto[id] = componente

        return componentes_por_producto

    def getDisabled(self):
        self.CUR.execute('SELECT id, id_producto, id_componente, cantidad FROM componentes_por_producto WHERE habilitado = 0')
        query = self.CUR.fetchall()
        componentes_por_producto = {}

        for id, id_producto, id_componente, cantidad in query:
            componente = {
                'id_producto' : int(id_producto),
                'id_componente' : int(id_componente),
                'cantidad' : float(cantidad)
            }
            componentes_por_producto[id] = componente

        return componentes_por_producto

    def getNext(self):
        try:
            id = self.DB.execute('SELECT seq + 1 FROM sqlite_sequence WHERE name = "componentes_por_producto"').fetchone()[0]

        except TypeError:
            return 1
        
        return id

    def set(self, id, id_producto, id_componente, cantidad):
        self.CUR.execute('UPDATE componentes_por_producto SET id_producto = ?, id_componente = ?, cantidad = ? WHERE id = ?',
                        (id_producto, id_componente, cantidad, id))
        self.DB.commit()

        return Mensajes['COMPONENTE-POR-PRODUCTO_EXITO_MODIFICAR']

    def delete(self, id):
        self.CUR.execute('UPDATE componentes_por_producto SET habilitado = 0 WHERE id = ?',
                        (id,))
        self.DB.commit()

        return Mensajes['COMPONENTE-POR-PRODUCTO_EXITO_ELIMINAR']

    def add(self, id_producto, id_componente, cantidad):
        self.CUR.execute('INSERT INTO componentes_por_producto (id_producto, id_componente, cantidad) VALUES (?,?,?)',
                        (id_producto, id_componente, cantidad))
        self.DB.commit()

        return Mensajes['COMPONENTE-POR-PRODUCTO_EXITO_AGREGAR']

class Stock:
    '''
    stock
        id INTEGER PRIMARY KEY AUTOINCREMENT
        id_item INTEGER NOT NULL
        tipo_item TEXT NOT NULL
        cantidad REAL NOT NULL
        movimiento TEXT NOT NULL -- ISO8601 YYYY-MM-DD HH:MM:SS
    '''
    
    def __init__(self, DB):
        self.DB = DB
        self.CUR = self.DB.cursor()

    def getAll(self):
        self.CUR.execute('SELECT id, tipo_item, id_item, cantidad, movimiento FROM stock')
        query = self.CUR.fetchall()
        stock = {}
        
        for id, tipo_item, id_item, cantidad, movimiento in query:
            item = {
                'tipo_item' : tipo_item,
                'id_item' : int(id_item),
                'cantidad' : float(cantidad),
                'movimiento' : movimiento
            }
            stock[id] = item

        return stock

    def set(self, id, cantidad):
        self.CUR.execute('UPDATE stock SET cantidad = ?, movimiento = ? WHERE id = ?',
                         (cantidad, Tiempo(), id))
        self.DB.commit()

        return Mensajes['STOCK_EXITO_MODIFICAR']

    def add(self, tipo_item, id_item, cantidad):
        cantidad_actual = self.CUR.execute('SELECT cantidad FROM stock WHERE tipo_item = ? AND id_item = ?',
                                          (tipo_item, id_item)).fetchone()[0]
        
        self.CUR.execute('UPDATE stock SET cantidad = ?, movimiento = ? WHERE tipo_item = ? AND id_item = ?',
                         (round(float(cantidad_actual) + float(cantidad), 2), Tiempo(), tipo_item, id_item))
        self.DB.commit()

        return Mensajes['STOCK_EXITO_MODIFICAR']
    
    def addFabricacion(self, id_productos, cantidades):
        for id_producto, cantidad in zip(id_productos, cantidades):
            self.CUR.execute(
                '''
                WITH cte AS (
                    SELECT
                    cp.id_componente,
                    cp.cantidad * ? AS cantidad_necesaria
                        FROM componentes_por_producto cp
                        JOIN stock s ON
                            s.id_item = cp.id_componente
                            AND s.tipo_item = 'Componente'
                WHERE cp.id_producto = ? )

                UPDATE stock
                SET
                    cantidad = cantidad - (SELECT cantidad_necesaria FROM cte)
                WHERE
                    id_item IN (SELECT id_componente FROM cte)
                    AND tipo_item = "Componente"
                ''', (float(cantidad), int(id_producto))).fetchall()

            self.CUR.execute(
                '''
                UPDATE stock
                SET
                    cantidad = cantidad + ?,
                    movimiento = ?
                WHERE id_item = ? AND tipo_item = "Producto"
                ''', ( float(cantidad), Tiempo(), int(id_producto) )
                )

            self.DB.commit()
        
        return Mensajes['STOCK_EXITO_MODIFICAR']

    def addFactura(self, id_productos, cantidades):
        query = self.CUR.execute(
            'SELECT cantidad FROM stock WHERE tipo_item = "Producto" AND id_item IN ({0})'.format(', '.join('?' for _ in id_productos)),
            (tuple(id_productos))).fetchall()
        cantidades_actuales = [columna[0] for columna in query]
        
        for id_producto, cantidad_actual, cantidad in zip(id_productos, cantidades_actuales, cantidades):
            self.CUR.execute('UPDATE stock SET cantidad = ?, movimiento = ? WHERE tipo_item = "Producto" AND id_item = ?',
                             (round(float(cantidad_actual) - float(cantidad), 2), Tiempo(), id_producto))
        self.DB.commit()
        
        return Mensajes['STOCK_EXITO_MODIFICAR']

class Fabricacion:
    '''
    facturas_encabezado
        id INTEGER PRIMARY KEY AUTOINCREMENT
        fecha TEXT NOT NULL
        cliente TEXT NOT NULL

    facturas_detalle
        id INTEGER PRIMARY KEY AUTOINCREMENT
        id_encabezado INTEGER NOT NULL
        id_producto INTEGER NOT NULL
        cantidad INTEGER NOT NULL
        precio_total REAL NOT NULL
        FOREIGN KEY(id_encabezado) REFERENCES facturas_encabezado(id)
        FOREIGN KEY(id_producto) REFERENCES productos(id)
    '''
    
    def __init__(self, DB):
        self.DB = DB
        self.CUR = self.DB.cursor()

    def getAll(self):
        self.CUR.execute('''
            SELECT
                cab.id,
                cab.fecha,
                GROUP_CONCAT(
                    det.id_producto || ',' ||
                    det.cantidad || ',' ||
                    det.costo_total
                    , ';')
            FROM fabricaciones_encabezado cab
            JOIN fabricaciones_detalle det ON cab.id = det.id_encabezado
            GROUP BY cab.id''')

        query = self.CUR.fetchall()
        fabricaciones = {}

        for id, fecha, productos in query:
            fabricacion = {
                'fecha' : fecha,
                'productos' : {}
            }

            for producto in productos.split(';'):
                id_producto, cantidad, costo_total = producto.split(',')
                producto_dict = {
                    'cantidad' : int(cantidad),
                    'costo_total' : float(costo_total)
                }
                fabricacion['productos'][int(id_producto)] = producto_dict
            fabricaciones[int(id)] = fabricacion

        return fabricaciones
    
    def getNext(self):
        try:
            id = self.DB.execute('SELECT seq + 1 FROM sqlite_sequence WHERE name = "fabricaciones_encabezado"').fetchone()[0]

        except TypeError:
            return 1
        
        return id
    
    def getCostos(self):
        query = self.CUR.execute('''
            SELECT p.id, SUM(c.precio_costo * cp.cantidad)
            FROM productos p
            JOIN componentes_por_producto cp ON cp.id_producto = p.id
            JOIN componentes c ON c.id = cp.id_componente
            GROUP BY p.id''').fetchall()
        
        costos_totales = {}
        for id_producto, costo_total in query:
            costos_totales[id_producto] = costo_total

        return costos_totales
    
    def add(self, fecha, id_productos, cantidades):
        if not Validar_Fecha(fecha):
            return Mensajes['FABRICACION_ERROR_FECHA']

        if len(id_productos) != len(set(id_productos)):
            return Mensajes['FABRICACION_ERROR_PRODUCTO_DUPLICADO']

        if not Validar_Fabricacion_Stock(self.DB, self.CUR, id_productos, cantidades):
            return Mensajes['FABRICACION_ERROR_STOCK']
        
        costos_totales = self.getCostos()
        
        self.CUR.execute('INSERT INTO fabricaciones_encabezado (fecha) VALUES (?)', (fecha,))
        self.DB.commit()
        
        id_encabezado = self.DB.execute('SELECT seq FROM sqlite_sequence WHERE name = "fabricaciones_encabezado"').fetchone()[0]
        
        for id_producto, cantidad in zip(id_productos, cantidades):
            costo_total = costos_totales.get(int(id_producto))
            self.CUR.execute('INSERT INTO fabricaciones_detalle (id_encabezado, id_producto, cantidad, costo_total) VALUES (?,?,?,?)',
                             (id_encabezado, id_producto, cantidad, costo_total))
        self.DB.commit()

        Stock(self.DB).addFabricacion(id_productos, cantidades)
        
        return Mensajes['FABRICACION_EXITO_AGREGAR']

class Factura:
    '''
    facturas_encabezado
        "id" INTEGER NOT NULL
        "fecha" TEXT NOT NULL
        "cliente" TEXT NOT NULL
        PRIMARY KEY ("id")
        
    facturas_detalle
        "id" INTEGER NOT NULL
        "id_encabezado" INTEGER NOT NULL
        "id_producto" INTEGER NOT NULL
        "cantidad" INTEGER NOT NULL
        "precio_total" REAL NOT NULL
        PRIMARY KEY ("id")
    '''

    def __init__(self, DB):
        self.DB = DB
        self.CUR = self.DB.cursor()

    def getAll(self):
        self.CUR.execute('''
            SELECT
                cab.id,
                cab.fecha,
                cab.cliente,
                GROUP_CONCAT(
                    det.id_producto || ',' ||
                    det.cantidad || ',' ||
                    det.precio_total
                    , ';')
            FROM facturas_encabezado cab
            JOIN facturas_detalle det ON cab.id = det.id_encabezado
            GROUP BY cab.id''')

        query = self.CUR.fetchall()
        facturas = {}

        for id, fecha, cliente, productos in query:
            factura = {
                'fecha' : fecha,
                'cliente' : cliente,
                'productos' : {}
            }

            for producto in productos.split(';'):
                id_producto, cantidad, precio_total = producto.split(',')
                producto_dict = {
                    'cantidad' : float(cantidad),
                    'precio_total' : float(precio_total)
                }
                factura['productos'][int(id_producto)] = producto_dict
            facturas[int(id)] = factura

        return facturas

    def getNext(self):
        try:
            id = self.DB.execute('SELECT seq + 1 FROM sqlite_sequence WHERE name = "facturas_encabezado"').fetchone()[0]

        except TypeError:
            return 1
        
        return id

    def getPrecios(self):
        query = self.CUR.execute('''
            SELECT p.id, p.precio_venta
            FROM productos p''').fetchall()
        
        precios_totales = {}
        for id_producto, precio_total in query:
            precios_totales[id_producto] = precio_total

        return precios_totales

    def add(self, fecha, cliente, id_productos, cantidades):
        precios_totales = self.getPrecios()

        if not Validar_Fecha(fecha):
            return Mensajes['FACTURA_ERROR_FECHA']

        if not Validar_Texto(cliente):
            return Mensajes['FACTURA_ERROR_CLIENTE']

        if not Validar_Factura_Stock(self.DB, self.CUR, id_productos, cantidades):
            return Mensajes['FACTURA_ERROR_STOCK']
            
        self.CUR.execute('INSERT INTO facturas_encabezado (fecha, cliente) VALUES (?, ?)', (fecha, cliente))
        self.DB.commit()
        
        id_encabezado = self.DB.execute('SELECT seq FROM sqlite_sequence WHERE name = "facturas_encabezado"').fetchone()[0]
        
        for id_producto, cantidad in zip(id_productos, cantidades):
            precio_total = precios_totales.get(int(id_producto)) * float(cantidad)
            self.CUR.execute('INSERT INTO facturas_detalle (id_encabezado, id_producto, cantidad, precio_total) VALUES (?,?,?,?)',
                             (id_encabezado, id_producto, float(cantidad), round(precio_total, 2)))
        self.DB.commit()

        Stock(self.DB).addFactura(id_productos, cantidades)
        
        return Mensajes['FACTURA_EXITO_AGREGAR']

class Informe:
    def __init__(self, DB):
        self.DB = DB
        self.CUR = self.DB.cursor()

    def Registros(self):
        query = self.CUR.execute(
            '''
            SELECT
                (SELECT COUNT(*) FROM productos WHERE habilitado = 1) AS productos_habilitados,
                (SELECT COUNT(*) FROM productos WHERE habilitado = 0) AS productos_deshabilitados,
                (SELECT COUNT(*) FROM componentes WHERE habilitado = 1) AS componentes_habilitados,
                (SELECT COUNT(*) FROM componentes WHERE habilitado = 0) AS componentes_deshabilitados,
                (SELECT COUNT(*) FROM stock) AS items_stock,
                (SELECT COUNT(*) FROM fabricaciones_encabezado) AS fabricaciones,
                (SELECT COUNT(*) FROM facturas_encabezado) AS facturas
            ''').fetchone()

        registros = {
            'Productos habilitados' : query[0],
            'Productos deshabilitados' : query[1],
            'Componentes habilitados' : query[2],
            'Componentes deshabilitados' : query[3],
            'Items en stock' : query[4],
            'Fabricaciones' : query[5],
            'Facturas' : query[6]
        }

        return registros

    def Fabricaciones_Producto(self):
        query = self.CUR.execute(
            '''
            SELECT
                det.id_producto,
                SUM(det.cantidad)
            FROM fabricaciones_encabezado cab
            JOIN fabricaciones_detalle det ON
                det.id_encabezado = cab.id
            GROUP BY det.id_producto
            ''').fetchall()

        return query
    
    def Ventas_Producto(self):
        query = self.CUR.execute(
            '''
            SELECT
                det.id_producto,
                SUM(det.cantidad)
            FROM facturas_encabezado cab
            JOIN facturas_detalle det ON
                det.id_encabezado = cab.id
            GROUP BY det.id_producto
            ''').fetchall()

        return query