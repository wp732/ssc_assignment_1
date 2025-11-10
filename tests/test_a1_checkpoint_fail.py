"""Test if rekor checkpoint ouput matches schema as per assignment 1 (pass)."""

import pytest

from run_test_wrappers import (
    get_test_dir,
    get_src_dir,
    validate_py_program_json_output
)


def test_a1_checkpoint_pass():
    test_dir = get_test_dir()
    src_dir = get_src_dir('rekor')
    validate_py_program_json_output(
        f"{test_dir}/checkpoint_schema_bad.json",   # output schema path
        f"{src_dir}/main.py",                       # py_path (program to run)
        [                                           # py_args (args to program) 
            '-c'
        ],
        True                                        # show output
    )
