from pathlib import Path

import pandas as pd


def extract_csv(path: str) -> pd.DataFrame:
    p = Path(path)
    if p.is_dir():
        files = sorted(p.glob("*.csv"))
        if not files:
            raise ValueError(f"No CSV files found in directory: {path}")
        return pd.concat(
            [pd.read_csv(f, sep='\t', encoding='utf-16') for f in files],
            ignore_index=True,
        )
    return pd.read_csv(p, sep='\t', encoding='utf-16')