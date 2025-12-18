# Semantic Model Validation — Test Cases

This directory contains **isolated test cases** for the semantic model validator.

The purpose of these tests is to verify that the validation engine:
- accepts valid semantic models,
- rejects invalid semantic models,
- fails deterministically at the correct validation stage.

These tests are **structural and semantic**.
They do **not** access any data and do **not** modify production artifacts.

---

## Design Principles

### 1. Isolation

Test cases:
- do not modify files under `metadata/`, `sql/`, or `scripts/`,
- operate only on test-specific YAML files,
- are executed by overriding the model path via `MODEL_PATH`.

Production behavior remains unchanged.

---

### 2. Determinism

Each test case:
- is self-contained,
- has a single responsibility,
- produces a predictable outcome (`PASS` or `FAIL`),
- validates a specific rule or failure mode.

---

### 3. Explicit Expectations

Negative test cases are designed to fail intentionally.

Each negative test documents:
- the violated semantic rule,
- the expected validation stage,
- the reason for failure.

A test that does not fail when expected indicates a defect in the validator.

---

## Directory Structure

test/
├── README.md
├── positive/
│ └── model_valid.yml
└── negative/
├── foreign_key_without_dimension.yml
└── measure_without_aggregation.yml

---

## Positive Tests

### `positive/model_valid.yml`

A known-good semantic model.

Purpose:
- regression safety net,
- ensures that valid models always pass validation,
- detects unintended breaking changes in the validator.

Expected result:

---

## Negative Tests

### `negative/foreign_key_without_dimension.yml`

**Rule violated:**  
Fact-to-dimension relationship integrity.

The fact declares a foreign key that does not map to any dimension key.

Expected failure stage:

---

### `negative/measure_without_aggregation.yml`

**Rule violated:**  
Fact measures must be aggregated in SQL.

The fact declares a measure that exists in SQL but is not aggregated.

Expected failure stage:

---

## Running Tests Locally

Each test is executed by overriding the model path:

MODEL_PATH=tests/positive/model_valid.yml python3 scripts/validate_model.py
MODEL_PATH=tests/negative/foreign_key_without_dimension.yml python3 scripts/validate_model.py
MODEL_PATH=tests/negative/measure_without_aggregation.yml python3 scripts/validate_model.py

CI Integration
These test cases are designed to be executed automatically in CI
using a dedicated test harness.
Production validation (metadata/model.example.yml) remains unchanged
and continues to run independently.
Non-Goals
This directory does not contain:
unit tests for Python functions,
SQL execution tests,
data quality checks.
The scope is strictly limited to semantic model contract validation.


---

## Automated Test Runner

### Purpose

The automated test runner executes all semantic model validation tests
defined under the `test/` directory and verifies their expected outcome.

It is designed to be:
- deterministic
- framework-free
- CI-friendly

---

### Running Tests Locally

From the repository root:

```bash
python3 scripts/run_tests.py


```
Exit codes:
0 — all tests behaved as expected
1 — at least one test produced an unexpected result

---

## Adding New Test Cases

### Positive Test

Place valid semantic model definitions under:

```bash
test/positive/
```
Rules:
- the validator must PASS
- exit code 0 is expected

### Negative Tests

Negative Tests

```bash
test/negative/
```

Rules:
- the validator must FAIL
- non-zero exit code is expected

Each test case is a standalone YAML file.
No SQL or metadata files are modified during test execution.

---

## Design Notes

- the validator engine is treated as a black box
- test execution is driven exclusively via MODEL_PATH
- no external dependencies or test frameworks are used
