"""Registro de experimentos y de modelos con MLflow, con alias en lugar de etapas.

Guía: https://formaciontech.es/guias/mlops-llevar-modelo-produccion/

- Lee la dirección del servidor de MLFLOW_TRACKING_URI: el mismo script vale
  en local y en un servidor de MLflow (también el gestionado de SageMaker AI).
  Si no está definida, usa una base de datos SQLite local (mlflow.db).
- Entrena tres versiones de un modelo de ejemplo con datos sintéticos,
  registra parámetros, métricas y el modelo, y crea tres versiones de
  «riesgo-impago» en el registro.
- Apunta el alias «champion» a la versión aprobada y la carga por su alias:
  el código de inferencia no cambia cuando cambia la versión.
"""

import os

import mlflow
import numpy as np
from mlflow import MlflowClient
from sklearn.datasets import make_classification
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import roc_auc_score
from sklearn.model_selection import train_test_split
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler

SEMILLA = 42
NOMBRE = "riesgo-impago"
mlflow.set_tracking_uri(os.environ.get("MLFLOW_TRACKING_URI", "sqlite:///mlflow.db"))
mlflow.set_experiment("guia-mlops")

# Datos sintéticos: 2.000 operaciones, un 10 % de impagos
X, y = make_classification(n_samples=2_000, n_features=8, n_informative=5, weights=[0.9],
                           random_state=SEMILLA)
X_tr, X_val, y_tr, y_val = train_test_split(X, y, test_size=0.3, stratify=y, random_state=SEMILLA)

for C in [0.01, 0.1, 1.0]:
    with mlflow.start_run(run_name=f"logreg-C{C}"):
        modelo = make_pipeline(StandardScaler(), LogisticRegression(C=C, max_iter=1000))
        modelo.fit(X_tr, y_tr)
        auc = roc_auc_score(y_val, modelo.predict_proba(X_val)[:, 1])
        mlflow.log_params({"C": C, "semilla": SEMILLA})
        mlflow.log_metric("roc_auc_validacion", auc)
        mlflow.sklearn.log_model(modelo, name="modelo", registered_model_name=NOMBRE,
                                 input_example=X_val[:2])
        print(f"C={C}: ROC-AUC de validación {auc:.4f}")

# El código de la guía: la versión 3 pasa a ser la aprobada
cliente = MlflowClient()
cliente.set_registered_model_alias(
    NOMBRE, "champion", 3)

modelo = mlflow.pyfunc.load_model(
    f"models:/{NOMBRE}@champion")

version = cliente.get_model_version_by_alias(NOMBRE, "champion")
cliente.set_model_version_tag(NOMBRE, version.version, "validacion", "aprobada")
print(f"\nAlias champion -> versión {version.version} de «{NOMBRE}»")
pred = np.asarray(modelo.predict(X_val))
print(f"Modelo cargado por alias: {int(pred.sum())} impagos previstos de {len(pred)} operaciones de validación")
