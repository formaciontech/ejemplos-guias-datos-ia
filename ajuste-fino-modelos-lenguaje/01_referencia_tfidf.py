"""Referencia sencilla antes de ajustar nada: TF-IDF con regresión logística.

Guía: https://formaciontech.es/guias/ajuste-fino-modelos-lenguaje/

Cubre los pasos de evaluación de la guía que no necesitan GPU:
1. Una referencia sencilla con la que comparar el modelo ajustado.
2. Métricas por clase: un buen F1 global puede esconder una clase que falla.
3. Intervalo de confianza por bootstrap: con pocos casos, uno o dos puntos
   de diferencia pueden ser azar.
4. Calibración: importa si la probabilidad decide qué pasa a revisión humana.
5. Robustez: textos sin tildes y con erratas.
Tres particiones separadas: entrenamiento, validación y prueba (al final).
"""

import random

import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import brier_score_loss, classification_report, f1_score
from sklearn.model_selection import train_test_split
from sklearn.pipeline import make_pipeline

from datos_textos import SEMILLA, con_erratas, generar, sin_tildes

textos, etiquetas = generar()
X_tmp, X_test, y_tmp, y_test = train_test_split(textos, etiquetas, test_size=0.2, stratify=etiquetas,
                                                random_state=SEMILLA)
X_tr, X_val, y_tr, y_val = train_test_split(X_tmp, y_tmp, test_size=0.25, stratify=y_tmp, random_state=SEMILLA)
print(f"Entrenamiento {len(X_tr)} · validación {len(X_val)} · prueba {len(X_test)}")

# Las tildes se normalizan en el propio vectorizador
referencia = make_pipeline(
    TfidfVectorizer(ngram_range=(1, 2), sublinear_tf=True, strip_accents="unicode"),
    LogisticRegression(max_iter=2000, C=4.0),
)
referencia.fit(X_tr, y_tr)
print(f"F1 macro en validación: {f1_score(y_val, referencia.predict(X_val), average='macro'):.3f}")

# La prueba se mira una sola vez, al final
pred = referencia.predict(X_test)
print("\nMétricas por clase en la prueba:")
print(classification_report(y_test, pred, digits=3))

# Intervalo de confianza del F1 macro por bootstrap
rng = np.random.default_rng(SEMILLA)
y_arr, p_arr = np.array(y_test), np.array(pred)
muestras = [f1_score(y_arr[i], p_arr[i], average="macro")
            for i in (rng.integers(0, len(y_arr), len(y_arr)) for _ in range(1_000))]
bajo, alto = np.percentile(muestras, [2.5, 97.5])
print(f"F1 macro: {f1_score(y_test, pred, average='macro'):.3f} (IC 95 % por bootstrap: {bajo:.3f}–{alto:.3f})")

# Calibración: puntuación de Brier por clase (más baja, mejor)
proba = referencia.predict_proba(X_test)
brier = {str(c): brier_score_loss(np.array(y_test) == c, proba[:, i]) for i, c in enumerate(referencia.classes_)}
print("Brier por clase:", {c: round(b, 4) for c, b in brier.items()})

# Robustez: los mismos textos de prueba sin tildes y con erratas
rnd = random.Random(SEMILLA)
for nombre, variante in [("sin tildes", [sin_tildes(t) for t in X_test]),
                         ("con erratas", [con_erratas(t, rnd) for t in X_test])]:
    print(f"F1 macro {nombre}: {f1_score(y_test, referencia.predict(variante), average='macro'):.3f}")
