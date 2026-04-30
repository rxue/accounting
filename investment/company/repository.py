import csv
from pathlib import Path

from investment.company.models import Company

_CSV_PATH = Path(__file__).parents[2] / "data" / "companies.csv"


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
