from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

import requests

_US_EASTERN = ZoneInfo("America/New_York")


def closing_price(symbol: str, date: datetime) -> float:
    """Fetch the closing price for the given symbol.

    Returns:
        The closing price, e.g. 182.63.
    """
    date_at_0 = date.replace(hour=0, minute=0, second=0, microsecond=0, tzinfo=_US_EASTERN)
    next_day_at_0 = date_at_0 + timedelta(days=1)

    period1 = int(date_at_0.timestamp())
    period2 = int(next_day_at_0.timestamp())

    url = f"https://query2.finance.yahoo.com/v8/finance/chart/{symbol}"
    response = requests.get(url, params={
        "period1": period1,
        "period2": period2,
        "interval": "1d",
        "events": "history",
    })
    response.raise_for_status()

    result = response.json()["chart"]["result"][0]
    close = result["indicators"]["quote"][0]["close"][0]

    return close


if __name__ == "__main__":
    import sys

    symbol = sys.argv[1]
    date = datetime.strptime(sys.argv[2], "%Y-%m-%d")
    print(closing_price(symbol, date))
