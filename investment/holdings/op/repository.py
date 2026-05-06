import pandas as pd

def find_tradings(transactions: pd.DataFrame) -> pd.DataFrame:
    def is_trading(row: pd.Series) -> bool:
        laji = row["Laji"]
        breakdown = row["Selitys"]
        def is_buy() -> bool:
            return laji == 700 and breakdown == "NOSTO"
        def is_sell() -> bool:
            return laji == 700 and breakdown == "PANO"
        return is_buy() or is_sell()

    rows = []
    for _, row in transactions.iterrows():
        if not is_trading(row):
            continue
        row = row.copy()
        rows.append(row)

    return pd.DataFrame(rows).reset_index(drop=True)
