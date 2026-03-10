from dataclasses import dataclass

import pandas as pd

from calculation.financialstatements.incomestatement.income_item import DividendIncomeInCent
from calculation.util import Period
from calculation.financialstatements.calc import calculate_profit_by_symbol
from calculation.financialstatements.transaction_filters import find_dividend_payments, find_all_stock_tradings_by_symbol, find_service_charges, find_expenses


@dataclass
class ExpensesInCent:
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


@dataclass
class IncomeStatementInCent:
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


def generate_income_statement(period: Period, gross_trading_income: int, dividend_income: DividendIncomeInCent, expenses_df: pd.DataFrame) -> IncomeStatementInCent:
    all_expense_in_cents = abs(round(expenses_df["Määrä EUROA"].str.replace(",", ".").astype(float).sum() * 100))
    service_expense_cents = abs(round(find_service_charges(expenses_df)["Määrä EUROA"].str.replace(",", ".").astype(float).sum() * 100))
    gross_dividend_income = dividend_income.gross_value()
    foreign_withholding_tax = dividend_income.withholding_tax()
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


def main():
    import argparse
    from calculation.financialstatements.csv_to_dataframe import read_csvs_to_dataframe

    parser = argparse.ArgumentParser(description="Generate income statement from CSV files")
    parser.add_argument("directory", help="Directory containing CSV files")
    args = parser.parse_args()

    df = read_csvs_to_dataframe(args.directory)
    gross_trading_income = sum(r.profit_in_cent for r in calculate_profit_by_symbol(find_all_stock_tradings_by_symbol(df)))
    dividend_income = DividendIncomeInCent(transactions=find_dividend_payments(df))
    from calculation.util import get_period
    print(generate_income_statement(get_period(df), gross_trading_income, dividend_income, find_expenses(df)))
