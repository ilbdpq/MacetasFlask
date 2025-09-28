DROP TABLE IF EXISTS usuarios;
DROP TABLE IF EXISTS productos;
DROP TABLE IF EXISTS componentes;
DROP TABLE IF EXISTS componentes_por_producto;
DROP TABLE IF EXISTS stock;
DROP TABLE IF EXISTS fabricaciones_encabezado;
DROP TABLE IF EXISTS fabricaciones_detalle;
DROP TABLE IF EXISTS facturas_encabezado;
DROP TABLE IF EXISTS facturas_detalle;

-- Tabla USUARIOS
CREATE TABLE usuarios (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL,
    nombres TEXT NOT NULL,
    rol TEXT NOT NULL
);

-- Tabla PRODUCTOS
CREATE TABLE productos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    tipo TEXT NOT NULL,
    nombre TEXT NOT NULL,
    modelo TEXT NOT NULL,
    estilo TEXT NOT NULL,
    medidas TEXT NOT NULL, -- Largo x Ancho x Alto
    precio_venta REAL NOT NULL,
    habilitado INTEGER NOT NULL DEFAULT 1
);

-- Tabla COMPONENTES
CREATE TABLE componentes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT NOT NULL,
    unidad TEXT NOT NULL,
    precio_costo REAL NOT NULL,
    habilitado INTEGER NOT NULL DEFAULT 1
);

-- Tabla COMPONENTES POR PRODUCTO
CREATE TABLE componentes_por_producto (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    id_producto INTEGER NOT NULL,
    id_componente INTEGER NOT NULL,
    cantidad REAL NOT NULL,
    habilitado INTEGER NOT NULL DEFAULT 1,
    FOREIGN KEY(id_producto) REFERENCES productos(id),
    FOREIGN KEY(id_componente) REFERENCES componentes(id)
);

-- Tabla STOCK
CREATE TABLE stock (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    id_item INTEGER NOT NULL,
    tipo_item TEXT NOT NULL,
    cantidad REAL NOT NULL,
    movimiento TEXT NOT NULL
);

-- Tablas FABRICACIONES
CREATE TABLE fabricaciones_encabezado (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    fecha TEXT NOT NULL
);

CREATE TABLE fabricaciones_detalle (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    id_encabezado INTEGER NOT NULL,
    id_producto INTEGER NOT NULL,
    cantidad INTEGER NOT NULL,
    costo_total REAL NOT NULL,
    FOREIGN KEY(id_encabezado) REFERENCES fabricaciones_encabezado(id),
    FOREIGN KEY(id_producto) REFERENCES productos(id)
);

-- Tablas FACTURAS
CREATE TABLE facturas_encabezado (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    fecha TEXT NOT NULL,
    cliente TEXT NOT NULL
);

CREATE TABLE facturas_detalle (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    id_encabezado INTEGER NOT NULL,
    id_producto INTEGER NOT NULL,
    cantidad INTEGER NOT NULL,
    precio_total REAL NOT NULL,
    FOREIGN KEY(id_encabezado) REFERENCES facturas_encabezado(id),
    FOREIGN KEY(id_producto) REFERENCES productos(id)
);

-- Insertar datos de ejemplo en USUARIOS
INSERT INTO usuarios (username, password, nombres, rol) VALUES
('admin', 'admin', 'Administrador Admin', 'Administrador'),
('agerente', 'passA', 'Ana Alvarez', 'Gerente'),
('bgerente', 'passB', 'Bruno Benitez', 'Gerente'),
('cencargado', 'passC', 'Carla Cortez', 'Encargado'),
('dencargado', 'passD', 'Diego Diaz', 'Encargado'),
('eoperario', 'passE', 'Elena Escobar', 'Operario'),
('foperario', 'passF', 'Fernando Fernandez', 'Operario'),
('goperario', 'passG', 'Gabriela Gomez', 'Operario'),
('hoperario', 'passH', 'Hugo Herrera', 'Operario'),
('ioperario', 'passI', 'Isabel Iglesias', 'Operario'),
('joperario', 'passJ', 'Javier Juarez', 'Operario'),
('koperario', 'passK', 'Karina Kruger', 'Operario'),
('loperario', 'passL', 'Luis Lopez', 'Operario'),
('moperario', 'passM', 'Maria Martinez', 'Operario'),
('noperario', 'passN', 'Nicolas Navarro', 'Operario'),
('ooperario', 'passO', 'Olga Ortega', 'Operario');

-- Insertar datos de ejemplos en PRODUCTOS
INSERT INTO productos (tipo, nombre, modelo, estilo, medidas, precio_venta) VALUES
('Maceta','Cubo'           ,'Base'    ,'Plano'   ,'20x20x20',1500.50),
('Maceta','Cubo'           ,'Alta'    ,'Plano'   ,'20x20x30',1800.75),
('Maceta','Cubo'           ,'Baja'    ,'Plano'   ,'20x20x10',1300.50),
('Maceta','Cubo'           ,'Colgante','Colgante','20x20x20',2100.00),
('Maceta','Prisma'         ,'Base'    ,'Plano'   ,'20x40x20',2000.00),
('Maceta','Prisma'         ,'Alta'    ,'Plano'   ,'20x40x20',2200.00),
('Maceta','Prisma'         ,'Colgante','Colgante','20x40x20',2850.05),
('Plato' ,'Rectangulo 20x20','Base'    ,'Plano'   ,'20x20x2' ,350.25),
('Plato' ,'Rectangulo 20x40','Base'    ,'Plano'   ,'20x40x2' ,550.50),
('Maceta','Cilindro'       ,'Base'    ,'Plano'   ,'20x20x20',1750.75),
('Plato' ,'Circulo 20x20'   ,'Base'    ,'Plano'   ,'20x20x2' ,400.00);