from typing import override, Self
from .expressions import (
    Expression as Exp,
    Relation as R,
    Source,
    Sum,
    ConstantString,
    ConstantNumber,
    ConstantBoolean,
    ConstantRelation,
    ConstantNull,
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

    def __add__(self, other: "Number[T] | int | float", /):
        match other:
            case Number():
                return Number(Sum(self.exp, other.exp))
            case int() | float():
                n = ConstantNumber(self.exp.source, other)
                return Number(Sum(self.exp, n))

    def __radd__(self, other: "Number[T] | int | float", /):
        match other:
            case Number():
                return Number(Sum(other.exp, self.exp))
            case int() | float():
                n = ConstantNumber(self.exp.source, other)
                return Number(Sum(n, self.exp))

    # def __radd__(self, other: Self, /):
    #     self.exp = Sum(self.exp, other.exp)
    #     return self


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

    def __add__(self, other: "String[T]", /):
        # if isinstance(other, str):
        #     other = String(other)
        return String(Sum(self.exp, other.exp))


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
