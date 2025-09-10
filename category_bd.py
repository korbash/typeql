from typing import final, Literal, NamedTuple, override, Callable, Self
from dataclasses import dataclass
from abc import ABC, abstractmethod


@dataclass
class Parametr:
    column: str

    @override
    def __repr__(self) -> str:
        return self.column


@dataclass
class Exp:
    fun: str
    arg0: Self | Parametr
    arg1: Self | Parametr


class Chain(ABC):
    def __init__(
        self, parent: "Chain | None" = None, relation: Parametr | Exp | None = None
    ) -> None:
        """element of Chain"""
        if (relation is None and parent is not None) or (
            relation is not None and parent is None
        ):
            raise ValueError("parent and relation must be both None or both not None")
        if parent is None:
            self.source: str = "placeholder"
            my_id = self.id
            self.source = str(my_id.relation)
        else:
            self.source = parent.source

        self.relation: Parametr | Exp | None = relation
        self.parent: Chain | None = parent
        if str(self.relation or self.source).startswith("base_type."):
            self.base_type = True
        else:
            self.base_type = False

    @property
    @abstractmethod
    def id(self) -> "Chain":
        """Beautiful representation of Chain with full path"""

    @override
    def __repr__(self) -> str:
        """Beautiful representation of Chain with column names and arrows"""

        path_parts: list[str] = []
        current = self

        while current.parent is not None:
            path_parts.append(str(current.relation))
            current = current.parent

        # Reverse to get correct order and join with arrows
        path_parts.append(self.source)
        path_parts.reverse()
        return " -> ".join(path_parts)


@final
class DateTime(Chain):
    """Any Date"""

    @property
    @override
    def id(self):
        return DateTime(self, Parametr("base_type.date_time"))


@final
class Number(Chain):
    """Any Number"""

    @property
    @override
    def id(self):
        return Number(self, Parametr("base_type.number"))


@final
class String(Chain):
    """Any String"""

    @property
    @override
    def id(self):
        return String(self, Parametr("base_type.string"))


@final
class RegInfo(Chain):
    """user uniq id"""

    @property
    @override
    def id(self):
        return String(self, Parametr("reg_info.user_id"))

    @property
    def regDate(self):
        return DateTime(self, Parametr("reg_info.reg_date"))


@final
class Goods(Chain):
    """good uniq id"""

    @property
    @override
    def id(self):
        return String(self, Parametr("goods.good_id"))

    @property
    def productId(self):
        return ProductId(self, Parametr("goods.product_id"))


@final
class ProductId(Chain):
    """another good uniq id"""

    base_type: bool = False

    @property
    @override
    def id(self):
        return String(self, Parametr("goods.product_id"))

    @property
    def goodId(self):
        return Goods(self, Parametr("goods.goods_id"))


@final
class Deals(Chain):
    """deal uniq id"""

    @property
    @override
    def id(self):
        return String(self, Parametr("deals.deal_id"))

    @property
    def buyerId(self):
        return RegInfo(self, Parametr("deals.buyer_id"))

    @property
    def sellerId(self):
        return RegInfo(self, Parametr("deals.seller_id"))

    @property
    def goodId(self):
        return Goods(self, Parametr("deals.good_id"))

    @property
    def dealDate(self):
        return DateTime(self, Parametr("deals.deal_date"))


deal = Deals()
buyer_reg_date = deal.buyerId.regDate
seller_reg_date = deal.sellerId.regDate
product_chain = deal.goodId.productId.goodId.productId

# Test examples to show the new Chain pattern
print("\n=== Chain pattern examples ===")
print("Deal ID:", deal)
print("Buyer registration date:", buyer_reg_date)
print("Seller registration date:", seller_reg_date)
print("Product chain:", product_chain)
