import sys
from investment.holdings.company.repository import find_companies_by_name

COMMANDS = ["find_companies_by_isin"]

if len(sys.argv) < 2 or sys.argv[1] not in COMMANDS:
    print(f"Usage: python -m investment.company <command> [args]")
    print(f"Commands: {', '.join(COMMANDS)}")
    sys.exit(1)

command = sys.argv[1]

if command == "find_companies_by_isin":
    if len(sys.argv) != 3:
        print("Usage: python -m investment.company find_companies_by_isin <isin1,isin2,...>")
        sys.exit(1)
    isins = sys.argv[2].split(",")
    companies = find_companies_by_name(*isins)
    for c in companies:
        print(c)
