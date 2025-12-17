import sys
import os
import yaml

MODEL_PATH = "metadata/model.example.yml"

# ---------- CORE HELPERS ----------

def fail(message: str):
    print(f"FAIL: {message}")
    sys.exit(1)

def pass_validation():
    print("PASS: semantic model validation successful")
    sys.exit(0)

def load_model(path: str) -> dict:
    if not os.path.exists(path):
        fail(f"model file not found: {path}")

    with open(path, "r") as f:
        try:
            model = yaml.safe_load(f)
        except yaml.YAMLError as e:
            fail(f"invalid YAML format: {e}")

    if not model:
        fail("model file is empty or invalid YAML")

    return model

# ---------- BASIC STRUCTURE VALIDATION ----------

def validate_facts(model: dict):
    facts = model.get("facts")
    if not facts:
        fail("no facts defined in model")

    for fact_name, fact_def in facts.items():
        grain = fact_def.get("grain")
        if not grain:
            fail(f"fact '{fact_name}' has no grain defined")

def validate_dimensions(model: dict):
    dimensions = model.get("dimensions")
    if not dimensions:
        fail("no dimensions defined in model")

    for dim_name, dim_def in dimensions.items():
        key = dim_def.get("key")
        if not key:
            fail(f"dimension '{dim_name}' has no key defined")

# ---------- RELATIONAL SEMANTICS ----------

def validate_fact_foreign_keys(model: dict):
    facts = model.get("facts", {})
    dimensions = model.get("dimensions", {})

    for fact_name, fact_def in facts.items():
        fact_grain = set(fact_def.get("grain", []))
        foreign_keys = fact_def.get("foreign_keys")

    if not foreign_keys:
        fail(f"fact '{fact_name}' defines no foreign_keys")

    if not isinstance(foreign_keys, list):
        fail(
        f"fact '{fact_name}' foreign_keys must be a list, "
        f"got {type(foreign_keys).__name__}"
    )

        for fk in foreign_keys:
            matching_dims = [
                dim_name
                for dim_name, dim_def in dimensions.items()
                if dim_def.get("key") == fk
            ]

            if matching_dims:
                if len(matching_dims) > 1:
                    fail(
                        f"foreign key '{fk}' in fact '{fact_name}' "
                        f"maps to multiple dimensions: {matching_dims}"
                    )
            else:
                if fk not in fact_grain:
                    fail(
                        f"foreign key '{fk}' in fact '{fact_name}' "
                        f"does not map to any dimension "
                        f"and is not part of fact grain"
                    )

def validate_grain_vs_foreign_keys(model: dict):
    facts = model.get("facts", {})

    for fact_name, fact_def in facts.items():
        grain = set(fact_def.get("grain", []))
        foreign_keys = set(fact_def.get("foreign_keys", []))

        overlap = grain.intersection(foreign_keys)
        if overlap:
            # Allowed ONLY if degenerate, but that is already checked above.
            # At this stage any overlap is invalid.
            fail(
                f"fact '{fact_name}' has foreign keys in grain: {sorted(overlap)}"
            )

def validate_no_many_to_many(model: dict):
    """
    Ensures that a single dimension key
    is not reused across multiple dimensions.
    """
    dimensions = model.get("dimensions", {})
    key_usage = {}

    for dim_name, dim_def in dimensions.items():
        key = dim_def.get("key")
        if not key:
            continue

        key_usage.setdefault(key, []).append(dim_name)

    for key, dims in key_usage.items():
        if len(dims) > 1:
            fail(
                f"many-to-many detected: key '{key}' "
                f"is used by multiple dimensions: {dims}"
            )

# ---------- SQL CONTRACT VALIDATION ----------

def validate_sql_files_exist(model: dict):
    facts = model.get("facts", {})
    for fact_name in facts.keys():
        path = f"sql/fact/{fact_name}.sql"
        if not os.path.exists(path):
            fail(f"missing SQL file for fact: {path}")

    dimensions = model.get("dimensions", {})
    for dim_name in dimensions.keys():
        path = f"sql/dim/{dim_name}.sql"
        if not os.path.exists(path):
            fail(f"missing SQL file for dimension: {path}")

def validate_sql_view_names(model: dict):
    objects = []
    objects.extend(model.get("facts", {}).keys())
    objects.extend(model.get("dimensions", {}).keys())

    for obj in objects:
        if obj.startswith("fact_"):
            path = f"sql/fact/{obj}.sql"
        else:
            path = f"sql/dim/{obj}.sql"

        if not os.path.exists(path):
            fail(f"SQL file not found for view name validation: {path}")

        with open(path, "r") as f:
            content = f.read().lower()

        expected = f"create or replace view {obj}".lower()
        if expected not in content:
            fail(f"SQL view name mismatch in {path}")

# ---------- ENTRYPOINT ----------

def main():
    model = load_model(MODEL_PATH)
    validate_facts(model)
    validate_dimensions(model)
    validate_fact_foreign_keys(model)
    validate_grain_vs_foreign_keys(model)
    validate_no_many_to_many(model)
    validate_sql_files_exist(model)
    validate_sql_view_names(model)
    pass_validation()

if __name__ == "__main__":
    main()
