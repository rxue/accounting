from investment.holdings.market_quote.google_finance_fetcher import get_stock_price


def test_nonexisting_stock_returns_none():
    result = get_stock_price("NONEXISTENT:INVALID")
    assert result is None
