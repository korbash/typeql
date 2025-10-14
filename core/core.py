import datetime
from abc import ABC, abstractmethod
from collections.abc import Mapping
from random import choice
from typing import Protocol, override, overload, runtime_checkable, Self, Any

from .expressions import (
    And,
    Case,
    Concat,
    ConstantBoolean,
    ConstantDateTime,
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
    Or,
    Source,
    Subtract,
    Sum,
    AggSum,
    AggAvg,
    AggCount,
    AggUniq,
)
from .expressions import (
    Expression as Exp,
)
from .expressions import (
    Relation as R,
)


@runtime_checkable
class Sourceble(Protocol):
    def get_source(self) -> Source: ...

    # def get_self_type(self) -> Source: ...

    # def get_expression(self) -> Exp[Source]: ...

    # def eq(self, other) -> "Bool[Source]": ...

    # def ne(self, other) -> "Bool[Source]": ...


@runtime_checkable
class SourcebleGN[S: Source, SS: Source](Protocol):
    def get_source(self) -> S: ...

    def get_self_type(self) -> SS: ...

    def get_expression(self) -> Exp[S]: ...


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

    def get_expression(self):
        return self.exp

    @classmethod
    def get_self_type(cls):
        return cls.ChainSrc()

    def _count[U: Source](self, path: SourcebleGN[T, U]):
        return Number(AggCount(path.get_self_type(), self.exp, path.get_expression()))

    def _uniq[U: Source](self, path: SourcebleGN[T, U]):
        return Number(AggUniq(path.get_self_type(), self.exp, path.get_expression()))

    @override
    def __hash__(self):
        """Hash based on the expression"""
        return hash(self.exp)

    # @abstractmethod
    # def eq(self, other: Self): ...

    # @abstractmethod
    # def ne(self, other: Self): ...


class DateTime[T: Source](Chain[T]):
    """Any Date"""

    class DateTimeSrc(Chain.ChainSrc):
        """Source for DateTime"""

    @property
    @override
    def id(self):
        return DateTime(R(self.exp, "null"))

    @classmethod
    @override
    def get_self_type(cls):
        return cls.DateTimeSrc()

    def _to_exp(self, other: "DateTime[T] | datetime.datetime", /):
        """Convert datetime or constant to expression"""
        match other:
            case DateTime():
                return other.exp
            case datetime.datetime():
                return ConstantDateTime(self.exp.source, other)

    def __lt__(self, other: "DateTime[T] | datetime.datetime", /):
        """Less than comparison operator"""
        return Bool(LessThan(self.exp, self._to_exp(other)))

    def __le__(self, other: "DateTime[T] | datetime.datetime", /):
        """Less than or equal comparison operator"""
        return Bool(LessEqual(self.exp, self._to_exp(other)))

    def __gt__(self, other: "DateTime[T] | datetime.datetime", /):
        """Greater than comparison operator"""
        return Bool(GreaterThan(self.exp, self._to_exp(other)))

    def __ge__(self, other: "DateTime[T] | datetime.datetime", /):
        """Greater than or equal comparison operator"""
        return Bool(GreaterEqual(self.exp, self._to_exp(other)))

    def ne(self, other: "DateTime[T] | datetime.datetime"):
        """Not equal comparison operator"""
        return Bool(NotEqual(self.exp, self._to_exp(other)))

    def eq(self, other: "DateTime[T] | datetime.datetime"):
        """Equal comparison operator"""
        return Bool(Equal(self.exp, self._to_exp(other)))

    def hour(self) -> "DateHour[T]":
        """Extract hour from datetime"""
        return DateHour(R(self.exp, "hour"))

    def day(self) -> "DateDay[T]":
        """Extract day from datetime"""
        return DateDay(R(self.exp, "day"))

    def week(self) -> "DateWeek[T]":
        """Extract week from datetime"""
        return DateWeek(R(self.exp, "week"))

    def month(self) -> "DateMonth[T]":
        """Extract month from datetime"""
        return DateMonth(R(self.exp, "month"))

    def year(self) -> "DateYear[T]":
        """Extract year from datetime"""
        return DateYear(R(self.exp, "year"))

    def second(self) -> "DateSecond[T]":
        """Extract second from datetime"""
        return DateSecond(R(self.exp, "second"))

    def minute(self) -> "DateMinute[T]":
        """Extract minute from datetime"""
        return DateMinute(R(self.exp, "minute"))


class DateHour[T: Source](DateTime[T]):
    """Hour part of DateTime"""

    class DateHourSrc(DateTime.DateTimeSrc):
        """Source for DateHour"""

    @property
    @override
    def id(self):
        return DateTime(R(self.exp, "null"))

    @classmethod
    @override
    def get_self_type(cls):
        return cls.DateHourSrc()


class DateDay[T: Source](DateTime[T]):
    """Day part of DateTime"""

    class DateDaySrc(DateTime.DateTimeSrc):
        """Source for DateDay"""

    @property
    @override
    def id(self):
        return DateTime(R(self.exp, "null"))

    @classmethod
    @override
    def get_self_type(cls):
        return cls.DateDaySrc()


class DateWeek[T: Source](DateTime[T]):
    """Week part of DateTime"""

    class DateWeekSrc(DateTime.DateTimeSrc):
        """Source for DateWeek"""

    @property
    @override
    def id(self):
        return DateTime(R(self.exp, "null"))

    @classmethod
    @override
    def get_self_type(cls):
        return cls.DateWeekSrc()


class DateMonth[T: Source](DateTime[T]):
    """Month part of DateTime"""

    class DateMonthSrc(DateTime.DateTimeSrc):
        """Source for DateMonth"""

    @property
    @override
    def id(self):
        return DateTime(R(self.exp, "null"))

    @classmethod
    @override
    def get_self_type(cls):
        return cls.DateMonthSrc()


class DateYear[T: Source](DateTime[T]):
    """Year part of DateTime"""

    class DateYearSrc(DateTime.DateTimeSrc):
        """Source for DateYear"""

    @property
    @override
    def id(self):
        return DateTime(R(self.exp, "null"))

    @classmethod
    @override
    def get_self_type(cls):
        return cls.DateYearSrc()


class DateSecond[T: Source](DateTime[T]):
    """Second part of DateTime"""

    class DateSecondSrc(DateTime.DateTimeSrc):
        """Source for DateSecond"""

    @property
    @override
    def id(self):
        return DateTime(R(self.exp, "null"))

    @classmethod
    @override
    def get_self_type(cls):
        return cls.DateSecondSrc()


class DateMinute[T: Source](DateTime[T]):
    """Minute part of DateTime"""

    class DateMinuteSrc(DateTime.DateTimeSrc):
        """Source for DateMinute"""

    @property
    @override
    def id(self):
        return DateTime(R(self.exp, "null"))

    @classmethod
    @override
    def get_self_type(cls):
        return cls.DateMinuteSrc()


class Number[T: Source](Chain[T]):
    """Any Number"""

    class NumberSrc(Chain.ChainSrc): ...

    @property
    @override
    def id(self):
        return Number(R(self.exp, "null"))

    @classmethod
    @override
    def get_self_type(cls):
        return cls.NumberSrc()

    def _sum[U: Source](self, path: SourcebleGN[T, U]):
        return Number(AggSum(path.get_self_type(), self.exp, path.get_expression()))

    def _avg[U: Source](self, path: SourcebleGN[T, U]):
        return Number(AggAvg(path.get_self_type(), self.exp, path.get_expression()))

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

    def ne(self, other: "Number[T] | int | float"):
        """Not equal comparison operator"""
        return Bool(NotEqual(self.exp, self._to_exp(other)))

    def eq(self, other: "Number[T] | int | float"):
        """Equal comparison operator"""
        return Bool(Equal(self.exp, self._to_exp(other)))


class Bool[T: Source](Chain[T]):
    """Bool"""

    class BoolSrc(Chain.ChainSrc): ...

    @property
    @override
    def id(self):
        return Bool(R(self.exp, "null"))

    @classmethod
    @override
    def get_self_type(cls):
        return cls.BoolSrc()

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

    def eq(self, other: "Bool[T] | bool", /):
        """Equality comparison operator"""
        return Bool(Equal(self.exp, self._to_exp(other)))

    def ne(self, other: "Bool[T] | bool", /):
        """Not equal comparison operator"""
        return Bool(NotEqual(self.exp, self._to_exp(other)))


class String[T: Source](Chain[T]):
    """Any String"""

    class StringSrc(Chain.ChainSrc): ...

    @property
    @override
    def id(self):
        return String(R(self.exp, "null"))

    @classmethod
    @override
    def get_self_type(cls):
        return cls.StringSrc()

    def _to_exp(self, other: "String[T] | str"):
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

    def eq(self, other: "String[T] | str"):
        """Equality comparison operator"""
        return Bool(Equal(self.exp, self._to_exp(other)))

    def ne(self, other: "String[T] | str"):
        """Not equal comparison operator"""
        return Bool(NotEqual(self.exp, self._to_exp(other)))


class Null[T: Source](Chain[T]):
    """Any Null"""

    class NullSrc(Chain.ChainSrc): ...

    @property
    @override
    def id(self):
        return Null(R(self.exp, "null"))

    @classmethod
    @override
    def get_self_type(cls):
        return cls.NullSrc()

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
    def eq(self, other: object):
        return self._to_null(other)

    def ne(self, other: object):
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

    def _sum(self, other: object, /):
        return self._to_null(other)

    def _avg(self, other: object, /):
        return self._to_null(other)


def oneOf[*T](*args: *tuple[*T]):
    return choice(args)


def case[
    S: Source,
    K: Sourceble | int | float | str | bool | datetime.datetime | None,
    K2: Sourceble | int | float | str | bool | datetime.datetime | None,
](
    # src: S,
    conditions: Mapping[Bool[S], K],
    default: K2 = None,
):
    c = choice(tuple(conditions.values()) + (default,))

    # Создаем выражение Case
    def _to_expression(value: K | datetime.datetime | K2, source: S) -> Exp[S]:
        if isinstance(value, str):
            return ConstantString(source, value)
        elif isinstance(value, bool):
            return ConstantBoolean(source, value)
        elif isinstance(value, (int, float)):
            return ConstantNumber(source, value)
        elif isinstance(value, datetime.datetime):
            return ConstantDateTime(source, value)
        elif value is None:
            return ConstantNull(source)
        elif isinstance(value, Sourceble):
            return value.get_expression()
        else:
            raise TypeError(f"Unsupported type for case value: {type(value)}")

    # Преобразуем условия в кортежи выражений
    src = list(conditions.keys())[0].get_source()
    conditions_exp = {k.exp: _to_expression(v, src) for k, v in conditions.items()}
    default_exp = _to_expression(default, src)
    case_exp = Case(conditions_exp, default_exp)

    return c, case_exp


@overload
def toChain[S: Source](t: tuple[bool, Exp[S]]) -> Bool[S]: ...
@overload
def toChain[S: Source](t: tuple[int | float, Exp[S]]) -> Number[S]: ...
@overload
def toChain[S: Source](t: tuple[str, Exp[S]]) -> String[S]: ...
@overload
def toChain[S: Source](t: tuple[datetime.datetime, Exp[S]]) -> DateTime[S]: ...
@overload
def toChain[S: Source](t: tuple[None, Exp[S]]) -> Null[S]: ...
@overload
def toChain[T: Sourceble, S: Source](t: tuple[T, Exp[S]]) -> T: ...
def toChain[S: Source](
    t: tuple[Sourceble | int | float | str | bool | datetime.datetime | None, Exp[S]],
):
    """Принимает tuple из case и сохраняет специфичность типов toChain"""
    c, exp = t
    if isinstance(c, str):
        return String(exp)
    elif isinstance(c, bool):
        return Bool(exp)
    elif isinstance(c, int | float):
        return Number(exp)
    elif isinstance(c, datetime.datetime):
        return DateTime(exp)
    elif c is None:
        return Null(exp)
    else:
        return c


def aggSum[S: Source](metrica, way):
    return metrica._sum(way)


def aggAvg[S: Source](metrica, way):
    return metrica._avg(way)


def aggCount[S: Source](metrica, way):
    return metrica._count(way)


def aggUniq[S: Source](metrica, way):
    return metrica._uniq(way)
