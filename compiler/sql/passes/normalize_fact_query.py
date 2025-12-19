from compiler.sql.passes.base import SqlCompilerPass
from compiler.sql.runtime.ir import SqlQuery, SqlFactQuery, SqlSelectColumn

class NormalizeFactQueryPass(SqlCompilerPass):
    """
    Normalizes a generic SqlQuery into a SqlFactQuery.

    Assumes input query represents a fact-level query.
    """
    def run(self, query: SqlQuery) -> SqlQuery:
        # Extract column aliases
        column_aliases = [col.alias for col in query.select]

        # Infer semantic roles deterministically
        grain_columns = list(query.group_by)
        foreign_keys = [
            col for col in column_aliases
            if col not in grain_columns
        ]

        # Measures are inferred as non-grain, non-FK columns
        measures = [
            col for col in foreign_keys
        ]

        return SqlFactQuery(
            select=query.select,
            from_table=query.from_table,
            group_by=query.group_by,
            grain_columns=grain_columns,
            foreign_keys=foreign_keys,
            measures=measures,
        )