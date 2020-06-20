from engine.strategy import Strategy


class BuyAndHoldStrategy(Strategy):
    def __init__(self, bars, events, portfolio):
        super().__init__(bars, events, portfolio)
        self.strategy_name = 'buy_and_hold'
        self.bought = dict([(symbol, False) for symbol in self.symbol_list])

    def handle_bar(self):
        for s in self.symbol_list:
            if self.bought[s] is False:
                self.order_shares(s, 10)
                self.bought[s] = True
