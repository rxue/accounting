import re
from datetime import datetime
from typing import get_args

import pdfplumber

from investment.holdings.models import Action, TradingLot
from investment.holdings.return_calculation import ReturnBreakdown

_TRANSACTION_RE = re.compile(
    r'(' + '|'.join(get_args(Action)) + r')\s+(\d{2}\.\d{2}\.\d{2})\s+(\d+)\s+([\d,]+)\s+([\d,]+)'
)
_COMPANY_RE = re.compile(r'^[A-Z][A-Z &.\-]+$')

#ai-generated
def extract(pdf_file_path: str) -> ReturnBreakdown:
    tradings = []
    current_company = None
    with pdfplumber.open(pdf_file_path) as pdf:
        for page in pdf.pages:
            for line in page.extract_text().splitlines():
                line = line.strip()
                if _COMPANY_RE.match(line):
                    current_company = line
                    continue
                m = _TRANSACTION_RE.search(line)
                if m and current_company:
                    action, date_str, amount, trade_price_str, charge_str = m.groups()
                    tradings.append(TradingLot(
                        company_name=current_company,
                        action=action,
                        date=datetime.strptime(date_str, "%d.%m.%y").date(),
                        amount=int(amount),
                        trade_price=float(trade_price_str.replace(",", ".")),
                        charge=float(charge_str.replace(",", ".")),
                    ))
    return ReturnBreakdown(tradings)