"""Test rekor log entry query as per assignment 1 fails."""

import sys
import json
import re
import pytest

from run_test_wrappers import (
    get_test_dir,
    get_src_dir,
    run_py_program
)


def test_a1_logentry_fail():

    test_dir = get_test_dir()
    src_dir = get_src_dir('rekor')

    run_status, tty_out = run_py_program(
        f"{src_dir}/main.py",                   # py_path (program to run)
        [                                       # py_args (args to program)
            '--entry', "-1",                    # force bad index failure
        ],
        True                                    # enable verbose mode
    )

    if run_status is True:
        match = re.search(r"^.*[Ee][Rr][Rr][Oo][Rr].*$", tty_out, re.MULTILINE)
        if match is not None:
            print(tty_out, flush=True)
        else:
            pytest.fail(tty_out)    # test ran clean so treat as failure
