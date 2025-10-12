# Install Tooling (note: all work was done within a Python venv environment):

pip install ruff
pip install black
pip install pylint
pip install mypy
pip install bandit
pip install doq

# Analysis and Remidations

cd rekor/src/

# Use ruff linter on original *.py from assignment 1

ruff check -o ../../logs/ruff.initial.txt

# Use flake8 linter on original *.py from assignment 1
# Note: The sed is to filter out non-printable color escape characters.
#       The --color never option did not work so used sed instead.

flake8 | sed -r "s/\x1B\[[0-9;]*[mK]//g" > ../../logs/flake8.initial.txt

# Use mypy type checker on original *.py from assignment 1

mypy main.py  merkle_proof.py  util.py > ../../logs/mypy.initial.txt

# Note: mypy initial run had error:
# main.py:5: error: Library stubs not installed for "requests"  [import-untyped]
# Remidiation was to run: mypy --install-types
# This subsequent run resutled in no errors:

mypy main.py  merkle_proof.py  util.py > ../../logs/mypy.installed_types.txt

# Use bandit SAST tool on original *.py from assignment 1

bandit -r . -o ../../logs/bandit.initial.txt -f txt 
[main]	INFO	profile include tests: None
[main]	INFO	profile exclude tests: None
[main]	INFO	cli include tests: None
[main]	INFO	cli exclude tests: None
[main]	INFO	running on Python 3.11.2
[text]	INFO	Text output written to file: ../../logs/bandit.initial.txt

# Use black code formatter to reformat code to be PEP-8 compliant

black --verbose ./main.py 2>&1 | tee ../../logs/black.initial.txt

# Use doq to create docstring skeletons in code, then edit the code to fill in the details

doq -f main.py --formatter google -w
