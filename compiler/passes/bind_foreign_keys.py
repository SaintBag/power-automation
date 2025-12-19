from compiler.passes.base import CompilerPass
from compiler.runtime.ir import SemanticModelIR


class BindForeignKeysPass(CompilerPass):
    """
    Validates that every fact foreign key maps to exactly one dimension key.
    """

    def run(self, ir: SemanticModelIR) -> SemanticModelIR:
        dimension_keys = {
            dim.key: dim_name
            for dim_name, dim in ir.dimensions.items()
        }

        for fact_name, fact in ir.facts.items():
            for fk in fact.foreign_keys:
                if fk not in dimension_keys:
                    raise ValueError(
                        f"Fact '{fact_name}' references unknown dimension key '{fk}'"
                    )

        return ir