import csv
from pathlib import Path

from investment.holdings.company.models import Company

_CSV_PATH = Path(__file__).parents[3] / "data" / "companies.csv"


def _fill_companies_cache() -> dict[str, str]:
    result = {}
    with open(_CSV_PATH, newline="") as f:
        for row in csv.DictReader(f):
            current_company_symbol = row["op_symbol"]
            result[current_company_symbol] = row["company_name"]
    return result

companies_cache = _fill_companies_cache()

def find_company_name_by_symbol(symbol:str) -> str | None:
    return companies_cache.get(symbol)

def find_companies_by_name(*names: str) -> list[Company]:
    name_set = set(names)
    result = []
    with open(_CSV_PATH, newline="") as f:
        for row in csv.DictReader(f):
            if row["company_name"] in name_set:
                result.append(Company(name=row["company_name"]))
    return result


def find_yahoo_symbols_by_name(*names: str) -> dict[str, str]:
    name_set = set(names)
    result = {}
    with open(_CSV_PATH, newline="") as f:
        for row in csv.DictReader(f):
            if row["company_name"] in name_set:
                result[row["company_name"]] = row["stock_symbol_yahoo"]
    return result
