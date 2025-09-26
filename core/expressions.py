from dataclasses import dataclass
from typing import override


@dataclass(frozen=True)
class Source:
    """Represents a data source, like a table."""

    name: str

    @override
    def __repr__(self) -> str:
        return self.name


@dataclass(frozen=True)
class Expression:
    """Base class for expressions."""

    source: Source


@dataclass(frozen=True, init=False)
class Relation(Expression):
    """Represents getting an attribute from another expression."""

    exp: Expression
    relation_name: str

    def __init__(self, exp: Expression, relation_name: str):
        super().__init__(source=exp.source)
        object.__setattr__(self, "exp", exp)
        object.__setattr__(self, "relation_name", relation_name)

    @override
    def __repr__(self) -> str:
        return f"{self.exp}.{self.relation_name}"


@dataclass(frozen=True, init=False)
class Sum(Expression):
    """Represents a sum function call."""

    left: Expression
    right: Expression

    def __init__(self, left: Expression, right: Expression):
        if left.source is right.source:
            super().__init__(source=left.source)
            object.__setattr__(self, "left", left)
            object.__setattr__(self, "right", right)
        else:
            raise ValueError("Expressions must have the same source")

    @override
    def __repr__(self) -> str:
        return f"sum({self.left}, {self.right})"


@dataclass(frozen=True, init=False)
class Coalesce(Expression):
    """Represents a coalesce function call."""

    values: tuple[Expression, ...]

    def __init__(self, *values: Expression):
        if len(values) < 2:
            raise ValueError("COALESCE requires at least 2 values")

        # Проверяем что все выражения из одного источника
        first_source = values[0].source
        if not all(v.source is first_source for v in values):
            raise ValueError("All expressions must have the same source")

        super().__init__(source=first_source)
        object.__setattr__(self, "values", values)

    @override
    def __repr__(self) -> str:
        values_str = ", ".join(str(v) for v in self.values)
        return f"coalesce({values_str})"
