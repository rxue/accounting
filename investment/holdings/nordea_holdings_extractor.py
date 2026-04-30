from pathlib import Path

import pandas as pd

from investment.holdings.models import Holding

def extract_from_nordnet_csv(file_path: str) -> list[Holding]:
    df = pd.read_csv(file_path, encoding="utf-16", sep="\t")
    return [
        Holding(
            company_name=row["Nimi"].strip(),
            amount=int(row["Määrä"]),
        )
        for _, row in df.iterrows()
    ]

def extract_from(file_path: str) -> list[Holding]:
    if Path(file_path).name.startswith("nordnet"):
        return extract_from_nordnet_csv(file_path)
    df = pd.read_excel(file_path, header=1)
    custody_rows = df[df["Type"] == "Custody"].dropna(subset=["ISIN"])
    return [
        Holding(
            company_name=row["NAME"],
            amount=int(row["HOLDINGS"]),
        )
        for _, row in custody_rows.iterrows()
    ]