from typing import List
from compiler.runtime.ir import SemanticModelIR
from compiler.passes.base import CompilerPass


class CompilerPipeline:
    """
    Sequential compiler pipeline executing registered passes.
    """

    def __init__(self, passes: List[CompilerPass]):
        self._passes = passes

    def run(self, ir: SemanticModelIR) -> SemanticModelIR:
        current_ir = ir
        for compiler_pass in self._passes:
            current_ir = compiler_pass.run(current_ir)
        return current_ir