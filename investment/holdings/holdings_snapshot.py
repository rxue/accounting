from pathlib import Path
from typing import NamedTuple

import pandas as pd

from investment.holdings.models import HoldingSnapshot
from investment.holdings.nordea_holdings_extractor import extract_from
from investment.company.repository import find_yahoo_symbols_by_name
from investment.holdings.market_quote.yfinance_fetcher import get_latest_quote


class HoldingsSnapshot(NamedTuple):
    bank: str
    holdings: list[HoldingSnapshot]

    @staticmethod
    def generate(holdings_excel_path: str) -> tuple["HoldingsSnapshot", list[str]]:
        holdings = extract_from(holdings_excel_path)
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
            snapshots.append(HoldingSnapshot(
                holding=holding,
                quote=quote,
            ))
        snapshots.sort(key=lambda s: s.quote.daily_change_rate(), reverse=True)
        bank_name=Path(holdings_excel_path).name.split("_")[0]
        return HoldingsSnapshot(bank=bank_name, holdings=snapshots), failed

    def to_dataframe(self) -> pd.DataFrame:
        return pd.DataFrame([
            {
                "company": s.holding.company_name,
                "amount": s.holding.amount,
                "price": s.quote.price,
                "currency": s.quote.currency,
                "daily_change": s.quote.daily_change_rate(),
                "dividend_yield": s.quote.dividend_yield,
                "pe": s.quote.pe,
                "roe": s.quote.roe,
                "timestamp": s.quote.timestamp_repr(),
            }
            for s in self.holdings
        ])
