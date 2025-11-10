"""Test rekor inclusion."""

import sys

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

    std_out = run_py_program(
        #f"{test_dir}/inclusion_schema.json",    # output schema path
        f"{src_dir}/main.py",                   # py_path (program to run)
        [                                       # py_args (args to program)
            '--inclusion', log_index,
            '--artifact', artifact_path
        ]
    )

    print(std_out, flush=True)
