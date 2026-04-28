from typing import NamedTuple

from investment.company.models import Company
from investment.holdings.market_quote.google_finance_fetcher import Price

class Holding(NamedTuple):
    isin: str
    amount: int

class HoldingSnapshot(NamedTuple):
    company: Company
    amount: int
    price: Price