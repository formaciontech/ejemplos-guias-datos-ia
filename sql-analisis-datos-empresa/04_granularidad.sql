-- Error 4: mezclar granularidades
-- https://formaciontech.es/guias/sql-analisis-datos-empresa/
SET search_path TO guia_sql;

-- Medida semiaditiva: clientes activos por mes (solo pedidos completados)
-- Grano: una fila por mes
WITH activos_mes AS (
  SELECT date_trunc('month', fecha)::date AS mes,
         COUNT(DISTINCT id_cliente)       AS clientes_activos
  FROM pedidos
  WHERE estado = 'completado'
  GROUP BY 1
)
SELECT mes, clientes_activos FROM activos_mes ORDER BY mes;
-- Resultado: enero 3, febrero 2, marzo 4

-- MAL: sumar los meses cuenta varias veces al cliente que compra en varios meses
WITH activos_mes AS (
  SELECT date_trunc('month', fecha)::date AS mes,
         COUNT(DISTINCT id_cliente)       AS clientes_activos
  FROM pedidos
  WHERE estado = 'completado'
  GROUP BY 1
)
SELECT SUM(clientes_activos) AS suma_de_meses FROM activos_mes;
-- Resultado: 9 (el cliente 1 compra los tres meses y cuenta tres veces)

-- BIEN: contar clientes distintos en el periodo completo
SELECT COUNT(DISTINCT id_cliente) AS activos_trimestre
FROM pedidos
WHERE estado = 'completado'
  AND fecha >= '2026-01-01' AND fecha < '2026-04-01';
-- Resultado: 6

-- Medida no aditiva: el precio medio no se promedia sin más
-- MAL: media simple de los precios de cada línea
-- BIEN: guardar los componentes (importe y unidades) y calcular el ratio al final
SELECT ROUND(AVG(precio), 2)                              AS precio_medio_mal,
       ROUND(SUM(cantidad * precio) / SUM(cantidad), 2)  AS precio_medio_bien
FROM lineas_pedido;
-- Resultado: 11.61 frente a 8.85
