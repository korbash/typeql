from typing import final
from .. import hub
from ..core import Connect

class Purchases:
    def connect_to[T:"Purchases"](self, other: T):
        return Connect(self, other)

@final
class Purchases__UserId(hub.UserId, Purchases):
    """Ссылка на пользователя"""

    real_name = "user_id"
    hub = False

user_id = Purchases__UserId()
