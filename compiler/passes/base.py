from abc import ABC, abstractmethod
from compiler.runtime.ir import SemanticModelIR


class CompilerPass(ABC):
    """
    Base class for all compiler passes.

    A compiler pass takes a SemanticModelIR and returns
    a (possibly) transformed SemanticModelIR.
    """

    @abstractmethod
    def run(self, ir: SemanticModelIR) -> SemanticModelIR:
        raise NotImplementedError