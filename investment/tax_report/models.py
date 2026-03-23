from typing import NamedTuple
from datetime import date
import yaml

from investment.accounting.financialstatements.incomestatement.models import DividendPayment
from investment.tax_report.pdf.models import Period, FormGenConfig, FormCompulsoryFields


class Country(NamedTuple):
    isin_code:str
    name:str
    income_tax_name:str
    tax_withholding_rate: int = 15

class ConfigData(NamedTuple):
    company_name: str
    business_id: str
    software_name: str
    service_provider_id: str
    accounting_period: Period
    input_dir: str
    empty_form8a_pdf_path: str
    empty_form70_pdf_path: str
    output_dir: str
    def form8a_pdf_gen_config(self) -> FormGenConfig:
        return FormGenConfig(
            empty_form_pdf_path=self.empty_form8a_pdf_path,
            compulsory_fields=FormCompulsoryFields(
                service_provider_id=self.service_provider_id,
                software_name=self.software_name,
                software_id="",
                company_name=self.company_name,
                business_id=self.business_id,
                accounting_period=self.accounting_period),
            output_dir=self.output_dir,
            gen_file_name="form8a_",
        )

    def form70_pdf_gen_config(self) -> FormGenConfig:
        return FormGenConfig(
            empty_form_pdf_path=self.empty_form70_pdf_path,
            compulsory_fields=FormCompulsoryFields(
                service_provider_id=self.service_provider_id,
                software_name=self.software_name,
                software_id="",
                company_name=self.company_name,
                business_id=self.business_id,
                accounting_period=self.accounting_period),
            output_dir=self.output_dir,
            gen_file_name="form70_",
        )
    @classmethod
    def get_config(cls, config_yaml_path: str) -> "ConfigData":
        with open(config_yaml_path) as f:
            cfg = yaml.safe_load(f)
        return cls(
            company_name=cfg["company"]["name"],
            business_id=cfg["company"]["business_id"],
            software_name=cfg["software"],
            service_provider_id=cfg["service_provider_id"],
            accounting_period=Period(*[date.fromisoformat(d) for d in cfg["account_period"].split(":")]),
            input_dir=cfg["input_dir"],
            empty_form8a_pdf_path=cfg["empty_form8a_pdf_path"],
            empty_form70_pdf_path=cfg["empty_form70_pdf_path"],
            output_dir=cfg["output_dir"]
        )

class Money(NamedTuple):
    euros: str
    cents: str

    @classmethod
    def new(cls, value: float) -> "Money":
        total_cents = round(value * 100)
        return cls(euros=str(total_cents // 100), cents=str(total_cents % 100))