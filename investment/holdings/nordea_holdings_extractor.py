import pandas as pd

from investment.holdings.models import Holding


def extract_from_excel(file_path: str) -> list[Holding]:
    df = pd.read_excel(file_path, header=1)
    custody_rows = df[df["Type"] == "Custody"].dropna(subset=["ISIN"])
    return [
        Holding(
            company_name=row["NAME"],
            amount=int(row["HOLDINGS"]),
        )
        for _, row in custody_rows.iterrows()
    ]