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

```bash
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




