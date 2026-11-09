"""Textos sintéticos de reclamaciones con semilla fija.

Guía: https://formaciontech.es/guias/ajuste-fino-modelos-lenguaje/

Cuatro categorías que comparten vocabulario a propósito (cobro, pedido,
cuenta...), como ocurre con las reclamaciones reales. Para que se parezca a un
corpus real, un 6 % de los textos son frases ambiguas y un 8 % de las
etiquetas están mal puestas. Las frases se generan combinando plantillas; no
proceden de ningún cliente.
"""

import random
import unicodedata

SEMILLA = 42
CATEGORIAS = ["facturacion", "envio", "producto", "baja"]

PLANTILLAS = {
    "facturacion": [
        "me habéis cobrado dos veces el {cosa} de {mes}",
        "el importe de la factura de {mes} no coincide con lo contratado",
        "quiero que me devolváis el cargo duplicado en mi cuenta",
        "la factura del {cosa} trae un concepto que no reconozco",
        "no entiendo por qué ha subido el recibo de {mes}",
    ],
    "envio": [
        "el pedido del {cosa} lleva {n} días sin llegar",
        "el repartidor dice que entregó el paquete pero no lo tengo",
        "el seguimiento del envío no se actualiza desde {mes}",
        "me han enviado el pedido a una dirección antigua de mi cuenta",
        "quiero cambiar la fecha de entrega del {cosa}",
    ],
    "producto": [
        "el {cosa} llegó roto y no funciona",
        "el {cosa} deja de funcionar a los {n} días de uso",
        "el {cosa} no corresponde con la descripción del pedido",
        "falta una pieza del {cosa} que compré en {mes}",
        "quiero cambiar el {cosa} porque viene defectuoso",
    ],
    "baja": [
        "quiero darme de baja y cerrar mi cuenta",
        "cancelad la suscripción a partir de {mes}",
        "no quiero que me cobréis más, solicito la baja del servicio",
        "cómo cierro mi cuenta y borro mis datos",
        "deseo cancelar el contrato del {cosa} este mes",
    ],
}
COSAS = ["router", "móvil", "portátil", "servicio", "plan", "televisor", "auricular"]
MESES = ["enero", "febrero", "marzo", "abril", "mayo", "junio"]
APERTURAS = ["", "hola, ", "buenos días, ", "por favor, ", "otra vez: "]
AMBIGUAS = [
    "tengo un problema con el {cosa} de {mes}",
    "nadie me responde sobre lo del {cosa}",
    "llevo {n} días esperando una solución con mi cuenta",
]


def sin_tildes(texto):
    return "".join(c for c in unicodedata.normalize("NFD", texto) if unicodedata.category(c) != "Mn")


def con_erratas(texto, rng, prob=0.08):
    """Intercambia letras vecinas al azar: simula erratas al teclear."""
    letras = list(texto)
    for i in range(len(letras) - 1):
        if letras[i].isalpha() and letras[i + 1].isalpha() and rng.random() < prob:
            letras[i], letras[i + 1] = letras[i + 1], letras[i]
    return "".join(letras)


def generar(n_por_clase=250, semilla=SEMILLA, ambiguas=0.06, ruido=0.08):
    rng = random.Random(semilla)
    textos, etiquetas = [], []
    for cat in CATEGORIAS:
        for _ in range(n_por_clase):
            plantilla = rng.choice(AMBIGUAS if rng.random() < ambiguas else PLANTILLAS[cat])
            frase = plantilla.format(cosa=rng.choice(COSAS), mes=rng.choice(MESES), n=rng.randint(2, 30))
            etiqueta = cat
            if rng.random() < ruido:  # etiqueta errónea, como en cualquier corpus real
                etiqueta = rng.choice([c for c in CATEGORIAS if c != cat])
            textos.append(rng.choice(APERTURAS) + frase)
            etiquetas.append(etiqueta)
    orden = list(range(len(textos)))
    rng.shuffle(orden)
    return [textos[i] for i in orden], [etiquetas[i] for i in orden]


if __name__ == "__main__":
    t, e = generar()
    for i in range(5):
        print(f"{e[i]:<12} {t[i]}")
