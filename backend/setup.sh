# Script de configuración mínima para el backend.
# - Instala los requisitos de Python
# - Genera la matriz de correlación y los archivos JSON top10
# Ejecuta esto desde la raíz del proyecto como: ./backend/setup.sh


set -euo pipefail

BASEDIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
echo "Using backend base dir: $BASEDIR"

# Install requirements
if command -v python3 >/dev/null 2>&1; then
  PY=python3
elif command -v python >/dev/null 2>&1; then
  PY=python
else
  echo "Python not found. Please install Python 3.8+ and retry." >&2
  exit 1
fi

echo "Installing requirements from $BASEDIR/requierements.txt..."
$PY -m pip install --upgrade pip
$PY -m pip install -r "$BASEDIR/requierements.txt"


cd "$BASEDIR/app"

echo "Generating correlation matrix..."
$PY scripts/generate_matrix.py || { echo "generate_matrix.py failed" >&2; exit 1; }

echo "Generating top10..."
$PY scripts/generate_top10.py || { echo "generate_top10.py failed" >&2; exit 1; }

echo "Backend setup complete. matriz_corr.json and top10.json should be in app/data_base/data/"
