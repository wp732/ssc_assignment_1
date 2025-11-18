"""Test rekor inclusion as per assignment 1 fails."""

import sys
import json
import re
import pytest

from run_test_wrappers import (
    get_test_dir,
    get_src_dir,
    get_data_dir,
    run_py_program
)


def test_a1_inclusion_fail():
    test_dir = get_test_dir()
    src_dir = get_src_dir('wp732-rekor-tools')
    data_dir = get_data_dir()
    artifact_path = f"{data_dir}/artifact.md"

    run_status, tty_out = run_py_program(
        f"{src_dir}/main.py",                   # py_path (program to run)
        [                                       # py_args (args to program)
            '--inclusion', "-1",                # cause bad index failure
            '--artifact', artifact_path
        ],
        True                                    # enable verbose mode
    )

    if run_status is True:
        match = re.search(
            r'^Offline root hash calculation for inclusion verified$',
            tty_out,
            re.MULTILINE
        )
        if match is not None:
            pytest.fail(tty_out)    # test ran clean so treat as failure
        else:
            print(tty_out, flush=True)
