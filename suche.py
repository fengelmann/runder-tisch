#!/usr/bin/env python3
"""Durchsucht den lokalen Vektorindex eines Korpus semantisch.

Aufruf: python suche.py "/Pfad/zum/Korpus" "deine Frage" [anzahl]
Der Korpus-Ordner ist Pflicht, damit immer bewusst gewählt wird, worauf
gearbeitet wird. Gibt die ähnlichsten Abschnitte mit Quellnotiz aus. Das ist
die Such-Schnittstelle, die der runde Tisch zur Erdung aufruft.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np
from fastembed import TextEmbedding

from index_bauen import index_verzeichnis


def main() -> None:
    if len(sys.argv) < 3:
        print('Aufruf: python suche.py "/Pfad/zum/Korpus" "deine Frage" [anzahl]')
        sys.exit(1)
    korpus = Path(sys.argv[1]).expanduser().resolve()
    frage = sys.argv[2]
    k = int(sys.argv[3]) if len(sys.argv) > 3 else 5

    index_dir = index_verzeichnis(korpus)
    if not (index_dir / "meta.json").exists():
        print(f"Kein Index für diesen Korpus vorhanden: {korpus}")
        print('Erst bauen mit: python index_bauen.py "/Pfad/zum/Korpus"')
        sys.exit(1)

    meta = json.loads((index_dir / "meta.json").read_text(encoding="utf-8"))
    chunks = json.loads((index_dir / "chunks.json").read_text(encoding="utf-8"))
    vektoren = np.nan_to_num(np.load(index_dir / "vektoren.npy")).astype(np.float32)

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
