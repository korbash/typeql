from dataclasses import dataclass
from typing import override
import datetime


@dataclass(init=False)
class Source:
    def __init__(self):
        self.name: str = self.__class__.__name__

    @override
    def __repr__(self) -> str:
        return self.name


@dataclass(frozen=True)
class Expression[T: Source]:
    """Base class for expressions."""

    source: T

    @override
    def __repr__(self) -> str:
        return str(self.source)


@dataclass(frozen=True)
class ConstantNumber[T: Source](Expression[T]):
    source: T
    value: int | float

    @override
    def __repr__(self) -> str:
        return f"{self.value}"


@dataclass(frozen=True)
class ConstantString[T: Source](Expression[T]):
    source: T
    value: str

    @override
    def __repr__(self) -> str:
        return f"'{self.value}'"


@dataclass(frozen=True)
class ConstantBoolean[T: Source](Expression[T]):
    source: T
    value: bool

    @override
    def __repr__(self) -> str:
        return f"{self.value}"


@dataclass(frozen=True)
class ConstantNull[T: Source](Expression[T]):
    source: T

    @override
    def __repr__(self) -> str:
        return "null"


@dataclass(frozen=True)
class ConstantDateTime[T: Source](Expression[T]):
    source: T
    value: datetime.datetime

    @override
    def __repr__(self) -> str:
        return f"{self.value}"


@dataclass(frozen=True, init=False)
class Relation[T: Source](Expression[T]):
    """Represents getting an attribute from another expression."""

    exp: Expression[T]
    relation_name: str

    def __init__(self, exp: Expression[T], relation_name: str):
        super().__init__(source=exp.source)
        object.__setattr__(self, "exp", exp)
        object.__setattr__(self, "relation_name", relation_name)

    @override
    def __repr__(self) -> str:
        return f"{self.exp}.{self.relation_name}"


@dataclass(frozen=True, init=False)
class Sum[T: Source](Expression[T]):
    """Represents a sum function call."""

    left: Expression[T]
    right: Expression[T]

    def __init__(self, left: Expression[T], right: Expression[T]):
        if left.source == right.source:
            super().__init__(source=left.source)
            object.__setattr__(self, "left", left)
            object.__setattr__(self, "right", right)
        else:
            raise ValueError("Expressions must have the same source")

    @override
    def __repr__(self) -> str:
        return f"sum({self.left}, {self.right})"


@dataclass(frozen=True, init=False)
class Subtract[T: Source](Expression[T]):
    """Represents a subtract function call."""

    left: Expression[T]
    right: Expression[T]

    def __init__(self, left: Expression[T], right: Expression[T]):
        if left.source == right.source:
            super().__init__(source=left.source)
            object.__setattr__(self, "left", left)
            object.__setattr__(self, "right", right)
        else:
            raise ValueError("Expressions must have the same source")

    @override
    def __repr__(self) -> str:
        return f"subtract({self.left}, {self.right})"


@dataclass(frozen=True, init=False)
class Multiply[T: Source](Expression[T]):
    """Represents a multiply function call."""

    left: Expression[T]
    right: Expression[T]

    def __init__(self, left: Expression[T], right: Expression[T]):
        if left.source == right.source:
            super().__init__(source=left.source)
            object.__setattr__(self, "left", left)
            object.__setattr__(self, "right", right)
        else:
            raise ValueError("Expressions must have the same source")

    @override
    def __repr__(self) -> str:
        return f"multiply({self.left}, {self.right})"


@dataclass(frozen=True, init=False)
class Divide[T: Source](Expression[T]):
    """Represents a divide function call."""

    left: Expression[T]
    right: Expression[T]

    def __init__(self, left: Expression[T], right: Expression[T]):
        if left.source == right.source:
            super().__init__(source=left.source)
            object.__setattr__(self, "left", left)
            object.__setattr__(self, "right", right)
        else:
            raise ValueError("Expressions must have the same source")

    @override
    def __repr__(self) -> str:
        return f"divide({self.left}, {self.right})"


@dataclass(frozen=True, init=False)
class Concat[T: Source](Expression[T]):
    """Represents a string concatenation function call."""

    left: Expression[T]
    right: Expression[T]

    def __init__(self, left: Expression[T], right: Expression[T]):
        if left.source == right.source:
            super().__init__(source=left.source)
            object.__setattr__(self, "left", left)
            object.__setattr__(self, "right", right)
        else:
            raise ValueError("Expressions must have the same source")

    @override
    def __repr__(self) -> str:
        return f"concat({self.left}, {self.right})"


@dataclass(frozen=True, init=False)
class Equal[T: Source](Expression[T]):
    """Represents an equality comparison."""

    left: Expression[T]
    right: Expression[T]

    def __init__(self, left: Expression[T], right: Expression[T]):
        if left.source == right.source:
            super().__init__(source=left.source)
            object.__setattr__(self, "left", left)
            object.__setattr__(self, "right", right)
        else:
            raise ValueError("Expressions must have the same source")

    @override
    def __repr__(self) -> str:
        return f"equal({self.left}, {self.right})"


@dataclass(frozen=True, init=False)
class NotEqual[T: Source](Expression[T]):
    """Represents a not-equal comparison."""

    left: Expression[T]
    right: Expression[T]

    def __init__(self, left: Expression[T], right: Expression[T]):
        if left.source == right.source:
            super().__init__(source=left.source)
            object.__setattr__(self, "left", left)
            object.__setattr__(self, "right", right)
        else:
            raise ValueError("Expressions must have the same source")

    @override
    def __repr__(self) -> str:
        return f"not_equal({self.left}, {self.right})"


@dataclass(frozen=True, init=False)
class LessThan[T: Source](Expression[T]):
    """Represents a less-than comparison."""

    left: Expression[T]
    right: Expression[T]

    def __init__(self, left: Expression[T], right: Expression[T]):
        if left.source == right.source:
            super().__init__(source=left.source)
            object.__setattr__(self, "left", left)
            object.__setattr__(self, "right", right)
        else:
            raise ValueError("Expressions must have the same source")

    @override
    def __repr__(self) -> str:
        return f"less_than({self.left}, {self.right})"


@dataclass(frozen=True, init=False)
class LessEqual[T: Source](Expression[T]):
    """Represents a less-than-or-equal comparison."""

    left: Expression[T]
    right: Expression[T]

    def __init__(self, left: Expression[T], right: Expression[T]):
        if left.source == right.source:
            super().__init__(source=left.source)
            object.__setattr__(self, "left", left)
            object.__setattr__(self, "right", right)
        else:
            raise ValueError("Expressions must have the same source")

    @override
    def __repr__(self) -> str:
        return f"less_equal({self.left}, {self.right})"


@dataclass(frozen=True, init=False)
class GreaterThan[T: Source](Expression[T]):
    """Represents a greater-than comparison."""

    left: Expression[T]
    right: Expression[T]

    def __init__(self, left: Expression[T], right: Expression[T]):
        if left.source == right.source:
            super().__init__(source=left.source)
            object.__setattr__(self, "left", left)
            object.__setattr__(self, "right", right)
        else:
            raise ValueError("Expressions must have the same source")

    @override
    def __repr__(self) -> str:
        return f"greater_than({self.left}, {self.right})"


@dataclass(frozen=True, init=False)
class GreaterEqual[T: Source](Expression[T]):
    """Represents a greater-than-or-equal comparison."""

    left: Expression[T]
    right: Expression[T]

    def __init__(self, left: Expression[T], right: Expression[T]):
        if left.source == right.source:
            super().__init__(source=left.source)
            object.__setattr__(self, "left", left)
            object.__setattr__(self, "right", right)
        else:
            raise ValueError("Expressions must have the same source")

    @override
    def __repr__(self) -> str:
        return f"greater_equal({self.left}, {self.right})"


@dataclass(frozen=True, init=False)
class Coalesce[T: Source](Expression[T]):
    """Represents a coalesce function call."""

    values: tuple[Expression[T], ...]

    def __init__(self, *values: Expression[T]):
        # Проверяем что все выражения из одного источника
        first_source = values[0].source
        if not all(v.source == first_source for v in values):
            raise ValueError("All expressions must have the same source")

        super().__init__(source=first_source)
        object.__setattr__(self, "values", values)

    @override
    def __repr__(self) -> str:
        values_str = ", ".join(str(v) for v in self.values)
        return f"coalesce({values_str})"


# @dataclass(frozen=True, init=False)
# class Stack[T: Source](Expression[T]):
#     values: tuple[Expression[T], ...]

#     def __init__(self, *values: Expression[T]):
#         # Проверяем что все выражения из одного источника
#         first_source = values[0].source
#         if not all(v.source is first_source for v in values):
#             raise ValueError("All expressions must have the same source")

#         super().__init__(source=first_source)
#         object.__setattr__(self, "values", values)

#     @override
#     def __repr__(self) -> str:
#         values_str = ", ".join(str(v) for v in self.values)
#         return f"stack({values_str})"
