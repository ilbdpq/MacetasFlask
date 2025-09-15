import re
import sqlite3

Mensajes = {
    'PRODUCTO_EXITO_AGREGAR': 'Producto agregado exitosamente.',
    'PRODUCTO_EXITO_MODIFICAR': 'Producto modificado exitosamente.',
    'PRODUCTO_EXITO_ELIMINAR': 'Producto eliminado exitosamente.',
    'PRODUCTO_ERROR_TIPO': 'Error: El tipo solo puede contener letras, números, espacios y guiones.',
    'PRODUCTO_ERROR_NOMBRE': 'Error: El nombre solo puede contener letras, números, espacios y guiones.',
    'PRODCUTO_ERROR_MODELO': 'Error: El modelo solo puede contener letras, números, espacios y guiones.',
    'PRODUCTO_ERROR_MEDIDAS': 'Error: Las medidas deben tener el formato AxBxC, donde A, B y C son números entre 1 y 4 dígitos.',
    'PRODUCTO_ERROR_NOENCONTRADO': 'Error: Producto no encontrado.'
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

class Productos:
    def __init__(self, DB):
        self.DB = DB
        
    def Consultar(self):
        return self.DB.execute('SELECT * FROM productos WHERE habilitado != 0').fetchall()
    
    def Consultar_Tipos(self):
        self.DB.row_factory = lambda cursor, row: row[0]
        return self.DB.execute('SELECT DISTINCT tipo FROM productos WHERE habilitado != 0').fetchall()
    
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