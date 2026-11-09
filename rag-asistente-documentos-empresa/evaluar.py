"""Evaluación de la recuperación con métricas exactas, sin LLM.

Guía: https://formaciontech.es/guias/rag-asistente-documentos-empresa/

Si el fragmento correcto no llega al prompt, ningún modelo responderá bien:
por eso la recuperación se evalúa por separado. Son métricas baratas, para
ejecutarlas en cada cambio:
- acierto@1 y acierto@3: el fragmento esperado está entre los primeros;
- MRR: media del inverso de la posición del primer acierto;
- fugas de permisos: fragmentos restringidos recuperados sin el grupo
  necesario (debe ser cero);
- documentos obsoletos indexados (debe ser cero).
Las métricas con un LLM evaluador (por ejemplo, la fidelidad de Ragas) y la
revisión humana de una muestra van después y no se ejecutan aquí.

    python evaluar.py
"""

import json
import sys
from pathlib import Path

from rag import Indice, ingerir

CASOS = json.loads((Path(__file__).resolve().parent / "preguntas_referencia.json").read_text(encoding="utf-8"))
fragmentos, descartados = ingerir()
indice = Indice(fragmentos)

aciertos1 = aciertos3 = rr = n = fugas = 0
print(f"{'id':<4} {'acierto':<8} recuperados")
for c in CASOS:
    res = indice.buscar(c["pregunta"], c["grupos"], k=3)
    fugas += sum(1 for f, _ in res if f.acceso != "todos" and f.acceso not in c["grupos"])
    if c["fuente_esperada"] is None:
        print(f"{c['id']:<4} {'—':<8} {[f.id for f, _ in res]}  ({c['nota']})")
        continue
    n += 1
    posiciones = [i for i, (f, _) in enumerate(res, 1)
                  if f.fuente == c["fuente_esperada"] and f.seccion == c["seccion_esperada"]]
    pos = posiciones[0] if posiciones else None
    aciertos1 += pos == 1
    aciertos3 += pos is not None
    rr += 1 / pos if pos else 0
    print(f"{c['id']:<4} {('@' + str(pos)) if pos else 'fallo':<8} {[f.id for f, _ in res]}")

obsoletos = sum(1 for f in fragmentos if f.fuente in descartados)
print(f"\nPreguntas con respuesta: {n} · acierto@1 {aciertos1 / n:.0%} · acierto@3 {aciertos3 / n:.0%} · MRR {rr / n:.3f}")
print(f"Fugas de permisos: {fugas} · documentos obsoletos indexados: {obsoletos} (descartados: {descartados})")
sys.exit(1 if fugas or obsoletos else 0)
