#!/usr/bin/env bash
set -e

ROOT="$(cd "$(dirname "$0")" && pwd)"
VENV="$ROOT/.venv"

if [ ! -x "$VENV/bin/streamlit" ]; then
  python3 -m venv "$VENV"
  "$VENV/bin/python" -m pip install --upgrade pip --quiet
  "$VENV/bin/python" -m pip install --quiet streamlit pypdf python-docx reportlab
fi

exec "$VENV/bin/streamlit" run "$ROOT/app.py" \
  --server.port "${PORT:-3000}" \
  --server.address 0.0.0.0 \
  --server.enableCORS false \
  --server.enableXsrfProtection false \
  --server.headless true
