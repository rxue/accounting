import sys
from investment.holdings.market_quote.yfinance_fetcher import get_latest_quotes

if len(sys.argv) != 2:
    print("Usage: python -m investment.holdings.market_quote <symbol1,symbol2,...>")
    print()
    print("  Example:  FORTUM.HE,ENB.TO,MRNA")
    sys.exit(1)

symbols = sys.argv[1].split(",")
for quote in get_latest_quotes(*symbols):
    print(quote)
