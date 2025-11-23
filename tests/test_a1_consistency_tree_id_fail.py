"""Test failure of rekor consistency as per assignment 1."""

import sys
import json
import re
import pytest

from run_test_wrappers import (
    get_src_dir,
    run_py_program
)


def test_a1_consistency_tree_id_fail():
    src_dir = get_src_dir('wp732-rekor-tools')

    run_status, tty_out = run_py_program(
        f"{src_dir}/main.py",                    # py_path (program to run)
        [                                        # py_args (args to program)
            '--consistency',
            #'--tree-id', '1193050959916656506', # was good tree-id
            '--tree-id', '-1',                   # force bad tree-id
            '--tree-size', '479325266',
            '--root-hash',
            'cec16c9b824001c21439320f882a661ce1d84ba93fa29edc2340725e9804f0fd'
        ]
    )

    if run_status is False:
        print(tty_out, flush=True)
    else:
        match = re.search(
            r'^.*[Ee][Rr][Rr][Oo][Rr].*$',
            tty_out,
            re.MULTILINE
        )
        if match is not None:
            print(tty_out, flush=True)
        else:
            pytest.fail(tty_out)
