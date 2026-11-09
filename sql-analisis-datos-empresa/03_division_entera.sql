-- Error 3: la división entera
-- https://formaciontech.es/guias/sql-analisis-datos-empresa/
SET search_path TO guia_sql;

SELECT 7 / 2;
-- 3
SELECT 7::numeric / 2;
-- 3.5000000000000000

-- Un ratio calculado con enteros sale truncado sin aviso
SELECT
  COUNT(*) FILTER (WHERE estado = 'cancelado') / COUNT(*)                     AS tasa_cancelacion_entera,
  CAST(COUNT(*) FILTER (WHERE estado = 'cancelado') AS NUMERIC) / COUNT(*)    AS tasa_cancelacion,
  ROUND(100.0 * COUNT(*) FILTER (WHERE estado = 'cancelado') / COUNT(*), 2)   AS porcentaje
FROM pedidos;
-- Resultado: 0 | 0.10000000000000000000 | 10.00

-- Para una media, usa AVG
SELECT SUM(cantidad) / COUNT(*) AS media_entera,
       AVG(cantidad)            AS media_avg
FROM lineas_pedido;
-- Resultado: 2 | 2.7647058823529412
