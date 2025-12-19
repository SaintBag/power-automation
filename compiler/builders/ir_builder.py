from compiler.runtime.ir import (
    SemanticModelIR,
    Fact,
    Measure,
    Dimension,
)


def build_ir(model: dict) -> SemanticModelIR:
    """
    Build Intermediate Representation (IR) from a validated semantic model.
    Assumes the model has already passed semantic validation.
    """

    facts_ir = {}
    for fact_name, fact_def in model.get("facts", {}).items():
        facts_ir[fact_name] = Fact(
            name=fact_name,
            grain=fact_def.get("grain", []),
            measures=[
                Measure(name=m)
                for m in fact_def.get("measures", [])
            ],
            foreign_keys=fact_def.get("foreign_keys", []),
        )

    dimensions_ir = {}
    for dim_name, dim_def in model.get("dimensions", {}).items():
        dimensions_ir[dim_name] = Dimension(
            name=dim_name,
            key=dim_def.get("key"),
            grain=dim_def.get("grain", []),
            attributes=dim_def.get("attributes", []),
        )

    return SemanticModelIR(
        facts=facts_ir,
        dimensions=dimensions_ir,
    )