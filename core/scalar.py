from typing import Any, Union
from abc import ABC, abstractmethod


class ScalarFunction(ABC):
    """Base class for all scalar SQL functions (non-aggregation)"""

    @abstractmethod
    def __repr__(self) -> str:
        pass


class Case(ScalarFunction):
    """SQL CASE expression"""

    def __init__(self, *conditions_and_values, else_value=None):
        """
        CASE WHEN condition1 THEN value1
             WHEN condition2 THEN value2
             ELSE else_value END
        """
        if len(conditions_and_values) % 2 != 0:
            raise ValueError("conditions_and_values must have even number of elements (condition, value pairs)")

        self.when_pairs = []
        for i in range(0, len(conditions_and_values), 2):
            condition = conditions_and_values[i]
            value = conditions_and_values[i + 1]
            self.when_pairs.append((condition, value))

        self.else_value = else_value

    def __repr__(self) -> str:
        parts = []
        for condition, value in self.when_pairs:
            parts.append(f"WHEN {condition} THEN {value}")

        result = "CASE " + " ".join(parts)
        if self.else_value is not None:
            result += f" ELSE {self.else_value}"
        result += " END"
        return result


class If(ScalarFunction):
    """SQL IF function"""

    def __init__(self, condition: Any, true_value: Any, false_value: Any):
        self.condition = condition
        self.true_value = true_value
        self.false_value = false_value

    def __repr__(self) -> str:
        return f"IF({self.condition}, {self.true_value}, {self.false_value})"


class Coalesce(ScalarFunction):
    """SQL COALESCE function - returns first non-null value"""

    def __init__(self, *values):
        if len(values) < 2:
            raise ValueError("COALESCE requires at least 2 values")
        self.values = values

    def __repr__(self) -> str:
        values_str = ", ".join(str(v) for v in self.values)
        return f"COALESCE({values_str})"


class Nullif(ScalarFunction):
    """SQL NULLIF function"""

    def __init__(self, value1: Any, value2: Any):
        self.value1 = value1
        self.value2 = value2

    def __repr__(self) -> str:
        return f"NULLIF({self.value1}, {self.value2})"


class Concat(ScalarFunction):
    """SQL CONCAT function"""

    def __init__(self, *values):
        if len(values) < 2:
            raise ValueError("CONCAT requires at least 2 values")
        self.values = values

    def __repr__(self) -> str:
        values_str = ", ".join(str(v) for v in self.values)
        return f"CONCAT({values_str})"


class Substring(ScalarFunction):
    """SQL SUBSTRING function"""

    def __init__(self, string: Any, start: int, length: int = None):
        self.string = string
        self.start = start
        self.length = length

    def __repr__(self) -> str:
        if self.length is not None:
            return f"SUBSTRING({self.string}, {self.start}, {self.length})"
        else:
            return f"SUBSTRING({self.string}, {self.start})"


class Upper(ScalarFunction):
    """SQL UPPER function"""

    def __init__(self, value: Any):
        self.value = value

    def __repr__(self) -> str:
        return f"UPPER({self.value})"


class Lower(ScalarFunction):
    """SQL LOWER function"""

    def __init__(self, value: Any):
        self.value = value

    def __repr__(self) -> str:
        return f"LOWER({self.value})"


class Length(ScalarFunction):
    """SQL LENGTH function"""

    def __init__(self, value: Any):
        self.value = value

    def __repr__(self) -> str:
        return f"LENGTH({self.value})"


class Trim(ScalarFunction):
    """SQL TRIM function"""

    def __init__(self, value: Any, chars: str = None):
        self.value = value
        self.chars = chars

    def __repr__(self) -> str:
        if self.chars:
            return f"TRIM({self.chars} FROM {self.value})"
        else:
            return f"TRIM({self.value})"


class Replace(ScalarFunction):
    """SQL REPLACE function"""

    def __init__(self, string: Any, old_substring: Any, new_substring: Any):
        self.string = string
        self.old_substring = old_substring
        self.new_substring = new_substring

    def __repr__(self) -> str:
        return f"REPLACE({self.string}, {self.old_substring}, {self.new_substring})"


class Round(ScalarFunction):
    """SQL ROUND function"""

    def __init__(self, value: Any, precision: int = 0):
        self.value = value
        self.precision = precision

    def __repr__(self) -> str:
        return f"ROUND({self.value}, {self.precision})"


class Abs(ScalarFunction):
    """SQL ABS function"""

    def __init__(self, value: Any):
        self.value = value

    def __repr__(self) -> str:
        return f"ABS({self.value})"


class DateFormat(ScalarFunction):
    """SQL DATE_FORMAT function"""

    def __init__(self, date: Any, format_string: str):
        self.date = date
        self.format_string = format_string

    def __repr__(self) -> str:
        return f"DATE_FORMAT({self.date}, '{self.format_string}')"


class DateDiff(ScalarFunction):
    """SQL DATEDIFF function"""

    def __init__(self, date1: Any, date2: Any):
        self.date1 = date1
        self.date2 = date2

    def __repr__(self) -> str:
        return f"DATEDIFF({self.date1}, {self.date2})"


class Cast(ScalarFunction):
    """SQL CAST function"""

    def __init__(self, value: Any, data_type: str):
        self.value = value
        self.data_type = data_type

    def __repr__(self) -> str:
        return f"CAST({self.value} AS {self.data_type})"


# Convenience functions for easy usage
def case(*conditions_and_values, else_value=None) -> Case:
    return Case(*conditions_and_values, else_value=else_value)


def if_(condition: Any, true_value: Any, false_value: Any) -> If:
    return If(condition, true_value, false_value)


def coalesce(*values) -> Coalesce:
    return Coalesce(*values)


def nullif(value1: Any, value2: Any) -> Nullif:
    return Nullif(value1, value2)


def concat(*values) -> Concat:
    return Concat(*values)


def substring(string: Any, start: int, length: int = None) -> Substring:
    return Substring(string, start, length)


def upper(value: Any) -> Upper:
    return Upper(value)


def lower(value: Any) -> Lower:
    return Lower(value)


def length(value: Any) -> Length:
    return Length(value)


def trim(value: Any, chars: str = None) -> Trim:
    return Trim(value, chars)


def replace(string: Any, old_substring: Any, new_substring: Any) -> Replace:
    return Replace(string, old_substring, new_substring)


def round_(value: Any, precision: int = 0) -> Round:
    return Round(value, precision)


def abs_(value: Any) -> Abs:
    return Abs(value)


def date_format(date: Any, format_string: str) -> DateFormat:
    return DateFormat(date, format_string)


def date_diff(date1: Any, date2: Any) -> DateDiff:
    return DateDiff(date1, date2)


def cast(value: Any, data_type: str) -> Cast:
    return Cast(value, data_type)
