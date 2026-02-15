#!/usr/bin/env python3
"""Analyze transaction data from DataFrames."""

import argparse
from dataclasses import dataclass

import pandas as pd

from tax_report.csv_to_dataframe import read_csvs_to_dataframe
from tax_report.transaction_filters import (
    find_dividend_payments,
    find_all_stock_tradings_by_symbol,
    find_expenses,
    match_trading, find_cash_infusion,
)


@dataclass
class Lot:
    date: str
    type: str
    share_amount: int
    money_amount_in_cent: int


@dataclass
class TaxReportItemsInCent:
    business_income: int
    business_expense: int
    cash: int
    financial_asset: int


def transfer_transactions_to_lots(df: pd.DataFrame) -> list[Lot]:
    """Parse buy/sell transactions into Transaction objects.

    Args:
        df: DataFrame with 'Kirjauspäivä' and 'Viesti' columns.
            Viesti format: "O:SYMBOL /amount" or "M:SYMBOL /amount"

    Returns:
        List of Transaction objects.
    """
    transactions = []

    for _, row in df.iterrows():
        viesti = row["Viesti"].strip()
        match = match_trading(viesti)
        if match:
            type_code = match.group(1)
            share_amount = int(match.group(3))
            transaction_type = "BUY" if type_code == "O" else "SELL"
            money_amount_in_cent = round(abs(float(row["Määrä EUROA"].replace(",", "."))) * 100)

            transactions.append(Lot(
                date=row["Kirjauspäivä"],
                type=transaction_type,
                share_amount=share_amount,
                money_amount_in_cent=money_amount_in_cent
            ))

    return transactions



def stock_trading_profit_in_fifo(transactions: list[Lot]) -> (int, list[Lot]):
    """Calculate profit from transactions using FIFO method.

    Args:
        transactions: List of Lot objects sorted by date.

    Returns:
        profit: Total profit (positive) or loss (negative)
        remaining_lots: List of Lot for unsold shares
    """
    buy_queue: list[tuple[str, int, int]] = []  # (date, shares, total_cost_in_cents)
    total_profit_cents = 0

    for tx in transactions:
        if tx.type == "BUY":
            buy_queue.append((tx.date, tx.share_amount, tx.money_amount_in_cent))
        elif tx.type == "SELL":
            sell_total_cents = tx.money_amount_in_cent
            shares_to_sell = tx.share_amount

            while shares_to_sell > 0 and buy_queue:
                buy_date, buy_shares, buy_total_cents = buy_queue[0]

                if buy_shares <= shares_to_sell:
                    sell_portion_cents = sell_total_cents * buy_shares // shares_to_sell
                    total_profit_cents += sell_portion_cents - buy_total_cents
                    sell_total_cents -= sell_portion_cents
                    shares_to_sell -= buy_shares
                    buy_queue.pop(0)
                else:
                    buy_portion_cents = buy_total_cents * shares_to_sell // buy_shares
                    total_profit_cents += sell_total_cents - buy_portion_cents
                    buy_queue[0] = (buy_date, buy_shares - shares_to_sell, buy_total_cents - buy_portion_cents)
                    shares_to_sell = 0

    remaining_lots = [Lot(date=date, type="BUY", share_amount=shares, money_amount_in_cent=cost_in_cents) for date, shares, cost_in_cents in buy_queue]
    return total_profit_cents, remaining_lots

def sum_money_in_cents(df: pd.DataFrame) -> int:
    """Sum money values in a DataFrame in cents.

    Args:
        df: DataFrame containing 'Määrä EUROA' column.

    Returns:
        Sum of the money values in cents.
    """
    values = df["Määrä EUROA"].str.replace(",", ".").astype(float)
    cents = (values * 100).round().astype(int)
    return int(cents.sum())


class TaxReport:
    def __init__(self, df: pd.DataFrame):
        self.df = df
        self.all_tradings_by_symbol = find_all_stock_tradings_by_symbol(df)
        self.dividend_payments_df = find_dividend_payments(df)
        self.expenses_df = find_expenses(df)
        self.cash_in_cents = sum_money_in_cents(df)
        self.cash_infusions_df = find_cash_infusion(df)
        if not self._total_rows_checksum():
            raise ValueError("Row separation checksum failed: filtered rows do not account for all rows in the DataFrame")

    def _stock_trading_profit_and_book_values_by_symbol(self) -> dict[str, tuple[int, int]]:
        """Calculate capital gains and book values of each Stock.

        Returns:
            map whose key is the stock symbol, and the value is the (profit_in_cent, book_value_in_cent)
        """
        result = {}
        for symbol, symbol_df in self.all_tradings_by_symbol.items():
            lots = transfer_transactions_to_lots(symbol_df)
            profit, remaining_lots = stock_trading_profit_in_fifo(lots)
            book_value = sum(lot.money_amount_in_cent for lot in remaining_lots)
            result[symbol] = (profit, book_value)
        return result

    def calculate_items(self) -> TaxReportItemsInCent:
        """Generate a tax report with business income and expenses.

        Returns:
            Report object with business income and expenses.
        """
        trading_profit_and_book_values = self._stock_trading_profit_and_book_values_by_symbol()
        total_trading_profit_cents = sum(profit for profit, _ in trading_profit_and_book_values.values())
        business_income_cents = sum_money_in_cents(pd.concat([self.dividend_payments_df])) + total_trading_profit_cents

        business_expense_cents = abs(sum_money_in_cents(self.expenses_df))

        total_financial_asset_cents = sum(book_value for _, book_value in trading_profit_and_book_values.values())

        if business_expense_cents + total_financial_asset_cents + self.cash_in_cents - business_income_cents != sum_money_in_cents(self.cash_infusions_df):
            raise ValueError("Checksum on tax report items failed")

        return TaxReportItemsInCent(
            business_income=business_income_cents,
            business_expense=business_expense_cents,
            cash=self.cash_in_cents,
            financial_asset=total_financial_asset_cents
        )

    def _total_rows_checksum(self) -> bool:
        """Verify that all rows are accounted for by the filter functions.

        Returns:
            True if the sum of filtered rows equals total rows, False otherwise.
        """
        total_stock_trading_rows = sum(len(symbol_df) for symbol_df in self.all_tradings_by_symbol.values())
        whole_sum = total_stock_trading_rows + len(self.dividend_payments_df) + len(self.expenses_df) + len(self.cash_infusions_df)
        return len(self.df) > 1 and len(self.df) == whole_sum


def main():
    parser = argparse.ArgumentParser(
        description="Analyze transactions from CSV files"
    )
    parser.add_argument("directory", help="Directory containing CSV files")
    args = parser.parse_args()

    df = read_csvs_to_dataframe(args.directory)
    print(df)
    print("------------Report---------------")
    taxReport = TaxReport(df)
    taxReportFactors = taxReport.calculate_items()
    print(taxReportFactors)


if __name__ == "__main__":
    main()
