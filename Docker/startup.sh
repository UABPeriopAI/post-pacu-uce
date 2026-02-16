#!/bin/sh
set -eu

REPO_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$REPO_ROOT"

sudo apt-get update
sudo DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends fonts-dejavu-core
sudo rm -rf /var/lib/apt/lists/*

rm -rf ~/.cache/matplotlib

# to make a blank database
#sqlite3 mlflow.db "VACUUM;"
git flow init -d || true

python3 -m pip install --upgrade pip setuptools wheel
python3 -m pip install -e ".[dev]"

#TODO Uncomment and update path to use MLFlow logging features
#mlflow server --backend-store-uri sqlite:////data/DATASCI/lab_notebook/mlflow.db --default-artifact-root /data/DATASCI/lab_notebook/mlruns
