#!/bin/sh
# @desc Initialize python venv
# @changed 2023.02.09, 16:59

test -f "./utils/config.sh" && . "./utils/config.sh"
test -f "./utils/config-local.sh" && . "./utils/config-local.sh"

# Global system requirements...
pip install setuptools virtualenv
# Create venv...
python -m virtualenv -p "$PYTHON_RUNTIME" .venv
# Activate venv
. ./.venv/Scripts/activate
# Install project dependencies...
pip install -r requirements-general.txt -r requirements-dev-only.txt
# User info...
echo "Use next command to activate venv: '. ./.venv/Scripts/activate'"
echo "Or for windows: 'call .venv/Scripts/activate'"

