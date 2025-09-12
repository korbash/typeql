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


class Chain[SourceT: str](ABC):
    def __init__(
        self,
        source: SourceT,
        parent: "Chain[SourceT] | None" = None,
        relation: Parametr | Exp | None = None,
    ) -> None:
        """Private constructor - use from_source() or from_parent() instead"""
        self.source: SourceT = source
        self.parent: Chain[SourceT] | None = parent
        self.relation: Parametr | Exp | None = relation

        # Определяем базовый тип
        relation_str = str(self.relation or self.source)
        self.base_type: bool = relation_str.startswith(
            "base_type."
        ) or self.source.startswith("base_type.")

    @classmethod
    def from_parent(cls, parent: "Chain[SourceT]", relation: Parametr | Exp):
        """Create child chain element"""
        return cls(source=parent.source, parent=parent, relation=relation)

    @property
    @abstractmethod
    def id(self) -> "Chain[SourceT] | None":
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

    def __getattr__(self, name: str):
        """If attribute not found, create a Null object"""
        return Null[SourceT].from_parent(self, Parametr(f"not_definet.{name}"))


@final
class DateTime[T: str](Chain[T]):
    """Any Date"""

    @property
    @override
    def id(self):
        return Null[T].from_parent(self, Parametr("base_type.date_time"))


@final
class Number[T: str](Chain[T]):
    """Any Number"""

    @property
    @override
    def id(self):
        return Bool[T].from_parent(self, Parametr("base_type.number"))


@final
class Bool[T: str](Chain[T]):
    """Any Number"""

    @property
    @override
    def id(self):
        return Null[T].from_parent(self, Parametr("base_type.bool"))


@final
class String[T: str](Chain[T]):
    """Any String"""

    @property
    @override
    def id(self):
        return Null[T].from_parent(self, Parametr("base_type.string"))


@final
class Null[T: str](Chain[T]):
    """Base type for all SQL types"""

    @property
    @override
    def id(self):
        return None
        # return Null[T].from_parent(self, Parametr("base_type.null"))
