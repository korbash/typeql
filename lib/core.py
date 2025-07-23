from typing import final, Protocol, Self, overload

@final
class Join[T, U]:
    def __init__(self, left: T, right: U):
        self.left = left
        self.right = right

@final
class Connect[T, U]:
    def __init__(self, left: T, right: U):
        self.left = left
        self.right = right

@final
class Path[T, U]:
    def __init__[*TS](self, p : tuple[T, *TS, U]) -> None:
        self.p = p

    @overload
    def __truediv__[V, B](self, other: "Path[V, B]") -> "Path[T, B]":
        ...

    @overload
    def __truediv__[V](self, other: V) -> "Path[T, V]":
        ...

    def __truediv__(self, other):
        if isinstance(other, Path):
            return Path((self.p[0], self.p[1:]) + other.p)
        else:
            return Path(self.p + (other,))






# class Column(Protocol):
#     def connect_to[T:"Column"](self, other: T) -> Connect[Self, T]:
#         ...
#     def join_to[T:"Column"](self, other: T) -> Join["Column", T]:
#         ...
