from typing import final, override, Self
from dataclasses import dataclass
from abc import ABC, abstractmethod

@dataclass
class Parametr:
    column: str

    @override
    def __repr__(self) -> str:
        return self.column


@dataclass
class Exp:
    fun: str
    arg0: Self | Parametr
    arg1: Self | Parametr


class Chain(ABC):

    def __init__(
        self,
        source: str,
        parent: "Chain | None" = None,
        relation: "Parametr | Exp | None" = None
    ) -> None:
        """Private constructor - use from_source() or from_parent() instead"""
        self.source: str = source
        self.parent: "Chain | None" = parent
        self.relation: "Parametr | Exp | None" = relation

        # Определяем базовый тип
        relation_str = str(self.relation or self.source)
        self.base_type: bool = relation_str.startswith("base_type.") or self.source.startswith("base_type.")

    @classmethod
    def from_source(cls, source: str) -> Self:
        """Create root chain element"""
        return cls(source=source)

    @classmethod
    def from_parent(cls, parent: "Chain", relation: Parametr | Exp) -> Self:
        """Create child chain element"""
        return cls(source=parent.source, parent=parent, relation=relation)

    @property
    @abstractmethod
    def id(self) -> "Chain":
        """Beautiful representation of Chain with full path"""

    @override
    def __repr__(self) -> str:
        """Beautiful representation of Chain with column names and arrows"""

        path_parts: list[str] = []
        current = self

        while current.parent is not None:
            path_parts.append(str(current.relation))
            current = current.parent

        # Reverse to get correct order and join with arrows
        path_parts.append(self.source)
        path_parts.reverse()
        return " -> ".join(path_parts)


@final
class DateTime(Chain):
    """Any Date"""

    @property
    @override
    def id(self):
        return Null.from_parent(self, Parametr("base_type.date_time"))


@final
class Number(Chain):
    """Any Number"""

    @property
    @override
    def id(self):
        return Null.from_parent(self, Parametr("base_type.number"))


@final
class String(Chain):
    """Any String"""

    @property
    @override
    def id(self):
        return Null.from_parent(self, Parametr("base_type.string"))

@final
class Null(Chain):
    """Base type for all SQL types"""

    @property
    @override
    def id(self):
        return Null.from_parent(self, Parametr("base_type.null"))
