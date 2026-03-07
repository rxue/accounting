import pandas as pd

from financialstatements.balance_sheet import BalanceSheetInCent
from financialstatements.incomestatement.income_item import DividendIncomeInCent
from financialstatements.incomestatement.income_statement import IncomeStatementInCent, generate_income_statement
from financialstatements.trading_calc import profit_and_book_values_by_symbol
from financialstatements.transaction_filters import find_all_stock_tradings_by_symbol, find_dividend_payments, find_expenses


def generate(df: pd.DataFrame) -> tuple[IncomeStatementInCent, BalanceSheetInCent]:
    profit_results = profit_and_book_values_by_symbol(find_all_stock_tradings_by_symbol(df))
    gross_trading_income = sum(r.profit_in_cent for r in profit_results)
    income_statement = generate_income_statement(gross_trading_income,
                                                 DividendIncomeInCent(transactions=find_dividend_payments(df)),
                                                 find_expenses(df))
    financial_securities = sum(
        lot.money_amount_in_cent for r in profit_results for lot in r.remaining_lots
    )
    cash = round(df["Määrä EUROA"].str.replace(",", ".").astype(float).sum() * 100)
    balance_sheet = BalanceSheetInCent(cash=cash, financial_securities=financial_securities)
    return income_statement, balance_sheet


def main():
    import argparse
    from financialstatements.csv_to_dataframe import read_csvs_to_dataframe

    parser = argparse.ArgumentParser(description="Generate financial statements from CSV files")
    parser.add_argument("directory", help="Directory containing CSV files")
    args = parser.parse_args()

    df = read_csvs_to_dataframe(args.directory)
    print(generate(df))
