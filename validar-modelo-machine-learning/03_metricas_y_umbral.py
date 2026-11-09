"""Métricas según el negocio, clases desequilibradas y elección del umbral.

Guía: https://formaciontech.es/guias/validar-modelo-machine-learning/

- Con una clase rara, la exactitud engaña: decir siempre «no» acierta mucho.
- Lee la matriz de confusión: cada error tiene un coste distinto.
- El umbral de 0,5 no tiene nada de especial. Aquí se elige con costes y
  beneficios inventados para el ejemplo y con TunedThresholdClassifierCV.
"""

import numpy as np
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (accuracy_score, average_precision_score, confusion_matrix, make_scorer,
                             precision_score, recall_score, roc_auc_score)
from sklearn.model_selection import TunedThresholdClassifierCV, train_test_split
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler

from datos import VARIABLES, generar, particion_temporal

entreno, _ = particion_temporal(generar())
X_tr, X_val, y_tr, y_val = train_test_split(entreno[VARIABLES], entreno["contrata"], test_size=0.3,
                                            stratify=entreno["contrata"], random_state=42)

# Costes del ejemplo: una llamada cuesta 5 € y una contratación aporta 60 €
COSTE_LLAMADA, BENEFICIO = 5.0, 60.0


def euros(x):
    """Formato español: punto de miles y coma decimal."""
    return f"{x:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".") + " €"


def beneficio(y, pred):
    tn, fp, fn, tp = confusion_matrix(y, pred, labels=[0, 1]).ravel()
    return tp * (BENEFICIO - COSTE_LLAMADA) - fp * COSTE_LLAMADA


modelo = make_pipeline(SimpleImputer(strategy="median"), StandardScaler(), LogisticRegression(max_iter=1000))
modelo.fit(X_tr, y_tr)
proba = modelo.predict_proba(X_val)[:, 1]

print(f"Tasa de positivos en validación: {y_val.mean():.2%}")
print(f"Exactitud de decir siempre «no»: {accuracy_score(y_val, np.zeros_like(y_val)):.2%}  <- engaña")
print(f"ROC-AUC {roc_auc_score(y_val, proba):.3f} · PR-AUC {average_precision_score(y_val, proba):.3f} "
      f"(referencia de PR-AUC: la tasa de positivos)")

for nombre, umbral in [("Umbral 0,5", 0.5)]:
    pred = (proba >= umbral).astype(int)
    print(f"\n{nombre}: matriz de confusión [[VN FP] [FN VP]] = {confusion_matrix(y_val, pred).tolist()}")
    print(f"   precisión {precision_score(y_val, pred, zero_division=0):.2f} · exhaustividad "
          f"{recall_score(y_val, pred):.2f} · beneficio {euros(beneficio(y_val, pred))}")

# Umbral ajustado con validación cruzada sobre el entrenamiento, maximizando el beneficio
ajustado = TunedThresholdClassifierCV(modelo, scoring=make_scorer(beneficio), cv=5, random_state=42)
ajustado.fit(X_tr, y_tr)
pred = ajustado.predict(X_val)
print(f"\nUmbral elegido por costes: {ajustado.best_threshold_:.3f}")
print(f"   matriz de confusión = {confusion_matrix(y_val, pred).tolist()}")
print(f"   precisión {precision_score(y_val, pred, zero_division=0):.2f} · exhaustividad "
      f"{recall_score(y_val, pred):.2f} · beneficio {euros(beneficio(y_val, pred))}")
