from models.base import BaseModel
from sqlalchemy import Column, Integer, Float, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship


class BarDaily(BaseModel):  # 继承生成的orm基类
    __tablename__ = "bar_daily"  # 表名
    fut_code = Column(String(8), ForeignKey("fut_info.code"))  # 合约code
    trade_date = Column(DateTime)  # 交易日期
    pre_close = Column(Float(8))  # 昨收盘价
    open = Column(Float(8))  # 开盘价
    high = Column(Float(8))  # 最高价
    low = Column(Float(8))  # 最低价
    close = Column(Float(8))  # 收盘价
    change = Column(Float(8))  # 涨跌 收盘价-昨结算价
    vol = Column(Integer)  # 成交量(手)
    amount = Column(Float(8))  # 成交金额(万元)
    oi = Column(Integer)  # 持仓量(手)
    indicator = relationship("Indicator", backref="bar_daily")
