from models.base import BaseModel
from sqlalchemy import Column, Integer, Float, ForeignKey


class Indicator(BaseModel):  # 继承生成的orm基类
    __tablename__ = "indicator"  # 表名
    bar_id = Column(Integer, ForeignKey("bar_daily.id"))
    ma5 = Column(Float(4))
    ma10 = Column(Float(4))
    ma30 = Column(Float(4))
    ma60 = Column(Float(4))
    ma120 = Column(Float(4))
    ma240 = Column(Float(4))
    boll_up = Column(Float(4))
    boll_mb = Column(Float(4))
    boll_dn = Column(Float(4))
    macd = Column(Float(4))
    rsi = Column(Float(4))

    def __init__(self, bar_id, ma5, ma10, ma30, ma60, ma120, ma240, boll_up, boll_mb, boll_dn, macd, rsi, id,
                 create_time, update_time):
        super().__init__(id, create_time, update_time)
        self.bar_id = bar_id
        self.ma5 = ma5
        self.ma10 = ma10
        self.ma30 = ma30
        self.ma60 = ma60
        self.ma120 = ma120
        self.ma240 = ma240
        self.boll_up = boll_up
        self.boll_mb = boll_mb
        self.boll_dn = boll_dn
        self.macd = macd
        self.rsi = rsi
