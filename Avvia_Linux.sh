#!/usr/bin/env bash
cd "$(dirname "$(readlink -f "$0")")" || exit 1
if [ -x ".venv/bin/python" ]; then
  PYTHON=".venv/bin/python"
elif command -v python3 >/dev/null 2>&1; then
  PYTHON="$(command -v python3)"
else
  echo "Python 3 non trovato."
  exit 1
fi
"$PYTHON" subtitles.py "$@"
status=$?
if [ -t 0 ]; then
  echo
  read -r -p "Operazione terminata (codice $status). Premi Invio per chiudere..." _
fi
exit "$status"
