from pathlib import Path

from setuptools import find_namespace_packages, setup

# Load packages from requirements.txt
BASE_DIR = Path(__file__).parent
with open(Path(BASE_DIR, "requirements.txt"), "r") as file:
    required_packages = [ln.strip() for ln in file.readlines()]

docs_packages = ["mkdocs==1.3.0", "mkdocstrings==0.18.1"]

style_packages = ["black==22.6.0", "flake8==3.9.2", "isort==5.10.1"]

# setup.py
setup(
    name="postpacu",
    version=0.1,
    description="Predict post-PACU escalations of care.",
    # who authored the file we're looking at right now
    author="Ryan L. Melvin",
    author_email="rmelvin@uabmc.edu",
    python_requires=">=3.8",
    packages=find_namespace_packages(),
    install_requires=[required_packages],
    extras_require={"dev": docs_packages + style_packages, "docs": docs_packages},
)
