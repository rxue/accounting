import csv
import sys
from datetime import date, datetime
from pathlib import Path

from investment.market_quote.ecb_fetcher import fetch_fx_rate_to_euro
from investment.market_quote.yahoo_finance_fetcher import fetch_closing_price, fetch_company
from investment.market_quote.models import Company, Price

_SYMBOL_MAP_PATH = Path(__file__).parent / "data" / "symbol_map.csv"


def _get_symbol(op_symbol:str) -> str:
    def trim(s: str) -> str:
        for suffix in (" US", " CN"):
            s = s.removesuffix(suffix)
        return s

    symbol_map = {}
    with _SYMBOL_MAP_PATH.open() as f:
        symbol_map = {row["OP Bank"]: row["Yahoo Finance"] for row in csv.DictReader(f)}
    trimmed_op_symbol = trim(op_symbol)
    return symbol_map.get(trimmed_op_symbol, trimmed_op_symbol)


def find_company_by_op_symbol(op_symbol: str) -> Company:
    yahoo_symbol = _get_symbol(op_symbol)
    return fetch_company(yahoo_symbol)

def find_closing_price_by_symbol(company:Company, d: date) -> Price:
    return Price(price=fetch_closing_price(company, d),
                 fx_rate=fetch_fx_rate_to_euro(company.currency, d))


def main():
    match sys.argv[1]:
        case "closing_price":
            quote_date = datetime.strptime(sys.argv[3], "%Y-%m-%d").date()
            company = find_company_by_op_symbol(sys.argv[2])
            print(find_closing_price_by_symbol(company, quote_date))
        case "company":
            print(find_company_by_op_symbol(sys.argv[2]))
        case "fx_rate":
            base_currency = sys.argv[2]
            quote_date = datetime.strptime(sys.argv[3], "%Y-%m-%d").date()
            print(fetch_fx_rate_to_euro(base_currency, quote_date))
        case _:
            print(f"Unknown method: {sys.argv[1]}", file=sys.stderr)
