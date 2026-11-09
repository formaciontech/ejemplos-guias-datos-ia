#!/usr/bin/env bash
# Ejecuta todos los ejemplos en orden contra la base de datos indicada.
# Uso: ./ejecutar.sh nombre_bd   (usa las variables PGHOST, PGPORT y PGUSER si las defines)
set -euo pipefail
BD="${1:?Indica la base de datos: ./ejecutar.sh nombre_bd}"
cd "$(dirname "$0")"
for f in 00_esquema_y_datos.sql 01_null.sql 02_join_multiplica.sql 03_division_entera.sql \
         04_granularidad.sql 05_modelo_estrella.sql 06_tests_datos.sql; do
  echo "=== $f"
  psql -X -q -v ON_ERROR_STOP=1 -d "$BD" -f "$f"
done
