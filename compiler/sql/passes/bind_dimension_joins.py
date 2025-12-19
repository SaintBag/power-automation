from compiler.sql.passes.base import SqlCompilerPass
from compiler.sql.runtime.ir import SqlQuery, SqlFactQuery, SqlJoin


class BindDimensionJoinsPass(SqlCompilerPass):
    """
    Attaches dimension join semantics to fact queries.
    """

    def run(self, query: SqlQuery) -> SqlQuery:
        if not isinstance(query, SqlFactQuery):
            return query

        joins = []
        dimension_columns = []

        for fk in query.foreign_keys:
            dimension_table = f"dim_{fk.replace('_id', '')}"

            joins.append(
                SqlJoin(
                    table=dimension_table,
                    on=f"{query.from_table}.{fk} = {dimension_table}.id",
                )
            )

            dimension_columns.append(f"{dimension_table}.name")

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