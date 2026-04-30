from typing import NamedTuple

from investment.company.models import Company
from investment.holdings.market_quote.yfinance_fetcher import Quote


class HoldingSnapshot(NamedTuple):
    company: Company
    amount:int
    quote: Quote

    def __format__(self, spec) -> str:
        return f"{self.company}{self.amount:<10}{self.quote}"
