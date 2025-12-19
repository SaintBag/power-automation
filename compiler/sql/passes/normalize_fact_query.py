from compiler.sql.passes.base import SqlCompilerPass
from compiler.sql.runtime.ir import (
    SqlQuery,
    SqlFactQuery,
)


class NormalizeFactQueryPass(SqlCompilerPass):
    """
    Normalizes a generic SqlQuery into a SqlFactQuery.

    Responsibilities:
    - infer fact-level semantics
    - establish grain / FK / measure roles
    - initialize empty aggregation + join structures

    Does NOT:
    - resolve dimension joins
    - bind aggregation semantics
    """

    def run(self, query: SqlQuery) -> SqlQuery:
        # Extract column aliases
        column_aliases = [col.alias for col in query.select]

        # Grain is defined by GROUP BY
        grain_columns = list(query.group_by)

        # Foreign keys = non-grain columns
        foreign_keys = [
            col for col in column_aliases
            if col not in grain_columns
        ]

        # Measures are inferred as non-grain columns
        measures = list(foreign_keys)

        return SqlFactQuery(
            select=query.select,
            from_table=query.from_table,
            group_by=query.group_by,
            grain_columns=grain_columns,
            foreign_keys=foreign_keys,
            measures=measures,
            dimension_columns=list(foreign_keys),
            aggregations={},
            joins=query.joins,
        )