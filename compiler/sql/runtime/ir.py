from dataclasses import dataclass
from typing import List, Dict

# ---------- SQL SELECT ----------

@dataclass(frozen=True)
class SqlSelectColumn:
    """
    Represents a single column in a SELECT clause.
    """
    expression: str
    alias: str

# ---------- BASE SQL QUERY ----------

@dataclass(frozen=True)
class SqlQuery:
    """
    Base SQL query abstraction.
    """
    select: List[SqlSelectColumn]
    from_table: str
    group_by: List[str]

# ---------- MEASURE AGGREGATION ----------

@dataclass(frozen=True)
class SqlMeasureAggregation:
    """
    Semantic definition of a measure aggregation.

    Example:
    - measure: total_amount
    - aggregation: SUM
    """
    measure: str
    aggregation: str

# ---------- FACT SQL QUERY ----------

@dataclass(frozen=True)
class SqlFactQuery(SqlQuery):
    """
    Specialized SQL query representing a FACT.
    """
    grain_columns: List[str]
    foreign_keys: List[str]
    measures: List[str]
    aggregations: Dict[str, SqlMeasureAggregation]