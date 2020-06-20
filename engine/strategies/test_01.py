import numpy as np
from engine.strategy import Strategy


class MovingAverageCrossStrategy(Strategy):

    def __init__(self, bars, events, portfolio):
        super().__init__(bars, events, portfolio)
        self.strategy_name = 'ma_cross'
        self.short_window = 10
        self.long_window = 100
        self.bought = self._calculate_initial_bought()

    
