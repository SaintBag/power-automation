from abc import ABC, abstractmethod
from compiler.sql.runtime.ir import SqlQuery


class SqlCompilerPass(ABC):
    """
    Base class for all SQL compiler passes.
    """

    @abstractmethod
    def run(self, query: SqlQuery) -> SqlQuery:
        raise NotImplementedError