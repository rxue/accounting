from datetime import date

import pandas as pd

from investment.holdings.op.holdings_calculation import to_trading, OPTrading


def make_row(viesti: str, selitys: str, maara: str, kirjauspaiva: str) -> pd.Series:
    return pd.Series({
        "Viesti": viesti,
        "Selitys": selitys,
        "Määrä EUROA": maara,
        "Kirjauspäivä": kirjauspaiva,
    })


def test_buy():
    row = make_row(" O:NOVO B /20", "NOSTO", "-690,83", "25.02.2026")
    assert to_trading(row) == OPTrading(
        company_identifier="NOVO B",
        action="O",
        date=date(2026, 2, 25),
        amount=20,
        trade_price=690.83,
    )


def test_sell():
    row = make_row(" M:MRNA /20 578876374313", "PANO", "689,71", "14.01.2026")
    assert to_trading(row) == OPTrading(
        company_identifier="MRNA",
        action="M",
        date=date(2026, 1, 14),
        amount=20,
        trade_price=689.71,
    )


def test_single_word_ticker():
    row = make_row(" O:MANTA /80", "NOSTO", "-551,40", "02.03.2026")
    result = to_trading(row)
    assert result.company_identifier == "MANTA"
    assert result.amount == 80
