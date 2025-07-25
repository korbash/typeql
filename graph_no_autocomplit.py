from typing import final


class Node:
    def __init__(self, path: tuple["Node", ...] = ()) -> None:
        """element of Node"""
        self.path: tuple["Node", ...] = path + (self,)


@final
class RegInfo__RegDate(Node):
    """user reg date"""

    @property
    def regInfo__userId__UP(self):
        return RegInfo__UserId(self.path)


@final
class RegInfo__UserId(Node):
    """user uniq id"""

    @property
    def regInfo__regDate(self):
        return RegInfo__RegDate(self.path)

    @property
    def deals__seller__UP(self):
        return Deals__Seller(self.path)

    @property
    def deals__buyer__UP(self):
        return Deals__Buyer(self.path)


@final
class Goods__GoodId(Node):
    """good uniq id"""

    @property
    def goods__productId(self):
        return Goods__ProductId(self.path)

    @property
    def deals__goodId__UP(self):
        return Deals__GoodId(self.path)


@final
class Goods__ProductId(Node):
    """another good uniq id"""

    @property
    def goods__goodId(self):
        return Goods__GoodId(self.path)


@final
class Deals__Seller(Node):
    """link to seller id"""

    @property
    def regInfo__userId(self):
        return RegInfo__UserId(self.path)

    @property
    def deals__id__UP(self):
        return Deals__Id(self.path)


@final
class Deals__Buyer(Node):
    """link to buyer id"""

    @property
    def regInfo__userId(self):
        return RegInfo__UserId(self.path)

    @property
    def deals__id__UP(self):
        return Deals__Id(self.path)


@final
class Deals__Date(Node):
    """deal daetime"""

    @property
    def deals__id__UP(self):
        return Deals__Id(self.path)


@final
class Deals__GoodId(Node):
    """link to good id"""

    @property
    def goods__goodId(self):
        return Goods__GoodId(self.path)

    @property
    def deals__id__UP(self):
        return Deals__Id(self.path)


@final
class Deals__Id(Node):
    """deal uniq id"""

    @property
    def deals__buyer(self):
        return Deals__Buyer(self.path)

    @property
    def deals__seller(self):
        return Deals__Seller(self.path)

    @property
    def deals__date(self):
        return Deals__Date(self.path)

    @property
    def deals__goodId(self):
        return Deals__GoodId(self.path)


deal = Deals__Id()
c: RegInfo__RegDate = deal.deals__buyer.regInfo__userId.regInfo__regDate
deal.deals__goodId.goods__goodId.goods__productId.goods__goodId.goods__productId

c.regInfo__userId__UP.deals__seller__UP.deals__id__UP.deals__goodId
