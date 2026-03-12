from investment.accounting.util import match_trading


def test_match_trading_buy():
    match = match_trading("O:MRNA /20")
    assert match is not None
    assert match.group(1) == "O"
    assert match.group(2) == "MRNA"
    assert match.group(3) == "20"


def test_match_trading_buy_with_country_code():
    match = match_trading("O:PFE US /100")
    assert match is not None
    assert match.group(1) == "O"
    assert match.group(2) == "PFE"
    assert match.group(3) == "100"


def test_match_trading_buy_stock_with_symbol_containing_dot():
    match = match_trading("O:STZ.N /4")
    assert match is not None
    assert match.group(1) == "O"
    assert match.group(2) == "STZ.N"
    assert match.group(3) == "4"


def test_match_trading_sell():
    match = match_trading("M:SIRI /100")
    assert match is not None
    assert match.group(1) == "M"
    assert match.group(2) == "SIRI"
    assert match.group(3) == "100"


def test_match_trading_invalid():
    assert match_trading("invalid") is None
    assert match_trading("X:MRNA /20") is None
    assert match_trading("O:MRNA") is None
