import sys
import os
import yaml
import re

MODEL_PATH = os.environ.get(
    "MODEL_PATH",
    "semantic/model.contract.yml"
)

# ---------- REFACTORED PATH CONSTANTS ----------

FACT_SQL_DIR = "sql/facts"
DIM_SQL_DIR = "sql/dimensions"

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
        fact_grain = {g.lower() for g in fact_def.get("grain", [])}
        foreign_keys = fact_def.get("foreign_keys")

        if not foreign_keys:
            fail(f"fact '{fact_name}' defines no foreign_keys")

        if not isinstance(foreign_keys, list):
            fail(
                f"fact '{fact_name}' foreign_keys must be a list, "
                f"got {type(foreign_keys).__name__}"
            )

        for fk in foreign_keys:
            fk_lower = fk.lower()
            matching_dims = [
                dim_name
                for dim_name, dim_def in dimensions.items()
                if dim_def.get("key", "").lower() == fk_lower
            ]

            if matching_dims:
                if len(matching_dims) > 1:
                    fail(
                        f"foreign key '{fk}' in fact '{fact_name}' "
                        f"maps to multiple dimensions: {matching_dims}"
                    )
            else:
                if fk_lower not in fact_grain:
                    fail(
                        f"foreign key '{fk}' in fact '{fact_name}' "
                        f"does not map to any dimension "
                        f"and is not part of fact grain"
                    )

def validate_grain_vs_foreign_keys(model: dict):
    facts = model.get("facts", {})

    for fact_name, fact_def in facts.items():
        grain = {g.lower() for g in fact_def.get("grain", [])}
        foreign_keys = {fk.lower() for fk in fact_def.get("foreign_keys", [])}

        overlap = grain.intersection(foreign_keys)
        if overlap:
            fail(
                f"fact '{fact_name}' has foreign keys in grain: {sorted(overlap)}"
            )

def validate_fact_grain_vs_sql(model: dict):
    facts = model.get("facts", {})

    for fact_name, fact_def in facts.items():
        grain = fact_def.get("grain", [])
        if not grain:
            continue

        sql_path = f"{FACT_SQL_DIR}/{fact_name}.sql"
        if not os.path.exists(sql_path):
            fail(f"missing SQL file for fact: {sql_path}")

        try:
            with open(sql_path, "r") as f:
                sql_content = f.read().lower()
        except OSError as e:
            fail(f"cannot read SQL file {sql_path}: {e}")

        for grain_col in grain:
            token = grain_col.lower()
            if token not in sql_content:
                fail(
                    f"fact '{fact_name}' grain column '{grain_col}' "
                    f"not found in SQL definition"
                )

def validate_no_many_to_many(model: dict):
    dimensions = model.get("dimensions", {})
    key_usage = {}

    for dim_name, dim_def in dimensions.items():
        key = dim_def.get("key")
        if not key:
            continue

        key_lower = key.lower()
        key_usage.setdefault(key_lower, []).append(dim_name)

    for key, dims in key_usage.items():
        if len(dims) > 1:
            fail(
                f"many-to-many detected: key '{key}' "
                f"is used by multiple dimensions: {dims}"
            )

def validate_fact_foreign_keys_vs_sql(model: dict):
    facts = model.get("facts", {})

    for fact_name, fact_def in facts.items():
        foreign_keys = fact_def.get("foreign_keys", [])
        if not foreign_keys:
            continue

        sql_path = f"{FACT_SQL_DIR}/{fact_name}.sql"
        if not os.path.exists(sql_path):
            fail(f"missing SQL file for fact: {sql_path}")

        try:
            with open(sql_path, "r") as f:
                sql_content = f.read().lower()
        except OSError as e:
            fail(f"cannot read SQL file {sql_path}: {e}")

        for fk in foreign_keys:
            token = fk.lower()
            if token not in sql_content:
                fail(
                    f"fact '{fact_name}' foreign key '{fk}' "
                    f"not found in SQL definition"
                )

def validate_fact_measures_vs_sql(model: dict):
    facts = model.get("facts", {})

    aggregations = ["sum(", "count(", "avg(", "min(", "max("]

    for fact_name, fact_def in facts.items():
        measures = fact_def.get("measures", [])
        grain = {g.lower() for g in fact_def.get("grain", [])}
        foreign_keys = {fk.lower() for fk in fact_def.get("foreign_keys", [])}

        if not measures:
            continue

        sql_path = f"{FACT_SQL_DIR}/{fact_name}.sql"
        if not os.path.exists(sql_path):
            fail(f"missing SQL file for fact: {sql_path}")

        try:
            with open(sql_path, "r") as f:
                sql_content = f.read().lower()
        except OSError as e:
            fail(f"cannot read SQL file {sql_path}: {e}")

        for measure in measures:
            token = measure.lower()

            if token not in sql_content:
                fail(
                    f"fact '{fact_name}' measure '{measure}' "
                    f"not found in SQL definition"
                )

            if token in grain:
                fail(
                    f"fact '{fact_name}' measure '{measure}' "
                    f"is part of grain — invalid fact design"
                )

            if token in foreign_keys:
                fail(
                    f"fact '{fact_name}' measure '{measure}' "
                    f"is also a foreign key — invalid fact design"
                )

            if not any(agg in sql_content for agg in aggregations):
                fail(
                    f"fact '{fact_name}' measure '{measure}' "
                    f"is not aggregated in SQL"
                )

def extract_sql_columns(sql: str) -> list[str]:
    select_match = re.search(
        r"select\s+(.*?)\s+from",
        sql,
        re.IGNORECASE | re.DOTALL,
    )
    if not select_match:
        return []

    columns_block = select_match.group(1)

    columns = []
    for line in columns_block.split(","):
        line = line.strip()
        if " as " in line.lower():
            alias = line.split()[-1]
            columns.append(alias)
        else:
            columns.append(line.split(".")[-1])

    return [c.strip() for c in columns]

def validate_fact_attributes(model: dict):
    facts = model.get("facts", {})

    for fact_name, fact_def in facts.items():
        path = f"{FACT_SQL_DIR}/{fact_name}.sql"
        if not os.path.exists(path):
            fail(f"missing SQL file for fact: {path}")

        with open(path) as f:
            sql = f.read()

        sql_columns = [c.lower() for c in extract_sql_columns(sql)]
        allowed = {c.lower() for c in (
            fact_def.get("grain", [])
            + fact_def.get("foreign_keys", [])
            + fact_def.get("measures", [])
            + fact_def.get("attributes", [])
        )}

        for col in sql_columns:
            if col not in allowed:
                fail(
                    f"fact '{fact_name}' has undeclared column '{col}' "
                    f"in SQL view (allowed: {sorted(allowed)})"
                )

def validate_dimension_attributes(model: dict):
    dimensions = model.get("dimensions", {})

    for dim_name, dim_def in dimensions.items():
        path = f"{DIM_SQL_DIR}/{dim_name}.sql"
        if not os.path.exists(path):
            fail(f"missing SQL file for dimension: {path}")

        with open(path) as f:
            sql = f.read()

        sql_columns = [c.lower() for c in extract_sql_columns(sql)]
        allowed = {c.lower() for c in (
            [dim_def.get("key")]
            + dim_def.get("attributes", [])
        )}

        for col in sql_columns:
            if col not in allowed:
                fail(
                    f"dimension '{dim_name}' has undeclared column '{col}' "
                    f"in SQL view (allowed: {sorted(allowed)})"
                )

# ---------- SQL CONTRACT VALIDATION ----------

def validate_sql_files_exist(model: dict):
    facts = model.get("facts", {})
    for fact_name in facts.keys():
        path = f"{FACT_SQL_DIR}/{fact_name}.sql"
        if not os.path.exists(path):
            fail(f"missing SQL file for fact: {path}")

    dimensions = model.get("dimensions", {})
    for dim_name in dimensions.keys():
        path = f"{DIM_SQL_DIR}/{dim_name}.sql"
        if not os.path.exists(path):
            fail(f"missing SQL file for dimension: {path}")

def validate_sql_view_names(model: dict):
    objects = []
    objects.extend(model.get("facts", {}).keys())
    objects.extend(model.get("dimensions", {}).keys())

    for obj in objects:
        if obj.startswith("fact_"):
            path = f"{FACT_SQL_DIR}/{obj}.sql"
        else:
            path = f"{DIM_SQL_DIR}/{obj}.sql"

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

    # 1. SQL filesystem contract
    validate_sql_files_exist(model)

    # 2. Core semantic structure
    validate_facts(model)
    validate_dimensions(model)

    # 3. Relational semantics
    validate_fact_foreign_keys(model)
    validate_grain_vs_foreign_keys(model)
    validate_no_many_to_many(model)

    # 4. SQL naming & relational alignment
    validate_sql_view_names(model)
    validate_fact_grain_vs_sql(model)
    validate_fact_foreign_keys_vs_sql(model)

    # 5. Measures semantics
    validate_fact_measures_vs_sql(model)

    # 6. Attribute contract (strictest)
    validate_fact_attributes(model)
    validate_dimension_attributes(model)

    pass_validation()

if __name__ == "__main__":
    main()