# from dataclasses import dataclass


# @dataclass
# class Column:
#     real_name: str

# @dataclass
# class Table:
#     columns: set[Column]

# @dataclass
# class JoinHub:
#     columns: set[Column]

# RegInfo__UserId = Column("user_id")
# RegInfo__RegDate = Column("reg_date")

# RegInfo = Table(
#     set([RegInfo__UserId, RegInfo__RegDate])
# )

# Purchases__UserId = Column("user_id")

# Purchases = Table(
#     set([Purchases__UserId])
# )

from lib.db import purchases, reg_info

p = {
    "user_id": purchases.user_id,
}
r = {
    "user_id": reg_info.user_id,
    "reg_date": reg_info.reg_date
}

db = {
    "purchases": p,
    "reg_info": r
}

k = db["purchases"]["user_id"]
