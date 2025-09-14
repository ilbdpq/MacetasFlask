import re

Mensajes = {
    'PRODUCTO_AGREGAR_EXITO': 'Producto agregado exitosamente.',
    'PRODUCTO_AGREGAR_ERROR_MEDIDAS': 'Error: Las medidas deben tener el formato AxBxC, donde A, B y C son números entre 1 y 4 dígitos.',
    'PRODUCTO_MODIFICAR_EXITO': 'Producto modificado exitosamente.',
    'PRODUCTO_MODIFICAR_ERROR_MEDIDAS': 'Error: Las medidas deben tener el formato AxBxC, donde A, B y C son números entre 1 y 4 dígitos.',
    'PRODUCTO_ELIMINAR_EXITO': 'Producto eliminado exitosamente.',
    'PRODUCTO_NO_ENCONTRADO': 'Error: Producto no encontrado.'
}

def Validar_Medidas(medidas):
    # 1 a 4 dígitos x 1 a 4 dígitos x 1 a 4 dígitos (10x20x30 cm)
    patron = r'^\d{1,4}x\d{1,4}x\d{1,4}$'

    if re.match(patron, medidas):
        return True

    return False

class Productos:
    def __init__(self, DB):
        self.DB = DB
        
    def Consultar(self):
        return self.DB.execute('SELECT * FROM productos WHERE habilitado != 0').fetchall()
    
    def Consultar_Tipos(self):
        return self.DB.execute('SELECT DISTINCT tipo FROM productos WHERE habilitado != 0').fetchall()
    
    def Seleccionar(self, id):
        return self.DB.execute('SELECT * FROM productos WHERE id = ?', (id,)).fetchone()
    
    def Agregar(self, tipo, nombre, modelo, medidas):
        if not Validar_Medidas(medidas):
            return Mensajes['PRODUCTO_AGREGAR_ERROR_MEDIDAS']
        
        self.DB.execute('INSERT INTO productos (tipo, nombre, modelo, medidas) VALUES (?, ?, ?, ?)', (tipo, nombre, modelo, medidas))
        self.DB.commit()
        
        return Mensajes['PRODUCTO_AGREGAR_EXITO']
    
    def Modificar(self, id, tipo, nombre, modelo, medidas):
        if not Validar_Medidas(medidas):
            return Mensajes['PRODUCTO_AGREGAR_ERROR_MEDIDAS']
        
        self.DB.execute('UPDATE productos SET tipo = ?, nombre = ?, modelo = ?, medidas = ? WHERE id = ?', (tipo, nombre, modelo, medidas, id))
        self.DB.commit()
        
        return Mensajes['PRODUCTO_MODIFICAR_EXITO']
    
    def Eliminar(self, id):
        self.DB.execute('UPDATE productos SET habilitado = 0 WHERE id = ?', (id,))
        self.DB.commit()
        
        return Mensajes['PRODUCTO_ELIMINAR_EXITO']