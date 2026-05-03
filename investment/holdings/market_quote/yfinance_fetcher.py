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
    def daily_change_rate(self) -> float:
        return self.daily_change / (self.price - self.daily_change)
    def daily_change_percentage(self) -> str:
        return f"{self.daily_change_rate() * 100:.2f}%"
    def timestamp_repr(self) -> str:
        return self.timestamp.strftime("%Y-%m-%d %H:%M %Z")
    def dividend_yield_percentage(self) -> str:
        if self.dividend_yield is None:
            return "N/A"
        return f"{self.dividend_yield:.2f}%"
    def __format__(self,spec):
        return f"{self.price:<10}{self.currency:<5s}{self.daily_change_percentage():<10s}{self.dividend_yield_percentage():<10s}{self.timestamp_repr()}"

def get_latest_quote(symbol: str) -> Quote | None:
    info = yf.Ticker(symbol).info
    price = info.get("currentPrice")
    currency = info.get("currency")
    dividend_yield = info.get("dividendYield")
    daily_change = info.get("regularMarketChange")
    market_time = info.get("regularMarketTime")
    time_zone = info.get("exchangeTimezoneName")
    if price is None or currency is None or daily_change is None or market_time is None or time_zone is None:
        return None
    return Quote(price=price,
                 currency=currency,
                 dividend_yield=dividend_yield,
                 daily_change=daily_change,
                 timestamp=datetime.fromtimestamp(market_time, tz=ZoneInfo(time_zone)))




def get_latest_quotes(*symbols: str) -> list[Quote]:
    return [quote for symbol in symbols if (quote := get_latest_quote(symbol)) is not None]
