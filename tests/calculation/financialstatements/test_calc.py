import pandas as pd

from calculation.financialstatements.calc import Period, get_period


def test_get_period():
    # First row from Tiliote_2025-07-15_2025-07-31.csv, last row from Tiliote_2026-01-31_2026-02-27.csv
    input_df = pd.DataFrame([
        {"Kirjauspäivä": "21.07.2025"},
        {"Kirjauspäivä": "27.02.2026"},
    ])
    assert get_period(input_df) == Period(start_date="2025-07-01", end_date="2026-02-28")


