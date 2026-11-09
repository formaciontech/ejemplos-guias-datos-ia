# Asistente con RAG sobre documentos de empresa

Código de la guía [Cómo crear un asistente con RAG sobre los documentos de tu empresa](https://formaciontech.es/guias/rag-asistente-documentos-empresa/): ingesta con metadatos, troceado, búsqueda híbrida con permisos, prompt con citas, guardarraíles y evaluación de la recuperación. Todo funciona en local y sin servicios de pago, salvo la llamada al modelo de lenguaje, que se deja preparada.

**Última revisión: 9 de noviembre de 2026.**

> Contenido técnico e informativo; no es asesoramiento jurídico.

## Qué hay

| Fichero | Qué muestra |
|---|---|
| `documentos/` | Cuatro documentos de una empresa ficticia, con metadatos de fuente, fecha, vigencia y nivel de acceso. Uno está obsoleto y otro es de acceso restringido. |
| `rag.py` | Ingesta (descarta lo no vigente), troceado por encabezados y con el troceador recursivo de la guía, BM25 más vectores fusionados con Reciprocal Rank Fusion, y permisos aplicados antes de recuperar. |
| `respuesta.py` | Guardarraíles de entrada (longitud, inyección de prompts, datos personales), el prompt que pide responder solo con los fragmentos y citarlos, y la validación con código de la salida (citas que existen, cifras presentes en la fuente, datos personales). |
| `evaluar.py` | Evaluación exacta de la recuperación con `preguntas_referencia.json`: acierto@1, acierto@3, MRR, fugas de permisos y documentos obsoletos indexados. |
| `preguntas_referencia.json` | Once preguntas con su fuente y sección esperadas, incluida una de permisos y otra sin respuesta en la documentación. |

## Cómo ejecutarlo

```bash
pip install -r requirements.txt
python rag.py "¿Qué día hay que ir a la oficina?"
python rag.py "¿Cómo se calcula el variable del comité de dirección?" direccion
python respuesta.py
python evaluar.py
```

## Qué se ha ejecutado

Los tres scripts, el 9 de noviembre de 2026, con Python 3.13, langchain-text-splitters 1.1, rank-bm25 0.2.2 y scikit-learn 1.9. Resultado de `evaluar.py`: acierto@1 del 89 %, acierto@3 del 100 % y MRR de 0,944 en las nueve preguntas con respuesta; cero fugas de permisos y cero documentos obsoletos indexados.

## Qué no se ha ejecutado

- **La llamada al modelo de lenguaje.** `llamar_modelo()` está vacía a propósito: depende del proveedor y del contrato de tu organización. Antes de enviar documentos reales, revisa con Seguridad y Protección de Datos la región de procesamiento, el uso para entrenar y la retención. `respuesta.py` valida dos respuestas escritas a mano para enseñar los guardarraíles de salida sin llamar a ningún servicio.
- **Embeddings reales.** Para no descargar modelos, los vectores son TF-IDF de n-gramas de caracteres reducido con SVD. En un proyecto real, usa un modelo de embeddings, el mismo para indexar y para consultar, y una base vectorial ligera como Chroma para empezar.
- **Métricas con un LLM evaluador**, como la fidelidad de Ragas, ni el reordenador. Necesitan un modelo. Si las añades, fija la versión de Ragas y del modelo evaluador para que las puntuaciones sean comparables.

Los patrones de datos personales y de inyección de `respuesta.py` son ejemplos mínimos, no una protección completa. Usa el OWASP Top 10 para aplicaciones con LLM como lista de revisión y mide los falsos positivos de cada guardarraíl.

## Fuentes

Son las de la guía:

- [Ragas: métrica de fidelidad (faithfulness)](https://docs.ragas.io/en/stable/concepts/metrics/available_metrics/faithfulness/)
- [OWASP Gen AI Security Project: Top 10 para LLM y IA generativa](https://genai.owasp.org/initiative/owasp-top-10-for-llm-and-genai/)
- [OWASP GenAI LLM Top 10 2026](https://genai.owasp.org/resource/owasp-genai-llm-top-10-2026/)
