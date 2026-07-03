#!/usr/bin/env python3
"""Baut und aktualisiert den lokalen Vektorindex über einen Korpus-Ordner.

Aufruf: python index_bauen.py "/Pfad/zum/Korpus"

Der Korpus-Ordner ist Pflicht, damit immer bewusst gewählt wird, worauf
gearbeitet wird. Liest alle Markdown-Notizen, zerlegt sie in Abschnitte und
bettet sie mit einem lokalen Modell ein. Jeder Korpus bekommt seinen eigenen
Unterordner unter index/, abgeleitet aus dem Korpus-Pfad. Kein externer
Dienst, keine Datenbank. Der Korpus verlässt den Rechner nicht.

Die Einbettungen werden inhaltsbasiert zwischengespeichert. Jeder Abschnitt
bekommt einen Fingerabdruck über seinen Text. Bei einem erneuten Lauf werden
alle unveränderten Abschnitte aus dem Zwischenspeicher übernommen, und nur neue
oder geänderte Abschnitte werden eingebettet. Ein erneuter Lauf ist damit immer
korrekt und schnell, auch wenn mitten im Korpus Notizen dazukommen.
"""
from __future__ import annotations

import hashlib
import json
import re
import sys
from pathlib import Path

import numpy as np
from fastembed import TextEmbedding

# --- Konfiguration ---
AUSSCHLUSS = {"PDS", "99_Personen"}             # Ordner, die nicht indiziert werden
MODELL = "jinaai/jina-embeddings-v2-base-de"     # deutsch und englisch, kein Präfix nötig, ONNX
INDEX_BASIS = Path(__file__).resolve().parent / "index"
MAX_ZEICHEN = 1200                               # Obergrenze je Abschnitt


def index_verzeichnis(korpus: Path) -> Path:
    """Eigener Index-Unterordner je Korpus, lesbar benannt und über einen
    Fingerabdruck des vollen Pfads eindeutig, auch bei gleichem Ordnernamen."""
    korpus = korpus.resolve()
    kuerzel = hashlib.sha256(str(korpus).encode("utf-8")).hexdigest()[:8]
    name = re.sub(r"[^A-Za-z0-9]+", "-", korpus.name).strip("-").lower() or "korpus"
    return INDEX_BASIS / f"{name}-{kuerzel}"


def lade_text(pfad: Path) -> tuple[str, str]:
    """Liest eine Notiz, entfernt das YAML-Frontmatter und zieht den Titel."""
    roh = pfad.read_text(encoding="utf-8", errors="ignore")
    titel = pfad.stem
    if roh.startswith("---"):
        ende = roh.find("\n---", 3)
        if ende != -1:
            kopf = roh[3:ende]
            roh = roh[ende + 4:]
            treffer = re.search(r"^title:\s*(.+)$", kopf, re.MULTILINE)
            if treffer:
                titel = treffer.group(1).strip().strip('"').strip("'")
    return titel, roh.strip()


def zerlege(titel: str, text: str) -> list[tuple[str, str]]:
    """Zerlegt einen Notiztext in (Abschnittsname, Abschnittstext)."""
    abschnitte: list[tuple[str, str]] = []
    aktueller_name = titel
    puffer: list[str] = []

    def schiebe() -> None:
        inhalt = "\n".join(puffer).strip()
        if inhalt:
            for i in range(0, len(inhalt), MAX_ZEICHEN):
                abschnitte.append((aktueller_name, inhalt[i:i + MAX_ZEICHEN]))

    for zeile in text.splitlines():
        if re.match(r"^#{1,6}\s", zeile):
            schiebe()
            aktueller_name = zeile.lstrip("#").strip()
            puffer = []
        else:
            puffer.append(zeile)
    schiebe()
    return abschnitte


def baue_chunks(korpus: Path) -> list[dict]:
    """Sammelt alle Abschnitte in deterministischer Reihenfolge."""
    dateien = sorted(
        (p for p in korpus.rglob("*.md")
         if not (set(p.relative_to(korpus).parts) & AUSSCHLUSS)),
        key=lambda p: str(p),
    )
    chunks: list[dict] = []
    for pfad in dateien:
        titel, text = lade_text(pfad)
        for name, stueck in zerlege(titel, text):
            chunks.append({
                "quelle": str(pfad.relative_to(korpus)),
                "titel": titel,
                "abschnitt": name,
                "text": stueck,
            })
    return chunks


def fingerabdruck(text: str) -> str:
    """Inhaltlicher Fingerabdruck eines Abschnitts."""
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def lade_cache(index_dir: Path) -> dict:
    """Lädt den inhaltsbasierten Zwischenspeicher, Fingerabdruck zu Vektor."""
    cache: dict = {}
    cache_hashes = index_dir / "cache_hashes.json"
    cache_vektoren = index_dir / "cache_vektoren.npy"
    if cache_hashes.exists() and cache_vektoren.exists():
        hashes = json.loads(cache_hashes.read_text(encoding="utf-8"))
        vek = np.load(cache_vektoren)
        for h, v in zip(hashes, vek):
            cache[h] = v
    return cache


def main() -> None:
    if len(sys.argv) < 2 or not sys.argv[1].strip():
        print('Aufruf: python index_bauen.py "/Pfad/zum/Korpus"')
        print("Der Korpus-Ordner ist Pflicht, damit bewusst gewählt wird, worauf gearbeitet wird.")
        sys.exit(1)
    korpus = Path(sys.argv[1]).expanduser().resolve()
    if not korpus.is_dir():
        print(f"Korpus-Ordner nicht gefunden: {korpus}")
        sys.exit(1)

    index_dir = index_verzeichnis(korpus)
    index_dir.mkdir(parents=True, exist_ok=True)
    print(f"Korpus: {korpus}", flush=True)

    chunks = baue_chunks(korpus)
    gesamt = len(chunks)
    print(f"{gesamt} Abschnitte im Korpus", flush=True)

    cache = lade_cache(index_dir)

    fehlend = [i for i, c in enumerate(chunks) if fingerabdruck(c["text"]) not in cache]
    print(f"{len(fehlend)} neue oder geänderte Abschnitte, {gesamt - len(fehlend)} wiederverwendet", flush=True)

    if fehlend:
        modell = TextEmbedding(model_name=MODELL)
        texte = [chunks[i]["text"] for i in fehlend]
        neu: list = []
        for n, v in enumerate(modell.embed(texte), 1):
            neu.append(v)
            if n % 100 == 0 or n == len(texte):
                print(f"  {n}/{len(texte)} eingebettet", flush=True)
        neu_arr = np.array(neu, dtype=np.float32)
        neu_arr /= np.linalg.norm(neu_arr, axis=1, keepdims=True) + 1e-12
        for i, v in zip(fehlend, neu_arr):
            cache[fingerabdruck(chunks[i]["text"])] = v

    # Index in aktueller Reihenfolge zusammensetzen
    vektoren = np.array([cache[fingerabdruck(c["text"])] for c in chunks], dtype=np.float32)
    vektoren = np.nan_to_num(vektoren, nan=0.0, posinf=0.0, neginf=0.0).astype(np.float32)

    np.save(index_dir / "vektoren.npy", vektoren)
    (index_dir / "chunks.json").write_text(json.dumps(chunks, ensure_ascii=False), encoding="utf-8")
    (index_dir / "meta.json").write_text(
        json.dumps(
            {
                "modell": MODELL,
                "dim": int(vektoren.shape[1]),
                "anzahl": int(vektoren.shape[0]),
                "korpus": str(korpus),
            },
            ensure_ascii=False,
        ),
        encoding="utf-8",
    )

    # Zwischenspeicher auf den aktuellen Stand bringen, nur aktuelle Abschnitte, ohne Dubletten
    akt_hashes: list[str] = []
    akt_vek: list = []
    gesehen: set = set()
    for c in chunks:
        h = fingerabdruck(c["text"])
        if h in gesehen:
            continue
        gesehen.add(h)
        akt_hashes.append(h)
        akt_vek.append(cache[h])
    (index_dir / "cache_hashes.json").write_text(json.dumps(akt_hashes), encoding="utf-8")
    np.save(index_dir / "cache_vektoren.npy", np.array(akt_vek, dtype=np.float32))

    print(f"Index aktualisiert: {vektoren.shape[0]} Abschnitte, gespeichert in {index_dir}", flush=True)


if __name__ == "__main__":
    main()
