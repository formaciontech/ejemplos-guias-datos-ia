-- El modelo en estrella: diseñar para que sea difícil equivocarse
-- https://formaciontech.es/guias/sql-analisis-datos-empresa/
--
-- Las cuatro decisiones, en este orden:
--   1. Proceso de negocio: las ventas.
--   2. Grano: una fila de hechos por línea de pedido completado.
--   3. Dimensiones: fecha, cliente y producto.
--   4. Medidas: unidades e importe (aditivas). Los gastos de envío son del
--      pedido, no de la línea, así que NO van en esta tabla de hechos.
SET search_path TO guia_sql;

DROP VIEW IF EXISTS hechos_ventas, dim_fecha, dim_cliente, dim_producto;

CREATE VIEW dim_cliente AS
SELECT id_cliente, nombre, COALESCE(ciudad, 'Sin ciudad') AS ciudad, segmento
FROM clientes;

CREATE VIEW dim_producto AS
SELECT id_producto, nombre, categoria
FROM productos;

CREATE VIEW dim_fecha AS
SELECT d::date                      AS fecha,
       EXTRACT(YEAR FROM d)::int    AS anio,
       EXTRACT(MONTH FROM d)::int   AS mes,
       'T' || EXTRACT(QUARTER FROM d)::int AS trimestre
FROM generate_series('2026-01-01'::date, '2026-12-31'::date, interval '1 day') AS d;

-- Grano: una fila por línea de pedido completado
CREATE VIEW hechos_ventas AS
SELECT p.fecha, p.id_cliente, l.id_producto, l.id_pedido, l.num_linea,
       l.cantidad              AS unidades,
       l.cantidad * l.precio   AS importe
FROM lineas_pedido AS l
JOIN pedidos AS p ON p.id_pedido = l.id_pedido
WHERE p.estado = 'completado';

-- Las dimensiones filtran y agrupan; los hechos se resumen
SELECT f.mes, c.segmento,
       SUM(h.unidades) AS unidades,
       SUM(h.importe)  AS importe
FROM hechos_ventas AS h
JOIN dim_fecha   AS f ON f.fecha = h.fecha
JOIN dim_cliente AS c ON c.id_cliente = h.id_cliente
GROUP BY f.mes, c.segmento
ORDER BY f.mes, c.segmento;
-- Resultado: 7 filas; el importe total (408.00) excluye el pedido cancelado
