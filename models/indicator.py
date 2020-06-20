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
