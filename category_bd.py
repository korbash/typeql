from typing import final, override

from core.core import (
    Bool,
    DateTime,
    String,
    Null,
    Number,
    oneOf,
    case,
    toChain,
)
from core.expressions import Expression as Exp, Relation as R, Source


@final
class Currency[T: Source](String[T]):
    """currency code one of RUB, EUR, USD"""

    class CurrencySrc(Source): ...

    @property
    @override
    def id(self):
        return String(R(self.exp, "toString"))


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
        """user's age in years"""
        return Number(R(self.exp, "age"))

    @property
    def email(self):
        exp = R(self.exp, "email")
        return oneOf(String(exp), Null(exp))


@final
class Pets[T: Source](String[T]):
    """goods of type pet"""

    class PetsSrc(Source): ...

    @property
    @override
    def id(self):
        return String(R(self.exp, "toString"))

    @property
    def type(self):
        """type of good always 'pet'"""
        return String(R(self.exp, "type"))

    @property
    def name(self):
        return String(R(self.exp, "name"))

    @property
    def age(self):
        """age of pet"""
        return Number(R(self.exp, "age"))

    @property
    def flyable(self):
        """is pet can fly"""
        return Bool(R(self.exp, "flyable"))

    @property
    def rideable(self):
        """is pet can ride"""
        return Bool(R(self.exp, "rideable"))

    @property
    def bornFrom(self):
        """egg pet born erom"""
        return Eggs(R(self.exp, "bornFrom"))


@final
class Eggs[T: Source](String[T]):
    """goods of type egg"""

    class EggsSrc(Source): ...

    @property
    @override
    def id(self):
        return String(R(self.exp, "toString"))

    @property
    def type(self):
        """type of good always 'egg'"""
        return String(R(self.exp, "type"))

    @property
    def name(self):
        return String(R(self.exp, "name"))


@final
class Deals[T: Source](String[T]):
    """deal uniq id"""

    class DealsSrc(Source): ...

    @property
    @override
    def id(self):
        return String(R(self.exp, "toString"))

    @property
    def buyer(self):
        return Users(R(self.exp, "buyer"))

    @property
    def seller(self):
        return Users(R(self.exp, "seller"))

    @property
    def good(self):
        exp = R(self.exp, "good")
        return oneOf(Pets(exp), Eggs(exp))

    @property
    def dealDate(self):
        return DateTime(R(self.exp, "dealDate"))

    @property
    def buyerPrice(self):
        return Number(R(self.exp, "buyerPrice"))

    @property
    def sellerPrice(self):
        return Number(R(self.exp, "sellerPrice"))

    @property
    def sellerCurrency(self):
        return Currency(R(self.exp, "sellerCurrency"))

    @property
    def buyerCurrency(self):
        return Currency(R(self.exp, "buyerCurrency"))

    @property
    def success(self):
        return Bool(R(self.exp, "success"))


class BD:
    @property
    def deals(self):
        return Deals(Exp(Deals.DealsSrc()))

    @property
    def users(self):
        return Users(Exp(Users.UsersSrc()))

    @property
    def pets(self):
        return Pets(Exp(Pets.PetsSrc()))

    @property
    def eggs(self):
        return Eggs(Exp(Eggs.EggsSrc()))


bd = BD()
d = bd.deals
seller_age = d.seller.age
buyer_age = d.buyer.age
cond = d.buyerCurrency.eq("rub")
c1 = case({d.success & d.buyerCurrency.eq("rub"): d})
success_deals = toChain(case({d.success & d.buyerCurrency.eq("rub"): d}))
spend = success_deals.buyerPrice
income = success_deals.buyerPrice - success_deals.sellerPrice
buyers = success_deals.buyer
sellers = success_deals.seller
print(income)
