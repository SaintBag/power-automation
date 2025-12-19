from typing import List
from compiler.sql.runtime.ir import SqlQuery
from compiler.sql.passes.base import SqlCompilerPass


class SqlCompilerPipeline:
    """
    Sequential SQL compiler pipeline.
    """

    def __init__(self, passes: List[SqlCompilerPass]):
        self._passes = passes

    def run(self, query: SqlQuery) -> SqlQuery:
        current = query
        for compiler_pass in self._passes:
            current = compiler_pass.run(current)
        return current