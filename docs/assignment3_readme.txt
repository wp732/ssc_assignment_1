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

poetry run genson ~/checkpoint.json|jq 'del(."$schema")' > tests/checkpoint_schema.json

# Run pytest

poetry run pytest

# or for ease of use run my bin/run_pyetsts.sh script. Here are some examples:

bin/run_pyetsts.sh	# run all tests

bin/run_pyetsts.sh-s  # run all tests with stdout/stderr output added
 
bin/run_pyetsts.sh -s -f test_a1_consistency_tree_size_fail.py	# runs only this test with stdout/stderr output added

# Install pytest-cov

poetry add --dev pytest-cov
poetry add --dev pytest-env

# add the following to pyproject.toml
[tool.pytest.ini_options]
env = ["PYTHONPATH=."]

# also create .coveragerc file in project root dir as follows.
# note: the omit declaration is to exclude the non test_*.py
#       utility wrapper file that the tests call for subprocess
#       handling code.
[run]
branch = True
parallel = True
concurrency = multiprocessing
source = rekor/src,tests
omit =
	tests/run_test_wrappers.py

# Run the coverage test

USE_COVERAGE_CMD=1 poetry run pytest --cov=. tests/

# NOTE: The code in run_test_wrappers.py that called subprocess.run() will use coverage
#       instead of python when USE_COVERAGE_CMD=1 in order to ensure that code called
#       via subprocess gets coveraged because pytest --cov does not follow through
#       subprocess calls.

# NOTE: For ease of use just run my bin/run_coverage_tests.sh script.

# Setup for pre-commit and secrets scanning.

# I saved this for last as I found that Trufflehog take forever to run so
# doing this prior I would never have finished on time.

# Install pre-commit

sudo apt install pre-commit

# Trufflehog

# I built an entire ecosystem around this in order to ensure a trusted install of it
# and also because it is very complex to run.
# In the trufflehog/bin directory you will find all the scripts.
# There is some additional documentation in the trufflehog/docs directory.
# The install.sh script will safely install Trufflehog as a docker container, but
# that means you need to have docker preinstalled on tour system.
# Instructions for installing docker vary between Linux distributions, and I am not
# sure how you would do it on macOS (or even get these scripts working as zsh?), and
# I do not work on Windows systems, so good luck with that!
# The install.sh uses the get_digest.sh to get correct container disgest to fetch
# from DockerHub for your architecture. The is_version_installed.sh script is called
# by the scan_local_repo.sh script (which gets invoked via the pre-commit hook) at
# run time to check if you ran the install.sh first. The scan_local_repo.sh is
# what calls the dockerized version of Trufflehog. The script determins your git
# repo root and volume mounts it read only to the container and then runs the scan.
# I do have a security concern about the fact the container runs as root user. In the
# future (given more time) I could build it from source and make it run as non-root. 
# The .pre-commit-config.yaml would look like this:
repos:
  - repo: local
    hooks:
      - id: trufflehog_scan
        name: Running Trufflehog scan
        entry: bash
        language: system
        pass_filenames: false   
        args: ["-c", "set -o pipefail; ../scan_local_repo.sh | tee /dev/tty"]
# The tty and pipeail stuff are need to force stdout/stderr to display to your terminal
# while the scan script runs.
