import argparse
import datetime

from investment.accounting.composite_generator import generate
from investment.accounting.csv_to_dataframe import read_csvs_to_dataframe
from investment.tax_report.securites_included_in_financial_assets import SecurityHoldingAsAsset, \
    to_SecurityHoldingsAsAsset


def main():
    parser = argparse.ArgumentParser(description="Generate tax report")
    parser.add_argument("--input-dir", required=True, help="Directory containing CSV files")
    parser.add_argument("--end-date", required=True, help="End date (YYYY-MM-DD)")
    args = parser.parse_args()

    df = read_csvs_to_dataframe(args.input_dir)
    end_date = datetime.date.fromisoformat(args.end_date)
    income_statement, balance_sheet, holdings = generate(df, end_date=end_date)

    securities: list[SecurityHoldingAsAsset] = to_SecurityHoldingsAsAsset(holdings, end_date)

    print(income_statement)
    print(balance_sheet)
    for security in securities:
        print(security)
