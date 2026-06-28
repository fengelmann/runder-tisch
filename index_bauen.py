#!/usr/bin/env python3
"""Baut den lokalen Vektorindex über den Ressourcen-Ordner.

Liest alle Markdown-Notizen, zerlegt sie in Abschnitte, bettet sie mit einem
lokalen Modell ein und legt Index und Metadaten flach im Ordner index/ ab.
Kein externer Dienst, keine Datenbank. Der Korpus verlässt den Rechner nicht.

Der Lauf ist fortsetzbar. Er speichert die Einbettungen batchweise als Shards in
index/shards/. Wird er unterbrochen, setzt ein erneuter Start dort fort, wo er
aufgehört hat. Sind alle Batches da, fügt er sie zu vektoren.npy zusammen.
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

import numpy as np
from fastembed import TextEmbedding

# --- Konfiguration ---
KORPUS = Path("/Users/d0e02236/Documents/Notes/Work/02 Ressourcen")
AUSSCHLUSS = {"PDS", "99_Personen"}             # Ordner, die nicht indiziert werden
MODELL = "jinaai/jina-embeddings-v2-base-de"     # deutsch und englisch, kein Präfix nötig, ONNX
INDEX_DIR = Path(__file__).resolve().parent / "index"
SHARD_DIR = INDEX_DIR / "shards"
MAX_ZEICHEN = 1200                               # Obergrenze je Abschnitt
BATCH = 250                                      # Abschnitte je Shard, häufiger Checkpoint


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
    """Sammelt alle Abschnitte in deterministischer Reihenfolge (wichtig fürs Fortsetzen)."""
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


def main() -> None:
    INDEX_DIR.mkdir(exist_ok=True)
    SHARD_DIR.mkdir(exist_ok=True)

    chunks = baue_chunks()
    gesamt = len(chunks)
    (INDEX_DIR / "chunks.json").write_text(
        json.dumps(chunks, ensure_ascii=False), encoding="utf-8"
    )
    print(f"{gesamt} Abschnitte", flush=True)

    modell = TextEmbedding(model_name=MODELL)
    for start in range(0, gesamt, BATCH):
        shard = SHARD_DIR / f"{start:07d}.npy"
        if shard.exists():
            continue                              # bereits erledigt, fortsetzen
        ende = min(start + BATCH, gesamt)
        texte = [chunks[i]["text"] for i in range(start, ende)]
        vek = np.array(list(modell.embed(texte)), dtype=np.float32)
        vek /= np.linalg.norm(vek, axis=1, keepdims=True) + 1e-12
        np.save(shard, vek)                       # Checkpoint sofort sichern
        print(f"  {ende}/{gesamt} eingebettet", flush=True)

    erwartet = (gesamt + BATCH - 1) // BATCH
    shards = sorted(SHARD_DIR.glob("*.npy"), key=lambda p: int(p.stem))
    if len(shards) < erwartet:
        print(f"Noch nicht vollständig: {len(shards)}/{erwartet} Batches. "
              f"Skript erneut starten, es setzt fort.", flush=True)
        sys.exit(2)

    vektoren = np.concatenate([np.load(s) for s in shards], axis=0)
    schlecht = ~np.isfinite(vektoren).all(axis=1)
    if schlecht.any():
        print(f"Hinweis: {int(schlecht.sum())} von {vektoren.shape[0]} Abschnitten "
              f"hatten ungültige Werte und werden auf Null gesetzt", flush=True)
    vektoren = np.nan_to_num(vektoren, nan=0.0, posinf=0.0, neginf=0.0).astype(np.float32)
    np.save(INDEX_DIR / "vektoren.npy", vektoren)
    (INDEX_DIR / "meta.json").write_text(
        json.dumps(
            {"modell": MODELL, "dim": int(vektoren.shape[1]), "anzahl": int(vektoren.shape[0])},
            ensure_ascii=False,
        ),
        encoding="utf-8",
    )
    print(f"Index vollständig: {vektoren.shape[0]} Abschnitte, gespeichert in {INDEX_DIR}", flush=True)


if __name__ == "__main__":
    main()
