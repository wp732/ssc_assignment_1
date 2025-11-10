"""Test rekor consistency as per assignment 1."""

import sys
import json
import re
import pytest

from run_test_wrappers import (
    get_src_dir,
    run_py_program
)


def test_consistency():
    src_dir = get_src_dir('rekor')

    run_status, tty_out = run_py_program(
        f"{src_dir}/main.py",                   # py_path (program to run)
        [                                       # py_args (args to program)
            '--consistency',
            '--tree-id', '1193050959916656506',
            '--tree-size', '479325266',
            '--root-hash',
            'cec16c9b824001c21439320f882a661ce1d84ba93fa29edc2340725e9804f0fd'
        ]
    )

    if run_status is False:
        pytest.fail(tty_out)
    else:
        print(tty_out, flush=True)
