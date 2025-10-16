from typeql import toChain, caseSQL, aggAvg, aggSum, aggCount, aggUniq
from typeql.generated_bd_schema import BD

bd = BD()
rate = bd.exchangeRate
eur_rate = aggAvg(rate.eurRate, rate.time.day())
rub_rate = aggAvg(rate.rubRate, rate.time.day())

buerPriceUSD = toChain(
    caseSQL(
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
    caseSQL(
        {
            bd.deals.sellerCurrency.eq("rub"): bd.deals.sellerPrice
            * (bd.deals.dealDate >> rub_rate),
            bd.deals.sellerCurrency.eq("eur"): bd.deals.sellerPrice
            * (bd.deals.dealDate >> eur_rate),
        },
        bd.deals.sellerPrice,
    )
)
income = toChain(caseSQL({bd.deals.success: buerPriceUSD - sellerPriceUSD}, 0))
daily_income = income._sum(bd.deals.dealDate.day())
income_from_user = (income._sum(bd.deals.buyer) + income._sum(bd.deals.seller)) / 2
print(income_from_user.exp)
