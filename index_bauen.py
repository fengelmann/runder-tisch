#!/usr/bin/env python3
"""Baut und aktualisiert den lokalen Vektorindex über den Ressourcen-Ordner.

Liest alle Markdown-Notizen, zerlegt sie in Abschnitte und bettet sie mit einem
lokalen Modell ein. Index und Metadaten liegen flach im Ordner index/. Kein
externer Dienst, keine Datenbank. Der Korpus verlässt den Rechner nicht.

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
from pathlib import Path

import numpy as np
from fastembed import TextEmbedding

# --- Konfiguration ---
KORPUS = Path("/Users/d0e02236/Documents/Notes/Work/02 Ressourcen")
AUSSCHLUSS = {"PDS", "99_Personen"}             # Ordner, die nicht indiziert werden
MODELL = "jinaai/jina-embeddings-v2-base-de"     # deutsch und englisch, kein Präfix nötig, ONNX
INDEX_DIR = Path(__file__).resolve().parent / "index"
MAX_ZEICHEN = 1200                               # Obergrenze je Abschnitt

VEKTOREN = INDEX_DIR / "vektoren.npy"
CHUNKS = INDEX_DIR / "chunks.json"
META = INDEX_DIR / "meta.json"
CACHE_HASHES = INDEX_DIR / "cache_hashes.json"
CACHE_VEKTOREN = INDEX_DIR / "cache_vektoren.npy"


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


def baue_chunks() -> list[dict]:
    """Sammelt alle Abschnitte in deterministischer Reihenfolge."""
    dateien = sorted(
        (p for p in KORPUS.rglob("*.md")
         if not (set(p.relative_to(KORPUS).parts) & AUSSCHLUSS)),
        key=lambda p: str(p),
    )
    chunks: list[dict] = []
    for pfad in dateien:
        titel, text = lade_text(pfad)
        for name, stueck in zerlege(titel, text):
            chunks.append({
                "quelle": str(pfad.relative_to(KORPUS)),
                "titel": titel,
                "abschnitt": name,
                "text": stueck,
            })
    return chunks


def fingerabdruck(text: str) -> str:
    """Inhaltlicher Fingerabdruck eines Abschnitts."""
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def lade_cache() -> dict:
    """Lädt den inhaltsbasierten Zwischenspeicher, Fingerabdruck zu Vektor."""
    cache: dict = {}
    if CACHE_HASHES.exists() and CACHE_VEKTOREN.exists():
        hashes = json.loads(CACHE_HASHES.read_text(encoding="utf-8"))
        vek = np.load(CACHE_VEKTOREN)
        for h, v in zip(hashes, vek):
            cache[h] = v
    return cache


def bootstrap_aus_altem_index(cache: dict) -> None:
    """Erster Lauf nach der Umstellung. Füllt den Zwischenspeicher aus dem
    vorhandenen Index, damit die alten Einbettungen nicht neu gerechnet werden."""
    if cache or not (CHUNKS.exists() and VEKTOREN.exists()):
        return
    chunks = json.loads(CHUNKS.read_text(encoding="utf-8"))
    vek = np.load(VEKTOREN)
    if len(chunks) == len(vek):
        for c, v in zip(chunks, vek):
            cache[fingerabdruck(c["text"])] = v
        print(f"Zwischenspeicher aus vorhandenem Index übernommen, {len(cache)} Einbettungen", flush=True)


def main() -> None:
    INDEX_DIR.mkdir(exist_ok=True)
    chunks = baue_chunks()
    gesamt = len(chunks)
    print(f"{gesamt} Abschnitte im Korpus", flush=True)

    cache = lade_cache()
    bootstrap_aus_altem_index(cache)

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

    np.save(VEKTOREN, vektoren)
    CHUNKS.write_text(json.dumps(chunks, ensure_ascii=False), encoding="utf-8")
    META.write_text(
        json.dumps(
            {"modell": MODELL, "dim": int(vektoren.shape[1]), "anzahl": int(vektoren.shape[0])},
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
    CACHE_HASHES.write_text(json.dumps(akt_hashes), encoding="utf-8")
    np.save(CACHE_VEKTOREN, np.array(akt_vek, dtype=np.float32))

    print(f"Index aktualisiert: {vektoren.shape[0]} Abschnitte, gespeichert in {INDEX_DIR}", flush=True)


if __name__ == "__main__":
    main()
