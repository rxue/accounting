import datetime

import pandas as pd

from investment.accounting.financialstatements.balance_sheet import BalanceSheetInCent
from investment.accounting.financialstatements.incomestatement.dividend_income import DividendIncomeInCent
from investment.accounting.financialstatements.incomestatement.income_statement import IncomeStatementInCent, generate_income_statement
from investment.accounting.financialstatements.reconciliation import reconcile
from investment.accounting.models import Holding
from investment.accounting.profit_calculation import calculate_profit_by_symbol
from investment.accounting.util import get_period
from investment.accounting.transaction_filters import find_all_stock_tradings_by_symbol, find_dividend_payments, find_expenses, find_cash_infusion, transactions_before


def generate(df: pd.DataFrame, end_date: datetime.date | None) -> tuple[IncomeStatementInCent, BalanceSheetInCent, list[Holding]]:
    def get_end_date(df: pd.DataFrame, end_date: datetime.date | None) -> datetime.date:
        if end_date is not None:
            return end_date
        latest = pd.to_datetime(df["Kirjauspäivä"], format="%d.%m.%Y").dt.date.max()
        last_day = (datetime.date(latest.year, latest.month, 1) + datetime.timedelta(days=32)).replace(day=1) - datetime.timedelta(days=1)
        return last_day

    end_date = get_end_date(df, end_date)
    filtered_df = transactions_before(df, end_date)
    profit_results = calculate_profit_by_symbol(find_all_stock_tradings_by_symbol(filtered_df))
    gross_trading_income = sum(r.profit_in_cent for r in profit_results)
    income_statement = generate_income_statement(get_period(filtered_df),
                                                 gross_trading_income,
                                                 DividendIncomeInCent(
                                                     dividend_payment_transactions_df=find_dividend_payments(filtered_df)),
                                                 find_expenses(filtered_df))
    financial_securities = sum(
        lot.money_amount_in_cent for r in profit_results for lot in r.remaining_lots
    )
    cash = round(filtered_df["Määrä EUROA"].str.replace(",", ".").astype(float).sum() * 100)
    balance_sheet = BalanceSheetInCent(date=end_date, cash=cash, financial_securities=financial_securities)
    return income_statement, balance_sheet, [r.get_holding() for r in profit_results]
def main():
    import argparse
    from investment.accounting.csv_to_dataframe import read_csvs_to_dataframe

    parser = argparse.ArgumentParser(description="Generate financial statements from CSV files")
    parser.add_argument("--input-dir", required=True, help="Directory containing CSV files")
    parser.add_argument("--end-date", required=False, help="end date")

    args = parser.parse_args()
    df = read_csvs_to_dataframe(args.input_dir)
    end_date = datetime.date.fromisoformat(args.end_date) if args.end_date else None
    income_statement, balance_sheet, holdings = generate(df, end_date)
    print(income_statement)
    print(f"total gross income={income_statement.total_gross_income()}")
    print(f"total expense={income_statement.expenses.total()}")
    print(balance_sheet)
    print("reconciled" if reconcile(find_cash_infusion(df), income_statement, balance_sheet) else "reconciliation failed")
    for holding in holdings:
        print(holding)

