from typing import NamedTuple

import pandas as pd


class NordeaHolding(NamedTuple):
    name: str
    amount: int

def extract_from_excel(file_path: str) -> list[NordeaHolding]:
    df = pd.read_excel(file_path, header=1)
    custody_rows = df[df["Type"] == "Custody"].dropna(subset=["ISIN"])
    return [
        NordeaHolding(
            name=row["NAME"],
            amount=int(row["HOLDINGS"]),
        )
        for _, row in custody_rows.iterrows()
    ]