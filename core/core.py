from typing import override
from .expressions import Expression as Exp, Relation as R, Source


class Null[T: Source]:
    def __init__(self, exp: Exp[T]) -> None:
        """Private constructor - use from_source() or from_parent() instead"""
        self.exp: Exp[T] = exp

    @property
    # @abstractmethod
    def id(self) -> "Null[T] | None":
        return None

    @override
    def __repr__(self) -> str:
        """Beautiful representation of Null with column names and arrows"""
        return self.exp.__repr__()

    def __getattr__(self, name: str):
        """If attribute not found, create a Null object"""
        return Null(self.exp)


class DateTime[T: Source](Null[T]):
    """Any Date"""

    @property
    @override
    def id(self):
        return Null(R(self.exp, "null"))


class Number[T: Source](Null[T]):
    """Any Number"""

    @property
    @override
    def id(self):
        return Null(R(self.exp, "null"))


class Bool[T: Source](Null[T]):
    """Any Number"""

    @property
    @override
    def id(self):
        return Null(R(self.exp, "null"))


class String[T: Source](Null[T]):
    """Any String"""

    @property
    @override
    def id(self):
        return Null(R(self.exp, "null"))
