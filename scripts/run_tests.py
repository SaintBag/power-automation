import os
import subprocess
import sys

VALIDATOR_PATH = "scripts/validate_model.py"
TEST_ROOT = "test"


def run_test(model_path: str) -> int:
    env = os.environ.copy()
    env["MODEL_PATH"] = model_path

    result = subprocess.run(
    [sys.executable, VALIDATOR_PATH],
        env=env,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )

    print(result.stdout.strip())
    if result.stderr:
        print(result.stderr.strip())

    return result.returncode


def main():
    if not os.path.isdir(TEST_ROOT):
        print("No test directory found.")
        sys.exit(1)

    test_files = []

    for root, _, files in os.walk(TEST_ROOT):
        for file in files:
            if file.endswith(".yml"):
                test_files.append(os.path.join(root, file))

    if not test_files:
        print("No test cases found.")
        sys.exit(1)

    print(f"Discovered {len(test_files)} test cases\n")

    failures = 0

    for test in sorted(test_files):
        print(f"Running test: {test}")
        exit_code = run_test(test)

        if exit_code != 0:
            failures += 1

        print("-" * 40)

    print(f"Finished. Failed tests: {failures}")
    sys.exit(failures)


if __name__ == "__main__":
    main()
