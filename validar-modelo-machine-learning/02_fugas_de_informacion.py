"""Dos fugas de información frecuentes y cómo se delatan.

Guía: https://formaciontech.es/guias/validar-modelo-machine-learning/

A. Una variable posterior al resultado: la duración de la llamada comercial.
   El modelo parece excelente en la evaluación y fracasaría en producción,
   porque al decidir a quién llamar ese dato aún no existe.
B. Preparar con todos los datos: seleccionar variables antes de separar
   entrenamiento y validación. Con variables de puro ruido, la selección
   fuera del pipeline da un resultado optimista; dentro, el real.
"""

import numpy as np
from sklearn.feature_selection import SelectKBest, f_classif
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import StratifiedKFold, cross_val_score
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler

from datos import VARIABLES, generar, particion_temporal

entreno, _ = particion_temporal(generar())
y = entreno["contrata"]
cv = StratifiedKFold(5, shuffle=True, random_state=42)


def pipeline():
    return make_pipeline(SimpleImputer(strategy="median"), StandardScaler(), LogisticRegression(max_iter=1000))


# A. Variable posterior al resultado
sin_fuga = cross_val_score(pipeline(), entreno[VARIABLES], y, cv=cv, scoring="roc_auc").mean()
con_fuga = cross_val_score(pipeline(), entreno[VARIABLES + ["duracion_llamada_seg"]], y, cv=cv, scoring="roc_auc").mean()
print("A. Variable posterior al resultado")
print(f"   Sin la duración de la llamada: ROC-AUC {sin_fuga:.3f}")
print(f"   Con la duración de la llamada: ROC-AUC {con_fuga:.3f}  <- demasiado bueno: sospecha")

# B. Selección de variables con todos los datos (2.000 variables de ruido, ninguna útil)
rng = np.random.default_rng(42)
X_ruido = rng.normal(size=(300, 2_000))
y_ruido = rng.integers(0, 2, 300)
mal = SelectKBest(f_classif, k=20).fit(X_ruido, y_ruido)          # mira también la validación
auc_mal = cross_val_score(LogisticRegression(max_iter=1000), mal.transform(X_ruido), y_ruido,
                          cv=cv, scoring="roc_auc").mean()
bien = make_pipeline(SelectKBest(f_classif, k=20), LogisticRegression(max_iter=1000))
auc_bien = cross_val_score(bien, X_ruido, y_ruido, cv=cv, scoring="roc_auc").mean()
print("\nB. Seleccionar variables antes de separar (datos de puro ruido)")
print(f"   Selección fuera del pipeline: ROC-AUC {auc_mal:.3f}  <- espejismo")
print(f"   Selección dentro del pipeline: ROC-AUC {auc_bien:.3f}  <- lo esperable: en torno a 0,5")
