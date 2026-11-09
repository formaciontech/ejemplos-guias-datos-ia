-- Tests de datos: cada consulta devuelve los casos que incumplen una regla.
-- Si todo está bien, devuelve cero filas. Ejecútalos después de cada carga.
-- https://formaciontech.es/guias/sql-analisis-datos-empresa/
SET search_path TO guia_sql;

-- Test 1: la clave de pedidos es única
SELECT 'clave de pedido repetida' AS test, id_pedido::text AS caso
FROM pedidos GROUP BY id_pedido HAVING COUNT(*) > 1
UNION ALL
-- Test 2: no hay pedidos sin líneas
SELECT 'pedido sin líneas', p.id_pedido::text
FROM pedidos AS p
WHERE NOT EXISTS (SELECT 1 FROM lineas_pedido AS l WHERE l.id_pedido = p.id_pedido)
UNION ALL
-- Test 3: cantidades y precios positivos
SELECT 'cantidad o precio no positivo', id_pedido || '-' || num_linea
FROM lineas_pedido WHERE cantidad <= 0 OR precio <= 0
UNION ALL
-- Test 4: el importe del modelo cuadra con el de origen (pedidos completados)
SELECT 'el importe no cuadra', (SELECT SUM(importe) FROM hechos_ventas)::text
WHERE (SELECT SUM(importe) FROM hechos_ventas) IS DISTINCT FROM
      (SELECT SUM(l.cantidad * l.precio) FROM lineas_pedido AS l
         JOIN pedidos AS p ON p.id_pedido = l.id_pedido
        WHERE p.estado = 'completado');
-- Resultado: 0 filas

-- Informativo (no es un error): clientes sin ciudad
SELECT id_cliente, nombre FROM clientes WHERE ciudad IS NULL ORDER BY id_cliente;
-- Resultado: clientes 3 y 6
