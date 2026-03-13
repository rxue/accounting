from typing import NamedTuple
from zoneinfo import ZoneInfo


class Company(NamedTuple):
    short_name: str
    yahoo_symbol: str
    time_zone: ZoneInfo
    currency: str

class Price(NamedTuple):
    price: float
    fx_rate: float | None = None
    def price_in_eur(self)->float:
        return self.price/self.fx_rate