from dataclasses import dataclass
from typing import List


@dataclass(frozen=True)
class SqlSelectColumn:
    """
    Represents a single column in a SELECT clause.
    """
    expression: str
    alias: str


@dataclass(frozen=True)
class SqlQuery:
    """
    Abstract representation of a SQL query.

    This is NOT a SQL string.
    """
    select: List[SqlSelectColumn]
    from_table: str
    group_by: List[str]