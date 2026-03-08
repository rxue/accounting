#!/usr/bin/env python3
"""Generate tax report as PDF using Typst."""

import argparse
from importlib.resources import files

import typst

from financialstatements.balance_sheet import BalanceSheetInCent
from financialstatements.csv_to_dataframe import read_csvs_to_dataframe
from financialstatements.cli import generate
from financialstatements.incomestatement.income_statement import IncomeStatementInCent

_INCOME_STATEMENT_TEMPLATE = files("financialstatements.pdfgeneration").joinpath("income_statement.typ")
_BALANCE_SHEET_TEMPLATE = files("financialstatements.pdfgeneration").joinpath("balance_sheet.typ")


def income_statement_pdf(income_statement: IncomeStatementInCent, output_path: str) -> None:
    def fmt_rows(items):
        return "\n".join(
            f'    [{label}], [{value_in_cents / 100:,.2f} EUR],'
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
    ])

    period = income_statement.period
    period_str = f"{period.start_date} – {period.end_date}"
    net_income = f"{income_statement.net_income() / 100:,.2f} EUR"
    source = _INCOME_STATEMENT_TEMPLATE.read_text(encoding="utf-8").format(
        period=period_str, income_rows=income_rows, expense_rows=expense_rows, net_income=net_income
    )
    typst.compile(source.encode(), output=output_path)


def balance_sheet_pdf(balance_sheet_in_cent: BalanceSheetInCent, output_path: str) -> None:
    def fmt_row(label, value_in_cents):
        return f'    [{label}], [{value_in_cents / 100:,.2f} EUR],'

    current_assets_rows = "\n".join([
        fmt_row("Cash", balance_sheet_in_cent.cash),
        fmt_row("Financial Securities", balance_sheet_in_cent.financial_securities),
    ])
    total_assets = f"{balance_sheet_in_cent.total_assets() / 100:,.2f} EUR"
    source = _BALANCE_SHEET_TEMPLATE.read_text(encoding="utf-8").format(
        as_of_date=balance_sheet_in_cent.date, current_assets_rows=current_assets_rows, total_assets=total_assets
    )
    typst.compile(source.encode(), output=output_path)
