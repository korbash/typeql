from typing import final, override

from core.core import DateTime, String
from core.expressions import Expression as Exp, Relation as R, Source
from sources import Sources as S


@final
class Users[T: Source](String[T]):
    """user uniq id"""

    @property
    @override
    def id(self):
        return String(R(self.exp, "toString"))

    @property
    def regDate(self):
        return DateTime(R(self.exp, "toDateTime"))


@final
class Goods[T: Source](String[T]):
    """good uniq id"""

    @property
    @override
    def id(self):
        return String(R(self.exp, "toString"))

    @property
    def productId(self):
        return ProductId(R(self.exp, "productId"))


@final
class ProductId[T: Source](String[T]):
    """another good uniq id"""

    base_type: bool = False

    @property
    @override
    def id(self):
        return String(R(self.exp, "toString"))

    @property
    def goodId(self):
        exp = R(self.exp, "goodId")
        return Goods(exp)


@final
class Deals[T: Source](String[T]):
    """deal uniq id"""

    @property
    @override
    def id(self):
        return String(R(self.exp, "toString"))

    @property
    def buyerId(self):
        return Users(R(self.exp, "buyerId"))

    @property
    def sellerId(self):
        return Users(R(self.exp, "sellerId"))

    @property
    def goodId(self):
        return Goods(R(self.exp, "goodId"))

    @property
    def dealDate(self):
        return DateTime(R(self.exp, "dealDate"))


class BD:
    @property
    def deals(self):
        return Deals(Exp(S.Deals()))

    @property
    def users(self):
        return Users(Exp(S.Users()))

    @property
    def goods(self):
        return Goods(Exp(S.Goods()))

    @property
    def products(self):
        return Goods(Exp(S.Products()))


bd = BD()
buyer_reg_date = bd.deals.buyerId.regDate
seller_reg_date = bd.deals.sellerId.regDate
product_chain = bd.deals.goodId.productId.goodId.productId
user_reg_date = bd.users.regDate
print(type(buyer_reg_date.exp.source) is type(product_chain.exp.source))
print(buyer_reg_date.exp.source == product_chain.exp.source)
print(type(buyer_reg_date.exp.source))
print(type(product_chain.exp.source))
# Test examples to show the new Chain pattern
print("\n=== Chain pattern examples ===")
print("Deal ID:", bd.deals)
print("Buyer registration date:", buyer_reg_date)
print("Seller registration date:", seller_reg_date)
print("Product chain:", product_chain)
for i in range(10):
    a = i * 0.2
