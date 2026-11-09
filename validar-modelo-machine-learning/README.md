# Cómo validar un modelo de machine learning

Código de la guía [Cómo validar un modelo de machine learning antes de usarlo en tu empresa](https://formaciontech.es/guias/validar-modelo-machine-learning/), con un problema inventado: «predecimos si un cliente contratará un producto para decidir a quién llamar, y lo mediremos con la precisión de las llamadas».

**Última revisión: 9 de noviembre de 2026.**

## Qué hay

| Fichero | Qué muestra |
|---|---|
| `datos.py` | 6.000 filas sintéticas con semilla fija y un 5,88 % de positivos. Incluye a propósito una variable con fuga, varias filas por cliente, una fecha, un atributo sensible sintético y valores ausentes. |
| `01_referencia_y_validacion.py` | El pipeline de la guía con validación cruzada, comparado con `DummyClassifier` y con la regla de negocio; `StratifiedKFold`, `GroupKFold` y `TimeSeriesSplit`; y un test de un periodo posterior que se abre una sola vez. |
| `02_fugas_de_informacion.py` | Dos fugas: una variable posterior al resultado (la ROC-AUC salta de 0,705 a 0,969) y seleccionar variables antes de separar (0,792 con datos de puro ruido, frente a 0,439 dentro del pipeline). |
| `03_metricas_y_umbral.py` | La exactitud engañosa con clases raras (94,30 % diciendo siempre «no»), la matriz de confusión, ROC-AUC y PR-AUC, y el umbral elegido por costes con `TunedThresholdClassifierCV` en lugar de 0,5. |
| `04_explicabilidad_y_equidad.py` | Importancia por permutación con datos de validación, dependencia parcial (PDP) e ICE, métricas por grupo con `MetricFrame` de Fairlearn y comprobaciones de reproducibilidad (semilla, versiones, huella de los datos y modelo recargado). |

Los costes del ejemplo de umbral (5 € por llamada y 60 € por contratación) son inventados, solo para ilustrar el método.

## Cómo ejecutarlo

```bash
pip install -r requirements.txt
python 01_referencia_y_validacion.py
python 02_fugas_de_informacion.py
python 03_metricas_y_umbral.py
python 04_explicabilidad_y_equidad.py
```

## Qué se ha ejecutado

Los cuatro scripts, el 9 de noviembre de 2026, con Python 3.13, scikit-learn 1.9, pandas 3.1 y Fairlearn 0.15, en CPU y en pocos segundos. Las cifras citadas arriba son las de esa ejecución; con otras versiones de las librerías pueden variar ligeramente.

La guía menciona también SHAP y la ficha del modelo (model card). No se incluyen aquí: SHAP añade una dependencia pesada para un ejemplo corto, y la ficha depende del uso real del modelo.

## Fuentes

Son las de la guía:

- [scikit-learn: errores comunes y prácticas recomendadas](https://scikit-learn.org/stable/common_pitfalls.html)
- [scikit-learn: validación cruzada](https://scikit-learn.org/stable/modules/cross_validation.html)
- [scikit-learn: ajuste del umbral de decisión](https://scikit-learn.org/stable/modules/classification_threshold.html)
- [scikit-learn: importancia por permutación](https://scikit-learn.org/stable/modules/generated/sklearn.inspection.permutation_importance.html)
- [Fairlearn: evaluación de la equidad](https://fairlearn.org/main/user_guide/assessment)
