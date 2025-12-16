import sys
import os
import yaml


MODEL_PATH = "metadata/model.example.yml"


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
            return yaml.safe_load(f)
        except yaml.YAMLError as e:
            fail(f"invalid YAML format: {e}")


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

def validate_fact_foreign_keys(model: dict):
    facts = model.get("facts", {})
    dimensions = model.get("dimensions", {})

    dimension_keys = {
        dim_def.get("key"): dim_name
        for dim_name, dim_def in dimensions.items()
    }

    for fact_name, fact_def in facts.items():
        foreign_keys = fact_def.get("foreign_keys", [])
        if not foreign_keys:
            fail(f"fact '{fact_name}' defines no foreign_keys")

        for fk in foreign_keys:
            if fk not in dimension_keys:
                fail(
                    f"fact '{fact_name}' foreign key '{fk}' "
                    f"does not match any dimension key"
                )
                
def validate_no_many_to_many(model: dict):
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

def main():
    model = load_model(MODEL_PATH)
    validate_facts(model)
    validate_dimensions(model)
    validate_fact_foreign_keys(model)
    validate_no_many_to_many(model)
    pass_validation()

if __name__ == "__main__":
    main()
