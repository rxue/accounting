from typing import NamedTuple

from investment.company.models import Company
from investment.holdings.market_quote.google_finance_fetcher import Price

class HoldingSnapshot(NamedTuple):
    company: Company
    amount: int
    price: Price
    def __format__(self, spec) -> str:
        return f"{self.company}{self.amount:<10}{self.price}"