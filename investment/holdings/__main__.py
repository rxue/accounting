import sys
from investment.holdings.nordea_holdings_extractor import extract_from_excel
from investment.holdings.nordea_holdings_snapshot import HoldingsSnapshot

EXTRACT = "extract_from_nordea_excel"

COMMANDS = [EXTRACT, "generate_holdings_snapshot"]

if len(sys.argv) < 2 or sys.argv[1] not in COMMANDS:
    print(f"Usage: python -m investment.holdings <command> [args]")
    print(f"Commands: {', '.join(COMMANDS)}")
    sys.exit(1)

command = sys.argv[1]

if command == EXTRACT:
    if len(sys.argv) != 3:
        print(f"Usage: python -m investment.holdings extract_nordea_excel <excel_file>")
        sys.exit(1)
    holdings = extract_from_excel(sys.argv[2])
    for h in holdings:
        print(h)

elif command == "generate_holdings_snapshot":
    if len(sys.argv) != 3:
        print(f"Usage: python -m investment.holdings generate_holdings_snapshot <excel_file>")
        sys.exit(1)
    snapshot, companies_failed_to_get_price = HoldingsSnapshot.generate_snapshot(sys.argv[2])
    print("Bank: ", snapshot.bank)
    for h in snapshot.holdings:
        print(f"{h}")
    print()
    if len(companies_failed_to_get_price) > 0:
        print("The following companies failed to get prices")
        print(companies_failed_to_get_price)