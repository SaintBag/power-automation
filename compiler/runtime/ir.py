from dataclasses import dataclass
from typing import List, Dict


# ---------- Dimensions ----------

@dataclass(frozen=True)
class Dimension:
    name: str
    key: str
    grain: List[str]
    attributes: List[str]


# ---------- Facts ----------

@dataclass(frozen=True)
class Measure:
    name: str


@dataclass(frozen=True)
class Fact:
    name: str
    grain: List[str]
    measures: List[Measure]
    foreign_keys: List[str]


# ---------- Model ----------

@dataclass(frozen=True)
class SemanticModelIR:
    facts: Dict[str, Fact]
    dimensions: Dict[str, Dimension]