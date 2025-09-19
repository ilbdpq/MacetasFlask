import re
import sqlite3

Mensajes = {
    'PRODUCTO_EXITO_AGREGAR'                  : 'Producto agregado exitosamente.',
    'PRODUCTO_EXITO_MODIFICAR'                : 'Producto modificado exitosamente.',
    'PRODUCTO_EXITO_ELIMINAR'                 : 'Producto eliminado exitosamente.',
    'PRODUCTO_ERROR_TIPO'                     : 'Error: El tipo solo puede contener letras, números, espacios y guiones.',
    'PRODUCTO_ERROR_NOMBRE'                   : 'Error: El nombre solo puede contener letras, números, espacios y guiones.',
    'PRODCUTO_ERROR_MODELO'                   : 'Error: El modelo solo puede contener letras, números, espacios y guiones.',
    'PRODUCTO_ERROR_MEDIDAS'                  : 'Error: Las medidas deben tener el formato AxBxC, donde A, B y C son números entre 1 y 4 dígitos.',
    'PRODUCTO_ERROR_NOENCONTRADO'             : 'Error: Producto no encontrado.',
    
    'COMPONENTE_EXITO_AGREGAR'                : 'Componente agregado exitosamente.',
    'COMPONENTE_EXITO_MODIFICAR'              : 'Componente modificado exitosamente.',
    'COMPONENTE_EXITO_ELIMINAR'               : 'Componente eliminado exitosamente.',
    'COMPONENTE_ERROR_NOMBRE'                 : 'Error: El nombre solo puede contener letras, números, espacios y guiones.',
    'COMPONENTE_ERROR_UNIDAD'                 : 'Error: Las medidas deben ser "m3" o "kg".',
    'COMPONENTE_ERROR_CANTIDAD'               : 'Error: La cantidad debe ser un número entero.',
    'COMPONENTE_ERROR_NOENCONTRADO'           : 'Error: Componente no encontrado.',
    
    'COMPONENTE-POR-PRODUCTO_EXITO_AGREGAR'   : 'Componente por producto agregado exitosamente.',
    'COMPONENTE-POR-PRODUCTO_EXITO_MODIFICAR' : 'Componente por producto modificado exitosamente.',
    'COMPONENTE-POR-PRODUCTO_EXITO_ELIMINAR'  : 'Componente por producto eliminado exitosamente.',
    'COMPONENTE-POR-PRODUCTO_ERROR_CANTIDAD'  : 'Error: La cantidad debe ser un número positivo.',

    'STOCK_ERROR_CANTIDAD'                    : 'Error: La cantidad debe ser cero o un número positivo.'
}

UNIDADES = {
    'm'  : 'Metro (m)',
    'm2' : 'Metro cuadrado (m²)',
    'm3' : 'Metro cúbico (m³)',
    'kg' : 'Kilogramo (kg)',
    'l'  : 'Litro (l)',
    'u'  : 'Unidad (u)'
}

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


class Productos:
    def __init__(self, DB):
        self.DB = DB
        
    def Consultar(self):
        return self.DB.execute('SELECT * FROM productos WHERE habilitado != 0').fetchall()
    
    def Consultar_Tipos(self):
        return self.DB.execute('SELECT DISTINCT tipo FROM productos WHERE habilitado != 0 ORDER BY tipo ASC').fetchall()[0]
    
    def Consultar_Siguiente_ID(self):
        resultado = self.DB.execute('SELECT seq + 1 FROM sqlite_sequence WHERE name = "productos"').fetchone()[0]
        
        if resultado is None:
            return 1
        
        return resultado

    def Consultar_Formateado(self):
        resultado = self.DB.execute('SELECT * FROM productos WHERE habilitado != 0').fetchall()
        return {fila[0] : f'{fila[1]} {fila[2]} ({fila[3]})' for fila in resultado}
    
    def Seleccionar(self, id):
        return self.DB.execute('SELECT * FROM productos WHERE id = ?', (id,)).fetchone()
    
    def Agregar(self, tipo, nombre, modelo, medidas):
        if not Validar_Texto(tipo):
            return Mensajes['PRODUCTO_ERROR_TIPO']
        
        if not Validar_Texto(nombre):
            return Mensajes['PRODUCTO_ERROR_NOMBRE']
        
        if not Validar_Texto(modelo):
            return Mensajes['PRODCUTO_ERROR_MODELO']
        
        if not Validar_Medidas(medidas):
            return Mensajes['PRODUCTO_ERROR_MEDIDAS']
        
        self.DB.execute('INSERT INTO productos (tipo, nombre, modelo, medidas) VALUES (?, ?, ?, ?)', (tipo, nombre, modelo, medidas))
        self.DB.commit()
        
        return Mensajes['PRODUCTO_EXITO_AGREGAR']
    
    def Modificar(self, id, tipo, nombre, modelo, medidas):
        if not Validar_Texto(tipo):
            return Mensajes['PRODUCTO_ERROR_TIPO']
        
        if not Validar_Texto(nombre):
            return Mensajes['PRODUCTO_ERROR_NOMBRE']
        
        if not Validar_Texto(modelo):
            return Mensajes['PRODCUTO_ERROR_MODELO']
        
        if not Validar_Medidas(medidas):
            return Mensajes['PRODUCTO_ERROR_MEDIDAS']
        
        self.DB.execute('UPDATE productos SET tipo = ?, nombre = ?, modelo = ?, medidas = ? WHERE id = ?', (tipo, nombre, modelo, medidas, id))
        self.DB.commit()
        
        return Mensajes['PRODUCTO_EXITO_MODIFICAR']
    
    def Eliminar(self, id):
        self.DB.execute('UPDATE productos SET habilitado = 0 WHERE id = ?', (id,))
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
        if not Validar_Cantidad(cantidad, minimo=0):
            return Mensajes['STOCK_ERROR_CANTIDAD']
        
        self.DB.execute(f'INSERT INTO stock (id_item, tipo_item, cantidad) VALUES (?, ?, ?)', (id_item, tipo_item, cantidad))
        self.DB.commit()
        
        return 'Stock agregado exitosamente.'

    def Modificar(self, id, cantidad):
        if not Validar_Cantidad(cantidad):
            return Mensajes['STOCK_ERROR_CANTIDAD']
        
        self.DB.execute('UPDATE stock SET cantidad = ? WHERE id = ?', (cantidad, id))
        self.DB.commit()
        
        return 'Stock modificado exitosamente.'

    def Eliminar(self, id):
        self.DB.execute('DELETE FROM stock WHERE id = ?', (id,))
        self.DB.commit()
        return 'Stock eliminado exitosamente.'