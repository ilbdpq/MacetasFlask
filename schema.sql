DROP TABLE IF EXISTS productos;
DROP TABLE IF EXISTS componentes;
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
    medidas TEXT NOT NULL,
    habilitado INTEGER NOT NULL DEFAULT 1
);

-- Tabla COMPONENTES
CREATE TABLE componentes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    id_producto INTEGER NOT NULL,
    nombre TEXT NOT NULL,
    medidas TEXT NOT NULL,
    cantidad INTEGER NOT NULL,
    habilitado INTEGER NOT NULL DEFAULT 1,
    FOREIGN KEY(id_producto) REFERENCES productos(id)
);

-- Tabla STOCK
CREATE TABLE stock (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    id_stock INTEGER NOT NULL,
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
('Maceta', 'Cubo', 'M-001', '10x10x10'),
('Maceta', 'Cilindro', 'M-002', '15x15x20'),
('Maceta', 'Esfera', 'M-003', '20x20x20'),
('Maceta', 'Cono', 'M-004', '12x12x25'),
('Maceta', 'Piramide', 'M-005', '18x18x30'),
('Maceta', 'Rectangular', 'M-006', '30x15x10'),
('Maceta', 'Hexagonal', 'M-007', '20x20x15'),
('Maceta', 'Octogonal', 'M-008', '25x25x20'),
('Maceta', 'Corazon', 'M-009', '15x15x15'),
('Maceta', 'Estrella', 'M-010', '20x20x10'),
('Maceta', 'Flor', 'M-011', '18x18x18'),
('Maceta', 'Animal', 'M-012', '22x22x22'),
('Maceta', 'Abstracta', 'M-013', '30x30x30'),
('Maceta', 'Personalizada', 'M-014', '20x20x20'),
('Maceta', 'Colgante', 'M-015', '15x15x30'),
('Maceta', 'Doble', 'M-016', '25x25x25'),
('Maceta', 'Triple', 'M-017', '30x30x20'),
('Macetón', 'Cuadrado Grande', 'ML-018', '40x40x40'),
('Macetón', 'Redondo Grande', 'ML-019', '35x35x35'),
('Maceta', 'Ovalada', 'M-020', '30x20x15');
-- Insertar datos de ejemplo en COMPONENTES
INSERT INTO componentes (id_producto, nombre, medidas, cantidad) VALUES
(1, 'Base', '10x10', 100),
(1, 'Pared', '10x10x10', 100),
(2, 'Base', '15x15', 80),
(2, 'Pared', '15x15x20', 80),
(3, 'Base', '20x20', 60),
(3, 'Pared', '20x20x20', 60),
(4, 'Base', '12x12', 70),
(4, 'Pared', '12x12x25', 70),
(5, 'Base', '18x18', 50),
(5, 'Pared', '18x18x30', 50),
(6, 'Base', '30x15', 90),
(6, 'Pared', '30x15x10', 90),
(7, 'Base', '20x20', 65),
(7, 'Pared', '20x20x15', 65),
(8, 'Base', '25x25', 55),
(8, 'Pared', '25x25x20', 55),
(9, 'Base', '15x15', 75),
(9, 'Pared', '15x15x15', 75),
(10, 'Base', '20x20', 85),
(10, 'Pared', '20x20x10', 85);