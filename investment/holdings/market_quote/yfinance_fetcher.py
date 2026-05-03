from datetime import datetime
from typing import NamedTuple
from zoneinfo import ZoneInfo

import yfinance as yf

class Quote(NamedTuple):
    price:float
    currency:str
    dividend_yield:float
    daily_change:float
    timestamp:datetime
    pe:int
    roe:float
    def daily_change_rate(self)->float:
        return self.daily_change / (self.price-self.daily_change)
    def timestamp_repr(self) -> str:
        return self.timestamp.strftime("%Y-%m-%d %H:%M %Z")

def get_latest_quote(symbol: str) -> Quote | None:
    info = yf.Ticker(symbol).info
    price = info.get("currentPrice")
    currency = info.get("currency")
    dividend_yield = info.get("dividendYield")
    daily_change = info.get("regularMarketChange")
    market_time = info.get("regularMarketTime")
    time_zone = info.get("exchangeTimezoneName")
    pe = info.get("trailingPE")
    roe = info.get("returnOnEquity")
    if price is None or currency is None or daily_change is None or market_time is None or time_zone is None:
        return None
    return Quote(price=price,
                 currency=currency,
                 dividend_yield=dividend_yield,
                 daily_change=daily_change,
                 timestamp=datetime.fromtimestamp(market_time, tz=ZoneInfo(time_zone)),
                 pe=int(round(pe)) if pe is not None else None,
                 roe=roe)




def get_latest_quotes(*symbols: str) -> list[Quote]:
    return [quote for symbol in symbols if (quote := get_latest_quote(symbol)) is not None]
