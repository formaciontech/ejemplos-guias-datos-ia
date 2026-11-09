"""Ingesta, troceado y búsqueda híbrida con permisos para un asistente RAG.

Guía: https://formaciontech.es/guias/rag-asistente-documentos-empresa/

Las piezas de la guía, en local y sin servicios de pago:
1. Ingesta: texto limpio y metadatos (fuente, fecha, vigencia y nivel de
   acceso). Los documentos no vigentes se descartan.
2. Troceado: primero por encabezados y después con un troceador recursivo;
   cada fragmento lleva el título y la sección.
3. Vectores: aquí, TF-IDF de n-gramas de caracteres reducido con SVD (LSA),
   para no descargar nada. En un proyecto real, usa un modelo de embeddings,
   el mismo para indexar y para consultar.
4. Búsqueda híbrida: BM25 (palabras exactas, códigos) + vectores, fusionados
   con Reciprocal Rank Fusion. Los permisos se aplican ANTES de recuperar.

    python rag.py "¿Cuántos días puedo teletrabajar?"
"""

import re
import sys
import unicodedata
from dataclasses import dataclass
from pathlib import Path

import numpy as np
from langchain_text_splitters import MarkdownHeaderTextSplitter, RecursiveCharacterTextSplitter
from rank_bm25 import BM25Okapi
from sklearn.decomposition import TruncatedSVD
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import normalize

CARPETA = Path(__file__).resolve().parent / "documentos"
PALABRAS_VACIAS = set("""a al algo con de del el en es la las lo los me mi mis o para por que qué se si
su sus un una y yo cuál cuánto cuántos cuántas cómo dónde hay tengo puedo""".split())


@dataclass
class Fragmento:
    id: str
    fuente: str
    titulo: str
    seccion: str
    acceso: str
    fecha: str
    texto: str


def normalizar(texto):
    texto = unicodedata.normalize("NFD", texto.lower())
    return "".join(c for c in texto if unicodedata.category(c) != "Mn")


def tokens(texto):
    return [t for t in re.findall(r"\w+", normalizar(texto)) if t not in {normalizar(p) for p in PALABRAS_VACIAS}]


def leer_documento(ruta):
    """Separa la cabecera de metadatos (entre líneas ---) del cuerpo en Markdown."""
    _, cabecera, cuerpo = ruta.read_text(encoding="utf-8").split("---", 2)
    meta = dict(linea.split(":", 1) for linea in cabecera.strip().splitlines())
    return {k.strip(): v.strip() for k, v in meta.items()}, cuerpo.strip()


def trocear(meta, cuerpo):
    por_encabezados = MarkdownHeaderTextSplitter(
        headers_to_split_on=[("#", "titulo"), ("##", "seccion")]).split_text(cuerpo)
    # El troceador de la guía. Los tamaños están en caracteres y no son una receta
    troceador = RecursiveCharacterTextSplitter(
        chunk_size=600, chunk_overlap=80)
    n = 0
    for doc in por_encabezados:
        seccion = doc.metadata.get("seccion")
        if not seccion:            # la entradilla sin sección no aporta contenido
            continue
        for trozo in troceador.split_text(doc.page_content):
            n += 1
            yield Fragmento(id=f"{Path(meta['fuente']).stem}#{n}", fuente=meta["fuente"], titulo=meta["titulo"],
                            seccion=seccion, acceso=meta["acceso"], fecha=meta["fecha"],
                            texto=f"{meta['titulo']} > {seccion}\n{trozo}")


def ingerir(carpeta=CARPETA):
    fragmentos, descartados = [], []
    for ruta in sorted(carpeta.glob("*.md")):
        meta, cuerpo = leer_documento(ruta)
        if meta.get("vigente") != "si":   # un documento obsoleto sin marcar acabaría en una respuesta
            descartados.append(ruta.name)
            continue
        fragmentos.extend(trocear(meta, cuerpo))
    return fragmentos, descartados


class Indice:
    def __init__(self, fragmentos, componentes=64, semilla=42):
        self.fragmentos = fragmentos
        textos = [f.texto for f in fragmentos]
        self.bm25 = BM25Okapi([tokens(t) for t in textos])
        self.tfidf = TfidfVectorizer(analyzer="char_wb", ngram_range=(3, 5), preprocessor=normalizar)
        matriz = self.tfidf.fit_transform(textos)
        self.svd = TruncatedSVD(n_components=min(componentes, len(textos) - 1), random_state=semilla)
        self.vectores = normalize(self.svd.fit_transform(matriz))

    def vector(self, texto):
        return normalize(self.svd.transform(self.tfidf.transform([texto])))[0]

    def buscar(self, pregunta, grupos, k=3, rrf_k=60):
        # 1) Permisos antes de recuperar: lo que entra en el prompt puede salir en la respuesta
        permitidos = [i for i, f in enumerate(self.fragmentos) if f.acceso == "todos" or f.acceso in grupos]
        if not permitidos:
            return []
        # 2) Dos rankings: por palabras (BM25) y por significado aproximado (vectores)
        bm25 = self.bm25.get_scores(tokens(pregunta))[permitidos]
        coseno = self.vectores[permitidos] @ self.vector(pregunta)
        # 3) Fusión por posiciones (Reciprocal Rank Fusion): no mezcla escalas distintas
        puntos = np.zeros(len(permitidos))
        for orden in (np.argsort(-bm25), np.argsort(-coseno)):
            puntos[orden] += 1.0 / (rrf_k + np.arange(1, len(permitidos) + 1))
        mejores = np.argsort(-puntos)[:k]
        return [(self.fragmentos[permitidos[i]], float(puntos[i])) for i in mejores]


if __name__ == "__main__":
    pregunta = sys.argv[1] if len(sys.argv) > 1 else "¿Cuántos días a la semana puedo teletrabajar?"
    grupos = sys.argv[2].split(",") if len(sys.argv) > 2 else ["todos"]
    fragmentos, descartados = ingerir()
    print(f"{len(fragmentos)} fragmentos indexados · descartados por no vigentes: {descartados}")
    indice = Indice(fragmentos)
    print(f"\nPregunta: {pregunta} (grupos: {grupos})")
    for f, p in indice.buscar(pregunta, grupos):
        print(f"  [{f.id}] {f.titulo} > {f.seccion} (RRF {p:.4f})")
