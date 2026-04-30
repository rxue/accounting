from typing import NamedTuple

from investment.company.models import Company
from investment.holdings.models import HoldingSnapshot
from investment.holdings.nordea_holdings_extractor import extract_from_excel
from investment.company.repository import find_yahoo_symbols_by_name
from investment.holdings.market_quote.yfinance_fetcher import get_latest_quote


class HoldingsSnapshot(NamedTuple):
    bank: str
    holdings: list[HoldingSnapshot]

    @staticmethod
    def generate(holdings_excel_path: str) -> tuple["HoldingsSnapshot", list[str]]:
        holdings = extract_from_excel(holdings_excel_path)
        names = [h.company_name for h in holdings]
        yahoo_symbols = find_yahoo_symbols_by_name(*names)
        snapshots = []
        failed = []
        for holding in holdings:
            yahoo_symbol = yahoo_symbols.get(holding.company_name)
            if yahoo_symbol is None:
                failed.append(holding.company_name)
                continue
            quote = get_latest_quote(yahoo_symbol)
            if quote is None:
                failed.append(holding.company_name)
                continue
            company = Company(name=holding.company_name)
            snapshots.append(HoldingSnapshot(
                holding=holding,
                quote=quote,
            ))
        snapshots.sort(key=lambda s: s.quote.daily_change_rate(), reverse=True)
        return HoldingsSnapshot(bank="Nordea", holdings=snapshots), failed
