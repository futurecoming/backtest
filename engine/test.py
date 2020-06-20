from engine.api import run_backtest
from engine.strategies.ma_cross import MovingAverageCrossStrategy
from engine.strategies.buy_and_hold import BuyAndHoldStrategy


if __name__ == "__main__":
    run_backtest(MovingAverageCrossStrategy, {
        'symbol_list': ['AU', 'AL', 'CU'],
        'init_cash': 100000000.0,
        'start': '2015-04-08',
        'end': '2017-10-27'
    })
