import csv
import io
from datetime import date

import requests


def fetch_fx_rate_to_euro(base_currency: str, date: date) -> float:
    if base_currency == 'EUR':
        return 1
    date_str = date.strftime("%Y-%m-%d")
    url = f"https://data-api.ecb.europa.eu/service/data/EXR/D.{base_currency}.EUR.SP00.A"
    response = requests.get(url, params={
        "startPeriod": date_str,
        "endPeriod": date_str,
        "format": "csvdata",
    })
    response.raise_for_status()
    reader = csv.DictReader(io.StringIO(response.text))
    row = next(reader)
    return float(row["OBS_VALUE"])
