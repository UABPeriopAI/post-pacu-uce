#!/bin/bash

cd /workspaces/WagenerPostPACU/src
pip install --upgrade pip setuptools wheel\
    && pip install -e ".[dev]"
