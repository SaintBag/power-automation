from typing import List

from compiler.sql.renderers.base import SqlRenderer
from compiler.sql.runtime.ir import (
    SqlFactQuery,
    SqlJoin,
    SqlSelectColumn,
    SqlMeasureAggregation,
)


class FactQueryRenderer(SqlRenderer):
    """
    Renders a SqlFactQuery into a deterministic SQL string.

    Foundations:
    - Single SELECT
    - FROM fact table
    - LEFT JOIN dimensions (if present)
    - GROUP BY grain columns
    """

    def __init__(self, query: SqlFactQuery):
        self.query = query

    def render(self) -> str:
        select_clause = self._render_select()
        from_clause = self._render_from()
        join_clause = self._render_joins()
        group_by_clause = self._render_group_by()

        clauses = [
            select_clause,
            from_clause,
            join_clause,
            group_by_clause,
        ]

        # Filter empty clauses deterministically
        return "\n".join([c for c in clauses if c])

    def _render_select(self) -> str:
        columns: List[str] = []

        # Grain columns first
        for col in self.query.grain_columns:
            if col not in columns:
                columns.append(col)

        # Dimension columns (excluding any duplicates)
        for col in self.query.dimension_columns:
            if col not in columns:
                columns.append(col)

        # Aggregated measures
        for measure, aggregation in self.query.aggregations.items():
            columns.append(
                f"{aggregation.aggregation}({measure}) AS {measure}"
            )

        return "SELECT\n  " + ",\n  ".join(columns)

    def _render_from(self) -> str:
        return f"FROM {self.query.from_table}"

    def _render_joins(self) -> str:
        if not self.query.joins:
            return ""

        rendered = []
        for join in self.query.joins:
            rendered.append(
                f"{join.join_type} JOIN {join.table} ON {join.on}"
            )

        return "\n".join(rendered)

    def _render_group_by(self) -> str:
        if not self.query.group_by:
            return ""

        return "GROUP BY " + ", ".join(self.query.group_by)