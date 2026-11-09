"""QLoRA: LoRA sobre un modelo base cargado en 4 bits (NF4). NECESITA GPU.

Guía: https://formaciontech.es/guias/ajuste-fino-modelos-lenguaje/

Ejemplo documentado, NO ejecutado en este repositorio: requiere una GPU
compatible, la librería bitsandbytes y descargar un modelo preentrenado.
Antes de usarlo:
- elige el modelo base y anota su revisión exacta;
- lee su licencia completa: «abierto» no significa «sin condiciones»;
- comprueba los nombres de target_modules con print(modelo_base).

    pip install -r requirements-gpu.txt
    python 03_qlora_gpu.py
"""

import torch
from peft import LoraConfig, get_peft_model, prepare_model_for_kbit_training
from transformers import AutoModelForCausalLM, AutoTokenizer, BitsAndBytesConfig

MODELO = "ORGANIZACION/MODELO-BASE"   # sustitúyelo por el identificador del modelo elegido
REVISION = "main"                     # mejor un commit concreto, para poder reproducirlo

if not torch.cuda.is_available():
    raise SystemExit("Este ejemplo necesita una GPU con CUDA. Para practicar en CPU, usa 02_lora_cpu.py.")

cuantizacion = BitsAndBytesConfig(
    load_in_4bit=True,
    bnb_4bit_quant_type="nf4",
    bnb_4bit_compute_dtype=torch.bfloat16,
    bnb_4bit_use_double_quant=True,
)
tokenizador = AutoTokenizer.from_pretrained(MODELO, revision=REVISION)
modelo_base = AutoModelForCausalLM.from_pretrained(MODELO, revision=REVISION,
                                                   quantization_config=cuantizacion, device_map="auto")
modelo_base = prepare_model_for_kbit_training(modelo_base)
print(modelo_base)  # comprueba aquí los nombres de las proyecciones de atención

config = LoraConfig(
    r=16, lora_alpha=32, lora_dropout=0.05,
    target_modules=["q_proj", "v_proj"],
    task_type="CAUSAL_LM")
modelo = get_peft_model(modelo_base, config)
modelo.print_trainable_parameters()

# A partir de aquí: tokeniza tus ejemplos etiquetados (entrenamiento y validación),
# entrena con transformers.Trainer o con tu bucle, guarda el adaptador con
# modelo.save_pretrained("adaptador/") y evalúalo con el mismo protocolo que la
# referencia de 01_referencia_tfidf.py (por clase, intervalos, calibración y robustez).
