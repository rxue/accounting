import pandas as pd

from accounting.financialstatements.balance_sheet import BalanceSheetInCent
from accounting.financialstatements.incomestatement.income_statement import IncomeStatementInCent


def reconcile(cash_infusion_df: pd.DataFrame, income_statement: IncomeStatementInCent, balance_sheet: BalanceSheetInCent) -> bool:
    cash_infused = round(cash_infusion_df["Määrä EUROA"].str.replace(",", ".").astype(float).sum() * 100)
    return cash_infused + income_statement.net_income() == balance_sheet.cash + balance_sheet.financial_securities



