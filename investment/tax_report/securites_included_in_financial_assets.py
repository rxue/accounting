from datetime import date
from typing import NamedTuple

from investment.accounting.models import Holding
from investment.market_quote.repository import find_closing_price_by_symbol, find_company_by_op_symbol


class SecurityHoldingAsAsset(NamedTuple):
    company_name:str
    number_of_shares:int
    closing_price_per_unit:float
    def comparison_value_per_unit(self) -> float:
        return round(self.closing_price_per_unit * 0.7, 2)
    def total_comparison_value(self):
        return round(self.closing_price_per_unit * self.number_of_shares * 0.7, 2)

    def __str__(self) -> str:
        return (f"SecurityHoldingAsAsset(company_name={self.company_name!r}, "
                f"number_of_shares={self.number_of_shares!r}, "
                f"closing_price_per_unit={self.closing_price_per_unit!r}, "
                f"comparison_value_per_unit={self.comparison_value_per_unit()}, "
                f"total_comparison_value={self.total_comparison_value()})")
    

def _to_SecurityHoldingAsAsset(holding: Holding, date: date) -> SecurityHoldingAsAsset:
    company = find_company_by_op_symbol(holding.symbol)
    price = find_closing_price_by_symbol(company, date)
    return SecurityHoldingAsAsset(
        company_name=company.short_name,
        number_of_shares=holding.share_amount,
        closing_price_per_unit=price.price_in_eur()
    )

def to_SecurityHoldingsAsAsset(holdings: list[Holding], date: date) -> list[SecurityHoldingAsAsset]:
    return [_to_SecurityHoldingAsAsset(holding, date) for holding in holdings]