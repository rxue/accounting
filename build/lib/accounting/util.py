import calendar
from dataclasses import dataclass

import pandas as pd


@dataclass
class Period:
    start_date: str
    end_date: str


def get_period(df: pd.DataFrame) -> Period:
    dates = pd.to_datetime(df["Kirjauspäivä"], format="%d.%m.%Y")
    first = dates.min()
    last = dates.max()
    start_date = first.replace(day=1).strftime("%Y-%m-%d")
    last_day = calendar.monthrange(last.year, last.month)[1]
    end_date = last.replace(day=last_day).strftime("%Y-%m-%d")
    return Period(start_date=start_date, end_date=end_date)
