from datetime import date
import pandas as pd

from investment.accounting.financialstatements.incomestatement.models import DividendPayment
from investment.accounting.models import Holding
from investment.tax_report.models import Country, TaxPaidAbroadEntryDTO
from investment.tax_report.securites_included_in_financial_assets import SecurityHoldingAsAsset, \
    to_SecurityHoldingAsAsset


def _load_countries(path: str) -> list[Country]:
    df = pd.read_csv(path, keep_default_na=False)
    return [Country(isin_code=row["isin_code"], name=row["country_name"], income_tax_name=row["income_tax_name"]) for _, row in df.iterrows()]

def generate_tax_paid_abroad_list(dividend_payments:list[DividendPayment]) -> list[TaxPaidAbroadEntryDTO]:
    countries = _load_countries("data/country.csv")
    def get_country_by_isin_code(payment: DividendPayment) -> Country:
        return next(c for c in countries if c.isin_code == payment.get_country_code())
    return [TaxPaidAbroadEntryDTO.from_dividend_payment(d, get_country_by_isin_code(d)) for d in dividend_payments]

def generate_SecurityHoldingsAsAsset(holdings: list[Holding], date: date) -> list[SecurityHoldingAsAsset]:
    return [to_SecurityHoldingAsAsset(holding, date) for holding in holdings]