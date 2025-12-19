from abc import ABC, abstractmethod


class SqlRenderer(ABC):
    """
    Base contract for SQL renderers.
    """

    @abstractmethod
    def render(self) -> str:
        """
        Render SQL IR into a SQL string.
        """
        raise NotImplementedError