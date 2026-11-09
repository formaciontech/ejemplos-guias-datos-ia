-- Guía: SQL para equipos de negocio y datos
-- https://formaciontech.es/guias/sql-analisis-datos-empresa/
--
-- Esquema y datos sintéticos para los ejemplos. Los datos están escritos a mano
-- y son pequeños a propósito: así se puede comprobar cada resultado mentalmente.
-- Todo se crea en el esquema guia_sql; borrarlo deja la base de datos como estaba.
-- Probado en PostgreSQL 16.

DROP SCHEMA IF EXISTS guia_sql CASCADE;
CREATE SCHEMA guia_sql;
SET search_path TO guia_sql;

-- Ocho clientes; dos no tienen ciudad (NULL)
CREATE TABLE clientes (
  id_cliente integer PRIMARY KEY,
  nombre     text    NOT NULL,
  ciudad     text,
  segmento   text    NOT NULL
);
INSERT INTO clientes VALUES
  (1, 'Cliente 01', 'Valencia',  'Pyme'),
  (2, 'Cliente 02', 'Madrid',    'Gran empresa'),
  (3, 'Cliente 03', NULL,        'Pyme'),
  (4, 'Cliente 04', 'Valencia',  'Gran empresa'),
  (5, 'Cliente 05', 'Barcelona', 'Pyme'),
  (6, 'Cliente 06', NULL,        'Autónomo'),
  (7, 'Cliente 07', 'Sevilla',   'Autónomo'),
  (8, 'Cliente 08', 'Valencia',  'Pyme');

-- Bajas registradas; una se grabó sin cliente (NULL)
CREATE TABLE clientes_baja (
  id_cliente integer,
  fecha_baja date NOT NULL
);
INSERT INTO clientes_baja VALUES
  (8,    '2026-03-31'),
  (NULL, '2026-03-31');

CREATE TABLE productos (
  id_producto integer PRIMARY KEY,
  nombre      text NOT NULL,
  categoria   text NOT NULL
);
INSERT INTO productos VALUES
  (1, 'Producto A', 'Consumibles'),
  (2, 'Producto B', 'Equipos'),
  (3, 'Producto C', 'Consumibles'),
  (4, 'Producto D', 'Accesorios');

-- Cabecera: una fila por pedido. Los gastos de envío son del pedido, no de cada línea
CREATE TABLE pedidos (
  id_pedido    integer PRIMARY KEY,
  id_cliente   integer NOT NULL REFERENCES clientes,
  fecha        date    NOT NULL,
  gastos_envio numeric(10, 2) NOT NULL,
  estado       text    NOT NULL CHECK (estado IN ('completado', 'cancelado'))
);
INSERT INTO pedidos VALUES
  (101, 1, '2026-01-10',  5.00, 'completado'),
  (102, 2, '2026-01-15',  0.00, 'completado'),
  (103, 3, '2026-01-20',  7.50, 'completado'),
  (104, 1, '2026-02-03',  5.00, 'completado'),
  (105, 4, '2026-02-11', 12.00, 'completado'),
  (106, 5, '2026-02-19',  5.00, 'cancelado'),
  (107, 1, '2026-03-02',  5.00, 'completado'),
  (108, 6, '2026-03-08',  0.00, 'completado'),
  (109, 2, '2026-03-15',  9.00, 'completado'),
  (110, 7, '2026-03-27',  5.00, 'completado');

-- Detalle: varias líneas por pedido. Grano: una fila por línea de pedido
CREATE TABLE lineas_pedido (
  id_pedido   integer NOT NULL REFERENCES pedidos,
  num_linea   integer NOT NULL,
  id_producto integer NOT NULL REFERENCES productos,
  cantidad    integer NOT NULL,
  precio      numeric(10, 2) NOT NULL,
  PRIMARY KEY (id_pedido, num_linea)
);
INSERT INTO lineas_pedido VALUES
  (101, 1, 1,  2, 10.00), (101, 2, 2,  1, 25.00),
  (102, 1, 3,  5,  4.00),
  (103, 1, 1,  1, 10.00), (103, 2, 4,  3,  8.00), (103, 3, 2, 1, 25.00),
  (104, 1, 2,  2, 25.00),
  (105, 1, 1, 10,  9.50), (105, 2, 3, 10,  3.80),
  (106, 1, 4,  1,  8.00),
  (107, 1, 3,  2,  4.00), (107, 2, 4,  1,  8.00),
  (108, 1, 1,  3, 10.00),
  (109, 1, 2,  1, 25.00), (109, 2, 4,  2,  8.00),
  (110, 1, 3,  1,  4.00), (110, 2, 1,  1, 10.00);
