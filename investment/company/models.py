from typing import NamedTuple


class CompanyCode(NamedTuple):
    """The Company Code used to search for stock quote from Google."""

    ticker_symbol:str
    stock_exchange_symbol:str

    def __repr__(self) -> str:
        return f"{self.ticker_symbol}:{self.stock_exchange_symbol}"

class Company(NamedTuple):
    company_code: CompanyCode
    name: str