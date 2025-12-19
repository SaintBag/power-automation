from compiler.sql.passes.base import SqlCompilerPass
from compiler.sql.runtime.ir import (
    SqlQuery,
    SqlFactQuery,
    SqlMeasureAggregation,
)


class BindMeasureAggregationPass(SqlCompilerPass):
    """
    Binds aggregation semantics to fact measures.

    Responsibilities:
    - attach aggregation operators to measures
    - preserve all previously inferred query semantics
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
            joins=query.joins,
            group_by=query.group_by,
            grain_columns=query.grain_columns,
            foreign_keys=query.foreign_keys,
            measures=query.measures,
            dimension_columns=query.dimension_columns,
            aggregations=aggregations,
        )