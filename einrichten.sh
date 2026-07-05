#!/usr/bin/env bash
#
# Richtet den runden Tisch auf einem frischen Rechner ein.
# Baut die lokale Python-Umgebung (.venv) und installiert die Abhängigkeit.
# Der Vektorindex und die venv werden bewusst nicht versioniert, sie
# entstehen lokal. Deshalb gibt es dieses Skript.
#
# Aufruf, im Projektordner:
#   ./einrichten.sh
#
set -euo pipefail

# Immer im Ordner des Skripts arbeiten, egal von wo aufgerufen.
cd "$(dirname "$0")"

echo "Runder Tisch, Einrichtung"
echo "Projektordner: $(pwd)"
echo

if ! command -v python3 >/dev/null 2>&1; then
  echo "Fehler: python3 ist nicht installiert. Bitte zuerst Python 3 einrichten."
  exit 1
fi
echo "Gefundenes Python: $(python3 --version)"

if [ -d ".venv" ]; then
  echo "Es gibt bereits eine .venv, sie wird wiederverwendet."
else
  echo "Lege neue .venv an ..."
  python3 -m venv .venv
fi

echo "Installiere Abhängigkeiten aus requirements.txt ..."
./.venv/bin/python -m pip install --quiet --upgrade pip
./.venv/bin/python -m pip install --quiet -r requirements.txt

echo
echo "Fertig. Die Umgebung steht."
echo
echo "Nächster Schritt, Index für einen Korpus-Ordner bauen (Ordner muss vorhanden sein):"
echo "  ./.venv/bin/python index_bauen.py \"/Pfad/zum/Korpus\""
echo
echo "Danach kann der Skill 'runder-tisch' genutzt werden."
