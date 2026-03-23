import re
from datetime import date, datetime
from typing import NamedTuple

import pandas as pd

from investment.accounting.util import Period


class PaymentCompany(NamedTuple):
    name:str
    country_code:str

class DividendPayment(NamedTuple):
    value_date: date
    company: PaymentCompany
    net_value_in_eur: float
    source_currency: str
    shares_owned: int
    dividend_per_share: float
    gross_income: float
    witholding_tax_rate: int
    withholding_tax: float
    exchange_rate: float

    @property
    def withholding_tax_in_eur(self) -> float:
        return self.withholding_tax / self.exchange_rate

    @property
    def gross_value_in_eur(self) -> float:
        return self.net_value_in_eur + self.withholding_tax_in_eur

    @classmethod
    def from_transaction(cls, row: pd.Series) -> "DividendPayment":
        def to_float(s: str) -> float:
            return float(s.replace(",", "."))

        message = row["Viesti"]

        stock_match = re.search(r"OP Säilytys Oy\s+(.+?)\s{2,}([A-Z]{2})[A-Z0-9]{10}", message)
        company_name = stock_match.group(1).strip() if stock_match else ""
        country_code = stock_match.group(2) if stock_match else ""

        div_match = re.search(r"Osinko\s+([\d,]+)\s+([A-Z]+)/Kpl", message)
        source_currency = div_match.group(2) if div_match else ""
        dividend_per_share = to_float(div_match.group(1)) if div_match else 0.0

        shares_match = re.search(r"Omistettu määrä\s+(\d+)\s*Kpl", message)
        shares_owned = int(shares_match.group(1)) if shares_match else 0

        gross_match = re.search(r"Tuoton määrä\s+([\d,]+)\s*\w+", message)
        gross_income = to_float(gross_match.group(1)) if gross_match else 0.0

        tax_match = re.search(r"Lähdevero\s+[A-Z]+([\d,]+)\s*%\s+([\d,]+)\s*\w+", message)
        rate_match = re.search(r"Val\.kurssi\s+([\d,]+)", message)
        exchange_rate = to_float(rate_match.group(1)) if rate_match else 0.0

        return cls(
            value_date=datetime.strptime(row["Arvopäivä"], "%d.%m.%Y").date(),
            net_value_in_eur=to_float(row["Määrä EUROA"]),
            company=PaymentCompany(name=company_name, country_code=country_code),
            source_currency=source_currency,
            shares_owned=shares_owned,
            dividend_per_share=dividend_per_share,
            gross_income=gross_income,
            witholding_tax_rate=int(to_float(tax_match.group(1))) if tax_match else 0,
            withholding_tax=(to_float(tax_match.group(2)) if tax_match else 0.0),
            exchange_rate=exchange_rate,
        )

    def get_country_code(self):
        return self.company.country_code

class DividendIncome(NamedTuple):
    dividend_payments: list[DividendPayment]

    def gross_value_in_cent(self) -> int:
        return round(sum(p.gross_value_in_eur for p in self.dividend_payments) * 100)

    def withholding_tax_in_cent(self) -> int:
        return round(sum(p.withholding_tax_in_eur for p in self.dividend_payments) * 100)

    @classmethod
    def from_transactions(cls, dividend_df: pd.DataFrame) -> "DividendIncome":
        return cls(
            [DividendPayment.from_transaction(row) for _, row in dividend_df.iterrows()]
        )


class ExpensesInCent(NamedTuple):
    service_expense: int
    other_expense: int
    foreign_withholding_tax: int
    salaries_and_wages: int = 0

    def total(self) -> int:
        return (
            self.service_expense
            + self.other_expense
            + self.foreign_withholding_tax
            + self.salaries_and_wages
        )


class IncomeStatement(NamedTuple):
    period: Period
    dividend_income: DividendIncome
    trading_income_in_cent: int
    expenses: ExpensesInCent
    @property
    def gross_dividend_income_in_cent(self):
        return self.dividend_income.gross_value_in_cent()

    def total_gross_income(self) -> int:
        return self.gross_dividend_income_in_cent + self.trading_income_in_cent

    def net_income(self) -> int:
        return (
            self.gross_dividend_income_in_cent
            + self.trading_income_in_cent
            - self.expenses.foreign_withholding_tax
            - self.expenses.service_expense
            - self.expenses.other_expense
            - self.expenses.salaries_and_wages
        )

    def dividend_payments(self) -> list[DividendPayment]:
        return self.dividend_income.dividend_payments

    def loss(self):
        return self.gross_dividend_income_in_cent + self.trading_income_in_cent - self.expenses.total()