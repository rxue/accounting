import sys
from investment.holdings.nordea_holdings_extractor import extract_from
from investment.holdings.holdings_snapshot import HoldingsSnapshot
from investment.holdings.nordea_tradings_extractor import extract as extract_tradings

EXTRACT_HOLDINGS = "extract_from_nordea_excel"
EXTRACT_TRADINGS = "extract_tradings_from_nordea_pdf"

COMMANDS = [EXTRACT_HOLDINGS, "generate_holdings_snapshot", EXTRACT_TRADINGS]

if len(sys.argv) < 2 or sys.argv[1] not in COMMANDS:
    print(f"Usage: python -m investment.holdings <command> [args]")
    print(f"Commands: {', '.join(COMMANDS)}")
    sys.exit(1)

command = sys.argv[1]

if command == EXTRACT_HOLDINGS:
    if len(sys.argv) != 3:
        print(f"Usage: python -m investment.holdings extract_nordea_excel <excel_file>")
        sys.exit(1)
    holdings = extract_from(sys.argv[2])
    for h in holdings:
        print(h)

elif command == EXTRACT_TRADINGS:
    if len(sys.argv) != 3:
        print(f"Usage: python -m investment.holdings {EXTRACT_TRADINGS} <pdf_file>")
        sys.exit(1)
    for trading in extract_tradings(sys.argv[2]):
        print(trading)

elif command == "generate_holdings_snapshot":
    if len(sys.argv) != 3:
        print(f"Usage: python -m investment.holdings generate_holdings_snapshot <excel_file>")
        sys.exit(1)
    snapshot, companies_failed_to_get_price = HoldingsSnapshot.generate(sys.argv[2])
    print("Bank: ", snapshot.bank)
    print(snapshot.to_dataframe())