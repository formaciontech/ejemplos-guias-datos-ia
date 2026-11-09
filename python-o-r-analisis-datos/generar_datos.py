"""Genera datos sintéticos de ventas con semilla fija (siempre los mismos).

Guía: https://formaciontech.es/guias/python-o-r-analisis-datos/

Crea datos/ventas.parquet y datos/ventas.csv: 2.000 líneas de venta inventadas,
con algunas devoluciones (unidades negativas). Parquet es el formato de
intercambio entre Python y R que propone la guía: guarda los tipos y ocupa
menos que el CSV.
"""

from pathlib import Path

import numpy as np
import pandas as pd

SEMILLA = 42
N = 2_000
CARPETA = Path(__file__).resolve().parent / "datos"


def generar(n=N, semilla=SEMILLA):
    rng = np.random.default_rng(semilla)
    tiendas = np.array(["Norte", "Sur", "Este", "Oeste"])
    productos = np.array(["P01", "P02", "P03", "P04", "P05"])
    precios = dict(zip(productos, [4.5, 12.0, 25.0, 7.9, 60.0]))
    prod = rng.choice(productos, n)
    unidades = rng.integers(1, 6, n)
    devolucion = rng.random(n) < 0.04          # un 4 % de líneas son devoluciones
    unidades = np.where(devolucion, -unidades, unidades)
    df = pd.DataFrame({
        "fecha": pd.to_datetime("2026-01-01") + pd.to_timedelta(rng.integers(0, 181, n), unit="D"),
        "tienda": rng.choice(tiendas, n),
        "producto": prod,
        "unidades": unidades,
        "precio": [precios[p] for p in prod],
    })
    df["importe"] = (df["unidades"] * df["precio"]).round(2)
    return df.sort_values(["fecha", "tienda", "producto"], ignore_index=True)


if __name__ == "__main__":
    CARPETA.mkdir(exist_ok=True)
    df = generar()
    df.to_parquet(CARPETA / "ventas.parquet", index=False)
    df.to_csv(CARPETA / "ventas.csv", index=False)
    print(f"{len(df):,} filas".replace(",", "."), "guardadas en", CARPETA)
    print("Tamaño: Parquet", (CARPETA / "ventas.parquet").stat().st_size, "bytes; CSV",
          (CARPETA / "ventas.csv").stat().st_size, "bytes")
