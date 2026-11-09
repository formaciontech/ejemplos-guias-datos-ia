"""LoRA con PEFT en CPU sobre un modelo diminuto creado en local.

Guía: https://formaciontech.es/guias/ajuste-fino-modelos-lenguaje/

No descarga nada: crea un modelo tipo Llama con pesos aleatorios y unos
pocos miles de parámetros, solo para ver la mecánica de la guía:
- comprobar los nombres de los módulos con print(modelo_base);
- aplicar la configuración LoRA y ver qué fracción se entrena;
- dar unos pasos de entrenamiento;
- fusionar el adaptador y comprobar que el modelo fusionado responde igual.
Para un ajuste real, sustituye el modelo por uno preentrenado y usa datos
etiquetados de tu tarea (ver 03_qlora_gpu.py).
"""

import torch
from peft import LoraConfig, get_peft_model
from transformers import LlamaConfig, LlamaForCausalLM

torch.manual_seed(42)
config_base = LlamaConfig(vocab_size=512, hidden_size=64, intermediate_size=128, num_hidden_layers=2,
                          num_attention_heads=4, num_key_value_heads=4, max_position_embeddings=64)
modelo_base = LlamaForCausalLM(config_base)

# Comprueba los nombres de los módulos antes de elegir target_modules
print(modelo_base.model.layers[0].self_attn)

# El código de la guía
from peft import LoraConfig, get_peft_model  # noqa: E402,F811

config = LoraConfig(
    r=16, lora_alpha=32, lora_dropout=0.05,
    target_modules=["q_proj", "v_proj"],
    task_type="CAUSAL_LM")
modelo = get_peft_model(modelo_base, config)
modelo.print_trainable_parameters()

# Unos pasos de entrenamiento con secuencias aleatorias: solo se mueven las matrices LoRA
optim = torch.optim.AdamW([p for p in modelo.parameters() if p.requires_grad], lr=1e-3)
lote = torch.randint(0, config_base.vocab_size, (8, 32))
modelo.train()
for paso in range(1, 21):
    perdida = modelo(input_ids=lote, labels=lote).loss
    perdida.backward()
    optim.step()
    optim.zero_grad()
    if paso in (1, 20):
        print(f"Paso {paso:>2}: pérdida {perdida.item():.4f}")

# Fusionar el adaptador: el resultado es un modelo normal, sin capas extra
modelo.eval()
with torch.no_grad():
    antes = modelo(input_ids=lote[:2]).logits
    fusionado = modelo.merge_and_unload()
    despues = fusionado(input_ids=lote[:2]).logits
print("Capas LoRA tras fusionar:", sum("lora" in n for n, _ in fusionado.named_modules()))
print("Mismas salidas antes y después de fusionar:", torch.allclose(antes, despues, atol=1e-5))
