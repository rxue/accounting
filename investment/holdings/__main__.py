import sys
import pandas as pd
from investment.holdings.nordea_holdings_extractor import extract_from
from investment.holdings.holdings_snapshot import HoldingsSnapshot
from investment.holdings.nordea_tradings_extractor import extract
from investment.holdings.return_calculation import calculate_total_return


EXTRACT_HOLDINGS = "extract_from_nordea_excel"
EXTRACT_RETURN_BREAKDOWN = "extract_return_breakdown_from_nordea_pdf"
TOTAL_RETURN = "total_return"
GENERATE_HOLDINGS_SNAPSHOT = "generate_holdings_snapshot"

COMMANDS = [EXTRACT_HOLDINGS, EXTRACT_RETURN_BREAKDOWN, TOTAL_RETURN, GENERATE_HOLDINGS_SNAPSHOT]

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

elif command == EXTRACT_RETURN_BREAKDOWN:
    if len(sys.argv) != 3:
        print(f"Usage: python -m investment.holdings {EXTRACT_RETURN_BREAKDOWN} <pdf_file>")
        sys.exit(1)
    return_breakdown = extract(sys.argv[2])
    print(f"capital gain: {return_breakdown.total_capital_gain_in_cent()/100}")
    print(f"capital loss: {return_breakdown.total_capital_loss_in_cent()/100}")
elif command == TOTAL_RETURN:
    if len(sys.argv) != 3:
        print(f"Usage: python -m investment.holdings {TOTAL_RETURN} <pdf_dir>")
        sys.exit(1)
    print(calculate_total_return(sys.argv[2]))

elif command == GENERATE_HOLDINGS_SNAPSHOT:
    if len(sys.argv) != 3:
        print(f"Usage: python -m investment.holdings generate_holdings_snapshot <excel_file>")
        sys.exit(1)
    snapshot, companies_failed_to_get_price = HoldingsSnapshot.generate(sys.argv[2])
    print("Bank: ", snapshot.bank)
    holdings_snapshot_df = snapshot.to_dataframe()
    holdings_snapshot_df["daily_change"] = holdings_snapshot_df["daily_change"].map(lambda x: f"{x*100:+.2f}%")
    holdings_snapshot_df["dividend_yield"] = holdings_snapshot_df["dividend_yield"].map(lambda x: f"{x:.2f}%" if not pd.isna(x) else "N/A")
print(holdings_snapshot_df)