#!/usr/bin/env bash
# ============================================================
#  compilar.sh — Script para compilar la tesis con un comando
#  Uso:  bash scripts/compilar.sh
# ============================================================

set -euo pipefail

# Ruta al Makefile de la tesis
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
THESIS_DIR="$(dirname "$SCRIPT_DIR")/documentacion"

echo "▶ Directorio de la tesis: ${THESIS_DIR}"
cd "${THESIS_DIR}"

# Comprobar que latexmk está disponible
if ! command -v latexmk >/dev/null 2>&1; then
    echo "⚠ No se encontró 'latexmk'." >&2
    echo "  Instala una distribución TeX Live junto con biber y latexmk." >&2
    exit 1
fi

echo "▶ Compilando (XeLaTeX + biber)…"
make pdf
