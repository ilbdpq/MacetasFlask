DROP TABLE IF EXISTS productos;
DROP TABLE IF EXISTS componentes;
DROP TABLE IF EXISTS componentes_por_producto;
DROP TABLE IF EXISTS stock;
DROP TABLE IF EXISTS fabricaciones_encabezado;
DROP TABLE IF EXISTS fabricaciones_detalle;
DROP TABLE IF EXISTS facturas_encabezado;
DROP TABLE IF EXISTS facturas_detalle;

-- Tabla PRODUCTOS
CREATE TABLE productos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    tipo TEXT NOT NULL,
    nombre TEXT NOT NULL,
    modelo TEXT NOT NULL,
    medidas TEXT NOT NULL, -- Largo x Ancho x Alto
    habilitado INTEGER NOT NULL DEFAULT 1
);

-- Tabla COMPONENTES
CREATE TABLE componentes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT NOT NULL,
    unidad TEXT NOT NULL,
    habilitado INTEGER NOT NULL DEFAULT 1
);

-- Tabla COMPONENTES POR PRODUCTO
CREATE TABLE componentes_por_producto (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    id_producto INTEGER NOT NULL,
    id_componente INTEGER NOT NULL,
    cantidad REAL NOT NULL,
    habilitado INTEGER NOT NULL DEFAULT 1,
    FOREIGN KEY(id_producto) REFERENCES productos(id)
    FOREIGN KEY(id_componente) REFERENCES componentes(id)
);

-- Tabla STOCK
CREATE TABLE stock (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    id_item INTEGER NOT NULL,
    tipo_item TEXT NOT NULL,
    cantidad INTEGER NOT NULL
);

-- Tablas FABRICACIONES
CREATE TABLE fabricaciones_encabezado (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    fecha TEXT NOT NULL
);

CREATE TABLE fabricaciones_detalle (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    id_producto INTEGER NOT NULL,
    cantidad INTEGER NOT NULL,
    precio_costo REAL NOT NULL,
    precio_venta REAL NOT NULL,
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
    id_factura INTEGER NOT NULL,
    id_producto INTEGER NOT NULL,
    cantidad INTEGER NOT NULL,
    precio REAL NOT NULL,
    FOREIGN KEY(id_factura) REFERENCES facturas_encabezado(id),
    FOREIGN KEY(id_producto) REFERENCES productos(id)
);

-- Insertar datos de ejemplo en PRODUCTOS
INSERT INTO productos (tipo, nombre, modelo, medidas) VALUES
    ('Maceta', 'Cubo'                 , 'M-001', '20x20x20'), -- ID 1
    ('Maceta', 'Cubo Baja'            , 'M-002', '20x20x10'), -- ID 2
    ('Maceta', 'Cubo Alta'            , 'M-003', '20x20x30'), -- ID 3
    ('Maceta', 'Cilindro'             , 'M-004', '20x20x20'), -- ID 4
    ('Maceta', 'Cilindro Baja'        , 'M-005', '20x20x10'), -- ID 5
    ('Maceta', 'Cilindro Alta'        , 'M-006', '20x20x30'), -- ID 6
    ('Maceta', 'Esfera'               , 'M-007', '20x20x20'), -- ID 7
    ('Maceta', 'Rectangular'          , 'M-008', '20x40x20'), -- ID 8
    ('Maceta', 'Rectangular Baja'     , 'M-009', '20x40x10'), -- ID 9
    ('Maceta', 'Rectangular Doble'    , 'M-010', '20x40x20'), -- ID 10
    ('Maceta', 'Rectangular Cuádruple', 'M-011', '20x40x20'), -- ID 11
    ('Maceta', 'Colgante Cuerda'      , 'M-012', '20x20x20'), -- ID 12
    ('Maceta', 'Colgante Cadena'      , 'M-013', '20x20x20'), -- ID 13
    ('Maceta', 'Cubo Grande'          , 'M-014', '40x40x20'); -- ID 14

-- Insertar datos de ejemplo en COMPONENTES
INSERT INTO componentes (nombre, unidad) VALUES
    ('Agua'                    , 'l'),  -- ID 1
    ('Cemento'                 , 'kg'), -- ID 2
    ('Arena'                   , 'kg'), -- ID 3
    ('Grava'                   , 'kg'), -- ID 4
    ('Cuerda'                  , 'm'),  -- ID 5
    ('Cadena'                  , 'm'),  -- ID 6
    ('Manija'                  , 'u'),  -- ID 7
    ('Enganche'                , 'u'),  -- ID 8
    ('Perno'                   , 'u'),  -- ID 9
    ('Plato Cuadrado 20cm'     , 'u'),  -- ID 10
    ('Plato Cuadrado 40cm'     , 'u'),  -- ID 11
    ('Plato Rectangulo 20x40cm', 'u'),  -- ID 12
    ('Plato Circulo 20cm'      , 'u');  -- ID 13

-- Insertar datos de ejemplo en COMPONENTES POR PRODUCTO
INSERT INTO componentes_por_producto (id_producto, id_componente, cantidad) VALUES
(1, 1, 2.0),   -- Maceta Cubo: Agua
(1, 2, 3.0),   -- Cemento
(1, 3, 4.0),   -- Arena
(1, 4, 2.0),   -- Grava
(1, 10, 1),    -- Plato Cuadrado 20cm

(2, 1, 1.5),   -- Maceta Cubo: Baja
(2, 2, 2.5),   -- Cemento
(2, 3, 3.0),   -- Arena
(2, 4, 1.5),   -- Grava
(2, 10, 1),    -- Plato Cuadrado 20cm

(3, 1, 2.5),   -- Maceta Cubo Alta: Agua
(3, 2, 4.0),   -- Cemento
(3, 3, 5.0),   -- Arena
(3, 4, 2.5),   -- Grava
(3, 10, 1),    -- Plato Cuadrado 20cm

(4, 1, 2.0),   -- Maceta Cilindro: Agua
(4, 2, 3.0),   -- Cemento
(4, 3, 4.0),   -- Arena
(4, 4, 2.0),   -- Grava
(4, 13, 1),    -- Plato Circulo 20cm

(5, 1, 1.5),   -- Maceta Cilindro Baja: Agua
(5, 2, 2.5),   -- Cemento
(5, 3, 3.0),   -- Arena
(5, 4, 1.5),   -- Grava
(5, 13, 1),    -- Plato Circulo 20cm

(6, 1, 2.5),   -- Maceta Cilindro Alta: Agua
(6, 2, 4.0),   -- Cemento
(6, 3, 5.0),   -- Arena
(6, 4, 2.5),   -- Grava
(6, 13, 1),    -- Plato Circulo 20cm

(7, 1, 2.0),   -- Maceta Esfera: Agua
(7, 2, 3.0),   -- Cemento
(7, 3, 4.0),   -- Arena
(7, 4, 2.0),   -- Grava
(7, 13, 1),    -- Plato Circulo 20cm

(8, 1, 3.0),   -- Maceta Rectangular: Agua
(8, 2, 5.0),   -- Cemento
(8, 3, 6.0),   -- Arena
(8, 4, 3.0),   -- Grava
(8, 12, 1),    -- Plato Rectangulo 20x40cm

(9, 1, 2.0),   -- Maceta Rectangular Baja: Agua
(9, 2, 3.5),   -- Cemento
(9, 3, 4.0),   -- Arena
(9, 4, 2.0),   -- Grava
(9, 12, 1),    -- Plato Rectangulo 20x40cm

(10, 1, 4.0),  -- Maceta Rectangular Doble: Agua
(10, 2, 7.0),  -- Cemento
(10, 3, 8.0),  -- Arena
(10, 4, 4.0),  -- Grava
(10, 12, 1),   -- Plato Rectangulo 20x40cm

(11, 1, 8.0),  -- Maceta Rectangular Cuádruple: Agua
(11, 2, 14.0), -- Cemento
(11, 3, 16.0), -- Arena
(11, 4, 8.0),  -- Grava
(11, 12, 1),   -- Plato Rectangulo 20x40cm

(12, 1, 2.0),  -- Maceta Colgante Cuerda: Agua
(12, 2, 3.0),  -- Cemento
(12, 3, 4.0),  -- Arena
(12, 4, 2.0),  -- Grava
(12, 5, 1.0),  -- Cuerda
(12, 13, 1),   -- Plato Circulo 20cm
(12, 8, 4),    -- 4 Enganches
(12, 7, 2),    -- 2 Manijas
(12, 9, 10),   -- 2 pernos por manija (2x2=4), 1 perno por enganche (4x1=4), total 8+2=10

(13, 1, 2.0),  -- Maceta Colgante Cadena: Agua
(13, 2, 3.0),  -- Cemento
(13, 3, 4.0),  -- Arena
(13, 4, 2.0),  -- Grava
(13, 6, 1.0),  -- Cadena
(13, 13, 1),   -- Plato Circulo 20cm
(13, 8, 4),    -- 4 Enganches
(13, 7, 2),    -- 2 Manijas
(13, 9, 10),   -- 2 pernos por manija (2x2=4), 1 perno por enganche (4x1=4), total 8+2=10

(14, 1, 5.0),  -- Maceta Cubo Grande: Agua
(14, 2, 8.0),  -- Cemento
(14, 3, 10.0), -- Arena
(14, 4, 5.0),  -- Grava
(14, 11, 1),   -- Plato Cuadrado 40cm
(14, 7, 2),    -- 2 Manijas
(14, 9, 4);    -- 2 pernos por manija (2x2=4)

-- Insertar datos de ejemplo en STOCK
INSERT INTO stock (id_item, tipo_item, cantidad) VALUES
    (1 , 'Producto'  , 50) , -- Maceta Cubo
    (2 , 'Producto'  , 50) , -- Maceta Cubo Baja
    (3 , 'Producto'  , 50) , -- Maceta Cubo Alta
    (4 , 'Producto'  , 50) , -- Maceta Cilindro
    (5 , 'Producto'  , 50) , -- Maceta Cilindro Baja
    (6 , 'Producto'  , 50) , -- Maceta Cilindro Alta
    (7 , 'Producto'  , 50) , -- Maceta Esfera
    (8 , 'Producto'  , 50) , -- Maceta Rectangular
    (9 , 'Producto'  , 50) , -- Maceta Rectangular Baja
    (10, 'Producto'  , 50) , -- Maceta Rectangular Doble
    (11, 'Producto'  , 50) , -- Maceta Rectangular Cuádruple
    (12, 'Producto'  , 50) , -- Maceta Colgante Cuerda
    (13, 'Producto'  , 50) , -- Maceta Colgante Cadena
    (14, 'Producto'  , 50) , -- Maceta Cubo Grande
    (1 , 'Componente', 200), -- Agua
    (2 , 'Componente', 150), -- Cemento
    (3 , 'Componente', 300), -- Arena
    (4 , 'Componente', 250), -- Grava
    (5 , 'Componente', 100), -- Cuerda
    (6 , 'Componente', 100), -- Cadena
    (7 , 'Componente', 100), -- Manija
    (8 , 'Componente', 200), -- Enganche
    (9 , 'Componente', 300), -- Perno
    (10, 'Componente', 50) , -- Plato Cuadrado 20cm
    (11, 'Componente', 50) , -- Plato Cuadrado 40cm
    (12, 'Componente', 50) , -- Plato Rectangulo 20x40cm
    (13, 'Componente', 50);  -- Plato Circulo 20cm