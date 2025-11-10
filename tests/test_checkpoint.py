from run_test_wrappers import get_test_dir, validate_json_output

def test_checkpoint():
    test_dir = get_test_dir()
    src_dir = f"{test_dir}/../rekor/src"
    validate_json_output(
        f"{test_dir}/checkpoint_schema.json",
        f"{src_dir}/main.py",
        [ '-c' ]
    )
