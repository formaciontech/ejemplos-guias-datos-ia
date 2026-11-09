-- Error 1: tratar NULL como un valor más
-- https://formaciontech.es/guias/sql-analisis-datos-empresa/
SET search_path TO guia_sql;

-- Deja fuera los clientes sin ciudad
SELECT COUNT(*) AS fuera_de_valencia_con_distinto
FROM clientes
WHERE ciudad <> 'Valencia';
-- Resultado: 3 (Madrid, Barcelona y Sevilla)

-- Los incluye
SELECT COUNT(*) AS fuera_de_valencia_is_distinct_from
FROM clientes
WHERE ciudad IS DISTINCT FROM
      'Valencia';
-- Resultado: 5 (los tres anteriores y los dos clientes sin ciudad)

-- Cualquier comparación con NULL da «desconocido» (NULL), nunca verdadero
SELECT NULL = NULL AS igual_a_null, NULL IS NULL AS es_null;
-- Resultado: igual_a_null vacío (NULL), es_null verdadero

-- NOT IN: basta un NULL en la subconsulta para que no devuelva ninguna fila
SELECT COUNT(*) AS activos_con_not_in
FROM clientes
WHERE id_cliente NOT IN (SELECT id_cliente FROM clientes_baja);
-- Resultado: 0, aunque solo hay un cliente de baja

-- NOT EXISTS: «no está en la lista», sin sorpresas
SELECT COUNT(*) AS activos_con_not_exists
FROM clientes AS c
WHERE NOT EXISTS (
  SELECT 1 FROM clientes_baja AS b WHERE b.id_cliente = c.id_cliente
);
-- Resultado: 7

-- COUNT(columna) no cuenta los NULL; COUNT(*) cuenta todas las filas
SELECT COUNT(*) AS filas, COUNT(ciudad) AS con_ciudad
FROM clientes;
-- Resultado: 8 filas, 6 con ciudad
