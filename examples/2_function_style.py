from test_uv import toChain, caseSQL, aggAvg, aggSum, aggCount, aggUniq
from test_uv import Source, Number, DateTime
from test_uv.generated_bd_schema import Currency, BD


def amount_in_usd[T: Source](curr: Currency[T], price: Number[T], time: DateTime[T]):
    bd = BD()
    rate = bd.exchangeRate
    eur_rate = aggAvg(rate.eurRate, rate.time.day())
    rub_rate = aggAvg(rate.rubRate, rate.time.day())
    return toChain(
        caseSQL(
            {
                curr.eq("rub"): price * (time >> rub_rate),
                curr.eq("eur"): price * (time >> eur_rate),
            },
            price,
        )
    )


bd = BD()
buerPriceUSD = amount_in_usd(
    bd.deals.buyerCurrency, bd.deals.buyerPrice, bd.deals.dealDate
)
sellerPriceUSD = amount_in_usd(
    bd.deals.sellerCurrency, bd.deals.sellerPrice, bd.deals.dealDate
)
income = toChain(caseSQL({bd.deals.success: buerPriceUSD - sellerPriceUSD}, 0))
daily_income = income._sum(bd.deals.dealDate.day())
income_from_user = (income._sum(bd.deals.buyer) + income._sum(bd.deals.seller)) / 2
print(income_from_user.exp)
