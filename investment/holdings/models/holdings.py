from dataclasses import dataclass
from enum import Enum, auto
from typing import NamedTuple
from datetime import date

from investment.holdings.market_quote.yfinance_fetcher import Quote

class Bank(Enum):
    NORDEA = auto()
    NORDNET = auto()
    OP = auto()

@dataclass(frozen=True, slots=True)
class Trading:
    company_identifier:str  # any string identifying the company, e.g. company name in Nordea trading lots, ticker symbol in OP
    action:str
    date:date
    amount:int
    trade_price:float


class Holding(NamedTuple):
    company_name:str
    amount:int

class HoldingSnapshot(NamedTuple):
    holding: Holding
    quote: Quote

class HoldingsSnapshot(NamedTuple):
    holding_snapshots:list[HoldingSnapshot]
