from engine.backtest import Backtest
from engine.data import DataBaseDataHandler
from engine.execution import SimulatedExecutionHandler
from engine.portfolio import NaivePortfolio


def run_backtest(strategy, config):
    """进行回测
    """
    backtest = Backtest(config['symbol_list'],
                        config['init_cash'],
                        config['start'],
                        config['end'],
                        DataBaseDataHandler,
                        SimulatedExecutionHandler,
                        NaivePortfolio,
                        strategy)
    return backtest.simulate_trading()
