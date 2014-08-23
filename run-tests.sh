#!/bin/sh
pylint --ignore='.venv' . | tee pylint.out
pep8 --exclude='.venv' . | tee pep8.out
python tests.py
