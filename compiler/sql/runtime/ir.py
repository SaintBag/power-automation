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


# ---------- SQL JOIN ----------

@dataclass(frozen=True)
class SqlJoin:
    """
    Semantic representation of a SQL JOIN.
    """
    table: str
    on: str
    join_type: str = "LEFT"


# ---------- BASE SQL QUERY ----------

@dataclass(frozen=True)
class SqlQuery:
    """
    Base SQL query abstraction.
    """
    select: List[SqlSelectColumn]
    from_table: str
    joins: List[SqlJoin]
    group_by: List[str]


# ---------- MEASURE AGGREGATION ----------

@dataclass(frozen=True)
class SqlMeasureAggregation:
    """
    Semantic definition of a measure aggregation.
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
    dimension_columns: List[str]