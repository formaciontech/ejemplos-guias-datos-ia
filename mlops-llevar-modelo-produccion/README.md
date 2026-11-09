# MLOps: llevar un modelo a producción y mantenerlo

Código de la guía [MLOps: cómo llevar un modelo de machine learning a producción y mantenerlo](https://formaciontech.es/guias/mlops-llevar-modelo-produccion/): el registro de modelos con alias de MLflow y el cálculo del PSI para vigilar la deriva.

**Última revisión: 9 de noviembre de 2026.**

## Qué hay

| Fichero | Qué muestra |
|---|---|
| `01_mlflow_registro.py` | Registra tres entrenamientos (parámetros, métricas y modelo) y tres versiones del modelo «riesgo-impago»; apunta el alias `champion` a la versión 3, como en la guía, y carga el modelo por su alias. Lee el servidor de `MLFLOW_TRACKING_URI`; si no está definida, usa una base de datos SQLite local. |
| `02_psi.py` | Función para calcular el PSI con tramos por cuantiles de la referencia y tres escenarios sintéticos: estable (0,002), vigilar (0,223) y deriva significativa (0,493), según la regla práctica de la guía. |

Los datos son sintéticos y se generan con semilla fija.

## Cómo ejecutarlo

```bash
pip install -r requirements.txt
python 02_psi.py
python 01_mlflow_registro.py
mlflow ui --backend-store-uri sqlite:///mlflow.db     # opcional: abre http://127.0.0.1:5000
```

El script de MLflow crea `mlflow.db` y la carpeta `mlruns/` (no se suben al repositorio). Si lo ejecutas varias veces, cada ejecución añade versiones nuevas; para empezar de cero, borra ambos. Para usar un servidor de MLflow, define antes la variable:

```bash
export MLFLOW_TRACKING_URI=https://tu-servidor-mlflow   # en Windows: set MLFLOW_TRACKING_URI=...
```

## Qué se ha ejecutado

Los dos scripts, el 9 de noviembre de 2026, con Python 3.13, MLflow 3.18 y scikit-learn 1.9, en local con SQLite y también con otra base de datos indicada en `MLFLOW_TRACKING_URI`.

## Qué no se incluye ni se ha ejecutado

La guía usa Amazon SageMaker AI como ejemplo (Pipelines, Model Registry, endpoints), además de Docker y OpenTofu. Son servicios de pago o necesitan una cuenta en la nube, así que no hay aquí código ejecutable para ellos. Las prácticas de la guía valen en cualquier plataforma: versionar código, datos y entorno; separar quién entrena, quién aprueba y quién despliega; desplegar desde el registro, y escribir las reglas de reentrenamiento.

## Fuentes

Son las de la guía:

- [AWS: Amazon SageMaker Pipelines](https://docs.aws.amazon.com/en_us/sagemaker/latest/dg/pipelines.html)
- [AWS: registro y despliegue con SageMaker Model Registry](https://docs.aws.amazon.com/us_en/sagemaker/latest/dg/model-registry.html)
- [AWS: cambio de disponibilidad de SageMaker Model Monitor](https://docs.aws.amazon.com/sagemaker/latest/dg/model-monitor-availability-change.html)
- [MLflow: flujos de trabajo del Model Registry (alias y versiones)](https://mlflow.org/docs/latest/ml/model-registry/workflow.html)
- [Documentación de OpenTofu](https://opentofu.org/docs/v1.13/)
