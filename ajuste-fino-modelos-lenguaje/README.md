# Fine-tuning de modelos de lenguaje

Código de la guía [Fine-tuning de modelos de lenguaje: cuándo compensa ajustar un modelo y cuándo no](https://formaciontech.es/guias/ajuste-fino-modelos-lenguaje/): la referencia con la que comparar, la evaluación que pide la guía y la configuración de LoRA y QLoRA con PEFT.

**Última revisión: 9 de noviembre de 2026.**

## Qué hay

| Fichero | Qué muestra | ¿Ejecutado? |
|---|---|---|
| `datos_textos.py` | 1.000 reclamaciones sintéticas en cuatro categorías que comparten vocabulario, con un 6 % de frases ambiguas y un 8 % de etiquetas erróneas, como en un corpus real. | Sí |
| `01_referencia_tfidf.py` | La referencia sencilla de la guía (TF-IDF con regresión logística) y su evaluación: tres particiones, métricas por clase, intervalo de confianza por bootstrap, calibración (Brier) y robustez con textos sin tildes y con erratas. | Sí, en CPU |
| `02_lora_cpu.py` | El código LoRA de la guía sobre un modelo tipo Llama diminuto creado en local con pesos aleatorios: nombres de los módulos, parámetros entrenables, unos pasos de entrenamiento y fusión del adaptador. | Sí, en CPU |
| `03_qlora_gpu.py` | QLoRA: el modelo base en 4 bits (NF4) con bitsandbytes y la misma configuración LoRA. | **No**: necesita GPU |

Resultados de la ejecución del 9 de noviembre de 2026:

- Referencia TF-IDF: F1 macro de 0,865 en la prueba, con un intervalo de confianza del 95 % entre 0,813 y 0,910; 0,840 con erratas.
- LoRA sobre el modelo diminuto: se entrenan 8.192 de 155.968 parámetros (5,25 %) y, una vez fusionado, el modelo da las mismas salidas sin capas adicionales.

El modelo diminuto no ha aprendido nada útil: sirve para ver la mecánica sin GPU ni descargas. Para un ajuste real necesitas un modelo preentrenado, ejemplos etiquetados de tu tarea y, en modelos de tamaño real, GPU.

## Cómo ejecutarlo

```bash
pip install torch --index-url https://download.pytorch.org/whl/cpu   # PyTorch solo para CPU, más ligero
pip install -r requirements.txt
python 01_referencia_tfidf.py
python 02_lora_cpu.py
```

Para `03_qlora_gpu.py`, en una máquina con GPU NVIDIA:

```bash
pip install -r requirements-gpu.txt
python 03_qlora_gpu.py
```

Antes, sustituye `ORGANIZACION/MODELO-BASE` por el modelo elegido, fija su revisión y lee su licencia completa: «abierto» no significa «sin condiciones». Sin GPU, el script termina con un aviso y no hace nada.

## Qué no se incluye

La guía también trata la exportación a ONNX, la cuantización en 8 bits y el servicio de modelos generativos con vLLM, Text Generation Inference o endpoints gestionados. No hay código para eso en este repositorio: depende de cada modelo, plataforma y contrato.

## Fuentes

Son las de la guía:

- [Hugging Face PEFT: guía conceptual de LoRA](https://huggingface.co/docs/peft/main/conceptual_guides/lora)
- [Hugging Face Transformers: cuantización con bitsandbytes (8 y 4 bits, QLoRA)](https://huggingface.co/docs/transformers/quantization/bitsandbytes)
- [ONNX Runtime: cuantización de modelos ONNX](https://www.onnxruntime.ai/docs/performance/model-optimizations/quantization.html)
