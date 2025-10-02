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
    movimiento TEXT NOT NULL -- ISO8601 YYYY-MM-DD HH:MM:SS.SSS
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
('Maceta','Cubo'           ,'Alta'    ,'Plano'   ,'20x20x30',1800.70),
('Maceta','Cubo'           ,'Baja'    ,'Plano'   ,'20x20x10',1300.50),
('Maceta','Cubo'           ,'Colgante','Colgante','20x20x20',2100.00),
('Maceta','Prisma'         ,'Base'    ,'Plano'   ,'20x40x20',2000.00),
('Maceta','Prisma'         ,'Alta'    ,'Plano'   ,'20x40x20',2200.00),
('Maceta','Prisma'         ,'Colgante','Colgante','20x40x20',2850.00),
('Plato' ,'Rectangulo 20x20','Base'    ,'Plano'   ,'20x20x2' ,350.20),
('Plato' ,'Rectangulo 20x40','Base'    ,'Plano'   ,'20x40x2' ,550.50),
('Maceta','Cilindro'       ,'Base'    ,'Plano'   ,'20x20x20',1750.70),
('Plato' ,'Circulo 20x20'   ,'Base'    ,'Plano'   ,'20x20x2' ,400.00);

-- Insertar datos de ejemplos en COMPONENTES
INSERT INTO componentes (nombre, unidad, precio_costo) VALUES
('Agua'   , 'l' , 9.5),
('Cemento', 'kg', 36.3),
('Arena'  , 'kg', 21.2),
('Grava'  , 'kg', 23.4);

-- Insertar datos de ejemplos en COMPONENTES POR PRODUCTO
INSERT INTO componentes_por_producto (id_producto, id_componente, cantidad) VALUES
(1, 1, 2.0),  -- Maceta Cubo Base: Agua
(1, 2, 3.0),  -- Maceta Cubo Base: Cemento
(1, 3, 5.0),  -- Maceta Cubo Base: Arena
(1, 4, 1.5),  -- Maceta Cubo Base: Grava

(2, 1, 2.5),  -- Maceta Cubo Alta: Agua
(2, 2, 3.5),  -- Maceta Cubo Alta: Cemento
(2, 3, 6.0),  -- Maceta Cubo Alta: Arena
(2, 4, 2.0),  -- Maceta Cubo Alta: Grava

(3, 1, 1.5),  -- Maceta Cubo Baja: Agua
(3, 2, 2.0),  -- Maceta Cubo Baja: Cemento
(3, 3, 3.5),  -- Maceta Cubo Baja: Arena
(3, 4, 1.0),  -- Maceta Cubo Baja: Grava

(4, 1, 2.0),  -- Maceta Cubo Colgante: Agua
(4, 2, 3.0),  -- Maceta Cubo Colgante: Cemento
(4, 3, 5.0),  -- Maceta Cubo Colgante: Arena
(4, 4, 1.5),  -- Maceta Cubo Colgante: Grava

(5, 1, 2.2),  -- Maceta Prisma Base: Agua
(5, 2, 3.2),  -- Maceta Prisma Base: Cemento
(5, 3, 5.5),  -- Maceta Prisma Base: Arena
(5, 4, 1.7),  -- Maceta Prisma Base: Grava

(6, 1, 2.7),  -- Maceta Prisma Alta: Agua
(6, 2, 3.7),  -- Maceta Prisma Alta: Cemento
(6, 3, 6.2),  -- Maceta Prisma Alta: Arena
(6, 4, 2.2),  -- Maceta Prisma Alta: Grava

(7, 1, 2.5),  -- Maceta Prisma Colgante: Agua
(7, 2, 3.5),  -- Maceta Prisma Colgante: Cemento
(7, 3, 6.0),  -- Maceta Prisma Colgante: Arena
(7, 4, 2.0),  -- Maceta Prisma Colgante: Grava

(8, 1, 0.5),  -- Plato Rectangulo 20x20: Agua
(8, 2, 1.0),  -- Plato Rectangulo 20x20: Cemento
(8, 3, 1.5),  -- Plato Rectangulo 20x20: Arena

(9, 1, 0.8),  -- Plato Rectangulo 20x40: Agua
(9, 2, 1.5),  -- Plato Rectangulo 20x40: Cemento
(9, 3, 2.2),  -- Plato Rectangulo 20x40: Arena

(10, 1, 2.0), -- Maceta Cilindro Base: Agua
(10, 2, 3.0), -- Maceta Cilindro Base: Cemento
(10, 3, 5.0), -- Maceta Cilindro Base: Arena
(10, 4, 1.5), -- Maceta Cilindro Base: Grava

(11, 1, 0.6), -- Plato Circulo 20x20: Agua
(11, 2, 1.2), -- Plato Circulo 20x20: Cemento
(11, 3, 1.8); -- Plato Circulo 20x20: Arena

-- Insertar datos de ejemplo en STOCK
INSERT INTO stock (id_item, tipo_item, cantidad, movimiento) VALUES
(1, 'Producto', 10, '2025-10-01 09:00:00.000'),
(2, 'Producto', 5, '2025-10-01 09:05:00.000'),
(3, 'Producto', 8, '2025-10-01 09:10:00.000'),
(4, 'Producto', 3, '2025-10-01 09:15:00.000'),
(5, 'Producto', 6, '2025-10-01 09:20:00.000'),
(6, 'Producto', 4, '2025-10-01 09:25:00.000'),
(7, 'Producto', 2, '2025-10-01 09:30:00.000'),
(8, 'Producto', 15, '2025-10-01 09:35:00.000'),
(9, 'Producto', 12, '2025-10-01 09:40:00.000'),
(10, 'Producto', 7, '2025-10-01 09:45:00.000'),
(11, 'Producto', 9, '2025-10-01 09:50:00.000'),
(1, 'Componente', 100, '2025-10-01 10:00:00.000'),
(2, 'Componente', 80, '2025-10-01 10:05:00.000'),
(3, 'Componente', 120, '2025-10-01 10:10:00.000'),
(4, 'Componente', 90, '2025-10-01 10:15:00.000');