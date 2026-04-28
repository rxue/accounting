import sys
from investment.holdings.nordea_holdings_extractor import extract_from_excel
from investment.holdings.holdings_snapshot import HoldingsSnapshot

COMMANDS = ["extract_from_nordea_excel", "generate_holdings_snapshot"]

if len(sys.argv) < 2 or sys.argv[1] not in COMMANDS:
    print(f"Usage: python -m investment.holdings <command> [args]")
    print(f"Commands: {', '.join(COMMANDS)}")
    sys.exit(1)

command = sys.argv[1]

if command == "extract_from_nordea_excel":
    if len(sys.argv) != 3:
        print(f"Usage: python -m investment.holdings extract_from_nordea_excel <excel_file>")
        sys.exit(1)
    holdings = extract_from_excel(sys.argv[2])
    for h in holdings:
        print(h)

elif command == "generate_holdings_snapshot":
    if len(sys.argv) != 3:
        print(f"Usage: python -m investment.holdings generate_holdings_snapshot <excel_file>")
        sys.exit(1)
    snapshot = HoldingsSnapshot.generate_snapshot(sys.argv[2])
    print(snapshot)
