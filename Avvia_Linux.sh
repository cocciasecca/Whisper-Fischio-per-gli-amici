#!/usr/bin/env bash
cd "$(dirname "$(readlink -f "$0")")" || exit 1
if [ ! -x ".venv/bin/python" ]; then
  if ! command -v python3 >/dev/null 2>&1; then
    echo "Python 3 non trovato. Installalo prima di avviare questo file."
    exit 1
  fi
  python3 -m venv .venv || exit 1
fi
PYTHON=".venv/bin/python"
"$PYTHON" setup_runtime.py "$@"
status=$?
if [ -t 0 ]; then
  echo
  read -r -p "Operazione terminata (codice $status). Premi Invio per chiudere..." _
fi
exit "$status"
