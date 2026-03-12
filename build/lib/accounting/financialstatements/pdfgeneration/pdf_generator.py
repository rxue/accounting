#!/usr/bin/env python3
"""Generate tax report as PDF using Typst."""

from importlib.resources import files

import typst

from accounting.financialstatements.balance_sheet import BalanceSheetInCent
from accounting.financialstatements.incomestatement.income_statement import IncomeStatementInCent

_INCOME_STATEMENT_TEMPLATE = files("accounting.financialstatements.pdfgeneration").joinpath("income_statement.typ")
_BALANCE_SHEET_TEMPLATE = files("accounting.financialstatements.pdfgeneration").joinpath("balance_sheet.typ")


def income_statement_pdf(income_statement: IncomeStatementInCent, output_path: str, company_name: str = "") -> None:
    def fmt_rows(items, negate=False):
        sign = "-" if negate else ""
        return "\n".join(
            f'    [{label}], [{sign}{value_in_cents / 100:,.2f} EUR],'
            for label, value_in_cents in items
        )

    income_rows = fmt_rows([
        ("Gross Dividend Income", income_statement.gross_dividend_income),
        ("Trading Income", income_statement.trading_income),
    ])
    expense_rows = fmt_rows([
        ("Foreign Withholding Tax", income_statement.expenses.foreign_withholding_tax),
        ("Salaries and Wages", income_statement.expenses.salaries_and_wages),
        ("Service Expense", income_statement.expenses.service_expense),
        ("Other Expense", income_statement.expenses.other_expense),
    ], negate=True)

    period = income_statement.period
    period_str = f"{period.start_date} – {period.end_date}"
    net_income = f"{income_statement.net_income() / 100:,.2f} EUR"
    source = _INCOME_STATEMENT_TEMPLATE.read_text(encoding="utf-8").format(
        company_name=company_name, period=period_str, income_rows=income_rows, expense_rows=expense_rows, net_income=net_income
    )
    typst.compile(source.encode(), output=output_path)


def balance_sheet_pdf(balance_sheet_in_cent: BalanceSheetInCent, output_path: str, company_name: str = "") -> None:
    def fmt_row(label, value_in_cents):
        return f'    [{label}], [{value_in_cents / 100:,.2f} EUR],'

    current_assets_rows = "\n".join([
        fmt_row("Cash", balance_sheet_in_cent.cash),
        fmt_row("Financial Securities", balance_sheet_in_cent.financial_securities),
    ])
    current_assets = f"{balance_sheet_in_cent.current_assets() / 100:,.2f} EUR"
    total_assets = f"{balance_sheet_in_cent.total_assets() / 100:,.2f} EUR"
    source = _BALANCE_SHEET_TEMPLATE.read_text(encoding="utf-8").format(
        company_name=company_name, as_of_date=balance_sheet_in_cent.date, current_assets_rows=current_assets_rows,
        current_assets=current_assets, total_assets=total_assets
    )
    typst.compile(source.encode(), output=output_path)
