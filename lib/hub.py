from typing import Self

from .core import Join


class Hub:
    def join_to(self, other: Self):
        return Join(self, other)


class UserId:
    def join_to[T: "UserId"](self, other: T):
        return Join(self, other)


__all__ = ["Hub", "UserId"]
