from compiler.runtime.ir import SemanticModelIR
from compiler.sql.runtime.ir import SqlQuery, SqlSelectColumn


def build_sql_ir_from_semantic(ir: SemanticModelIR) -> list[SqlQuery]:
    """
    Translate SemanticModelIR into initial SQL IR objects.

    This function defines the explicit boundary:
    Semantic IR -> SQL IR

    No SQL rendering or optimization is performed here.
    """

    queries: list[SqlQuery] = []

    for fact_name, fact in ir.facts.items():
        select_columns = []

        # Grain columns
        for column in fact.grain:
            select_columns.append(
                SqlSelectColumn(expression=column, alias=column)
            )

        # Foreign keys
        for fk in fact.foreign_keys:
            select_columns.append(
                SqlSelectColumn(expression=fk, alias=fk)
            )

        # Measures (no aggregation yet)
        for measure in fact.measures:
            select_columns.append(
                SqlSelectColumn(
                    expression=measure.name,
                    alias=measure.name,
                )
            )

        queries.append(
            SqlQuery(
                select=select_columns,
                from_table=fact_name,
                group_by=list(fact.grain),
            )
        )

    return queries