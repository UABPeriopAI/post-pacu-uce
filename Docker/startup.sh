#!/bin/sh
sudo apt-get update
sudo apt-get install msttcorefonts -qq
rm ~/.cache/matplotlib -rf

# to make a blank database
#sqlite3 mlflow.db "VACUUM;"
git flow init -d

cd src/
python3 -m pip install pip setuptools wheel
python3 -m pip install -e ".[dev]"
cd ../

#TODO Uncomment and update path to use MLFlow logging features
#mlflow server --backend-store-uri sqlite:////data/DATASCI/lab_notebook/mlflow.db --default-artifact-root /data/DATASCI/lab_notebook/mlruns