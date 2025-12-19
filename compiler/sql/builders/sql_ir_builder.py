from typing import List

from compiler.runtime.ir import SemanticModelIR
from compiler.sql.runtime.ir import (
    SqlQuery,
    SqlSelectColumn,
)


def build_sql_ir_from_semantic(
    semantic_ir: SemanticModelIR,
) -> List[SqlQuery]:
    """
    Translates SemanticModelIR into initial SQL IR objects.

    Compiler boundary:
        Semantic IR  →  SQL IR

    Responsibilities:
    - materialize fact-level SELECT projections
    - preserve grain semantics
    - initialize join structure (empty at this stage)

    Explicitly DOES NOT:
    - generate joins
    - apply aggregations
    - render SQL
    - infer semantics
    """

    queries: List[SqlQuery] = []

    for fact_name, fact in semantic_ir.facts.items():
        select_columns: List[SqlSelectColumn] = []

        # --- Grain columns ---
        for column in fact.grain:
            select_columns.append(
                SqlSelectColumn(
                    expression=column,
                    alias=column,
                )
            )

        # --- Foreign keys ---
        for fk in fact.foreign_keys:
            select_columns.append(
                SqlSelectColumn(
                    expression=fk,
                    alias=fk,
                )
            )

        # --- Measures (raw, no aggregation yet) ---
        for measure in fact.measures:
            select_columns.append(
                SqlSelectColumn(
                    expression=measure.name,
                    alias=measure.name,
                )
            )

        query = SqlQuery(
            select=select_columns,
            from_table=fact_name,
            group_by=list(fact.grain),
            joins=[],  # ← REQUIRED by SqlQuery contract
        )

        queries.append(query)

    return queries