from typing import NamedTuple


class Holding(NamedTuple):
    symbol:str
    share_amount: int
    book_value:float

class Lot(NamedTuple):
    date: str
    type: str
    share_amount: int
    money_amount_in_cent: int


class ProfitCalculationResult(NamedTuple):
    symbol: str
    profit_in_cent: int
    remaining_lots: list[Lot]

    def get_holding(self) -> Holding:
        return Holding(symbol=self.symbol,
                       share_amount=sum(lot.share_amount for lot in self.remaining_lots),
                       book_value=sum(lot.money_amount_in_cent for lot in self.remaining_lots)/100)
