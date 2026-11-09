# Ejemplos de las guías de datos e IA

El código de las seis guías técnicas de [formaciontech.es](https://formaciontech.es/guias/), organizado por guía, con datos sintéticos generados con semilla fija y listo para ejecutar.

**Última revisión: 9 de noviembre de 2026.**

| Carpeta | Guía | Qué incluye |
|---|---|---|
| [`sql-analisis-datos-empresa/`](sql-analisis-datos-empresa/) | [SQL para equipos de negocio y datos](https://formaciontech.es/guias/sql-analisis-datos-empresa/) | Los cuatro errores que falsean las cifras (NULL, JOIN que duplica, división entera y granularidad), el modelo en estrella y tests de datos, en PostgreSQL. |
| [`python-o-r-analisis-datos/`](python-o-r-analisis-datos/) | [¿Python o R para el análisis de datos?](https://formaciontech.es/guias/python-o-r-analisis-datos/) | La asignación encadenada en pandas 3, la misma consulta con pandas, Polars y DuckDB, y la versión en R con arrow y dplyr. |
| [`validar-modelo-machine-learning/`](validar-modelo-machine-learning/) | [Cómo validar un modelo de machine learning](https://formaciontech.es/guias/validar-modelo-machine-learning/) | Referencias, validación cruzada con pipeline, fugas de información, métricas y umbral por costes, explicabilidad, equidad por grupos y reproducibilidad. |
| [`ajuste-fino-modelos-lenguaje/`](ajuste-fino-modelos-lenguaje/) | [Fine-tuning de modelos de lenguaje](https://formaciontech.es/guias/ajuste-fino-modelos-lenguaje/) | Referencia TF-IDF con evaluación completa, LoRA con PEFT en CPU sobre un modelo diminuto y QLoRA para GPU. |
| [`mlops-llevar-modelo-produccion/`](mlops-llevar-modelo-produccion/) | [MLOps: llevar un modelo a producción](https://formaciontech.es/guias/mlops-llevar-modelo-produccion/) | Registro de modelos con alias en MLflow y cálculo del PSI para vigilar la deriva. |
| [`rag-asistente-documentos-empresa/`](rag-asistente-documentos-empresa/) | [Asistente con RAG sobre documentos de empresa](https://formaciontech.es/guias/rag-asistente-documentos-empresa/) | Ingesta, troceado, búsqueda híbrida con permisos, citas, guardarraíles y evaluación de la recuperación. |

Cada carpeta tiene su README, con lo que hace cada fichero, cómo ejecutarlo, qué se ha probado y las fuentes de la guía, y su `requirements.txt` con versiones mínimas.

## Cómo empezar

Necesitas Python 3.10 o superior (probado con 3.13) y, para la guía de SQL, PostgreSQL.

```bash
python -m venv .venv
source .venv/bin/activate            # en Windows: .venv\Scripts\activate
cd validar-modelo-machine-learning   # o la carpeta que te interese
pip install -r requirements.txt
python 01_referencia_y_validacion.py
```

## Qué se ha ejecutado y qué no

Todo se ha ejecutado el 9 de noviembre de 2026 en un entorno limpio, en CPU, salvo lo que necesita GPU, servicios de pago o software que no estaba disponible:

| Qué | Estado |
|---|---|
| SQL (PostgreSQL 16) | Ejecutado; resultados anotados en cada consulta. |
| Python: pandas, Polars, DuckDB | Ejecutado; las tres herramientas dan las mismas cifras. |
| R (`analisis.R`) | No ejecutado: el entorno de pruebas no tenía R. |
| Validación de modelos | Ejecutado. |
| Referencia TF-IDF y LoRA en CPU | Ejecutado. |
| QLoRA (`03_qlora_gpu.py`) | No ejecutado: necesita GPU. |
| MLflow con SQLite y PSI | Ejecutado. |
| SageMaker AI, Docker, OpenTofu | Sin código ejecutable: necesitan una cuenta en la nube. |
| RAG: recuperación, guardarraíles y evaluación | Ejecutado. |
| RAG: llamada al modelo y métricas con LLM evaluador | No ejecutado: servicio de pago; se deja preparado. |

Los datos son sintéticos: se generan con semilla fija o están escritos a mano, y no proceden de ninguna organización real. Los documentos de la carpeta de RAG son de una empresa ficticia.

## Licencia

- Código: [MIT](LICENSE).
- Datos sintéticos, documentos de ejemplo y textos de los README: [CC BY 4.0](LICENSE-CC-BY-4.0.txt) ([resumen en español](https://creativecommons.org/licenses/by/4.0/deed.es)). Cita «José María Arroyo Sánchez · FormacionTech (https://formaciontech.es)».

© 2026 José María Arroyo Sánchez · FormacionTech · [formaciontech.es](https://formaciontech.es)
