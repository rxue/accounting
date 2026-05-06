from dataclasses import dataclass
from typing import Literal, NamedTuple

from investment.holdings.models.holdings import Trading

Type = Literal["GAIN", "LOSS"]

class ValuationResult(NamedTuple):
    type: Type
    value:float

@dataclass(frozen=True, slots=True)
class NordeaTradingLot(Trading):
    charge:float