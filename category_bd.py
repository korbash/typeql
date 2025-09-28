from typing import final, override

from core.core import DateTime, String, Null, Number
from core.expressions import Expression as Exp, Relation as R, Source


@final
class Users[T: Source](String[T]):
    """user uniq id"""

    class UsersSrc(Source): ...

    @property
    @override
    def id(self):
        return String(R(self.exp, "toString"))

    @property
    def regDate(self):
        return DateTime(R(self.exp, "toDateTime"))

    @property
    def age(self):
        return Number(R(self.exp, "age"))


@final
class Goods[T: Source](String[T]):
    """good uniq id"""

    class GoodsSrc(Source): ...

    @property
    @override
    def id(self):
        return String(R(self.exp, "toString"))

    @property
    def productId(self):
        return Products(R(self.exp, "productId"))


@final
class Products[T: Source](String[T]):
    """another good uniq id"""

    class ProductsSrc(Source): ...

    @property
    @override
    def id(self):
        return String(R(self.exp, "toString"))

    @property
    def goodId(self):
        exp = R(self.exp, "goodId")
        return Goods(exp) | Users(exp)


@final
class Deals[T: Source](String[T]):
    """deal uniq id"""

    class DealsSrc(Source): ...

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
        return Deals(Exp(Deals.DealsSrc()))

    @property
    def users(self):
        return Users(Exp(Users.UsersSrc()))

    @property
    def goods(self):
        return Goods(Exp(Goods.GoodsSrc()))

    @property
    def products(self):
        return Goods(Exp(Products.ProductsSrc()))


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

a = bd.goods.productId.goodId.productId
a = product_chain.id
b = bd.deals
print(b.id.exp.source)
print(bd.deals.sellerId.exp.source)
print(type(bd.deals.sellerId.exp.source) is type(b.id.exp.source))
d = b.id + bd.deals.sellerId
a = 11 + bd.users.age / 0 * 4 > 6
b = bd.deals.buyerId.id + "qqq"
print(b)
print(a)
