# SQL para equipos de negocio y datos

Código de la guía [SQL para equipos de negocio y datos: qué deben saber y qué errores falsean las cifras](https://formaciontech.es/guias/sql-analisis-datos-empresa/), listo para ejecutar en PostgreSQL con datos sintéticos.

**Última revisión: 9 de noviembre de 2026.**

## Qué hay

| Fichero | Qué muestra |
|---|---|
| `00_esquema_y_datos.sql` | Crea el esquema `guia_sql` con clientes, bajas, productos, pedidos y líneas de pedido. Datos escritos a mano, pequeños para poder comprobarlos de cabeza. |
| `01_null.sql` | Error 1: `<>` deja fuera los NULL, `IS DISTINCT FROM` los incluye; `NOT IN` con un NULL no devuelve nada y `NOT EXISTS` sí; `COUNT(columna)` frente a `COUNT(*)`. |
| `02_join_multiplica.sql` | Error 2: los gastos de envío del pedido se repiten por línea (104,50 en lugar de 53,50) y cómo evitarlo agregando antes de unir. |
| `03_division_entera.sql` | Error 3: `7 / 2` da 3; una tasa de cancelación del 10 % sale 0 si se calcula con enteros. |
| `04_granularidad.sql` | Error 4: los clientes activos por mes no se suman (9 frente a 6 distintos) y el precio medio no se promedia sin más (11,61 frente a 8,85). |
| `05_modelo_estrella.sql` | Las cuatro decisiones del modelo en estrella, con vistas de hechos y dimensiones. |
| `06_tests_datos.sql` | Tests de datos: consultas que devuelven los casos que incumplen una regla; cero filas significa que todo está bien. |
| `ejecutar.sh` | Ejecuta todos los ficheros en orden. |

Cada consulta lleva debajo, en un comentario, el resultado que debe dar.

## Cómo ejecutarlo

Necesitas PostgreSQL (probado con la versión 16) y `psql`.

```bash
createdb guias                 # o usa una base de datos de pruebas que ya tengas
./ejecutar.sh guias            # en Windows: psql -d guias -f 00_esquema_y_datos.sql, y así con cada fichero
```

También puedes abrir los ficheros en DBeaver, pgAdmin o cualquier cliente y ejecutarlos uno a uno. Para limpiar: `DROP SCHEMA guia_sql CASCADE;`.

Ejecutado el 9 de noviembre de 2026 en PostgreSQL 16.15: todos los resultados coinciden con los comentarios y los tests devuelven cero filas.

## Fuentes

Son las de la guía:

- [PostgreSQL: funciones y operadores de comparación (NULL, IS DISTINCT FROM)](https://postgresql.org/docs/current/functions-comparison.html)
- [PostgreSQL: operadores matemáticos (división de enteros)](https://www.postgresql.org/docs/17/functions-math.html)
- [Microsoft Learn: el esquema en estrella y su importancia para Power BI](https://learn.microsoft.com/power-bi/guidance/star-schema)
