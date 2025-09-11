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
('Maceta', 'Maceta Cubo', 'M-001', '10x10x10'),
('Maceta', 'Maceta Cilindro', 'M-002', '15x15x20'),
('Maceta', 'Maceta Esfera', 'M-003', '20x20x20'),
('Maceta', 'Maceta Cono', 'M-004', '12x12x25'),
('Maceta', 'Maceta Piramide', 'M-005', '18x18x30'),
('Maceta', 'Maceta Rectangular', 'M-006', '30x15x10'),
('Maceta', 'Maceta Hexagonal', 'M-007', '20x20x15'),
('Maceta', 'Maceta Octogonal', 'M-008', '25x25x20'),
('Maceta', 'Maceta Corazon', 'M-009', '15x15x15'),
('Maceta', 'Maceta Estrella', 'M-010', '20x20x10'),
('Maceta', 'Maceta Flor', 'M-011', '18x18x18'),
('Maceta', 'Maceta Animal', 'M-012', '22x22x22'),
('Maceta', 'Maceta Abstracta', 'M-013', '30x30x30'),
('Maceta', 'Maceta Personalizada', 'M-014', '20x20x20'),
('Maceta', 'Maceta Colgante', 'M-015', '15x15x30'),
('Maceta', 'Maceta Doble', 'M-016', '25x25x25'),
('Maceta', 'Maceta Triple', 'M-017', '30x30x20'),
('Maceta', 'Maceta Cuadrada Grande', 'M-018', '40x40x40'),
('Maceta', 'Maceta Redonda Grande', 'M-019', '35x35x35'),
('Maceta', 'Maceta Ovalada', 'M-020', '30x20x15');