from typing import override
from .expressions import (
    Expression as Exp,
    Relation as R,
    Source,
    Sum,
    Subtract,
    Multiply,
    Divide,
    Concat,
    Equal,
    NotEqual,
    LessThan,
    LessEqual,
    GreaterThan,
    GreaterEqual,
    ConstantString,
    ConstantNumber,
)
from random import choice
from abc import ABC, abstractmethod


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

    def __or__[K](self, value: K):
        c = choice((1, 2))
        if c == 1:
            return self
        else:
            return value

    # def __ror__(self, value: Self):
    #     c = choice((1, 2))
    #     if c == 1:
    #         return value
    #     else:
    #         return self


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


class Null[T: Source](Chain[T]):
    """Any Null"""

    class NullSrc(Source): ...

    @property
    @override
    def id(self):
        return Null(R(self.exp, "null"))


# class Constant:
#     @classmethod
#     def constNumber(cls, source: Source, n: int | float):
#         return Number((source, n))

# def constNumber(source: Source, n: int | float):
#     return Number(R(source, n))
