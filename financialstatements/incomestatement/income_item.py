import re
from abc import ABC, abstractmethod

import pandas as pd

from financialstatements.trading_calc import ProfitCalculationResult



class IncomeItemInCent(ABC):
    """An income item of the Gross Income in the income statement.

    Currently there are 2 types of income items: dividend income and trading income.
    """
    transactions: pd.DataFrame

    @abstractmethod
    def gross_value(self) -> int: ...


class TradingIncome(IncomeItemInCent):
    def __init__(self, profit_calculation_results: list[ProfitCalculationResult]):
        self.profit_calculation_results = profit_calculation_results

    def gross_value(self) -> int:
        return sum(r.profit_in_cent for r in self.profit_calculation_results)


class DividendIncome(IncomeItemInCent):
    def __init__(self, transactions: pd.DataFrame):
        self.transactions = transactions

    def gross_value(self) -> int:
        return sum(
            DividendIncome._gross_value_per_transaction(detail)
            for detail in self.transactions["Viesti"]
        )

    @staticmethod
    def _gross_value_in_base_unit(transaction_detail: str) -> float:
        amount_match = re.search(r"Tuoton määrä\s+([\d,]+)[A-Z]{3}", transaction_detail)
        if not amount_match:
            raise ValueError("Could not parse gross amount from transaction detail")
        return float(amount_match.group(1).replace(",", "."))

    @staticmethod
    def _gross_value_per_transaction(transaction_detail: str) -> int:
        amount_usd = DividendIncome._gross_value_in_base_unit(transaction_detail)
        exchange_rate = DividendIncome._exchange_rate_per_transaction(transaction_detail)
        return int(amount_usd / exchange_rate * 100)

    def withholding_tax(self) -> int:
        return sum(
            DividendIncome.withholding_tax_per_transaction(detail)
            for detail in self.transactions["Viesti"]
        )

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
        exchange_rate = DividendIncome._exchange_rate_per_transaction(transaction_detail)
        return int(tax_usd / exchange_rate * 100)
