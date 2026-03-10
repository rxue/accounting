import pandas as pd

from calculation.financialstatements.incomestatement.income_item import DividendIncomeInCent

TRANSACTION_DETAIL_USD = (
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


TELUS_CAD_ROW = pd.Series({
    "Määrä EUROA": "+10,98",
    "Viesti": TRANSACTION_DETAIL_CAD,
})


def test_gross_value_per_transaction_cad():
    assert DividendIncomeInCent._gross_value_per_transaction(TELUS_CAD_ROW) == 1291


def test_withholding_tax_per_transaction():
    assert DividendIncomeInCent.withholding_tax_per_transaction(TRANSACTION_DETAIL_USD) == 307


def test_withholding_tax_per_transaction_cad():
    assert DividendIncomeInCent.withholding_tax_per_transaction(TRANSACTION_DETAIL_CAD) == 193


SIRIUSXM_USD_ROW = pd.DataFrame([{
    "Kirjauspäivä": "27.02.2026",
    "Arvopäivä": "27.02.2026",
    "Määrä EUROA": "+17,39",
    "Laji": 710,
    "Selitys": "ARVOPAPERIT",
    "Saaja/Maksaja": "OUTLIERX OY",
    "Saajan tilinumero ja pankin BIC": " ",
    "Viite": float("nan"),
    "Viesti": TRANSACTION_DETAIL_USD,
    "Arkistointitunnus": "2602275OMH00001897",
}])


def test_withholding_tax():
    assert DividendIncomeInCent(transactions=SIRIUSXM_USD_ROW).withholding_tax() == 307



def test_gross_value():
    assert DividendIncomeInCent(transactions=SIRIUSXM_USD_ROW).gross_value() == 2046
