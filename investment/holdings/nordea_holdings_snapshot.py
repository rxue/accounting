from typing import NamedTuple

from investment.company.models import Company
from investment.holdings.models import HoldingSnapshot
from investment.holdings.nordea_holdings_extractor import extract_from_excel
from investment.company.repository import find_companies_by_name
from investment.holdings.market_quote.google_finance_fetcher import get_stock_price


class HoldingsSnapshot(NamedTuple):
    bank:str
    holdings:list[HoldingSnapshot]

    @staticmethod
    def generate_snapshot(holdings_excel_path:str) -> tuple["HoldingsSnapshot", list[Company]]:
        holdings = extract_from_excel(holdings_excel_path)
        names = [h.name for h in holdings]
        companies_by_name = {c.name: c for c in find_companies_by_name(*names)}
        snapshots = []
        missing_companies = []
        for holding in holdings:
            company = companies_by_name.get(holding.name)
            if company is None:
                continue
            price = get_stock_price(company.company_code)
            if price is None:
                missing_companies.append(company)
                continue
            snapshots.append(HoldingSnapshot(company=company, amount=holding.amount, price=price))
        return HoldingsSnapshot(bank="Nordea", holdings=snapshots), missing_companies
