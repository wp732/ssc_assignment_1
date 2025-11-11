"""Test rekor log entry query as per assignment 1."""

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


def test_inclusion():
    test_dir = get_test_dir()
    src_dir = get_src_dir('rekor')
    data_dir = get_data_dir()
    artifact_path = f"{data_dir}/artifact.md"
    artifact_bundle_path = f"{data_dir}/artifact.bundle"
    log_index = None
    with open(artifact_bundle_path, "r") as artifact_bundle_file:
        artifact_bundle = json.load(artifact_bundle_file)
        log_index = artifact_bundle['rekorBundle']['Payload']['logIndex']
        log_index_str = str(log_index)

    run_status, tty_out = run_py_program(
        f"{src_dir}/main.py",                   # py_path (program to run)
        [                                       # py_args (args to program)
            '--entry', log_index_str,
        ]
    )

    if run_status is False:
        pytest.fail(tty_out)
    else:
        match = re.search(
            r'^.*[Ee][Rr][Rr][Oo][Rr].*$',
            tty_out,
            re.MULTILINE
        )
        if match is None:
            print(tty_out, flush=True)
        else:
            pytest.fail(tty_out)
