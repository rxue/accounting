

def test__get_symbol():
    from investment.market_quote.repository import _get_symbol
    symbol = _get_symbol("SIRI")
    assert symbol == "SIRI"

def test__get_symbol_with_country_code_us():
    from investment.market_quote.repository import _get_symbol
    symbol = _get_symbol("PFE US")
    assert symbol == "PFE"
