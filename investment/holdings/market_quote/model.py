from typing import NamedTuple
from datetime import datetime, timezone


class Price(NamedTuple):
    value: float
    currency: str
    last_timestamp: int
    timezone_offset: int

    def __repr__(self) -> str:
        from datetime import timedelta
        offset = timezone(timedelta(milliseconds=self.timezone_offset))
        ts = datetime.fromtimestamp(self.last_timestamp, tz=offset)
        return f"Price({self.value} {self.currency} at {ts.strftime('%Y-%m-%d %H:%M:%S %Z')})"
