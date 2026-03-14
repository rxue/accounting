from datetime import date

import pandas as pd

from investment.accounting.financialstatements.incomestatement.models import DividendPayment

def test_from_transaction():
    transaction_message = (
        " OP Säilytys Oy                     SIRIUSXM HOLDINGS                  "
        "US8299331004                       Osinkotuotto                       "
        "Osinko        0,27          USD/KplOmistettu määrä             90Kpl  "
        "Tuoton määrä               24,30USDLähdevero  US15,0   %       3,65USD"
        "Veroero                     0,01USDVal.kurssi                1,1876"
    )
    row = pd.Series({"Arvopäivä": "14.03.2026", "Määrä EUROA": "5,94", "Viesti": transaction_message})
    payment = DividendPayment.from_transaction(row)

    assert payment.value_date == date(2026, 3, 14)
    assert payment.company_name == "SIRIUSXM HOLDINGS"
    assert payment.source_currency == "USD"
    assert payment.net_value_in_eur == 5.94
    assert payment.shares_owned == 90
    assert payment.dividend_per_share == 0.27
    assert payment.gross_income == 24.30
    assert payment.withholding_tax == 3.65
    assert payment.exchange_rate == 1.1876

def test_from_transaction_from_canada():
    transaction_message = (
        " OP Säilytys Oy                     TELUS CORP                         "
        "CA87971M1032                       Osinkotuotto                       "
        "Osinko        0,4184        CAD/KplOmistettu määrä             50Kpl  "
        "Tuoton määrä               20,92CADLähdevero  CA15,0   %       3,14CAD"
        "Val.kurssi                1,6188"
    )
    transaction_row = pd.Series({"Arvopäivä": "12.01.2026", "Määrä EUROA": "10,98", "Viesti": transaction_message})
    payment = DividendPayment.from_transaction(transaction_row)

    assert payment.value_date == date(2026, 1, 12)
    assert payment.company_name == "TELUS CORP"
    assert payment.net_value_in_eur == 10.98
    assert payment.source_currency == "CAD"
    assert payment.shares_owned == 50
    assert payment.dividend_per_share == 0.4184
    assert payment.gross_income == 20.92
    assert payment.withholding_tax == 3.14
    assert payment.exchange_rate == 1.6188
