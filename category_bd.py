from typing import final, override

from core.core import Chain, DateTime, Parametr, String


@final
class RegInfo(Chain):
    """user uniq id"""

    @property
    @override
    def id(self):
        return String.from_parent(self, Parametr("reg_info.user_id"))

    @property
    def regDate(self):
        return DateTime.from_parent(self, Parametr("reg_info.reg_date"))


@final
class Goods(Chain):
    """good uniq id"""

    @property
    @override
    def id(self):
        return String.from_parent(self, Parametr("goods.good_id"))

    @property
    def productId(self):
        return ProductId.from_parent(self, Parametr("goods.product_id"))


@final
class ProductId(Chain):
    """another good uniq id"""

    base_type: bool = False

    @property
    @override
    def id(self):
        return String.from_parent(self, Parametr("goods.product_id"))

    @property
    def goodId(self):
        return Goods.from_parent(self, Parametr("goods.goods_id"))


@final
class Deals(Chain):
    """deal uniq id"""

    @property
    @override
    def id(self):
        return String.from_parent(self, Parametr("deals.deal_id"))

    @property
    def buyerId(self):
        return RegInfo.from_parent(self, Parametr("deals.buyer_id"))

    @property
    def sellerId(self):
        return RegInfo.from_parent(self, Parametr("deals.seller_id"))

    @property
    def goodId(self):
        return Goods.from_parent(self, Parametr("deals.good_id"))

    @property
    def dealDate(self):
        return DateTime.from_parent(self, Parametr("deals.deal_date"))


class BD:
    @property
    def deals(self):
        return Deals.from_source("deals")

    @property
    def reg_info(self):
        return RegInfo.from_source("reg_info")

    @property
    def goods(self):
        return Goods.from_source("goods")

    @property
    def productId(self):
        return Goods.from_source("goods.product_id")


bd = BD()
buyer_reg_date = bd.deals.buyerId.regDate
seller_reg_date = bd.deals.sellerId.regDate
product_chain = bd.deals.goodId.productId.goodId.productId

# Test examples to show the new Chain pattern
print("\n=== Chain pattern examples ===")
print("Deal ID:", bd.deals)
print("Buyer registration date:", buyer_reg_date)
print("Seller registration date:", seller_reg_date)
print("Product chain:", product_chain)
