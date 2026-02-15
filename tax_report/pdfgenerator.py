#!/usr/bin/env python3
"""Generate tax report as PDF."""

from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas

import argparse

from tax_report.csv_to_dataframe import read_csvs_to_dataframe
from tax_report.generation import TaxReport, TaxReportItemsInCent


def generate_tax_report_pdf(report: TaxReportItemsInCent, output_path: str) -> None:
    """Generate a PDF file from tax report items.

    Args:
        report: TaxReportItemsInCent containing the calculated tax figures.
        output_path: File path for the generated PDF.
    """
    c = canvas.Canvas(output_path, pagesize=A4)
    width, height = A4

    c.setFont("Helvetica-Bold", 18)
    c.drawString(50, height - 50, "Tax Report")

    c.setFont("Helvetica", 12)
    y = height - 100

    items = [
        ("Business Income", report.business_income),
        ("Business Expense", report.business_expense),
        ("Cash", report.cash),
        ("Financial Asset", report.financial_asset),
    ]

    for label, value_in_cents in items:
        euros = value_in_cents / 100
        c.drawString(50, y, f"{label}: {euros:,.2f} EUR")
        y -= 30

    c.save()


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
