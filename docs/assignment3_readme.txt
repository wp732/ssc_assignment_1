# Install poetry

curl -sSL https://install.python-poetry.org | python3 -

cd <to root of this project>
export projdir=`git rev-parse --show-toplevel`	# we will use this later on

poetry init
poetry install --no-root

# Install deptry to discover import packages missing from poetry venv

# Need to restict python version for this in pyproject.toml via: requires-python = ">=3.11,<4.0"

poetry add --dev deptry

# Also set the folling in pyproject.toml:
[tool.deptry]
root = ["src", "tests"]
exclude = ["venv", ".venv", ".direnv", ".git", "setup.py"]

# Now we can report on missing or unused packages (excluding local imported .py files):

poetry run deptry . 2>&1|egrep -v -e "[']merkle_proof[']|[']util[']"

# As a result, the following needed to be added:

poetry add requests
poetry add cryptography

# Reinstall Tooling via poetry

poetry add --dev pylint
poetry add --dev black
poetry add --dev ruff
poetry add --dev mypy
poetry add --dev bandit
poetry add --dev doq

# Exmaples for running assignment 2 tooling via poetry:

cd ${projdir}/rekor/src
poetry run ruff check -o ../../logs/ruff.final.txt
poetry run flake8 | sed -r "s/\x1B\[[0-9;]*[mK]//g" > ../../logs/flake8.final.txt
poetry run pylint . --output ../../logs/pylint.final.txt
poetry run mypy main.py  merkle_proof.py  util.py > ../../logs/mypy.final.txt
poetry run bandit -r . -o ../../logs/bandit.final.txt -f txt

# Install pytest

poetry add --dev pytest
poetry add jsonschema	# needed in test .py codes

# Genrate test schemas

poetry add --dev genson	# nice tool for generating JSON schemas from .json files

# for example, from a previously saved checkpoint.json output...

poetry run genson ~/checkpoint.json|jq '.' > tests/checkpoint_schema.json
