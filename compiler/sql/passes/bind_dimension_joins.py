from compiler.sql.passes.base import SqlCompilerPass
from compiler.sql.runtime.ir import SqlQuery, SqlFactQuery, SqlJoin


class BindDimensionJoinsPass(SqlCompilerPass):
    """
    Attaches dimension join semantics to fact queries.

    Responsibilities:
    - map foreign keys to dimension tables
    - attach deterministic LEFT JOIN clauses
    - expose dimension key columns for SELECT
    """

    def __init__(self, semantic_ir):
        """
        semantic_ir: SemanticModelIR
        Used to map foreign keys to dimension definitions.
        """
        self.semantic_ir = semantic_ir

    def run(self, query: SqlQuery) -> SqlQuery:
        if not isinstance(query, SqlFactQuery):
            return query

        joins = []
        dimension_columns = []

        # Build FK → dimension mapping from semantic IR
        fk_to_dimension = {}
        for dim_name, dim in self.semantic_ir.dimensions.items():
            fk_to_dimension[dim.key] = dim_name

        for fk in query.foreign_keys:
            if fk not in fk_to_dimension:
                # Skip unknown FKs (semantic validator should catch this)
                continue

            dim_name = fk_to_dimension[fk]
            dim_table = dim_name  # e.g. dim_customer
            dim_key = self.semantic_ir.dimensions[dim_name].key

            joins.append(
                SqlJoin(
                    table=dim_table,
                    on=f"{query.from_table}.{fk} = {dim_table}.{dim_key}",
                )
            )

            # Expose dimension key in SELECT
            dimension_columns.append(f"{dim_table}.{dim_key}")

        return SqlFactQuery(
            select=query.select,
            from_table=query.from_table,
            joins=joins,
            group_by=query.group_by,
            grain_columns=query.grain_columns,
            foreign_keys=query.foreign_keys,
            measures=query.measures,
            aggregations=query.aggregations,
            dimension_columns=dimension_columns,
        )