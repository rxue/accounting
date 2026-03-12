from dataclasses import dataclass

from datetime import date

@dataclass
class BalanceSheetInCent:
    date: date
    cash: int
    financial_securities: int

    def current_assets(self) -> int:
        return self.cash + self.financial_securities

    def total_assets(self) -> int:
        return self.current_assets()

