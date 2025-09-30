from abc import ABC, abstractmethod
from collections.abc import Mapping
from random import choice
from typing import Protocol, override, overload

from .expressions import (
    And,
    Concat,
    ConstantBoolean,
    ConstantNumber,
    ConstantString,
    ConstantNull,
    Divide,
    Equal,
    GreaterEqual,
    GreaterThan,
    LessEqual,
    LessThan,
    Multiply,
    Not,
    NotEqual,
    OneOf,
    Or,
    Source,
    Subtract,
    Sum,
)
from .expressions import (
    Expression as Exp,
)
from .expressions import (
    Relation as R,
)


class Sourceble(Protocol):
    def get_source(self) -> Source: ...


class Chain[T: Source](ABC):
    class ChainSrc(Source): ...

    def __init__(self, exp: Exp[T]) -> None:
        """Private constructor - use from_source() or from_parent() instead"""
        self.exp: Exp[T] = exp

    @property
    @abstractmethod
    def id(self) -> "Chain[T]": ...

    @override
    def __repr__(self) -> str:
        """Beautiful representation of Null with column names and arrows"""
        return self.exp.__repr__()

    def __getattr__(self, name: str):
        """If attribute not found, create a Null object"""
        return Null(R(self.exp, name))

    def get_source(self):
        return self.exp.source


class DateTime[T: Source](Chain[T]):
    """Any Date"""

    class DateTimeSrc(Source): ...

    @property
    @override
    def id(self):
        return DateTime(R(self.exp, "null"))


class Number[T: Source](Chain[T]):
    """Any Number"""

    class NumberSrc(Source): ...

    @property
    @override
    def id(self):
        return Number(R(self.exp, "null"))

    def _to_exp(self, other: "Number[T] | int | float", /):
        """Convert number or constant to expression"""
        match other:
            case Number():
                return other.exp
            case int() | float():
                return ConstantNumber(self.exp.source, other)

    def __add__(self, other: "Number[T] | int | float", /):
        return Number(Sum(self.exp, self._to_exp(other)))

    def __radd__(self, other: "Number[T] | int | float", /):
        return Number(Sum(self._to_exp(other), self.exp))

    def __sub__(self, other: "Number[T] | int | float", /):
        return Number(Subtract(self.exp, self._to_exp(other)))

    def __rsub__(self, other: "Number[T] | int | float", /):
        return Number(Subtract(self._to_exp(other), self.exp))

    def __mul__(self, other: "Number[T] | int | float", /):
        return Number(Multiply(self.exp, self._to_exp(other)))

    def __rmul__(self, other: "Number[T] | int | float", /):
        return Number(Multiply(self._to_exp(other), self.exp))

    def __truediv__(self, other: "Number[T] | int | float", /):
        return Number(Divide(self.exp, self._to_exp(other)))

    def __rtruediv__(self, other: "Number[T] | int | float", /):
        return Number(Divide(self._to_exp(other), self.exp))

    def __eq__(self, other: "Number[T] | int | float", /):
        """Equality comparison operator"""
        return Bool(Equal(self.exp, self._to_exp(other)))

    def __ne__(self, other: "Number[T] | int | float", /):
        """Not equal comparison operator"""
        return Bool(NotEqual(self.exp, self._to_exp(other)))

    def __lt__(self, other: "Number[T] | int | float", /):
        """Less than comparison operator"""
        return Bool(LessThan(self.exp, self._to_exp(other)))

    def __le__(self, other: "Number[T] | int | float", /):
        """Less than or equal comparison operator"""
        return Bool(LessEqual(self.exp, self._to_exp(other)))

    def __gt__(self, other: "Number[T] | int | float", /):
        """Greater than comparison operator"""
        return Bool(GreaterThan(self.exp, self._to_exp(other)))

    def __ge__(self, other: "Number[T] | int | float", /):
        """Greater than or equal comparison operator"""
        return Bool(GreaterEqual(self.exp, self._to_exp(other)))


class Bool[T: Source](Chain[T]):
    """Bool"""

    class BoolSrc(Source): ...

    @property
    @override
    def id(self):
        return Bool(R(self.exp, "null"))

    def _to_exp(self, other: "Bool[T] | bool", /):
        """Convert bool or constant to expression"""
        match other:
            case Bool():
                return other.exp
            case bool():
                return ConstantBoolean(self.exp.source, other)

    def __and__(self, other: "Bool[T] | bool", /):
        """Logical AND operator"""
        return Bool(And(self.exp, self._to_exp(other)))

    def __or__(self, other: "Bool[T] | bool", /):
        """Logical OR operator"""
        return Bool(Or(self.exp, self._to_exp(other)))

    def __invert__(self, /):
        """Logical NOT operator (~)"""
        return Bool(Not(self.exp))

    def __rand__(self, other: "Bool[T] | bool", /):
        """Reverse logical AND operator"""
        return Bool(And(self._to_exp(other), self.exp))

    def __ror__(self, other: "Bool[T] | bool", /):
        """Reverse logical OR operator"""
        return Bool(Or(self._to_exp(other), self.exp))

    def __eq__(self, other: "Bool[T] | bool", /):
        """Equality comparison operator"""
        return Bool(Equal(self.exp, self._to_exp(other)))

    def __ne__(self, other: "Bool[T] | bool", /):
        """Not equal comparison operator"""
        return Bool(NotEqual(self.exp, self._to_exp(other)))


class String[T: Source](Chain[T]):
    """Any String"""

    class StringSrc(Source): ...

    @property
    @override
    def id(self):
        return String(R(self.exp, "null"))

    def _to_exp(self, other: "String[T] | str", /):
        """Convert string or constant to expression"""
        match other:
            case String():
                return other.exp
            case str():
                return ConstantString(self.exp.source, other)

    def __add__(self, other: "String[T] | str", /):
        return String(Concat(self.exp, self._to_exp(other)))

    def __radd__(self, other: "String[T] | str", /):
        return String(Concat(self._to_exp(other), self.exp))

    def __eq__(self, other: "String[T] | str", /):
        """Equality comparison operator"""
        return Bool(Equal(self.exp, self._to_exp(other)))

    def __ne__(self, other: "String[T] | str", /):
        """Not equal comparison operator"""
        return Bool(NotEqual(self.exp, self._to_exp(other)))


class Null[T: Source](Chain[T]):
    """Any Null"""

    class NullSrc(Source): ...

    @property
    @override
    def id(self):
        return Null(R(self.exp, "null"))

    def _to_null(self, other: object, /):
        """Any operation with null returns null"""
        return Null(R(self.exp, "null"))

    # Arithmetic operations
    def __add__(self, other: object, /):
        return self._to_null(other)

    def __radd__(self, other: object, /):
        return self._to_null(other)

    def __sub__(self, other: object, /):
        return self._to_null(other)

    def __rsub__(self, other: object, /):
        return self._to_null(other)

    def __mul__(self, other: object, /):
        return self._to_null(other)

    def __rmul__(self, other: object, /):
        return self._to_null(other)

    def __truediv__(self, other: object, /):
        return self._to_null(other)

    def __rtruediv__(self, other: object, /):
        return self._to_null(other)

    # Comparison operations
    def __eq__(self, other: object, /):
        return self._to_null(other)

    def __ne__(self, other: object, /):
        return self._to_null(other)

    def __lt__(self, other: object, /):
        return self._to_null(other)

    def __le__(self, other: object, /):
        return self._to_null(other)

    def __gt__(self, other: object, /):
        return self._to_null(other)

    def __ge__(self, other: object, /):
        return self._to_null(other)

    # Logical operations
    def __and__(self, other: object, /):
        return self._to_null(other)

    def __or__(self, other: object, /):
        return self._to_null(other)

    def __invert__(self, /):
        return self._to_null(None)

    def __rand__(self, other: object, /):
        return self._to_null(other)

    def __ror__(self, other: object, /):
        return self._to_null(other)


def oneOf[*T](*args: *tuple[*T]):
    return choice(args)


def case[
    S: Source,
    K: Sourceble | int | float | str | bool | None,
    K2: Sourceble | int | float | str | bool | None,
](
    # src: S,
    conditions: Mapping[Bool[S], K],
    default: K2 = None,
):
    c = choice(tuple(conditions.values()) + (default,))
    src = list(conditions.keys())[0].get_source()
    return c, src


@overload
def toChain[S: Source](t: tuple[bool, S]) -> Bool[S]: ...
@overload
def toChain[S: Source](t: tuple[int, S]) -> Number[S]: ...
@overload
def toChain[S: Source](t: tuple[float, S]) -> Number[S]: ...
@overload
def toChain[S: Source](t: tuple[str, S]) -> String[S]: ...
@overload
def toChain[S: Source](t: tuple[None, S]) -> Null[S]: ...
@overload
def toChain[T: Sourceble, S: Source](t: tuple[T, S]) -> T: ...


def toChain[S: Source](
    t: tuple[Sourceble | int | float | str | bool | None, Source],
):
    """Принимает tuple из case и сохраняет специфичность типов toChain"""
    c, src = t
    if isinstance(c, str):
        return ConstantString(src, c)
    elif isinstance(c, bool):
        return ConstantBoolean(src, c)
    elif isinstance(c, int | float):
        return ConstantNumber(src, c)
    elif c is None:
        return ConstantNull(src)
    else:
        return c
