from engine.strategy import Strategy


class BuyAndHoldStrategy(Strategy):
    def __init__(self, bars, events, portfolio):
        super().__init__(bars, events, portfolio)
        self.strategy_name = 'buy_and_hold'
        self.bought = dict([(symbol, False) for symbol in self.symbol_list])

 
