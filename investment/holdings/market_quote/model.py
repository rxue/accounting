from typing import NamedTuple
from datetime import datetime, timezone


class Price(NamedTuple):
    value: float
    currency: str
    last_timestamp: int
    timezone_offset: int
    def timestamp_val(self)->str:
        from datetime import timedelta
        offset = timezone(timedelta(milliseconds=self.timezone_offset))
        dt = datetime.fromtimestamp(self.last_timestamp, tz=offset)
        return dt.strftime('%Y-%m-%d %H:%M:%S %Z')
    def __repr__(self) -> str:
        return f"Price({self.value} {self.currency} at {self.timestamp_val()})"

    def __format__(self, spec) -> str:
        return format(f"{self.value:<10}{self.currency:<5}{self.timestamp_val()}", spec)
