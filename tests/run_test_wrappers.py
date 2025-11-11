"""Utility wrapper for running tests."""

import json
from jsonschema import validate, ValidationError
import os
import subprocess
import sys
import pytest


def get_test_dir():
    return os.path.dirname(os.path.abspath(__file__))


def get_data_dir():
    return f"{get_test_dir()}/../data"


def get_src_dir(service):
    src_dir=None
    match service:
        case "rekor":
            src_dir = f"{get_test_dir()}/../rekor/src"
        case _:
            pass
    return src_dir


def get_bin_dir(service):
    src_dir=None
    match service:
        case "rekor":
            src_dir = f"{get_test_dir()}/../rekor/bin"
        case _:
            pass
    return src_dir


def run_py_program(py_path, py_args, verbose=False):

    run_status = True

    if os.environ.get("USE_COVERAGE_CMD") == "1":
        cmd_to_run = [ 'coverage', 'run', '--parallel-mode', py_path ]
    else:
        cmd_to_run = [ 'python', py_path, ]

    if verbose:
        print(
            f"\nINFO: running command: {py_path} {' '.join(py_args)}",
            flush=True
        )
    try:
        result = subprocess.run(
            cmd_to_run + py_args,
            capture_output=True,
            check=True,
            text=True
        )

        tty_out = f"{result.stdout}\n{result.stderr}"
        if result.returncode != 0:
            run_status = False
    except subprocess.CalledProcessError as e:
        run_status = False
        tty_out = f"Process failed with returncode: {str(e.returncode)}"
        tty_out = f"{tty_out}\n\n{e.stderr}"

    return (run_status, tty_out)

def run_cmd_program(cmd_path, cmd_args, verbose=False):

    run_status = True

    if verbose:
        print(
            f"\nINFO: running command: {cmd_path} {' '.join(cmd_args)}",
            flush=True
        )
    try:
        result = subprocess.run(
            [  cmd_path, ] + cmd_args,
            capture_output=True,
            check=True,
            text=True
        )

        tty_out = f"{result.stdout}\n{result.stderr}"
        if result.returncode != 0:
            run_status = False
    except subprocess.CalledProcessError as e:
        run_status = False
        tty_out = f"Process failed with returncode: {str(e.returncode)}"
        tty_out = f"{tty_out}\n\n{e.stderr}"

    return (run_status, tty_out)


def validate_py_program_json_output(schema_path, py_path, py_args, fail=False):

    run_status, tty_out = run_py_program(py_path, py_args)

    if run_status is True:
        data = json.loads(tty_out)

        with open(schema_path, "r") as schema_file:
            schema = json.load(schema_file)

        try:
            validate(instance=data, schema=schema)
            if fail is False:
                print(
                   f"\nSUCCESS: \
                        output from {py_path} matches schema {schema_path}"
                )
            else:
                pytest.fail(tty_out) # force fail when success on fail testing
        except ValidationError as e:
            if fail is False:
                pytest.fail(str(e))
            else:
                print(str(e), flush=True) # show error proof on fail testing
    else:
        if fail is False:
            pytest.fail(tty_out)
        else:
            print(tty_out, flush=True) # show error proof on fail testing


# Sample usage:
if __name__ == "__main__":
    test_dir = os.path.dirname(os.path.abspath(__file__))
    src_dir = f"{test_dir}/../rekor/src"
    validate_py_program_json_output(
        f"{test_dir}/checkpoint_schema.json",
        f"{src_dir}/main.py",
        [ '-c' ]
    )
