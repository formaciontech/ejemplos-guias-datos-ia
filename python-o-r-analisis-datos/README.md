# ¿Python o R para el análisis de datos?

Código de la guía [¿Python o R para el análisis de datos en tu empresa? Cuándo elegir cada uno](https://formaciontech.es/guias/python-o-r-analisis-datos/): el cambio de pandas 3, la misma consulta con pandas, Polars y DuckDB, y la convivencia con R a través de Parquet.

**Última revisión: 9 de noviembre de 2026.**

## Qué hay

| Fichero | Qué muestra |
|---|---|
| `generar_datos.py` | Crea `datos/ventas.parquet` y `datos/ventas.csv`: 2.000 líneas de venta sintéticas con semilla fija. El Parquet ocupa unas seis veces menos que el CSV. |
| `pandas3_asignacion.py` | En pandas 3, `df[neg]["tipo"] = ...` no modifica el DataFrame (pandas avisa con `ChainedAssignmentError`); `df.loc[neg, "tipo"] = ...` sí. También que los textos usan por defecto el tipo `str`. |
| `tres_motores.py` | Ventas por tienda del primer trimestre con pandas, con la API lazy de Polars (muestra el plan optimizado) y con SQL de DuckDB sobre el DataFrame de pandas. Comprueba que las tres cifras coinciden. |
| `analisis.R` | La misma consulta en R con arrow y dplyr, leyendo el Parquet de Python, y la comparación con el resultado de Python. |

## Cómo ejecutarlo

```bash
python -m venv .venv
source .venv/bin/activate            # en Windows: .venv\Scripts\activate
pip install -r requirements.txt

python generar_datos.py
python pandas3_asignacion.py
python tres_motores.py
Rscript analisis.R                   # opcional: necesita R con los paquetes arrow y dplyr
```

Para fijar el entorno, como propone la guía:

```bash
# Python: con el entorno activado
python -m pip freeze > requirements-bloqueado.txt

# R: guardar las versiones y recuperarlas en otro equipo
Rscript -e 'renv::init()'       # una vez por proyecto
Rscript -e 'renv::snapshot()'
Rscript -e 'renv::restore()'
```

## Qué se ha ejecutado

El 9 de noviembre de 2026, con Python 3.13, pandas 3.1, Polars 2.1, DuckDB 2.0 y PyArrow 26: los tres scripts de Python se ejecutan sin errores y pandas, Polars y DuckDB dan las mismas cifras.

`analisis.R` **no se ha ejecutado** aquí porque el entorno de pruebas no tiene R. Está escrito con funciones estándar de arrow y dplyr; si encuentras algún problema, abre una incidencia.

## Fuentes

Son las de la guía:

- [pandas: novedades de la versión 3.0.0](https://pandas.pydata.org/docs/whatsnew/v3.0.0.html)
- [Polars: la API lazy](https://docs.pola.rs/user-guide/concepts/lazy-api/)
- [DuckDB: SQL sobre DataFrames de pandas](https://duckdb.org/docs/current/guides/python/sql_on_pandas)
- [tidyverse: paquetes](https://tidyverse.org/packages/)
- [renv: entornos reproducibles para R](https://rstudio.github.io/renv/)
- [Python: venv, creación de entornos virtuales](https://docs.python.org/library/venv.html)
- [Quarto: parámetros](https://www.quarto.org/docs/computations/parameters.html)
