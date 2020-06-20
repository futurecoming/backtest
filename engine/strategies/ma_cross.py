import numpy as np
from engine.strategy import Strategy


class MovingAverageCrossStrategy(Strategy):

    def __init__(self, bars, events, portfolio):
        super().__init__(bars, events, portfolio)
        self.strategy_name = 'ma_cross'
        self.short_window = 10
        self.long_window = 100
        self.bought = self._calculate_initial_bought()

    def _calculate_initial_bought(self):
        bought = {}
        for s in self.symbol_list:
            bought[s] = 'OUT'
        return bought

    def handle_bar(self):
        for symbol in self.symbol_list:
            bars = self.bars.get_latest_bars_values(
                symbol, "close", N=self.long_window)
            if bars is not None and bars != []:
                short_sma = np.mean(bars[-self.short_window:])
                long_sma = np.mean(bars[-self.long_window:])

                if short_sma > long_sma and self.bought[symbol] == "OUT":
                    self.order_percent(symbol, 0.1, 'LONG')
                    self.bought[symbol] = 'LONG'

                elif short_sma < long_sma and self.bought[symbol] == "LONG":
                    self.order_percent(symbol, 0.1, 'SHORT')
                    self.bought[symbol] = 'OUT'
