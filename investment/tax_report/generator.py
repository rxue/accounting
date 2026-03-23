import argparse
from pathlib import Path
from investment import accounting
from investment.accounting.csv_to_dataframe import read_csvs_to_dataframe
from investment.tax_report.models import Country, ConfigData
from investment.accounting.financialstatements.pdf.generator import income_statement_pdf, balance_sheet_pdf
from investment.tax_report.pdf.generator import generate_pdf_forms

def main():
    parser = argparse.ArgumentParser(description="Generate tax report")
    parser.add_argument("command", help="Command to run (e.g. pdf)")
    parser.add_argument("config", help="Path to YAML config file")
    args = parser.parse_args()

    config = ConfigData.get_config(args.config)
    generate_pdf = args.command == "pdf"

    output_dir = config.output_dir
    Path(output_dir).mkdir(parents=True, exist_ok=True)

    df = read_csvs_to_dataframe(config.input_dir)
    end_date = config.accounting_period.end
    income_statement, balance_sheet, holdings = accounting.generator.generate(df, end_date=end_date)

    if generate_pdf:
        income_statement_pdf(income_statement, f"{output_dir}/income_statement.pdf", config.company_name)
        balance_sheet_pdf(balance_sheet, f"{output_dir}/balance_sheet.pdf", config.company_name)
        generate_pdf_forms(config.form8a_pdf_gen_config(), holdings, True)
        generate_pdf_forms(config.form70_pdf_gen_config(), income_statement.dividend_payments(), True)
    print("Required forms in tax report generated")