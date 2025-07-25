from typing import final, Literal, NamedTuple, override

type JoinKind = Literal["parametr", "metrica"]


class Join(NamedTuple):
    node: "Node"
    kind: JoinKind


class Node:
    def __init__(self, join: Join | None = None) -> None:
        """element of Node"""
        if join is None:
            self.source: "Node" = self
            self.kind: JoinKind = "parametr"
            self.joins: tuple[Join, ...] = ()
        else:
            parent = join.node
            self.source = parent.source
            if join.kind == "metrica":
                self.kind = "metrica"
            else:
                self.kind = parent.kind
            self.joins = parent.joins + (join,)

    @override
    def __repr__(self) -> str:
        """Beautiful representation of Node with full path"""

        path = ""
        for join in self.joins:
            arrow = " <> " if join.kind == "metrica" else " -> "
            path += join.node.__class__.__name__ + arrow
        path += self.__class__.__name__
        return f"{self.kind.capitalize()}({path})"


@final
class RegInfo__RegDate(Node):
    """user reg date"""

    @property
    def regInfo__userId__UP(self):
        return RegInfo__UserId(Join(self, "metrica"))


@final
class RegInfo__UserId(Node):
    """user uniq id"""

    @property
    def regInfo__regDate(self):
        return RegInfo__RegDate(Join(self, "parametr"))

    @property
    def deals__seller__UP(self):
        return Deals__Seller(Join(self, "metrica"))

    @property
    def deals__buyer__UP(self):
        return Deals__Buyer(Join(self, "metrica"))


@final
class Goods__GoodId(Node):
    """good uniq id"""

    @property
    def goods__productId(self):
        return Goods__ProductId(Join(self, "parametr"))

    @property
    def deals__goodId__UP(self):
        return Deals__GoodId(Join(self, "metrica"))


@final
class Goods__ProductId(Node):
    """another good uniq id"""

    @property
    def goods__goodId(self):
        return Goods__GoodId(Join(self, "parametr"))


@final
class Deals__Seller(Node):
    """link to seller id"""

    @property
    def regInfo__userId(self):
        return RegInfo__UserId(Join(self, "parametr"))

    @property
    def deals__id__UP(self):
        return Deals__Id(Join(self, "metrica"))


@final
class Deals__Buyer(Node):
    """link to buyer id"""

    @property
    def regInfo__userId(self):
        return RegInfo__UserId(Join(self, "parametr"))

    @property
    def deals__id__UP(self):
        return Deals__Id(Join(self, "metrica"))


@final
class Deals__Date(Node):
    """deal daetime"""

    @property
    def deals__id__UP(self):
        return Deals__Id(Join(self, "metrica"))


@final
class Deals__GoodId(Node):
    """link to good id"""

    @property
    def goods__goodId(self):
        return Goods__GoodId(Join(self, "parametr"))

    @property
    def deals__id__UP(self):
        return Deals__Id(Join(self, "metrica"))


@final
class Deals__Id(Node):
    """deal uniq id"""

    @property
    def deals__buyer(self):
        return Deals__Buyer(Join(self, "parametr"))

    @property
    def deals__seller(self):
        return Deals__Seller(Join(self, "parametr"))

    @property
    def deals__date(self):
        return Deals__Date(Join(self, "parametr"))

    @property
    def deals__goodId(self):
        return Deals__GoodId(Join(self, "parametr"))


deal = Deals__Id()
c: RegInfo__RegDate = deal.deals__buyer.regInfo__userId.regInfo__regDate
c2 = deal.deals__goodId.goods__goodId.goods__productId.goods__goodId.goods__productId.goods__goodId.goods__productId.goods__goodId.goods__productId

(c.regInfo__userId__UP.deals__seller__UP.deals__id__UP.deals__goodId)


# Test examples to show beautiful repr in action
print("\n=== Beautiful repr examples ===")
print("Simple node:", deal)
print("Short chain:", deal.deals__buyer)
print("Medium chain:", deal.deals__buyer.regInfo__userId)
print("Long chain:", c)
print("Very long chain:", c2)
print("\nMetrica example:", c.regInfo__userId__UP)
print("Complex path:", c.regInfo__userId__UP.deals__seller__UP.deals__id__UP)

print("\n=== Difference between repr and str ===")
print("repr(very long chain):", repr(c2))
print("str(very long chain): ", str(c2))
print(
    "\nrepr(complex path):   ",
    repr(c.regInfo__userId__UP.deals__seller__UP.deals__id__UP),
)
print(
    "str(complex path):    ", str(c.regInfo__userId__UP.deals__seller__UP.deals__id__UP)
)
