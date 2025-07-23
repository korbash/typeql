from csv import QUOTE_NOTNULL
from lib.db import purchases, reg_info
from lib.core import Path

# c1 = purchases.user_id
c1 = purchases.user_id
c2 = reg_info.user_id
c3 = reg_info.reg_date
j1 = c1.join_to(c2)
con1 = c2.connect_to(other=c3)

p = Path((1, "r" , 2, "q"))
p2 = Path(("r" , 2, "q"))
p3 = p / p2
q = isinstance(p, Path)
