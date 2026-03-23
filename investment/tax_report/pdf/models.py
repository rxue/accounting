from dataclasses import dataclass, field
from datetime import date, datetime
from typing import NamedTuple

class Period(NamedTuple):
    start:date
    end:date
    def start_date_string(self):
        return self.start.strftime("%d%m%Y")
    def end_date_string(self):
        return self.end.strftime("%d%m%Y")
    def to_form8a_string(self):
        return f"{self.start_date_string()}-{self.end_date_string()}"

@dataclass(frozen=True)
class FormCompulsoryFields:
    service_provider_id: str
    software_name: str
    software_id: str
    company_name: str
    business_id: str
    accounting_period: Period
    timestamp: str = field(default_factory=lambda: datetime.now().strftime("%Y%m%d%H%M%S"))

class FormGenConfig(NamedTuple):
    empty_form_pdf_path:str
    compulsory_fields: FormCompulsoryFields
    output_dir: str
    gen_file_name: str
    def output_file_path(self, file_name_suffix:int):
        return self.output_dir + "/" + self.gen_file_name + str(file_name_suffix) + ".pdf"