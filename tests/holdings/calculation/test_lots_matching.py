from datetime import date

from investment.holdings.calculation.lots_matching import Action, Lot, fifo_lots_matching, RealizedLots


def test_fifo_one_lot_removed():
    buy1 = Lot(date=date(2026, 1, 13), action=Action.BUY, share_amount=20, value_in_cent=57596)
    buy2 = Lot(date=date(2026, 1, 13), action=Action.BUY, share_amount=20, value_in_cent=57468)
    sell = Lot(date=date(2026, 1, 14), action=Action.SELL, share_amount=20, value_in_cent=61200)

    result = fifo_lots_matching([buy1, buy2, sell])

    assert result.realized_lots_list == [RealizedLots([sell, buy1])]
    assert result.remaining_lots == [buy2]