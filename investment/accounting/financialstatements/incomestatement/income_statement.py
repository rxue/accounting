from typing import NamedTuple

import pandas as pd

from investment.accounting.financialstatements.incomestatement.models import DividendIncome
from investment.accounting.transaction_filters import find_service_charges
from investment.accounting.util import Period


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


class IncomeStatementInCent(NamedTuple):
    period: Period
    gross_dividend_income: int
    trading_income: int
    expenses: ExpensesInCent

    def total_gross_income(self) -> int:
        return self.gross_dividend_income + self.trading_income

    def net_income(self) -> int:
        return (
            self.gross_dividend_income
            + self.trading_income
            - self.expenses.foreign_withholding_tax
            - self.expenses.service_expense
            - self.expenses.other_expense
            - self.expenses.salaries_and_wages
        )
    def loss(self):
        return self.gross_dividend_income + self.trading_income - self.expenses.total()

def generate_income_statement(period: Period, gross_trading_income: int, dividend_income: DividendIncome, expenses_df: pd.DataFrame) -> IncomeStatementInCent:
    all_expense_in_cents = abs(round(expenses_df["Määrä EUROA"].str.replace(",", ".").astype(float).sum() * 100))
    service_expense_cents = abs(round(find_service_charges(expenses_df)["Määrä EUROA"].str.replace(",", ".").astype(float).sum() * 100))
    gross_dividend_income = dividend_income.gross_value_in_cent()
    foreign_withholding_tax = dividend_income.withholding_tax_in_cent()
    return IncomeStatementInCent(
        period=period,
        gross_dividend_income=gross_dividend_income,
        trading_income=gross_trading_income,
        expenses=ExpensesInCent(
            service_expense=service_expense_cents,
            other_expense=all_expense_in_cents - service_expense_cents,
            foreign_withholding_tax=foreign_withholding_tax,
        ),
    )
