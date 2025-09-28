import re
import sqlite3
import datetime

Mensajes = {
    'USUARIO_EXITO_AGREGAR'                   : 'Usuario agregado exitosamente.',
    'USUARIO_EXITO_MODIFICAR'                   : 'Usuario modificado exitosamente.',
    'USUARIO_EXITO_ELIMINAR'                   : 'Usuario eliminado exitosamente.',
    'USUARIO_ERROR_USERNAME'                   : 'Error: Usuario duplicado.',
    
    'PRODUCTO_EXITO_AGREGAR'                  : 'Producto agregado exitosamente.',
    'PRODUCTO_EXITO_MODIFICAR'                : 'Producto modificado exitosamente.',
    'PRODUCTO_EXITO_ELIMINAR'                 : 'Producto eliminado exitosamente.',
    'PRODUCTO_ERROR_TIPO'                     : 'Error: El tipo solo puede contener letras, números, espacios y guiones.',
    'PRODUCTO_ERROR_NOMBRE'                   : 'Error: El nombre solo puede contener letras, números, espacios y guiones.',
    'PRODUCTO_ERROR_MODELO'                   : 'Error: El modelo solo puede contener letras, números, espacios y guiones.',
    'PRODUCTO_ERROR_DUPLICADO'                : 'Error: Ya existe un producto con ese nombre y modelo.',
    'PRODUCTO_ERROR_MEDIDAS'                  : 'Error: Las medidas deben tener el formato AxBxC, donde A, B y C son números entre 1 y 4 dígitos.',
    'PRODUCTO_ERROR_NOENCONTRADO'             : 'Error: Producto no encontrado.',
    
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
    'FABRICACION_ERROR_PRODUCTO_DUPLICADO'    : 'Error: No se pueden agregar productos duplicados en la misma fabricación.',

    'FACTURAS_EXITO_AGREGAR'                  : 'Factura agregada exitosamente.',
    'FACTURAS_ERROR_PRODUCTO_DUPLICADO'       : 'Error: No se pueden agregar productos duplicados en la misma factura.',
    'FACTURAS_ERROR_CANTIDAD'                 : 'Error: La cantidad debe ser un número positivo.',
    'FACTURAS_ERROR_PRECIO'                   : 'Error: El precio debe ser un número positivo.',
}

UNIDADES = {
    'm'  : 'Metro (m)',
    'm2' : 'Metro cuadrado (m²)',
    'm3' : 'Metro cúbico (m³)',
    'kg' : 'Kilogramo (kg)',
    'l'  : 'Litro (l)',
    'u'  : 'Unidad (u)'
}

def Tiempo():
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

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

def Validar_Cantidad(cantidad, minimo=1):
    try:
        valor = float(cantidad)
        
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

class Usuario:
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
            query = self.DB.execute('SELECT seq + 1 FROM sqlite_sequence WHERE name = "usuarios"').fetchone()[0]

        except TypeError:
            return 1
        
        return query

    def get(self, username):
        self.CUR.execute('SELECT FROM usuarios WHERE username = ?',
                         (username))
        
        return self.CUR.fetchone()

    def add(self, username, password, nombres, rol):
        try:
            self.CUR.execute('''INSERT INTO usuarios (username, password, nombres, rol)
                             VALUES (?, ?, ?, ?)''', (username, password, nombres, rol))
            self.DB.commit()

            return Mensajes['USUARIO_EXITO_AGREGAR']

        except sqlite3.IntegrityError:
            return Mensajes['USUARIO_ERROR_USERNAME']

    def set(self, id, username, password, nombres, rol):
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
            query = self.DB.execute('SELECT seq + 1 FROM sqlite_sequence WHERE name = "productos"').fetchone()[0]

        except TypeError:
            return 1
        
        return query

    def set(self, id, tipo, nombre, modelo, estilo, medidas, precio_venta):
        self.CUR.execute('UPDATE productos SET tipo = ?, nombre = ?, modelo = ?, estilo = ?, medidas = ?, precio_venta = ? WHERE id = ?',
                             (tipo, nombre, modelo, estilo, medidas, precio_venta, id))
        self.DB.commit()

        return Mensajes['PRODUCTO_EXITO_MODIFICAR']

    def add(self, tipo, nombre, modelo, estilo, medidas, precio_venta):
        self.CUR.execute('INSERT INTO productos (tipo, nombre, modelo, estilo, medidas, precio_venta) VALUES (?,?,?,?,?,?)',
                         (tipo, nombre, modelo, estilo, medidas, precio_venta))
        self.DB.commit()

        return Mensajes['PRODUCTO_EXITO_MODIFICAR']

    def delete(self, id):
        self.CUR.execute('UPDATE productos SET habilitado = 0 WHERE id = ?',
                         (id,))
        self.DB.commit()

        return Mensajes['PRODUCTO_EXITO_ELIMINAR']


class Componentes:
    def __init__(self, DB):
        self.DB = DB
    
    def Consultar(self):
        return self.DB.execute('SELECT * FROM componentes WHERE habilitado != 0').fetchall()
    
    def Consultar_Siguiente_ID(self):
        try:
            resultado = self.DB.execute('SELECT seq + 1 FROM sqlite_sequence WHERE name = "componentes"').fetchone()[0]

        except TypeError:
            return 1
        
        return resultado
    
    def Consultar_Formateado(self):
        resultado = self.DB.execute('SELECT * FROM componentes WHERE habilitado != 0').fetchall()
        return {fila[0] : f'{fila[1]} ({fila[2]})' for fila in resultado}
    
    def Seleccionar(self, id):
        return self.DB.execute('SELECT * FROM componentes WHERE id = ?', (id,)).fetchone()[0]
    
    def Agregar(self, nombre, unidad):
        if not Validar_Texto(nombre):
            return Mensajes['COMPONENTE_ERROR_NOMBRE']
        
        if not Validar_Unidad(unidad):
            return Mensajes['COMPONENTE_ERROR_UNIDAD']

        if not Validar_Duplicado(self.DB, 'componentes', 'nombre', nombre):
            return Mensajes['COMPONENTE_ERROR_DUPLICADO']
        
        self.DB.execute('INSERT INTO componentes (nombre, unidad) VALUES (?, ?)', (nombre, unidad))
        self.DB.commit()
        
        return Mensajes['COMPONENTE_EXITO_AGREGAR']
    
    def Modificar(self, id, nombre, unidad):
        if not Validar_Texto(nombre):
            return Mensajes['COMPONENTE_ERROR_NOMBRE']
        
        if not Validar_Unidad(unidad):
            return Mensajes['COMPONENTE_ERROR_UNIDAD']
        
        self.DB.execute('UPDATE componentes SET nombre = ?, unidad = ? WHERE id = ?', (nombre, unidad, id))
        self.DB.commit()
        
        return Mensajes['COMPONENTE_EXITO_MODIFICAR']
    
    def Eliminar(self, id):
        self.DB.execute('UPDATE componentes SET habilitado = 0 WHERE id = ?', (id,))
        self.DB.commit()
        
        return Mensajes['COMPONENTE_EXITO_ELIMINAR']
    
    
class Componentes_Por_Producto:
    def __init__(self, DB):
        self.DB = DB

    def Consultar(self):
        return self.DB.execute('SELECT * FROM componentes_por_producto').fetchall()

    def Consultar_Siguiente_ID(self):
        try:
            resultado = self.DB.execute('SELECT seq + 1 FROM sqlite_sequence WHERE name = "componentes_por_producto"').fetchone()[0]

        except TypeError:
            return 1
        
        return resultado

    def Seleccionar(self, id):
        return self.DB.execute('SELECT * FROM componentes_por_producto WHERE id = ?', (id,)).fetchone()

    def Agregar(self, id_producto, id_componente, cantidad):
        if not Validar_Cantidad(cantidad):
            return Mensajes['COMPONENTE-POR-PRODUCTO_ERROR_CANTIDAD']
        
        self.DB.execute(f'INSERT INTO componentes_por_producto (id_producto, id_componente, cantidad) VALUES (?, ?, ?)', (id_producto, id_componente, cantidad))
        self.DB.commit()
        
        return Mensajes['COMPONENTE-POR-PRODUCTO_EXITO_AGREGAR']

    def Modificar(self, id, id_producto, nombre, medidas, cantidad):
        if not Validar_Texto(nombre):
            return 'Error: El nombre solo puede contener letras, números, espacios y guiones.'
        
        self.DB.execute('UPDATE componentes_por_producto SET id_producto = ?, nombre = ?, medidas = ?, cantidad = ? WHERE id = ?', (id_producto, nombre, medidas, cantidad, id))
        self.DB.commit()
        
        return Mensajes['COMPONENTE_EXITO_MODIFICAR']

    def Eliminar(self, id):
        self.DB.execute('DELETE FROM componentes_por_producto WHERE id = ?', (id,))
        self.DB.commit()
        return Mensajes['COMPONENTE_EXITO_ELIMINAR']

class Stock:
    def __init__(self, DB):
        self.DB = DB

    def Consultar(self):
        return self.DB.execute('SELECT id, tipo_item, id_item, cantidad FROM stock').fetchall()

    def Consultar_Siguiente_ID(self):
        try:
            resultado = self.DB.execute('SELECT seq + 1 FROM sqlite_sequence WHERE name = "stock"').fetchone()[0]

        except TypeError:
            return 1
        
        return resultado

    def Agregar(self, id_item, tipo_item, cantidad):
        if not Validar_Item(self.DB, tipo_item, id_item):
            return Mensajes['STOCK_ERROR_ITEM']

        if not Validar_Stock(self.DB, tipo_item, id_item):
            return Mensajes['STOCK_ERROR_ITEM']

        if not Validar_Cantidad(cantidad, minimo=0):
            return Mensajes['STOCK_ERROR_CANTIDAD']
        
        self.DB.execute(f'INSERT INTO stock (id_item, tipo_item, cantidad) VALUES (?, ?, ?)', (id_item, tipo_item, cantidad))
        self.DB.commit()
        
        return 'Stock agregado exitosamente.'

    def Agregar_Fabricacion(self, id_items, cantidades):
        for i in range(len(id_items)):
            if not Validar_Item(self.DB, 'Producto', id_items[i]):
                return Mensajes['STOCK_ERROR_ITEM']

            if not Validar_Cantidad(cantidades[i], minimo=0):
                return Mensajes['STOCK_ERROR_CANTIDAD']
        
            self.DB.execute(f'UPDATE stock SET cantidad = cantidad + ? WHERE id_item = ? AND tipo_item = "Producto"', (cantidades[i], id_items[i]))
        
        self.DB.commit()
        
        return 'Stock actualizado exitosamente.'

    def Modificar(self, id, cantidad):
        if not Validar_Cantidad(cantidad):
            return Mensajes['STOCK_ERROR_CANTIDAD']
        
        self.DB.execute('UPDATE stock SET cantidad = ? WHERE id = ?', (cantidad, id))
        self.DB.commit()
        
        return Mensajes['STOCK_EXITO_MODIFICAR']

    def Facturar(self, id_items, cantidades):
        for i in range(len(id_items)):
            if not Validar_Item(self.DB, 'Producto', id_items[i]):
                return Mensajes['STOCK_ERROR_ITEM']

            if not Validar_Cantidad(cantidades[i], minimo=0):
                return Mensajes['STOCK_ERROR_CANTIDAD']
        
            self.DB.execute(f'UPDATE stock SET cantidad = cantidad - ? WHERE id_item = ? AND tipo_item = "Producto"', (cantidades[i], id_items[i]))
        
        self.DB.commit()
        
        return 'Stock actualizado exitosamente.'

class Fabricaciones:
    def __init__(self, DB):
        self.DB = DB

    def Consultar(self):
        consulta = '''\
            SELECT
                cab.fecha,
                GROUP_CONCAT(
                    det.id_producto || ':' ||
                    det.cantidad || ',' ||
                    det.precio_costo || ',' ||
                    det.precio_venta
                    , ';')
            FROM fabricaciones_encabezado cab
            JOIN fabricaciones_detalle det ON det.id_encabezado = cab.id
            GROUP BY cab.fecha'''

        fabricaciones = self.DB.execute(consulta).fetchall()
        fabricacionesLista = {}

        for fechas, productos in fabricaciones:
            fecha = {}

            for producto in productos.split(';'):
                id_producto_str, valores_str = producto.split(':')
                id_producto = int(id_producto_str)
                valores = [float(valor) if '.' in valor else int(valor) for valor in valores_str.split(',')]
                fecha[id_producto] = valores

            fabricacionesLista[fechas] = fecha

        return fabricacionesLista
        

    def Consultar_Siguiente_ID(self):
        try:
            resultado = self.DB.execute('SELECT seq + 1 FROM sqlite_sequence WHERE name = "fabricaciones"').fetchone()[0]

        except TypeError:
            return 1
        
        return resultado

    def Agregar(self, fecha, productos, cantidades, costos, ventas):
        if len(productos) != len(set(productos)):
            return Mensajes['FABRICACION_ERROR_PRODUCTO_DUPLICADO']
        
        row = self.DB.execute('SELECT id FROM fabricaciones_encabezado WHERE fecha = ?', (fecha,)).fetchone()

        if row:
            id_encabezado = row[0]

        else:
            id_encabezado = self.DB.execute('INSERT INTO fabricaciones_encabezado (fecha) VALUES (?)', (fecha,)).lastrowid

        for i in range(len(productos)):
            self.DB.execute(f'INSERT INTO fabricaciones_detalle (id_encabezado, id_producto, cantidad, precio_costo, precio_venta) VALUES ({id_encabezado}, {productos[i]}, {cantidades[i]}, {costos[i]}, {ventas[i]})')
        
        self.DB.commit()
        
        return Mensajes['FABRICACION_EXITO_AGREGAR']

    def Modificar(self, id, id_producto, cantidad, costo, precio_venta):
        if not Validar_Cantidad(cantidad):
            return Mensajes['FABRICACION_ERROR_CANTIDAD']
        
        self.DB.execute('UPDATE fabricaciones SET id_producto = ?, cantidad = ?, costo = ?, precio_venta = ? WHERE id = ?', (id_producto, cantidad, costo, precio_venta, id))
        self.DB.commit()
        
        return Mensajes['FABRICACION_EXITO_MODIFICAR']

class Facturas:
    def __init__(self, DB):
        self.DB = DB

    def Consultar(self):
        consulta = '''\
            SELECT
                cab.id,
                cab.fecha,
                cab.cliente,
                GROUP_CONCAT(
                det.id_producto || ',' ||
                det.cantidad || ',' ||
                det.precio
                , ';')
            FROM facturas_encabezado cab
            JOIN facturas_detalle det ON det.id_encabezado = cab.id
            GROUP BY cab.id'''

        facturas = self.DB.execute(consulta).fetchall()
        facturasLista = {}

        for id_factura, fecha, cliente, productos in facturas:
            factura = {
                'fecha': fecha,
                'cliente': cliente,
                'productos': []
            }

            for producto in productos.split(';'):
                id_producto, cantidad, precio = producto.split(',')
                factura['productos'].append({
                    'id_producto': int(id_producto),
                    'cantidad': int(cantidad),
                    'precio': float(precio)
                })
            facturasLista[id_factura] = factura
            

        print(facturasLista)
        return facturasLista

    def Consultar_Siguiente(self):
        try:
            resultado = self.DB.execute('SELECT seq + 1 FROM sqlite_sequence WHERE name = "facturas_encabezado"').fetchone()[0]

        except TypeError:
            return 1
        
        return resultado

    def Agregar(self, fecha, cliente, productos, cantidades, precios):
        if len(productos) != len(set(productos)):
            return Mensajes['FACTURAS_ERROR_PRODUCTO_DUPLICADO']

        for cantidad in cantidades:
            if not Validar_Cantidad(cantidad):
                return Mensajes['FACTURAS_ERROR_CANTIDAD']

        for precio in precios:
            if not Validar_Cantidad(precio):
                return Mensajes['FACTURAS_ERROR_PRECIO']

        id_encabezado = self.DB.execute('INSERT INTO facturas_encabezado (fecha, cliente) VALUES (?, ?)', (fecha, cliente,)).lastrowid

        for i in range(len(productos)):
            self.DB.execute(f'INSERT INTO facturas_detalle (id_encabezado, id_producto, cantidad, precio) VALUES ({id_encabezado}, {productos[i]}, {cantidades[i]}, {precios[i]})')

        self.DB.commit()
        return Mensajes['FACTURAS_EXITO_AGREGAR']