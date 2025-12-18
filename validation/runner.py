import os
import subprocess
import sys

VALIDATOR_PATH = "validation/engine.py"

# ---------- PATH CONTRACT ----------
TEST_ROOT = "validation/tests"
POSITIVE_DIR = f"{TEST_ROOT}/positive"
NEGATIVE_DIR = f"{TEST_ROOT}/negative"


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

    tests = []

    # iterate explicitly over positive/negative dirs
    for root in (POSITIVE_DIR, NEGATIVE_DIR):
        if not os.path.isdir(root):
            continue
        for file in os.listdir(root):
            if file.endswith(".yml"):
                full_path = os.path.join(root, file)
                expected = 0 if "positive" in root else 1
                tests.append((full_path, expected))

    if not tests:
        print("No test cases found.")
        sys.exit(1)

    print(f"Discovered {len(tests)} test cases\n")

    failures = 0

    for test_path, expected in sorted(tests):
        print(f"Running test: {test_path}")
        exit_code = run_test(test_path)

        if (exit_code == 0 and expected != 0) or (exit_code != 0 and expected == 0):
            print(f"UNEXPECTED RESULT for {test_path}")
            failures += 1

        print("-" * 40)

    if failures:
        print(f"Test run failed. Unexpected results: {failures}")
        sys.exit(1)

    print("All tests behaved as expected.")
    sys.exit(0)


if __name__ == "__main__":
    main()