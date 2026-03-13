from datetime import date, datetime, timedelta

from zoneinfo import ZoneInfo

from investment.market_quote.models import Company

def fetch_closing_price(company: Company, date: date) -> float:
    date_at_0 = datetime(date.year, date.month, date.day, tzinfo=company.time_zone)
    next_day_at_0 = date_at_0 + timedelta(days=1)

    url = f"https://query2.finance.yahoo.com/v8/finance/chart/{company.yahoo_symbol}"
    response = requests.get(url, headers={"User-Agent": "Mozilla/5.0"}, params={
        "period1": int(date_at_0.timestamp()),
        "period2": int(next_day_at_0.timestamp()),
        "interval": "1d",
        "events": "history",
    })
    response.raise_for_status()

    quote = response.json()["chart"]["result"][0]["indicators"]["quote"][0]
    return quote["close"][0]


import requests

def fetch_company(symbol: str) -> Company:
    """Fetch company metadata for a given symbol from Yahoo Finance."""
    url = f"https://query2.finance.yahoo.com/v8/finance/chart/{symbol}"
    response = requests.get(url, headers={"User-Agent": "Mozilla/5.0"}, params={
        "interval": "1d",
        "range": "1d",
    })
    response.raise_for_status()

    meta = response.json()["chart"]["result"][0]["meta"]
    return Company(
        short_name=meta["shortName"],
        yahoo_symbol=meta["symbol"],
        time_zone=ZoneInfo(meta["exchangeTimezoneName"]),
        currency=meta["currency"],
    )


