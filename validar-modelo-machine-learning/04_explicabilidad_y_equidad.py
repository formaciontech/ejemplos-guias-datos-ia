"""Explicabilidad global y local aproximada, equidad por grupos y reproducibilidad.

Guía: https://formaciontech.es/guias/validar-modelo-machine-learning/

- Importancia por permutación, calculada con datos de validación.
- Dependencia parcial (PDP) e ICE de una variable, en números.
- Equidad: métricas por grupo con MetricFrame de Fairlearn. El atributo
  sensible no entra en el modelo, pero otras variables pueden actuar de proxy.
- Reproducibilidad: semillas, versiones, huella de los datos y comprobación
  de que el modelo recargado da las mismas predicciones.
"""

import hashlib
import pickle
import platform

import numpy as np
import pandas as pd
import sklearn
from fairlearn.metrics import MetricFrame, selection_rate
from sklearn.ensemble import HistGradientBoostingClassifier
from sklearn.inspection import partial_dependence, permutation_importance
from sklearn.metrics import recall_score, roc_auc_score
from sklearn.model_selection import train_test_split

from datos import SEMILLA, VARIABLES, generar, particion_temporal

entreno, _ = particion_temporal(generar())
X_tr, X_val, y_tr, y_val, g_tr, g_val = train_test_split(
    entreno[VARIABLES].astype(float), entreno["contrata"], entreno["grupo"],
    test_size=0.3, stratify=entreno["contrata"], random_state=SEMILLA)

modelo = HistGradientBoostingClassifier(max_depth=3, learning_rate=0.05, max_iter=200, random_state=SEMILLA)
modelo.fit(X_tr, y_tr)
proba = modelo.predict_proba(X_val)[:, 1]
print(f"ROC-AUC en validación: {roc_auc_score(y_val, proba):.3f}")

# Importancia por permutación (con validación, no con entrenamiento)
imp = permutation_importance(modelo, X_val, y_val, scoring="roc_auc", n_repeats=10, random_state=SEMILLA)
tabla = pd.DataFrame({"variable": VARIABLES, "caida_auc": imp.importances_mean, "desv": imp.importances_std})
print("\nImportancia por permutación (caída de ROC-AUC al desordenar cada variable):")
print(tabla.sort_values("caida_auc", ascending=False).round(4).to_string(index=False))

# PDP e ICE: cómo cambia la predicción al mover una variable
pd_res = partial_dependence(modelo, X_val, ["visitas_web_30d"], kind="both", grid_resolution=6)
rejilla = pd_res["grid_values"][0]
print("\nDependencia parcial de visitas_web_30d (probabilidad media):")
for v, p in zip(rejilla, pd_res["average"][0]):
    print(f"   {v:>4.0f} visitas -> {p:.3f}")
print(f"   ICE: {pd_res['individual'][0].shape[0]} curvas individuales calculadas")

# Equidad por grupo, con un umbral de decisión de ejemplo
UMBRAL = 0.15
pred = (proba >= UMBRAL).astype(int)
mf = MetricFrame(metrics={"tasa_seleccion": selection_rate, "exhaustividad": recall_score},
                 y_true=y_val, y_pred=pred, sensitive_features=g_val)
print(f"\nMétricas por grupo (umbral {UMBRAL}):")
print(mf.by_group.round(3).to_string())
print("Diferencia máxima entre grupos:", mf.difference().round(3).to_dict())

# Reproducibilidad: huella de los datos, versiones y modelo recargado
huella = hashlib.sha256(pd.util.hash_pandas_object(entreno, index=True).values.tobytes()).hexdigest()
recargado = pickle.loads(pickle.dumps(modelo))
iguales = np.array_equal(recargado.predict_proba(X_val), modelo.predict_proba(X_val))
print("\nReproducibilidad")
print(f"   Semilla: {SEMILLA} · Python {platform.python_version()} · scikit-learn {sklearn.__version__}")
print(f"   Huella SHA-256 de los datos de entrenamiento: {huella[:16]}…")
print(f"   El modelo recargado da las mismas predicciones: {iguales}")
