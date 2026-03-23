import pandas as pd
from pathlib import Path

def _load_form8a_spec() -> pd.DataFrame:
    path = Path(__file__).parent.parent.parent.parent / "data" / "form8a_spec.csv"
    return pd.read_csv(path, dtype=str)

_FORM8A_SPEC = _load_form8a_spec()

def find_code(description: str, section: str = None) -> str:
    if section is None:
        match = _FORM8A_SPEC.loc[_FORM8A_SPEC["Description"] == description, "Code"]
        return match.iloc[0]
    ots_indices = _FORM8A_SPEC.index[_FORM8A_SPEC["Code"] == "OTS"].tolist()
    section_idx = _FORM8A_SPEC.index[
        (_FORM8A_SPEC["Code"] == "OTS") & (_FORM8A_SPEC["Description"] == section)
    ][0]
    next_ots_indices = [i for i in ots_indices if i > section_idx]
    end_idx = next_ots_indices[0] if next_ots_indices else len(_FORM8A_SPEC)
    section_df = _FORM8A_SPEC.iloc[section_idx + 1:end_idx]
    match = section_df.loc[section_df["Description"] == description, "Code"]
    return match.iloc[0]

def find_compulsory_fields() -> list[dict[str, str]]:
    return _FORM8A_SPEC[_FORM8A_SPEC["P/V"] == "P"].drop(columns=["P/V"]).to_dict(orient="records")

def _load_country() -> pd.DataFrame:
    path = Path(__file__).parent.parent.parent.parent / "data" / "country.csv"
    return pd.read_csv(path, dtype=str)

_COUNTRY = _load_country()

def find_withholding_tax_name(isin_code: str) -> str:
    match = _COUNTRY.loc[_COUNTRY["isin_code"] == isin_code, "withholding_tax_name"]
    return match.iloc[0]
