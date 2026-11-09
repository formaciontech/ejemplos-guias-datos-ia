"""La misma consulta con pandas, Polars (API lazy) y DuckDB, con cifras de control.

Guía: https://formaciontech.es/guias/python-o-r-analisis-datos/

Ventas netas y unidades por tienda en el primer trimestre de 2026. Si un
cálculo existe en varias herramientas, compara sus resultados: aquí se
comprueba que los tres coinciden. Ejecuta antes generar_datos.py.
"""

from pathlib import Path

import duckdb
import pandas as pd
import polars as pl

DATOS = Path(__file__).resolve().parent / "datos" / "ventas.parquet"
INICIO, FIN = "2026-01-01", "2026-04-01"

# 1) pandas: los datos caben holgadamente en memoria
ventas = pd.read_parquet(DATOS)
q1 = ventas[(ventas["fecha"] >= INICIO) & (ventas["fecha"] < FIN)]
r_pandas = (q1.groupby("tienda", as_index=False)
              .agg(unidades=("unidades", "sum"), importe=("importe", "sum"))
              .sort_values("tienda", ignore_index=True))

# 2) Polars lazy: construye un plan y lo optimiza antes de ejecutarlo;
#    filtra y elige columnas mientras lee el fichero
plan = (pl.scan_parquet(DATOS)
          .filter((pl.col("fecha") >= pl.datetime(2026, 1, 1)) & (pl.col("fecha") < pl.datetime(2026, 4, 1)))
          .group_by("tienda")
          .agg(pl.col("unidades").sum(), pl.col("importe").sum())
          .sort("tienda"))
print("Plan optimizado de Polars:\n", plan.explain(), "\n", sep="")
r_polars = plan.collect().to_pandas()

# 3) DuckDB: SQL sobre el DataFrame de pandas, por su nombre
r_duckdb = duckdb.sql(f"""
    SELECT tienda, SUM(unidades) AS unidades, SUM(importe) AS importe
    FROM ventas
    WHERE fecha >= DATE '{INICIO}' AND fecha < DATE '{FIN}'
    GROUP BY tienda
    ORDER BY tienda
""").df()

print(r_pandas.to_string(index=False))

# Cifras de control: las tres herramientas deben dar lo mismo
for nombre, r in [("Polars", r_polars), ("DuckDB", r_duckdb)]:
    pd.testing.assert_frame_equal(
        r_pandas.astype({"unidades": "int64", "importe": "float64", "tienda": "str"}),
        r.astype({"unidades": "int64", "importe": "float64", "tienda": "str"}),
        check_exact=False, rtol=1e-9,
    )
    print(f"pandas y {nombre} coinciden.")

r_pandas.to_csv(DATOS.parent / "resumen_python.csv", index=False)
