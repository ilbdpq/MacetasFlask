import re

def Validar_Medidas(medidas):
    # 1 a 4 dígitos x 1 a 4 dígitos x 1 a 4 dígitos (10x20x30 cm)
    patron = r'^\d{1,4}x\d{1,4}x\d{1,4}$'

    if re.match(patron, medidas):
        return True

    return False

def Productos_Tabla(DB):
    return DB.execute('SELECT * FROM productos WHERE habilitado != 0').fetchall()

def Productos_Tipos(DB):
    return DB.execute('SELECT DISTINCT tipo FROM productos WHERE habilitado != 0').fetchall()