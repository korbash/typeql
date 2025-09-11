from typing import final, override, Literal

from core.core import Chain, DateTime, Parametr, String


@final
class RegInfo[T: str](Chain[T]):
    """user uniq id"""

    @property
    @override
    def id(self):
        return String[T].from_parent(self, Parametr("reg_info.user_id"))

    @property
    def regDate(self):
        return DateTime[T].from_parent(self, Parametr("reg_info.reg_date"))


@final
class Goods[T: str](Chain[T]):
    """good uniq id"""

    @property
    @override
    def id(self):
        return String[T].from_parent(self, Parametr("goods.good_id"))

    @property
    def productId(self):
        return ProductId[T].from_parent(self, Parametr("goods.product_id"))


@final
class ProductId[T: str](Chain[T]):
    """another good uniq id"""

    base_type: bool = False

    @property
    @override
    def id(self):
        return String[T].from_parent(self, Parametr("goods.product_id"))

    @property
    def goodId(self):
        return Goods[T].from_parent(self, Parametr("goods.goods_id"))


@final
class Deals[T: str](Chain[T]):
    """deal uniq id"""

    @property
    @override
    def id(self):
        return String[T].from_parent(self, Parametr("deals.deal_id"))

    @property
    def buyerId(self):
        return RegInfo[T].from_parent(self, Parametr("deals.buyer_id"))

    @property
    def sellerId(self):
        return RegInfo[T].from_parent(self, Parametr("deals.seller_id"))

    @property
    def goodId(self):
        return Goods[T].from_parent(self, Parametr("deals.good_id"))

    @property
    def dealDate(self):
        return DateTime[T].from_parent(self, Parametr("deals.deal_date"))


class BD:
    @property
    def deals(self):
        return Deals[Literal["deals"]]("deals")

    @property
    def reg_info(self):
        return RegInfo[Literal["reg_info"]]("reg_info")

    @property
    def goods(self):
        return Goods[Literal["goods"]]("goods")

    @property
    def productId(self):
        return Goods[Literal["goods.product_id"]]("goods.product_id")


bd = BD()
buyer_reg_date = bd.deals.buyerId.regDate
seller_reg_date = bd.deals.sellerId.regDate
product_chain = bd.deals.goodId.productId.goodId.productId
user_reg_date = bd.reg_info.regDate

# Test examples to show the new Chain pattern
print("\n=== Chain pattern examples ===")
print("Deal ID:", bd.deals)
print("Buyer registration date:", buyer_reg_date)
print("Seller registration date:", seller_reg_date)
print("Product chain:", product_chain)
for i in range(10):
    a = i * 0.2
