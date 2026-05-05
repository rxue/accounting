from datetime import date
from enum import Enum, auto
from typing import Literal, NamedTuple

from investment.holdings.market_quote.yfinance_fetcher import Quote

Type = Literal["GAIN", "LOSS"]


class Action(Enum):
    BUY = auto()
    SELL = auto()

class ValuationResult(NamedTuple):
    type: Type
    value:float

class NordeaTradingLot(NamedTuple):
    company_symbol:str
    action:str
    date:date
    amount:int
    trade_price:float
    charge:float

class Holding(NamedTuple):
    company_name:str
    amount:int
    def __format__(self, spec) -> str:
        return f"{self.company_name:<50}{self.amount:<10}"

class HoldingSnapshot(NamedTuple):
    holding: Holding
    quote: Quote
    def __format__(self, spec) -> str:
        return f"{self.holding}{self.quote}"
