import pandas as pd

from financialstatements.incomestatement.income_item import DividendIncome

TRANSACTION_DETAIL = (
    " OP Säilytys Oy                     SIRIUSXM HOLDINGS                  "
    "US8299331004                       Osinkotuotto                       "
    "Osinko        0,27          USD/KplOmistettu määrä             90Kpl  "
    "Tuoton määrä               24,30USDLähdevero  US15,0   %       3,65USD"
    "Veroero                     0,01USDVal.kurssi                1,1876"
)


TRANSACTION_DETAIL_CAD = (
    " OP Säilytys Oy                     TELUS CORP                         "
    "CA87971M1032                       Osinkotuotto                       "
    "Osinko        0,4184        CAD/KplOmistettu määrä             50Kpl  "
    "Tuoton määrä               20,92CADLähdevero  CA15,0   %       3,14CAD"
    "Val.kurssi                1,6188"
)


def test_gross_value_per_transaction_cad():
    assert DividendIncome._gross_value_per_transaction(TRANSACTION_DETAIL_CAD) == 1292


def test_gross_value_in_base_unit():
    assert DividendIncome._gross_value_in_base_unit(TRANSACTION_DETAIL) == 24.30


def test_withholding_tax_per_transaction():
    assert DividendIncome.withholding_tax_per_transaction(TRANSACTION_DETAIL) == 307


def test_withholding_tax_per_transaction_cad():
    assert DividendIncome.withholding_tax_per_transaction(TRANSACTION_DETAIL_CAD) == 193


def test_withholding_tax():
    df = pd.DataFrame([{
        "Kirjauspäivä": "27.02.2026",
        "Arvopäivä": "27.02.2026",
        "Määrä EUROA": "+17,39",
        "Laji": 710,
        "Selitys": "ARVOPAPERIT",
        "Saaja/Maksaja": "OUTLIERX OY",
        "Saajan tilinumero ja pankin BIC": " ",
        "Viite": float("nan"),
        "Viesti": TRANSACTION_DETAIL,
        "Arkistointitunnus": "2602275OMH00001897",
    }])
    item = DividendIncome(transactions=df)
    assert item.withholding_tax() == 307


def test_gross_value():
    df = pd.DataFrame([{
        "Kirjauspäivä": "27.02.2026",
        "Arvopäivä": "27.02.2026",
        "Määrä EUROA": "+17,39",
        "Laji": 710,
        "Selitys": "ARVOPAPERIT",
        "Saaja/Maksaja": "OUTLIERX OY",
        "Saajan tilinumero ja pankin BIC": " ",
        "Viite": float("nan"),
        "Viesti": TRANSACTION_DETAIL,
        "Arkistointitunnus": "2602275OMH00001897",
    }])
    item = DividendIncome(transactions=df)
    assert item.gross_value() == 2046
