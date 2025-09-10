from typing import final, Literal, NamedTuple, override, Callable, Self
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
        self, parent: "Chain | None" = None, relation: Parametr | Exp | None = None
    ) -> None:
        """element of Chain"""
        if (relation is None and parent is not None) or (
            relation is not None and parent is None
        ):
            raise ValueError("parent and relation must be both None or both not None")
        if parent is None:
            self.source: str = "placeholder"
            my_id = self.id
            self.source = str(my_id.relation)
        else:
            self.source = parent.source

        self.relation: Parametr | Exp | None = relation
        self.parent: Chain | None = parent
        if str(self.relation or self.source).startswith("base_type."):
            self.base_type = True
        else:
            self.base_type = False

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
        return Null(self, Parametr("base_type.date_time"))


@final
class Number(Chain):
    """Any Number"""

    @property
    @override
    def id(self):
        return Null(self, Parametr("base_type.number"))


@final
class String(Chain):
    """Any String"""

    @property
    @override
    def id(self):
        return Null(self, Parametr("base_type.string"))

@final
class Null(Chain):
    """Base type for all SQL types"""

    @property
    @override
    def id(self):
        return Null(self, Parametr("base_type.null"))
