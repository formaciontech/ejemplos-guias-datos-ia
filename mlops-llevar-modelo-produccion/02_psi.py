"""PSI (Population Stability Index) para vigilar la deriva de datos.

Guía: https://formaciontech.es/guias/mlops-llevar-modelo-produccion/

PSI = suma de (actual - referencia) * ln(actual / referencia) por tramos.
Los tramos se fijan con los cuantiles de la referencia (los datos de
entrenamiento). Regla práctica habitual: menos de 0,10, estable; entre 0,10
y 0,25, vigilar; más de 0,25, deriva significativa. Los umbrales definitivos
dependen de tu modelo.
"""

import numpy as np


def psi(referencia, actual, tramos=10, eps=1e-6):
    cortes = np.quantile(referencia, np.linspace(0, 1, tramos + 1))
    cortes[0], cortes[-1] = -np.inf, np.inf
    ref = np.histogram(referencia, cortes)[0] / len(referencia)
    act = np.histogram(actual, cortes)[0] / len(actual)
    ref, act = np.clip(ref, eps, None), np.clip(act, eps, None)
    return float(np.sum((act - ref) * np.log(act / ref)))


def lectura(valor):
    return "estable" if valor < 0.10 else ("vigilar" if valor <= 0.25 else "deriva significativa")


if __name__ == "__main__":
    rng = np.random.default_rng(42)
    entrenamiento = rng.normal(600, 50, 20_000)          # puntuación en el entrenamiento
    escenarios = {
        "Mes 1 (igual que el entrenamiento)": rng.normal(600, 50, 5_000),
        "Mes 2 (desplazamiento moderado)": rng.normal(625, 55, 5_000),
        "Mes 3 (cambio de población)": rng.normal(640, 60, 5_000),
    }
    for nombre, datos in escenarios.items():
        v = psi(entrenamiento, datos)
        print(f"{nombre:<38} PSI = {v:.3f} -> {lectura(v)}")
