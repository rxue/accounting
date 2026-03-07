from dataclasses import dataclass

import pandas as pd

from financialstatements.incomestatement.income_item import DividendIncome, TradingIncome
from financialstatements.trading_calc import profit_and_book_values_by_symbol
from query.transaction_filters import find_dividend_payments, find_all_stock_tradings_by_symbol, find_service_charges, find_expenses


@dataclass
class IncomeStatementInCent:
    gross_dividend_income: int
    trading_income: int
    service_expense: int
    other_expense: int
    foreign_withholding_tax: int


def generate_income_statement(df: pd.DataFrame) -> IncomeStatementInCent:
    dividend_income = DividendIncome(transactions=find_dividend_payments(df))
    trading_income = TradingIncome(profit_calculation_results=profit_and_book_values_by_symbol(find_all_stock_tradings_by_symbol(df)))
    all_expenses_df = find_expenses(df)
    all_expense_in_cents = abs(round(all_expenses_df["Määrä EUROA"].str.replace(",", ".").astype(float).sum() * 100))
    service_expense_cents = abs(round(find_service_charges(all_expenses_df)["Määrä EUROA"].str.replace(",", ".").astype(float).sum() * 100))
    gross_dividend_income = dividend_income.gross_value()
    foreign_withholding_tax = dividend_income.withholding_tax()
    if not dividend_income.reconcile():
        raise ValueError("Dividend income reconciliation failed")
    return IncomeStatementInCent(
        gross_dividend_income=gross_dividend_income,
        trading_income=trading_income.gross_value(),
        service_expense=service_expense_cents,
        other_expense=all_expense_in_cents - service_expense_cents,
        foreign_withholding_tax=foreign_withholding_tax,
    )


def main():
    import argparse
    from tax_report.csv_to_dataframe import read_csvs_to_dataframe

    parser = argparse.ArgumentParser(description="Generate income statement from CSV files")
    parser.add_argument("directory", help="Directory containing CSV files")
    args = parser.parse_args()

    df = read_csvs_to_dataframe(args.directory)
    print(generate_income_statement(df))
