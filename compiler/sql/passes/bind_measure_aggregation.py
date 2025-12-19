from compiler.sql.passes.base import SqlCompilerPass
from compiler.sql.runtime.ir import (
    SqlQuery,
    SqlFactQuery,
    SqlMeasureAggregation,
)

class BindMeasureAggregationPass(SqlCompilerPass):
    """
    Binds semantic aggregation rules to fact measures.

    Assumes:
    - input is SqlFactQuery
    - default aggregation is SUM
    """

    DEFAULT_AGGREGATION = "SUM"

    def run(self, query: SqlQuery) -> SqlQuery:
        if not isinstance(query, SqlFactQuery):
            return query

        aggregations = {}

        for measure in query.measures:
            aggregations[measure] = SqlMeasureAggregation(
                measure=measure,
                aggregation=self.DEFAULT_AGGREGATION,
            )

        return SqlFactQuery(
            select=query.select,
            from_table=query.from_table,
            group_by=query.group_by,
            grain_columns=query.grain_columns,
            foreign_keys=query.foreign_keys,
            measures=query.measures,
            aggregations=aggregations,
        )