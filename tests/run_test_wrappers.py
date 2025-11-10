"""Utility wrapper for running tests."""

import json
from jsonschema import validate
import os
import subprocess
import sys


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


def run_py_program(py_path, py_args):

    result = subprocess.run(
        [ 'python', py_path, ] + py_args,
        capture_output=True,
        text=True
    )

    return result.stdout


def validate_py_program_json_output(schema_path, py_path, py_args):

    std_out = run_py_program(py_path, py_args)

    data = json.loads(std_out)

    with open(schema_path, "r") as schema_file:
        schema = json.load(schema_file)

    validate(instance=data, schema=schema)


# Sample usage:
if __name__ == "__main__":
    test_dir = os.path.dirname(os.path.abspath(__file__))
    src_dir = f"{test_dir}/../rekor/src"
    validate_py_program_json_output(
        f"{test_dir}/checkpoint_schema.json",
        f"{src_dir}/main.py",
        [ '-c' ]
    )
