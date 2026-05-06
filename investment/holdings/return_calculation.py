from investment.holdings.model import NordeaTradingLot


class ReturnBreakdown:
    def __init__(self, trading_lots: list[NordeaTradingLot]):
        self.trading_lots = trading_lots

    def _net_result_per_group_in_cent(self) -> list[int]:
        results = []
        group_total = None
        for lot in self.trading_lots:
            if lot.action == "Withdrawal":
                if group_total is not None:
                    results.append(round(group_total * 100))
                group_total = lot.trade_price - lot.charge
            else:
                group_total -= lot.trade_price + lot.charge
        if group_total is not None:
            results.append(round(group_total * 100))
        return results

    def total_capital_gain_in_cent(self) -> int:
        return sum(r for r in self._net_result_per_group_in_cent() if r > 0)

    def total_capital_loss_in_cent(self) -> int:
        return sum(-r for r in self._net_result_per_group_in_cent() if r < 0)


class ReturnCalculator:
    def __init__(self, trading_lots: list[ReturnBreakdown]):
        self.return_breakdowns =trading_lots

    def total_return(self) -> int:
        return sum(rb.total_capital_gain_in_cent() - rb.total_capital_loss_in_cent() for rb in self.return_breakdowns)

def calculate_total_return(input_dir: str) -> float:
    import os
    from investment.holdings.nordea_trading_lots_extractor import extract
    breakdowns = []
    for filename in sorted(os.listdir(input_dir)):
        if filename.endswith('.pdf'):
            breakdowns.append(extract(os.path.join(input_dir, filename)))
    return ReturnCalculator(breakdowns).total_return() / 100