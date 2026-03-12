#!/usr/bin/env python3
"""Filter functions for transaction DataFrames. All functions' return type is based on pf.DataFrame"""

import argparse
import datetime

import pandas as pd

from investment.accounting.util import match_trading

def find_dividend_payments(df: pd.DataFrame) -> pd.DataFrame:
    """Find rows where Laji is 'Arvopaperit' (stock tradings).

    Args:
        df: DataFrame containing a 'Laji' column.

    Returns:
        DataFrame with only rows where Laji == 'Arvopaperit'.
    """
    return df[df["Selitys"].str.lower() == "arvopaperit"]


def find_service_charges(df: pd.DataFrame) -> pd.DataFrame:
    return df[df["Selitys"].str.lower() == "palvelumaksu"]


def find_all_stock_tradings_by_symbol(df: pd.DataFrame) -> dict[str, pd.DataFrame]:
    """Find stock trading transactions grouped by ticker symbol.

    Args:
        df: DataFrame containing 'Laji' and 'Viesti' columns.

    Returns:
        Dict with stock symbol as key and DataFrame of transactions as value.
    """

    def is_trading(row)->bool:
        return row["Laji"] == 700 and (row["Selitys"] == "NOSTO" or row["Selitys"] == "PANO")

    def get_symbol(message: str) -> str:
        match = match_trading(message.strip())
        if not match:
            raise ValueError(f"No symbol found in message: {message}")
        return match.group(2)

    symbol_to_row_index_list_map: dict[str, list[int]] = {}

    for idx, row in df.iterrows():
        if not is_trading(row):
            continue
        symbol = get_symbol(row["Viesti"])
        if symbol not in symbol_to_row_index_list_map:
            symbol_to_row_index_list_map[symbol] = []
        symbol_to_row_index_list_map[symbol].append(idx)

    return {symbol: df.loc[indices] for symbol, indices in symbol_to_row_index_list_map.items()}



def transactions_before(df: pd.DataFrame, date: datetime.date) -> pd.DataFrame:
    dates = pd.to_datetime(df["Kirjauspäivä"], format="%d.%m.%Y").dt.date
    return df[dates <= date]


def find_cash_infusion(df: pd.DataFrame) -> pd.DataFrame:
    return df[(df["Laji"] == 710) & (df["Selitys"].str.strip().str.lower() == "tilisiirto")]


def find_expenses(df: pd.DataFrame) -> pd.DataFrame:
    """Find expense rows, i.e. Määrä EUROA is negative and not a stock trading.

    Args:
        df: DataFrame containing 'Määrä EUROA' and 'Viesti' columns.

    Returns:
        DataFrame with only rows where amount is negative and Viesti doesn't match a trading pattern.
    """
    amounts = df["Määrä EUROA"].str.replace(",", ".").astype(float)
    negative = df[amounts < 0]
    is_trading = negative["Viesti"].apply(lambda v: match_trading(v.strip()) is not None)
    return negative[~is_trading]


def main():
    from investment.accounting.csv_to_dataframe import read_csvs_to_dataframe
    parser = argparse.ArgumentParser(
        description="Filter transactions from CSV files"
    )
    parser.add_argument("directory", help="Directory containing CSV files")
    args = parser.parse_args()

    df = read_csvs_to_dataframe(args.directory)
    print(f"Total rows: {len(df)}")


if __name__ == "__main__":
    main()
