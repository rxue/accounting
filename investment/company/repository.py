import csv
from pathlib import Path

from investment.company.models import Company, CompanyCode

_CSV_PATH = Path(__file__).parents[2] / "data" / "companies.csv"


def find_companies_by_name(*names: str) -> list[Company]:
    name_set = set(names)
    result = []
    with open(_CSV_PATH, newline="") as f:
        for row in csv.DictReader(f):
            if row["company_name"] in name_set:
                result.append(Company(
                    company_code=CompanyCode(
                        ticker_symbol=row["symbol"],
                        stock_exchange_symbol=row["stock_exchange_symbol"],
                    ),
                    name=row["company_name"],
                ))
    return result
