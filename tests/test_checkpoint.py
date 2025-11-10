from run_test_wrappers import get_test_dir, get_src_dir, validate_json_output

def test_checkpoint():
    test_dir = get_test_dir()
    src_dir = get_src_dir('rekor')
    validate_json_output(
        f"{test_dir}/checkpoint_schema.json",
        f"{src_dir}/main.py",
        [ '-c' ]
    )
