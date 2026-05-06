from pathlib import Path

import pandas as pd


def extract_csv(path: str, sep: str = '\t', encoding: str = 'utf-16') -> pd.DataFrame:
    p = Path(path)
    if p.is_dir():
        files = sorted(p.glob("*.csv"))
        if not files:
            raise ValueError(f"No CSV files found in directory: {path}")
        dfs = []
        for f in files:
            dfs.append(pd.read_csv(f, sep=sep, encoding=encoding))
        return pd.concat(dfs, ignore_index=True)
    return pd.read_csv(p, sep=sep, encoding=encoding)