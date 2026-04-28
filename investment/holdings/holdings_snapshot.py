from typing import NamedTuple

from investment.holdings.models import HoldingSnapshot
from investment.holdings.nordea_holdings_extractor import extract_from_excel
from investment.company.repository import find_companies_by_isin
from investment.holdings.market_quote.google_finance_fetcher import get_stock_price


class HoldingsSnapshot(NamedTuple):
    bank_account:str
    holdings:list[HoldingSnapshot]

    @staticmethod
    def generate_snapshot(holdings_excel_path:str) -> "HoldingsSnapshot":
        holdings = extract_from_excel(holdings_excel_path)
        isins = [h.isin for h in holdings]
        companies_by_isin = {c.isin: c for c in find_companies_by_isin(*isins)}
        snapshots = []
        for holding in holdings:
            company = companies_by_isin.get(holding.isin)
            if company is None:
                continue
            price = get_stock_price(company.company_code)
            if price is None:
                continue
            snapshots.append(HoldingSnapshot(company=company, amount=holding.amount, price=price))
        return HoldingsSnapshot(bank_account="Nordea", holdings=snapshots)
