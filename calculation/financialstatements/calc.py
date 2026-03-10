from dataclasses import dataclass

import pandas as pd

from calculation.profit_calculation import Lot, ProfitCalculationResult, calculate_profit_by_symbol, calculate_trading_profit_in_fifo, transfer_transactions_to_lots


@dataclass
class Period:
    start_date: str
    end_date: str


def reconcile(cash_infusion_df: pd.DataFrame, income_statement: "IncomeStatementInCent", balance_sheet: "BalanceSheetInCent") -> bool:
    from calculation.financialstatements.incomestatement.income_statement import IncomeStatementInCent
    from calculation.financialstatements.balance_sheet import BalanceSheetInCent
    cash_infused = round(cash_infusion_df["Määrä EUROA"].str.replace(",", ".").astype(float).sum() * 100)
    return cash_infused + income_statement.net_income() == balance_sheet.cash + balance_sheet.financial_securities


def get_period(df: pd.DataFrame) -> Period:
    import calendar
    dates = pd.to_datetime(df["Kirjauspäivä"], format="%d.%m.%Y")
    first = dates.min()
    last = dates.max()
    start_date = first.replace(day=1).strftime("%Y-%m-%d")
    last_day = calendar.monthrange(last.year, last.month)[1]
    end_date = last.replace(day=last_day).strftime("%Y-%m-%d")
    return Period(start_date=start_date, end_date=end_date)


