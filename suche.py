#!/usr/bin/env python3
"""Durchsucht den lokalen Vektorindex semantisch.

Aufruf: python suche.py "deine Frage" [anzahl]
Gibt die ähnlichsten Abschnitte mit Quellnotiz aus. Das ist die Such-Schnittstelle,
die der runde Tisch zur Erdung aufruft.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np
from fastembed import TextEmbedding

INDEX_DIR = Path(__file__).resolve().parent / "index"


def main() -> None:
    if len(sys.argv) < 2:
        print('Aufruf: python suche.py "deine Frage" [anzahl]')
        sys.exit(1)
    frage = sys.argv[1]
    k = int(sys.argv[2]) if len(sys.argv) > 2 else 5

    meta = json.loads((INDEX_DIR / "meta.json").read_text(encoding="utf-8"))
    chunks = json.loads((INDEX_DIR / "chunks.json").read_text(encoding="utf-8"))
    vektoren = np.nan_to_num(np.load(INDEX_DIR / "vektoren.npy")).astype(np.float32)

    modell = TextEmbedding(model_name=meta["modell"])
    frage_vektor = np.array(list(modell.embed([frage]))[0], dtype=np.float32)
    frage_vektor /= np.linalg.norm(frage_vektor) + 1e-12

    # numpy/Accelerate meldet bei matmul auf macOS gelegentlich Pseudo-Warnungen,
    # obwohl die Daten geprüft finit sind. Daher hier bewusst stummgeschaltet.
    with np.errstate(all="ignore"):
        aehnlichkeit = vektoren @ frage_vektor
    beste = np.argsort(-aehnlichkeit)[:k]

    for rang, i in enumerate(beste, 1):
        c = chunks[i]
        schnipsel = " ".join(c["text"].split())[:240]
        print(f"\n[{rang}] {aehnlichkeit[i]:.3f}  {c['titel']} › {c['abschnitt']}")
        print(f"     Quelle: {c['quelle']}")
        print(f"     {schnipsel}")


if __name__ == "__main__":
    main()
