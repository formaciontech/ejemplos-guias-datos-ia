"""Datos sintéticos de clientes con semilla fija para los ejemplos de la guía.

Guía: https://formaciontech.es/guias/validar-modelo-machine-learning/

Problema inventado: «predecimos si un cliente contratará un producto para
decidir a quién llamar, y lo mediremos con la precisión de las llamadas».
La clase positiva es rara (en torno a un 6 %). Incluye a propósito:
- una variable con fuga (duracion_llamada_seg), que solo se conoce después
  de la llamada, es decir, después del resultado;
- varias filas por cliente (cliente_id) y una fecha, para GroupKFold y
  TimeSeriesSplit;
- un atributo sensible sintético (grupo), para medir la equidad;
- valores ausentes en saldo_medio, para el imputador.
"""

import numpy as np
import pandas as pd

SEMILLA = 42
VARIABLES = ["edad", "antiguedad_meses", "num_productos", "saldo_medio", "visitas_web_30d"]


def generar(n=6_000, semilla=SEMILLA):
    rng = np.random.default_rng(semilla)
    grupo = rng.choice(["A", "B"], n, p=[0.6, 0.4])
    edad = rng.integers(18, 76, n)
    antiguedad = rng.integers(0, 241, n)
    num_productos = rng.poisson(1.5, n) + 1
    # El saldo difiere algo entre grupos: puede actuar como proxy del atributo sensible
    saldo = rng.lognormal(mean=np.where(grupo == "A", 8.0, 7.7), sigma=0.8)
    visitas = rng.poisson(3, n)
    logit = (-7.6 + 0.32 * visitas + 0.45 * num_productos + 0.28 * np.log(saldo)
             - 0.012 * (edad - 45) + 0.002 * antiguedad)
    contrata = (rng.random(n) < 1 / (1 + np.exp(-logit))).astype(int)
    # Fuga: la duración de la llamada solo se conoce cuando la llamada termina
    duracion = np.where(contrata == 1, rng.gamma(9, 40, n), rng.gamma(3, 40, n)).round()
    saldo = np.where(rng.random(n) < 0.05, np.nan, saldo.round(2))
    df = pd.DataFrame({
        "cliente_id": rng.integers(0, 2_000, n),
        "fecha": pd.Timestamp("2025-01-01") + pd.to_timedelta(rng.integers(0, 547, n), unit="D"),
        "grupo": grupo,
        "edad": edad,
        "antiguedad_meses": antiguedad,
        "num_productos": num_productos,
        "saldo_medio": saldo,
        "visitas_web_30d": visitas,
        "duracion_llamada_seg": duracion,
        "contrata": contrata,
    })
    return df.sort_values("fecha", ignore_index=True)


def particion_temporal(df, corte="2026-04-01"):
    """Entrenamiento con el pasado y test con un periodo posterior (se abre una vez, al final)."""
    return df[df["fecha"] < corte].reset_index(drop=True), df[df["fecha"] >= corte].reset_index(drop=True)


if __name__ == "__main__":
    df = generar()
    print(df.head().to_string())
    print(f"\nFilas: {len(df):,}".replace(",", "."), "| tasa de positivos:", f"{df['contrata'].mean():.2%}")
