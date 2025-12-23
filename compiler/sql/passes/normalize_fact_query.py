from compiler.sql.passes.base import SqlCompilerPass
from compiler.sql.runtime.ir import (
    SqlQuery,
    SqlFactQuery,
)


class NormalizeFactQueryPass(SqlCompilerPass):
    """
    Normalizes a generic SqlQuery into a SqlFactQuery.

    Responsibilities:
    - derive fact-level semantics from the initial SQL IR
    - establish grain / foreign key / measure roles
    - initialize empty aggregation structures

    Does NOT:
    - resolve dimension joins
    - bind aggregation semantics
    """

    def run(self, query: SqlQuery) -> SqlQuery:
        # Column aliases from the SELECT clause
        column_aliases = [col.alias for col in query.select]

        # Grain is defined by GROUP BY
        grain_columns = list(query.group_by)

        # Foreign keys: heuristically, columns ending with "_id" and not part of the grain
        foreign_keys = [
            alias
            for alias in column_aliases
            if alias.endswith("_id") and alias not in grain_columns
        ]

        # Dimension-like columns: foreign keys + date-like columns (e.g. *_date),
        # excluding grain columns to avoid duplication
        dimension_columns = list(foreign_keys)
        for alias in column_aliases:
            if (
                alias.endswith("_date")
                and alias not in dimension_columns
                and alias not in grain_columns
            ):
                dimension_columns.append(alias)

        # Measures: non-grain, non-FK, non-date columns
        measures = [
            alias
            for alias in column_aliases
            if alias not in grain_columns
            and alias not in foreign_keys
            and not alias.endswith("_date")
        ]

        return SqlFactQuery(
            select=query.select,
            from_table=query.from_table,
            joins=query.joins,
            group_by=query.group_by,
            grain_columns=grain_columns,
            foreign_keys=foreign_keys,
            measures=measures,
            aggregations={},
            dimension_columns=dimension_columns,
        )