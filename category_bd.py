from typing import final, override

from core.core import (
    Bool,
    DateTime,
    DateHour,
    DateDay,
    DateWeek,
    DateMonth,
    DateYear,
    DateSecond,
    DateMinute,
    String,
    Null,
    Number,
    Chain,
    aggAvg,
    aggUniq,
    oneOf,
    case,
    toChain,
    aggSum,
)
from core.expressions import Expression as Exp, Relation as R, Source, Stack


@final
class ExchangeRate[T: Source](String[T]):
    """category of goods"""

    class ExchangeRateSrc(String.StringSrc): ...

    @property
    @override
    def id(self):
        return String(R(self.exp, "toString"))

    @classmethod
    @override
    def get_self_type(cls):
        return cls.ExchangeRate()

    @property
    def time(self):
        return DateTime(R(self.exp, "time"))

    @property
    def eurRate(self):
        return Number(R(self.exp, "eurRate"))

    @property
    def rubRate(self):
        return Number(R(self.exp, "rubRate"))

    @override
    def __rrshift__[S: Source](self, other: "Chain[S]"):
        """Right shift comparison operator"""
        exp = Stack(other.get_expression(), self.get_expression())
        return ExchangeRate(exp)


@final
class Currency[T: Source](String[T]):
    """currency code one of RUB, EUR, USD"""

    class CurrencySrc(String.StringSrc): ...

    @property
    @override
    def id(self):
        return String(R(self.exp, "toString"))

    @classmethod
    @override
    def get_self_type(cls):
        return cls.CurrencySrc()

    @override
    def __rrshift__[S: Source](self, other: "Chain[S]"):
        """Right shift comparison operator"""
        exp = Stack(other.get_expression(), self.get_expression())
        return Currency(exp)


@final
class Users[T: Source](String[T]):
    """user uniq id"""

    class UsersSrc(String.StringSrc): ...

    @property
    @override
    def id(self):
        return String(R(self.exp, "toString"))

    @classmethod
    @override
    def get_self_type(cls):
        return cls.UsersSrc()

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

    @override
    def __rrshift__[S: Source](self, other: "Chain[S]"):
        """Right shift comparison operator"""
        exp = Stack(other.get_expression(), self.get_expression())
        return Users(exp)


@final
class Pets[T: Source](String[T]):
    """goods of type pet"""

    class PetsSrc(String.StringSrc): ...

    @property
    @override
    def id(self):
        return String(R(self.exp, "toString"))

    @classmethod
    @override
    def get_self_type(cls):
        return cls.PetsSrc()

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

    @override
    def __rrshift__[S: Source](self, other: "Chain[S]"):
        """Right shift comparison operator"""
        exp = Stack(other.get_expression(), self.get_expression())
        return Pets(exp)


@final
class Eggs[T: Source](String[T]):
    """goods of type egg"""

    class EggsSrc(Source): ...

    @property
    @override
    def id(self):
        return String(R(self.exp, "toString"))

    @classmethod
    @override
    def get_self_type(cls):
        return cls.EggsSrc()

    @property
    def type(self):
        """type of good always 'egg'"""
        return String(R(self.exp, "type"))

    @property
    def name(self):
        return String(R(self.exp, "name"))

    @override
    def __rrshift__[S: Source](self, other: "Chain[S]"):
        """Right shift comparison operator"""
        exp = Stack(other.get_expression(), self.get_expression())
        return Eggs(exp)


@final
class Deals[T: Source](String[T]):
    """deal uniq id"""

    class DealsSrc(String.StringSrc): ...

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

    @classmethod
    @override
    def get_self_type(cls):
        return cls.DealsSrc()

    @override
    def __rrshift__[S: Source](self, other: "Chain[S]"):
        """Right shift comparison operator"""
        exp = Stack(other.get_expression(), self.get_expression())
        return Deals(exp)


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

    @property
    def exchangeRate(self):
        return ExchangeRate(Exp(ExchangeRate.ExchangeRateSrc()))


bd = BD()
rate = bd.exchangeRate
eur_rate = aggAvg(rate.eurRate, rate.time.day())
rub_rate = aggAvg(rate.rubRate, rate.time.day())

buerPriceUSD = toChain(
    case(
        {
            bd.deals.buyerCurrency.eq("rub"): bd.deals.buyerPrice
            * (bd.deals.dealDate >> rub_rate),
            bd.deals.buyerCurrency.eq("eur"): bd.deals.buyerPrice
            * (bd.deals.dealDate >> eur_rate),
        },
        bd.deals.buyerPrice,
    )
)
sellerPriceUSD = toChain(
    case(
        {
            bd.deals.sellerCurrency.eq("rub"): bd.deals.sellerPrice
            * (bd.deals.dealDate >> rub_rate),
            bd.deals.sellerCurrency.eq("eur"): bd.deals.sellerPrice
            * (bd.deals.dealDate >> eur_rate),
        },
        bd.deals.sellerPrice,
    )
)
income = toChain(case({bd.deals.success: buerPriceUSD - sellerPriceUSD}, 0))
daily_income = income._sum(bd.deals.dealDate.day())
income_from_user = (income._sum(bd.deals.buyer) + income._sum(bd.deals.seller)) / 2
