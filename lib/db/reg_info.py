from typing import final
from .. import hub
from ..core import Connect

class RegInfo:
    def connect_to[T:"RegInfo"](self, other: T):
        return Connect(self, other)

@final
class RegInfo__UserId(hub.UserId, RegInfo):
    """Ссылка на пользователя"""

    real_name = "user_id"
    hub = False

@final
class RegInfo__RegDate(hub.Hub, RegInfo):
    """Дата регистрации"""

    real_name = "reg_date"
    hub = True

user_id = RegInfo__UserId()
reg_date = RegInfo__RegDate()
# u: Column = user_id
