from typing import NamedTuple

class Company(NamedTuple):
    name: str
    def __format__(self, spec):
        return format(f"{self.name:<40s}", spec)