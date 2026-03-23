from pathlib import Path

import PyPDF2

from investment.tax_report.pdf.models import FormGenConfig

from datetime import date, timedelta
from typing import TypeVar

from investment.accounting.financialstatements.incomestatement.models import DividendPayment
from investment.accounting.models import Holding
from investment.market_quote.repository import find_company_by_op_symbol, find_closing_price_by_symbol
from investment.tax_report.pdf.finder import find_compulsory_fields, find_code, find_withholding_tax_name
from investment.tax_report.models import FormCompulsoryFields, Money

def _fill_compulsory_fields_without_accounting_period(compulsory_fields: FormCompulsoryFields) -> dict[str, str]:
    compulsory_fields_spec = find_compulsory_fields()
    compulsory_key_value_pair_result = {}
    for field_spec in compulsory_fields_spec:
        code = field_spec["Code"]
        allowed_value = field_spec["Allowed values"]
        if isinstance(allowed_value, str):
            compulsory_key_value_pair_result[code] = allowed_value
        elif field_spec["Description"] == "Service provider's ID code":
            compulsory_key_value_pair_result[code] = compulsory_fields.service_provider_id
        elif field_spec["Description"] == "Software that generated the file":
            compulsory_key_value_pair_result[code] = compulsory_fields.software_name
        elif field_spec["Description"] == "Identifier of the software that generated the file":
            compulsory_key_value_pair_result[code] = compulsory_fields.software_id
        elif field_spec["Description"] == "Business ID of limited company":
            compulsory_key_value_pair_result[code] = compulsory_fields.business_id
    return compulsory_key_value_pair_result

T = TypeVar("T")

def to_form_pdf_input(compulsory_fields: FormCompulsoryFields, input:list[T]) -> list[dict[str,str]]:
    if not input:
        return []
    if isinstance(input[0], Holding):
        return to_form8a_pdf_input(input, compulsory_fields)
    if isinstance(input[0], DividendPayment):
        return to_form70_pdf_input(input, compulsory_fields)
    raise ValueError(f"Unsupported input type: {type(input[0])}")

def _to_money(val: float) -> Money:
    return Money.new(val)

def to_form8a_pdf_input(holdings:list[Holding], compulsory_fields: FormCompulsoryFields) -> list[dict[str, str]]:
    compulsory_fields_input = _fill_compulsory_fields_without_accounting_period(compulsory_fields)
    accounting_period_code = find_code("Accounting period")
    accounting_period = compulsory_fields.accounting_period
    compulsory_fields_input[accounting_period_code + "_1"] = accounting_period.start_date_string()
    compulsory_fields_input[accounting_period_code + "_2"] = accounting_period.end_date_string()
    def backtrack_to_work_date(d: date) -> date:
        while d.weekday() > 4:
            d -= timedelta(days=1)
        return d

    pdf_input_batch = []
    current_pdf_input = compulsory_fields_input.copy()
    counter = 1
    for holding in holdings:
        section = "Financial assets (Business Tax Act (EVL))"
        company = find_company_by_op_symbol(holding.symbol)
        suffix = ";" + str(counter)
        current_pdf_input[find_code(section=section,
                            description="Complete name of limited company or cooperative / Financial assets") + suffix] = company.short_name
        current_pdf_input[find_code(section=section, description="Business ID") + suffix] = "0000000-0"
        current_pdf_input[find_code(section=section, description="Quantity, pcs / Financial assets") + suffix] = str(holding.quantity)
        acquisition_cost_code = find_code(section=section,
                         description="Undepreciated acquisition cost for income tax purposes / Financial assets")
        acquisition_cost = _to_money(holding.book_value)
        current_pdf_input[acquisition_cost_code + suffix] = acquisition_cost.euros
        current_pdf_input["s" + acquisition_cost_code + suffix] = acquisition_cost.cents
        price = find_closing_price_by_symbol(company, backtrack_to_work_date(compulsory_fields.accounting_period.end))
        comparison_value_per_unit = round(price.price_in_eur() * 0.7, 2)
        comparison_value_per_unit_code = find_code(section=section, description="Comparison value of each / Financial assets")
        comparison_value_per_unit_m = _to_money(comparison_value_per_unit)
        current_pdf_input[comparison_value_per_unit_code + suffix] = comparison_value_per_unit_m.euros
        current_pdf_input["s" + comparison_value_per_unit_code + suffix] = comparison_value_per_unit_m.cents
        comparison_value_code = find_code(section=section, description="Comparison value, totals / Financial assets")
        comparison_value_m = _to_money(comparison_value_per_unit * holding.quantity)
        current_pdf_input[comparison_value_code + suffix] = comparison_value_m.euros
        current_pdf_input["s" + comparison_value_code + suffix] = comparison_value_m.cents
        if counter % 2 == 0:
            counter = 0
            pdf_input_batch.append(current_pdf_input)
            current_pdf_input = compulsory_fields_input.copy()
        counter = counter + 1
    return pdf_input_batch

def to_form70_pdf_input(dividend_payments:list[DividendPayment], compulsory_fields: FormCompulsoryFields) -> list[dict[str, str]]:

    header = {
        "020": compulsory_fields.company_name,
        "010": compulsory_fields.business_id,
        "054_1": compulsory_fields.accounting_period.start_date_string(),
        "054_2": compulsory_fields.accounting_period.end_date_string(),
    }

    pdf_input_batch = []
    current_pdf_input = header.copy()
    counter = 1
    total_tax_in_eur = 0.0
    for payment in dividend_payments:
        suffix = ";" + str(counter)
        current_pdf_input["245" + suffix] = payment.company.country_code
        current_pdf_input["200" + suffix] = "1"
        current_pdf_input["204" + suffix] = find_withholding_tax_name(payment.company.country_code)
        current_pdf_input["207" + suffix] = payment.value_date.strftime("%d%m%Y")
        current_pdf_input["205" + suffix] = str(payment.witholding_tax_rate)
        current_pdf_input["208" + suffix] = str(payment.exchange_rate)
        gross_income_m = _to_money(payment.gross_value_in_eur)
        current_pdf_input["201" + suffix] = gross_income_m.euros
        current_pdf_input["s201" + suffix] = gross_income_m.cents
        net_income_m = _to_money(payment.net_value_in_eur)
        current_pdf_input["203" + suffix] = net_income_m.euros
        current_pdf_input["s203" + suffix] = net_income_m.cents
        foreign_tax_m = _to_money(payment.withholding_tax_in_eur)
        current_pdf_input["206" + suffix] = foreign_tax_m.euros
        current_pdf_input["s206" + suffix] = foreign_tax_m.cents
        current_pdf_input["209" + suffix] = foreign_tax_m.euros
        current_pdf_input["s209" + suffix] = foreign_tax_m.cents
        current_pdf_input["211" + suffix] = "1"
        total_tax_in_eur += payment.withholding_tax_in_eur
        if counter % 2 == 0:
            counter = 0
            total_m = _to_money(total_tax_in_eur)
            current_pdf_input["551;1"] = total_m.euros
            current_pdf_input["s551;1"] = total_m.cents
            pdf_input_batch.append(current_pdf_input)
            current_pdf_input = header.copy()
            total_tax_in_eur = 0.0
        counter = counter + 1
    return pdf_input_batch

def _set_checkbox_option(writer: PyPDF2.PdfWriter, page_idx: int, field_name: str, option_value: int) -> None:
    page = writer.pages[page_idx]
    if '/Annots' not in page:
        return
    matching_kids = [
        annot_ref.get_object()
        for annot_ref in page['/Annots']
        if (parent := annot_ref.get_object().get('/Parent')) is not None
        and parent.get_object().get('/T') == field_name
    ]
    #if option_name.isdigit():
    kid = matching_kids[option_value - 1]
    ap_n = kid.get('/AP', {}).get('/N', {})
    on_key = next((k for k in ap_n if k != '/Off'), None)
    if on_key:
        kid[PyPDF2.generic.NameObject('/AS')] = PyPDF2.generic.NameObject(on_key)
        kid[PyPDF2.generic.NameObject('/V')] = PyPDF2.generic.NameObject(on_key)

def fill_form_pdf(input:dict[str,str], form_pdf_path: str, output_path: str) -> None:
    path = Path(form_pdf_path)
    reader = PyPDF2.PdfReader(open(path, "rb"))
    fields = reader.get_fields() or {}
    btn_fields = {k: v for k, v in input.items() if fields.get(k, {}).get('/FT') == '/Btn'}
    text_fields = {k: v for k, v in input.items() if k not in btn_fields}
    writer = PyPDF2.PdfWriter()
    writer.append(reader)
    writer.update_page_form_field_values(writer.pages[0], text_fields)
    for field_name, option_value in btn_fields.items():
        _set_checkbox_option(writer, 0, field_name, int(option_value))
    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, "wb") as f:
        writer.write(f)

def generate_pdf_forms(pdf_form_gen_config:FormGenConfig, input:list[T], combine: bool = False):
    pdf_form_input_list = to_form_pdf_input(pdf_form_gen_config.compulsory_fields, input)
    idx = 0
    output_paths = []
    for pdf_input in pdf_form_input_list:
        output_path = pdf_form_gen_config.output_file_path(idx)
        fill_form_pdf(pdf_input, pdf_form_gen_config.empty_form_pdf_path, output_path)
        output_paths.append(output_path)
        idx = idx + 1

    def combine_pdfs(input_file_paths:str, combined_path:str):
        writer = PyPDF2.PdfWriter()
        for path in input_file_paths:
            writer.append(PyPDF2.PdfReader(open(path, "rb")))
        src_root = PyPDF2.PdfReader(open(input_file_paths[0], "rb")).trailer['/Root'].get_object()
        src_acroform = src_root.get('/AcroForm')
        new_af = PyPDF2.generic.DictionaryObject()
        if src_acroform:
            for key, val in src_acroform.get_object().items():
                if key != '/Fields':
                    new_af[key] = val
        new_af[PyPDF2.generic.NameObject('/NeedAppearances')] = PyPDF2.generic.BooleanObject(True)
        new_af[PyPDF2.generic.NameObject('/Fields')] = PyPDF2.generic.ArrayObject()
        writer._root_object[PyPDF2.generic.NameObject('/AcroForm')] = new_af
        with open(combined_path, "wb") as f:
            writer.write(f)

    if combine and output_paths:
        combine_pdfs(output_paths, pdf_form_gen_config.output_file_path("combined"))
        for path in output_paths:
            Path(path).unlink()

