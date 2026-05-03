import pandas as pd

def extract(file_path: str) -> pd.DataFrame:
    return pd.read_csv(file_path, sep='\t', encoding='utf-16')

def get_deposit(transactions: pd.DataFrame) -> float:
    deposits = transactions[transactions["Tapahtumatyyppi"] == "TALLETUS"]
    return deposits["Summa"].astype(str).str.replace(",", ".").astype(float).sum()

def get_withdrawal(transactions: pd.DataFrame) -> float:
    deposits = transactions[transactions["Tapahtumatyyppi"] == "NOSTO"]
    return deposits["Summa"].astype(str).str.replace(",", ".").astype(float).sum()