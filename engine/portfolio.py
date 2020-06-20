import pandas as pd
import matplotlib.pyplot as plt
from engine.event import OrderEvent
from abc import ABCMeta, abstractmethod
from utils.backtest_utils import create_sharpe_ratio, create_drawdowns, create_annualized_return


class Portfolio(object):
    __mateclass__ = ABCMeta

    @abstractmethod
    def update_signal(self, event):
        raise NotImplementedError("Should implement update_signal()")

    @abstractmethod
    def update_fill(self, event):
        raise NotImplementedError("Should implement update_fill()")


class NaivePortfolio(Portfolio):
    """
    Portfolio类包含所有资产的的仓位和市值。
    positions DataFrame存储着仓位数量的时间序列。
    holdings DataFrame存储现金和各个资产的市值，以及变化。
    """
    def __init__(self, bars, events, start_date, initial_capital=100000.0):
        """
        初始化bars、时间队列、初始资本。
        """
        self.bars = bars
        self.events = events
        self.symbol_list = self.bars.symbol_list
        self.start_date = start_date
        self.initial_capital = initial_capital
        self.all_positions = self.construct_all_positions()
        self.current_positions = dict((k, v) for k, v in [(s, 0) for s in self.symbol_list])
        self.all_holdings = self.construct_all_holdings()
        self.current_holdings = self.construct_current_holdings()

    def construct_all_positions(self):
        """
        构造仓位
        """
        d = dict((k, v) for k, v in [(s, 0) for s in self.symbol_list])
        d['datetime'] = self.start_date
        return [d]

    def construct_all_holdings(self):
        """
        构造持有资产
        """
        d = dict((k, v) for k, v in [(s, 0.0) for s in self.symbol_list])
        d['datetime'] = self.start_date
        d['cash'] = self.initial_capital  # 现金
        d['total'] = self.initial_capital
        return [d]

    def construct_current_holdings(self):

        d = dict((k, v) for k, v in [(s, 0.0) for s in self.symbol_list])
        d['cash'] = self.initial_capital
        d['total'] = self.initial_capital
        return d

    def update_timeindex(self):

        latest_datetime = self.bars.get_latest_bar_datetime(self.symbol_list[0])

        # 更新仓位
        dp = dict((k, v) for k, v in [(s, 0) for s in self.symbol_list])
        dp['datetime'] = latest_datetime

        for s in self.symbol_list:
            dp[s] = self.current_positions[s]

        # 添加当前仓位
        self.all_positions.append(dp)

        # 更新持仓
        dh = dict((k, v) for k, v in [(s, 0) for s in self.symbol_list])
        dh['datetime'] = latest_datetime
        dh['cash'] = self.current_holdings['cash']
        dh['total'] = self.current_holdings['cash']

        for s in self.symbol_list:
            market_value = self.current_positions[s] * self.bars.get_latest_bars(s)[0][3]
            dh[s] = market_value
            dh['total'] += market_value

        # 添加当前持仓
        self.all_holdings.append(dh)

    # ======================
    # FILL/POSITION HANDLING
    # ======================
    def update_positions_from_fill(self, fill):
        """根据成交单更新仓位
        """
        fill_dir = 0
        if fill.direction == 'BUY':
            fill_dir = 1
        if fill.direction == 'SELL':
            fill_dir = -1

        self.current_positions[fill.symbol] += fill_dir * fill.quantity

    def update_holdings_from_fill(self, fill):
        """Takes a Fill object and updates the holdings matrix to
        reflect the holdings value.

        Parameters:
        fill - The Fill object to update the holdings with.
        """
        fill_dir = 0
        if fill.direction == 'BUY':
            fill_dir = 1
        if fill.direction == 'SELL':
            fill_dir = -1

        # 更新持仓列表
        fill_cost = self.bars.get_latest_bars(fill.symbol)[0][3]
        cost = fill_dir * fill_cost * fill.quantity
        self.current_holdings[fill.symbol] += cost
        self.current_holdings['cash'] -= cost
        self.current_holdings['total'] -= cost

    def update_fill(self, event):
        """下单后，更新仓位和持仓情况
        """
        if event.type == 'FILL':
            self.update_positions_from_fill(event)
            self.update_holdings_from_fill(event)

    def generate_naive_order(self, signal):
        """
        Parameters:
        quantity - 生成订单
        """
        order = None

        symbol = signal.symbol
        direction = signal.signal_type
        # 确定下单数
        mkt_quantity = signal.quantity
        cur_quantity = self.current_positions[symbol]
        order_type = signal.order_type
        if direction == 'LONG':
            order = OrderEvent(symbol, order_type, mkt_quantity, 'BUY')

        if direction == 'SHORT':
            order = OrderEvent(symbol, order_type, mkt_quantity, 'SELL')

        if direction == 'EXIT' and cur_quantity > 0:
            order = OrderEvent(symbol, order_type, abs(cur_quantity), 'SELL')
        if direction == 'EXIT' and cur_quantity < 0:
            order = OrderEvent(symbol, order_type, abs(cur_quantity), 'BUY')
        return order

    def update_signal(self, event):
        """根据交易信号生成订单
        """
        if event.type == 'SIGNAL':
            order_event = self.generate_naive_order(event)
            self.events.put(order_event)

    # ========================
    # POST-BACKTEST STATISTICS
    # ========================
    def create_equity_curve_dataframe(self):
        curve = pd.DataFrame(self.all_holdings)
        curve.set_index('datetime', inplace=True)
        curve['returns'] = curve['total'].pct_change()
        curve['equity_curve'] = (1.0 + curve['returns']).cumprod()
        self.equity_curve = curve

    def output_summary_stats(self):
        """创建投资组合的一个统计总结
        """
        total_return = self.equity_curve['equity_curve'][-1]
        returns = self.equity_curve['returns']
        annualized_return = create_annualized_return(self.equity_curve)
        pnl = self.equity_curve['equity_curve']
        sharpe_ratio = create_sharpe_ratio(returns)
        max_dd, dd_duration = create_drawdowns(pnl)
        stats = [("总收益率", "%0.2f%%" % ((total_return - 1.0) * 100.0)),
                 ("年化收益率", "%0.2f%%" % annualized_return),
                 ("夏普比率", "%0.2f" % sharpe_ratio),
                 ("最大回撤", "%0.2f%%" % (max_dd * 100.0)),
                 ("最大回撤持续期", "%d" % dd_duration)]
        plt.clf()
        plt.plot(self.equity_curve.index, pnl)
        plt.savefig('output/cumulative_return')
        return stats
