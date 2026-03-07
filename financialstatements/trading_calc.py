from dataclasses import dataclass

import pandas as pd


@dataclass
class Lot:
    date: str
    type: str
    share_amount: int
    money_amount_in_cent: int

@dataclass
class ProfitCalculationResult:
    symbol: str
    profit_in_cent: int
    remaining_lots: list[Lot]


def transfer_transactions_to_lots(df: pd.DataFrame) -> list[Lot]:
    from financialstatements.transaction_filters import match_trading
    transactions = []
    for _, row in df.iterrows():
        viesti = row["Viesti"].strip()
        match = match_trading(viesti)
        if match:
            type_code = match.group(1)
            share_amount = int(match.group(3))
            transaction_type = "BUY" if type_code == "O" else "SELL"
            money_amount_in_cent = round(abs(float(row["Määrä EUROA"].replace(",", "."))) * 100)
            transactions.append(Lot(
                date=row["Kirjauspäivä"],
                type=transaction_type,
                share_amount=share_amount,
                money_amount_in_cent=money_amount_in_cent
            ))
    return transactions


def trading_profit_in_fifo(transactions: list[Lot]) -> tuple[int, list[Lot]]:
    buy_queue: list[tuple[str, int, int]] = []
    total_profit_cents = 0
    for tx in transactions:
        if tx.type == "BUY":
            buy_queue.append((tx.date, tx.share_amount, tx.money_amount_in_cent))
        elif tx.type == "SELL":
            sell_total_cents = tx.money_amount_in_cent
            shares_to_sell = tx.share_amount
            while shares_to_sell > 0 and buy_queue:
                buy_date, buy_shares, buy_total_cents = buy_queue[0]
                if buy_shares <= shares_to_sell:
                    sell_portion_cents = sell_total_cents * buy_shares // shares_to_sell
                    total_profit_cents += sell_portion_cents - buy_total_cents
                    sell_total_cents -= sell_portion_cents
                    shares_to_sell -= buy_shares
                    buy_queue.pop(0)
                else:
                    buy_portion_cents = buy_total_cents * shares_to_sell // buy_shares
                    total_profit_cents += sell_total_cents - buy_portion_cents
                    buy_queue[0] = (buy_date, buy_shares - shares_to_sell, buy_total_cents - buy_portion_cents)
                    shares_to_sell = 0
    remaining_lots = [Lot(date=date, type="BUY", share_amount=shares, money_amount_in_cent=cost_in_cents) for date, shares, cost_in_cents in buy_queue]
    return total_profit_cents, remaining_lots


def profit_and_book_values_by_symbol(stock_tradings_by_symbol: dict[str, pd.DataFrame]) -> list[ProfitCalculationResult]:
    result = []
    for symbol, symbol_df in stock_tradings_by_symbol.items():
        lots = transfer_transactions_to_lots(symbol_df)
        profit, remaining_lots = trading_profit_in_fifo(lots)
        result.append(ProfitCalculationResult(symbol=symbol, profit_in_cent=profit, remaining_lots=remaining_lots))
    return result
