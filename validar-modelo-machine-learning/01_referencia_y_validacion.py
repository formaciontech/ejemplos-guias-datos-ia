"""Referencias y validación cruzada con el preprocesado dentro del pipeline.

Guía: https://formaciontech.es/guias/validar-modelo-machine-learning/

1. Compara siempre con una referencia: un modelo trivial (DummyClassifier)
   y la regla de negocio que ya se usa.
2. Valida el pipeline completo: la mediana y la escala se recalculan en cada
   partición sin mirar la validación.
3. Elige el esquema de partición según los datos: StratifiedKFold, GroupKFold
   o TimeSeriesSplit.
4. Reserva un test de un periodo posterior y ábrelo una sola vez, al final.
"""

from sklearn.dummy import DummyClassifier
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import roc_auc_score
from sklearn.model_selection import GroupKFold, StratifiedKFold, TimeSeriesSplit, cross_val_score
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler

from datos import VARIABLES, generar, particion_temporal

df = generar()
entreno, test = particion_temporal(df)
X_train, y_train = entreno[VARIABLES], entreno["contrata"]
X_test, y_test = test[VARIABLES], test["contrata"]
print(f"Entrenamiento: {len(entreno):,} filas · test (periodo posterior): {len(test):,} filas".replace(",", "."))

# El código de la guía
modelo = make_pipeline(
    SimpleImputer(strategy="median"),
    StandardScaler(),
    LogisticRegression(max_iter=1000),
)
auc = cross_val_score(
    modelo, X_train, y_train,
    cv=5, scoring="roc_auc",
)
print(f"\nPipeline, cv=5 (estratificada por defecto): ROC-AUC {auc.mean():.3f} ± {auc.std():.3f}")

# Referencias
dummy = cross_val_score(DummyClassifier(strategy="prior"), X_train, y_train, cv=5, scoring="roc_auc")
print(f"DummyClassifier:                           ROC-AUC {dummy.mean():.3f}")
regla = roc_auc_score(y_train, X_train["visitas_web_30d"])   # regla actual: llamar a quien más visita la web
print(f"Regla de negocio (visitas a la web):       ROC-AUC {regla:.3f}")

# Esquemas de partición
esquemas = {
    "StratifiedKFold": (StratifiedKFold(5, shuffle=True, random_state=42), None),
    "GroupKFold (por cliente)": (GroupKFold(5), entreno["cliente_id"]),
    "TimeSeriesSplit (pasado -> siguiente)": (TimeSeriesSplit(5), None),
}
print()
for nombre, (cv, grupos) in esquemas.items():
    s = cross_val_score(modelo, X_train, y_train, cv=cv, groups=grupos, scoring="roc_auc")
    print(f"{nombre:<40} ROC-AUC {s.mean():.3f} ± {s.std():.3f}")

# Test reservado: se abre una vez, al final, para confirmar el modelo elegido
modelo.fit(X_train, y_train)
print(f"\nTest del periodo posterior: ROC-AUC {roc_auc_score(y_test, modelo.predict_proba(X_test)[:, 1]):.3f}")
