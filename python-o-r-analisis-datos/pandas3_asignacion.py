"""pandas 3: la asignación encadenada ya no modifica el DataFrame.

Guía: https://formaciontech.es/guias/python-o-r-analisis-datos/

Desde pandas 3.0 (enero de 2026) se aplica siempre «copy-on-write»:
df[neg]["tipo"] = ... trabaja sobre una copia y df no cambia. La forma
correcta es df.loc[filas, columna] = valor. Además, los textos usan por
defecto el tipo str.
"""

import warnings

import pandas as pd

df = pd.DataFrame({
    "producto": ["P01", "P02", "P03", "P04"],
    "unidades": [3, -1, 2, -2],
    "tipo": ["venta"] * 4,
})
print("pandas", pd.__version__)
print("Tipo de la columna de texto:", df["tipo"].dtype)

neg = df["unidades"] < 0

# No modifica df en pandas 3
with warnings.catch_warnings(record=True) as avisos:
    warnings.simplefilter("always")
    df[neg]["tipo"] = "devolución"
print("\nTras la asignación encadenada:", df["tipo"].tolist())
for a in avisos:
    print("  Aviso de pandas:", a.category.__name__)

# Forma correcta
df.loc[neg, "tipo"] = "devolución"
print("Tras df.loc[neg, 'tipo']:     ", df["tipo"].tolist())

assert df["tipo"].tolist() == ["venta", "devolución", "venta", "devolución"]
