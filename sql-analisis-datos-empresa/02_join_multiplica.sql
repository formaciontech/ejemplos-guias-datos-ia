-- Error 2: un JOIN que multiplica filas
-- https://formaciontech.es/guias/sql-analisis-datos-empresa/
SET search_path TO guia_sql;

-- Cuenta las filas antes y después del JOIN
SELECT
  (SELECT COUNT(*) FROM pedidos) AS filas_pedidos,
  (SELECT COUNT(*) FROM pedidos AS p
     JOIN lineas_pedido AS l ON l.id_pedido = p.id_pedido) AS filas_tras_join;
-- Resultado: 10 y 17. Si las filas aumentan, revisa qué medidas sumas después

-- MAL: los gastos de envío del pedido se repiten una vez por línea
SELECT SUM(p.gastos_envio)         AS envio,
       SUM(l.cantidad * l.precio)  AS importe
FROM pedidos AS p
JOIN lineas_pedido AS l
  ON l.id_pedido = p.id_pedido;
-- Resultado: envio 104.50 (inflado) e importe 416.00

-- BIEN: agrega primero el detalle al nivel de la cabecera y une después
-- Grano: una fila por pedido
WITH lineas AS (
  SELECT id_pedido,
    SUM(cantidad * precio) AS importe
  FROM lineas_pedido
  GROUP BY id_pedido
)
SELECT SUM(p.gastos_envio) AS envio,
       SUM(l.importe) AS importe
FROM pedidos AS p
JOIN lineas AS l
  ON l.id_pedido = p.id_pedido;
-- Resultado: envio 53.50 (correcto) e importe 416.00
-- Ambos importes incluyen el pedido cancelado 106: para ventas reales, filtra por estado

-- Comprobación: la clave del lado «uno» debe ser única (cero filas = correcto)
SELECT id_pedido, COUNT(*) AS veces
FROM pedidos
GROUP BY id_pedido
HAVING COUNT(*) > 1;
-- Resultado: 0 filas
