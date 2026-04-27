from typing import NamedTuple
import pandas as pd


class Holding(NamedTuple):
    isin: str
    mic: str
    currency: str
    name: str
    holdings: int


def extract_from_excel(file_path: str) -> list[Holding]:
    df = pd.read_excel(file_path, header=1)
    custody_rows = df[df["Type"] == "Custody"].dropna(subset=["ISIN"])
    return [
        Holding(
            isin=row["ISIN"],
            mic=row["MIC"],
            currency=row["CURRENCY"],
            name=row["NAME"],
            holdings=int(row["HOLDINGS"]),
        )
        for _, row in custody_rows.iterrows()
    ]