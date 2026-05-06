import re
import sys
from datetime import datetime
from pathlib import Path

import pandas as pd

from investment.holdings.calculation.lots_matching import Action, Lot, fifo_lots_matching, Result
from investment.holdings.company.repository import find_company_name_by_symbol
from investment.holdings.model import Trading
from investment.holdings.models.holdings import Holding
from investment.holdings.op.repository import find_tradings
from investment.holdings.util import extract_csv

class OPTrading(Trading):
    def to_lot(self) -> Lot:
        return Lot(
            date=self.date,
            action=Action.BUY if self.action == "O" else Action.SELL,
            share_amount=self.amount,
            value_in_cent=self.trade_price
            )

def to_trading(row: pd.Series) -> Trading:
    match = re.match(r"^\s*([OM]):(.+?)\s*/(\d+)", row["Viesti"])
    action = match.group(1)
    ticker = match.group(2).strip()
    quantity = int(match.group(3))
    trade_date = datetime.strptime(row["Kirjauspäivä"], "%d.%m.%Y").date()
    trade_price = abs(float(row["Määrä EUROA"].replace(",", ".")))
    return OPTrading(
        company_identifier=ticker,
        action=action,
        date=trade_date,
        amount=quantity,
        trade_price=trade_price,
    )


def to_tradings_by_ticker_symbol(tradings: pd.DataFrame) -> dict[str, list[Trading]]:
    result: dict[str, list[Trading]] = {}
    for _, row in tradings.iterrows():
        trading = to_trading(row)
        result.setdefault(trading.company_identifier, []).append(trading)
    return result

def generate(csv_directory:str) -> tuple[list[Holding], list[str]]:
    transactions = extract_csv(path=csv_directory, sep=";", encoding="latin-1")
    tradings = find_tradings(transactions)
    lots_matching_result_by_company_symbol = {}
    for company_symbol, tradings in to_tradings_by_ticker_symbol(tradings).items():
        print(company_symbol)
        lots = [tr.to_lot() for tr in tradings]
        lots_matching_result_by_company_symbol[company_symbol] = fifo_lots_matching(lots)
    def to_holding(company_symbol:str,lots_matching_result:Result) -> Holding | None:
        company_name = find_company_name_by_symbol(company_symbol)
        if company_name is not None:
            print(f"found company {company_name}")
            return Holding(
                company_name=company_name,
                amount=sum(l.share_amount for l in lots_matching_result.remaining_lots))
        print(f"did not find company name for symbol: {company_symbol}")
        return None
    holdings = []
    missing_company_symbols = []
    for symbol, result in lots_matching_result_by_company_symbol.items():
        holding = to_holding(symbol, result)
        if holding is None:
            missing_company_symbols.append(symbol)
        else:
            holdings.append(holding)
    return holdings, missing_company_symbols



if __name__ == "__main__":
    if len(sys.argv) != 2:
        print(f"Usage: {Path(sys.argv[0]).name} <directory>")
        sys.exit(1)

    directory = sys.argv[1]
    holdings, missing_company_symbols = generate(sys.argv[1])
    print(holdings)
    print(missing_company_symbols)
