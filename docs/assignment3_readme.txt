# Install poetry

curl -sSL https://install.python-poetry.org | python3 -

cd <to root of this project>
export projdir=`git rev-parse --show-toplevel`	# we will use this later on

poetry init
poetry install --no-root

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

