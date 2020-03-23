from models.base import BaseModel
from sqlalchemy import Column, Integer, Float, String, ForeignKey
from sqlalchemy.orm import relationship


class BarDaily(BaseModel):  # 继承生成的orm基类
    __tablename__ = "bar_daily"  # 表名
    fut_id = Column(Integer, ForeignKey("fut_info.id"))  # 合约id
    trade_date = Column(String(32))  # 交易日期
    pre_close = Column(Float(8))  # 昨收盘价
    open = Column(Float(8))  # 开盘价
    high = Column(Float(8))  # 最高价
    low = Column(Float(8))  # 最低价
    close = Column(Float(8))  # 收盘价
    change = Column(Float(8))  # 涨跌 收盘价-昨结算价
    vol = Column(Integer)  # 成交量(手)
    amount = Column(Float(8))  # 成交金额(万元)
    oi = Column(Integer)  # 持仓量(手)
    oi_chg = Column(Integer)  # 持仓量变化
    indicator = relationship("Indicator", backref="bar_daily")

    def __init__(self, fut_id, trade_date, pre_close, open, high, low, close, change, vol, amount, oi,
                 oi_chg, id, create_time, update_time):
        super().__init__(id, create_time, update_time)
        self.fut_id = fut_id
        self.trade_date = trade_date
        self.pre_close = pre_close
        self.open = open
        self.high = high
        self.low = low
        self.close = close
        self.change = change
        self.vol = vol
        self.amount = amount
        self.oi = oi
        self.oi_chg = oi_chg
