import sys
from investment.data_extract.nordea_holdings_extractor import extract_from_excel

if len(sys.argv) != 2:
    print(f"Usage: python -m investment.data_extract <excel_file>")
    sys.exit(1)

holdings = extract_from_excel(sys.argv[1])
for h in holdings:
    print(h)
