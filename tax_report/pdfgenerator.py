#!/usr/bin/env python3
"""Generate tax report as PDF using Typst."""

import argparse

import typst

from tax_report.csv_to_dataframe import read_csvs_to_dataframe
from tax_report.generation import TaxReport, TaxReportItemsInCent


def _build_typst_source(report: TaxReportItemsInCent) -> bytes:
    """Build Typst markup from tax report items.

    Args:
        report: TaxReportItemsInCent containing the calculated tax figures.

    Returns:
        Typst source as bytes.
    """
    items = [
        ("Business Income", report.business_income),
        ("Business Expense", report.business_expense),
        ("Cash", report.cash),
        ("Financial Asset", report.financial_asset),
    ]

    rows = "\n".join(
        f'    [{ label }], [{ value_in_cents / 100:,.2f} EUR],'
        for label, value_in_cents in items
    )

    source = f"""\
#set page(paper: "a4")
#set text(size: 12pt)

= Tax Report

#table(
  columns: 2,
  align: (left, right),
  stroke: none,
  table.header([*Item*], [*Amount*]),
{rows}
)
"""
    return source.encode()


def generate_tax_report_pdf(report: TaxReportItemsInCent, output_path: str) -> None:
    """Generate a PDF file from tax report items.

    Args:
        report: TaxReportItemsInCent containing the calculated tax figures.
        output_path: File path for the generated PDF.
    """
    source = _build_typst_source(report)
    typst.compile(source, output=output_path)


def main():
    parser = argparse.ArgumentParser(
        description="Generate tax report as PDF from CSV files"
    )
    parser.add_argument("directory", help="Directory containing CSV files")
    parser.add_argument("-o", "--output", default="tax_report.pdf", help="Output PDF file path")
    args = parser.parse_args()

    df = read_csvs_to_dataframe(args.directory)
    report = TaxReport(df).calculate_items()
    generate_tax_report_pdf(report, args.output)
    print(f"PDF generated: {args.output}")


if __name__ == "__main__":
    main()
