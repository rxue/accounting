from typing import NamedTuple

from investment.company.models import Company
from investment.holdings.market_quote.yfinance_fetcher import Quote

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
