# models.py
from __future__ import annotations

# from dataclasses import dataclass
from typing import final, Self, Literal

from typing import Protocol


class Hub:
    def join_to(self, other: Self):
        return Join(self, other)


class Hub_UserId:
    def join_to(self, other: "Hub_UserId"):
        return Join(self, other)


@final
class Join[T, U]:
    def __init__(self, left: T, right: U):
        self.left = left
        self.right = right


# class Hubs:
#     class User__Id:
#         def join_to[T: Users__Id | Purchase__UserId | Topups__UserId](self, other: T):
#             return Join(self, other)


@final
class Users__Id(Hub_UserId):
    """User identifier"""

    real_name = "id"
    hub = True


@final
class Users__RegDate(Hub):
    """Дата регистрации"""

    real_name = "reg_date"
    hub = True


@final
class Users:
    Id = Users__Id()
    RegDate = Users__RegDate()


@final
class Purchase__UserId(Hub_UserId):
    """Ссылка на пользователя"""

    real_name = "user_id"
    hub = False


@final
class Purchase:
    UserId = Purchase__UserId()


@final
class Topups__UserId(Hub_UserId):
    """Ссылка на пользователя (пополнение)"""

    real_name = "user_id"
    hub = False


@final
class Topups:
    UserId = Topups__UserId()


def main():
    print("Hello from test-uv!")
    c1 = Topups.UserId
    c2 = Purchase.UserId
    c3 = Topups.UserId
    c4 = Users.RegDate
    u = Users.Id
    j = c2.join_to(c3)

    j = h1.join_to(h2)

    if c1 == c2:
        print("Equal")
    else:
        print("Not equal")


if __name__ == "__main__":
    main()
