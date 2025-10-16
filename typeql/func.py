import datetime
from random import choice
from typing import overload
from collections.abc import Mapping
from .expressions import (
    Expression as Exp,
    Source,
    ConstantString,
    ConstantBoolean,
    ConstantNumber,
    ConstantDateTime,
    ConstantNull,
    Case,
)
from .core import Sourceble, Bool, Number, String, DateTime, Null


def oneOf[*T](*args: *tuple[*T]):
    return choice(args)


def caseSQL[
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


def aggSum(metrica, way):
    return metrica._sum(way)


def aggAvg[S: Source](metrica, way):
    return metrica._avg(way)


def aggCount[S: Source](metrica, way):
    return metrica._count(way)


def aggUniq[S: Source](metrica, way):
    return metrica._uniq(way)
