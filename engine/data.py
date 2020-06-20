from abc import ABCMeta, abstractmethod
import pandas
from sqlalchemy.orm import sessionmaker
import utils.db_utils as db
from models import *
from engine.event import MarketEvent

FutInfo = fut_info.FutInfo
BarDaily = bar_daily.BarDaily


class DataHandler(object):
    __metaclass__ = ABCMeta

    def __init__(self, events, symbol_list, start_date, end_date):
        self.events = events
        self.symbol_list = symbol_list
        self.start_date = start_date
        self.end_date = end_date
        self.symbol_data = {}
        self.latest_symbol_data = {}
        self.continue_backtest = True
        self.init_data()

    @abstractmethod
    def init_data(self):
        raise NotImplementedError('Should implement init_data()')

    @abstractmethod
    def get_latest_bars(self, symbol, N=1):
        raise NotImplementedError('Should implement get_latest_bars()')

    @abstractmethod
    def update_bars(self):
        raise NotImplementedError('Should implement update_bars()')

    def get_latest_bars_dict(self, symbol_list, N=1):
        bar_dict = {}
        for symbol in symbol_list:
            bar_dict[symbol] = self.get_latest_bars(symbol, N=N)
        return bar_dict

    def get_latest_bars_values(self, symbol, column, N=1):
        bar_columns = ['symbol', 'datetime', 'open', 'close', 'high', 'low', 'volume']
        bar_list = self.get_latest_bars(symbol, N=N)
        return [bar[bar_columns.index(column)] for bar in bar_list]

    def get_latest_bar_datetime(self, symbol):
        """获取最新的bar的执行日期
        """
        bar_list = self.get_latest_bars(symbol)
        dt = str(bar_list[0][1]).split(' ')[0]
        return dt

    def get_data_number(self, symbol):
        return len(self.latest_symbol_data[symbol])


class HistoricDataHandler(DataHandler):
    def init_data(self):
        comb_index = None
        for s in self.symbol_list:
            self.symbol_data[s] = self.history(s)
            if comb_index is None:
                comb_index = self.symbol_data[s].index
            else:
                comb_index = comb_index.union(self.symbol_data[s].index)
            self.latest_symbol_data[s] = []

        for s in self.symbol_list:
            self.symbol_data[s] = self.symbol_data[s].reindex(index=comb_index).iterrows()

    def history(self, symbol):
        """获取历史数据
        """
        pass

    def __get_new_bar(self, symbol):
        for b in self.symbol_data[symbol]:
            yield tuple([symbol, b[0], b[1][0], b[1][1], b[1][2], b[1][3], b[1][4]])

    def get_latest_bars(self, symbol, N=1):
        try:
            bar_list = self.latest_symbol_data[symbol]
        except KeyError:
            print("That symbol is not available in the historical data set.")
        else:
            return bar_list[-N:]

    def update_bars(self):
        for s in self.symbol_list:
            try:
                bar = self.__get_new_bar(s).__next__()
            except StopIteration:
                self.continue_backtest = False
            else:
                if bar is not None:
                    self.latest_symbol_data[s].append(bar)
        self.events.put(MarketEvent())


class DataBaseDataHandler(HistoricDataHandler):
    def __init__(self, events, symbol_list, start_date, end_date):
        engine = db.connent()
        self.DB_Session = sessionmaker(bind=engine)
        db.init_db(engine)
        super().__init__(events, symbol_list, start_date, end_date)

    def history(self, symbol):
        db_session = self.DB_Session()
        ret = db_session.query(BarDaily).filter(BarDaily.fut_code == symbol,
                                                BarDaily.trade_date.between(self.start_date,
                                                                            self.end_date)).all()
        bars = BarDaily.to_json(ret)
        _bars = []
        for bar in bars:
            _bar = {}
            for k, v in bar.items():
                if k == 'trade_date' or k == 'open' or k == 'close' or k == 'high' or k == 'low' or k == 'vol':
                    if k != 'trade_date':
                        _bar[k] = float(v)
                    else:
                        _bar[k] = v
            _bars.append(_bar)
        df = pandas.DataFrame(_bars)
        df.trade_date = pandas.to_datetime(df.trade_date, format='%Y-%m-%d')
        df.set_index("trade_date", inplace=True, drop=True)
        df = df.sort_values(by='trade_date')
        db_session.close()
        return df
