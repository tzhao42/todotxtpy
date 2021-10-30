#!/bin/bash

# refresh environment

cd ..

if [[ -d "env" ]]; then
    rm -r env
fi

python3.10 -m venv env
source env/bin/activate

python3 -m pip install --upgrade pip

# install development packages
pip3 install mypy
pip3 install isort
pip3 install black
pip3 install pylint
pip3 install pytest
