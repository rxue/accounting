from enum import Enum, auto
from typing import NamedTuple
from datetime import date

class Action(Enum):
    BUY = auto()
    SELL = auto()

class Lot(NamedTuple):
    date: date
    action:Action
    share_amount: int
    value_in_cent: int

class RealizedLots(NamedTuple):
    lots: list[Lot]
    def realized_gain(self):
        return sum([lot.value_in_cent if lot.action == Action.BUY else -lot.value_in_cent for lot in self.lots])

class Result(NamedTuple):
    realized_lots_list:list[RealizedLots]
    remaining_lots:list[Lot]
    def unrealized_holding(self):
        sum([lot.share_amount for lot in self.remaining_lots])

def fifo_lots_matching(tradings:list[Lot]) -> Result:
    remaining_lots: list[Lot] = []

    def dequeue(buy_trading:Lot) -> RealizedLots:
        head_lot = remaining_lots[0]
        realized = [buy_trading]
        amount_to_dequeue = buy_trading.share_amount
        while amount_to_dequeue > 0:
            if buy_trading.share_amount >= head_lot.share_amount:
                amount_to_dequeue -= head_lot.share_amount
                realized.append(remaining_lots.pop(0))
        return RealizedLots(realized)
    realized_lots_list = []
    for tr in tradings:
        if tr.action == Action.BUY:
            remaining_lots.append(tr)
        else:
            realized_lots_list.append(dequeue(tr))

    return Result(realized_lots_list, remaining_lots)