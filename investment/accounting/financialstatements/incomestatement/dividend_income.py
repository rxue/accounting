import re

import pandas as pd


class DividendIncomeInCent:
    def __init__(self, dividend_payment_transactions_df: pd.DataFrame):
        self.transactions = dividend_payment_transactions_df
        self._gross_value: int | None = None
        self._withholding_tax: int | None = None

    def _calculate(self) -> None:
        self._gross_value = sum(DividendIncomeInCent._gross_value_per_transaction(row) for _, row in self.transactions.iterrows())
        self._withholding_tax = sum(DividendIncomeInCent.withholding_tax_per_transaction(row["Viesti"]) for _, row in self.transactions.iterrows())

    def gross_value(self) -> int:
        if self._gross_value is None:
            self._calculate()
        return self._gross_value

    @staticmethod
    def _gross_value_per_transaction(row: pd.Series) -> int:
        return DividendIncomeInCent._net_value_per_transaction(row) + DividendIncomeInCent.withholding_tax_per_transaction(row["Viesti"])

    @staticmethod
    def _net_value_per_transaction(row: pd.Series) -> int:
        return round(float(row["Määrä EUROA"].replace(",", ".")) * 100)

    def withholding_tax(self) -> int:
        if self._withholding_tax is None:
            self._calculate()
        return self._withholding_tax

    @staticmethod
    def _exchange_rate_per_transaction(transaction_detail: str) -> float:
        rate_match = re.search(r"Val\.kurssi\s+([\d,]+)", transaction_detail)
        if not rate_match:
            raise ValueError("Could not parse exchange rate from transaction detail")
        return float(rate_match.group(1).replace(",", "."))

    @staticmethod
    def withholding_tax_per_transaction(transaction_detail: str) -> int:
        tax_match = re.search(r"Lähdevero\s+\S+\s+%\s+([\d,]+)[A-Z]{3}", transaction_detail)
        if not tax_match:
            raise ValueError("Could not parse tax from transaction detail")
        tax_usd = float(tax_match.group(1).replace(",", "."))
        exchange_rate = DividendIncomeInCent._exchange_rate_per_transaction(transaction_detail)
        return int(tax_usd / exchange_rate * 100)
